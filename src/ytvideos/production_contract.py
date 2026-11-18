"""Resolve pinned channel requirements and reject incomplete production manifests.

This is a technical/coverage contract. It does not judge a story, hear a mix or
prove that a reviewer actually watched a file. Those observations stay explicit.
"""
import copy
from fractions import Fraction
import math
from pathlib import Path
import re

from .errors import WorkflowError
from .util import digest, require_text


SCHEMA = "ytv-production-requirements-v1"
DELIVERY_SCHEMA = "ytv-production-delivery-v1"
LEGACY_MONTAGE_DIRECTIONS = ("left_to_right", "right_to_left", "none")
MONTAGE_DIRECTIONS = {*LEGACY_MONTAGE_DIRECTIONS, "top_to_bottom", "bottom_to_top"}


def _merge(base, override):
    result = copy.deepcopy(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(result.get(key), dict):
            result[key] = _merge(result[key], value)
        else:
            result[key] = copy.deepcopy(value)
    return result


def production_requirements(profile, format, *, variant=None):
    """Return one resolved policy, with useful blockers instead of silent defaults."""
    policy = profile.get("production") or {}
    if not isinstance(policy, dict):
        raise WorkflowError("channel production policy must be an object")
    formats = policy.get("formats", {})
    if not isinstance(formats, dict):
        raise WorkflowError("production.formats must be an object")
    selected = formats.get(format, {})
    if not isinstance(selected, dict):
        raise WorkflowError("production format policy must be an object")
    variants = selected.get("variants", {})
    if not isinstance(variants, dict):
        raise WorkflowError("production variants must be an object")
    unresolved = []
    values = _merge({k: v for k, v in policy.items() if k != "formats"},
                    {k: v for k, v in selected.items() if k != "variants"})
    if format not in formats:
        unresolved.append("production.formats." + str(format))
    if variants:
        if variant not in variants:
            unresolved.append("production_variant")
        elif not isinstance(variants[variant], dict):
            raise WorkflowError("production variant policy must be an object")
        else:
            values = _merge(values, variants[variant])
    elif variant is not None:
        unresolved.append("production_variant")
    result = {"schema": SCHEMA, "channel": profile.get("id"), "format": format,
              "variant": variant, "available_variants": sorted(variants),
              "video": values.get("video", {}), "audio": values.get("audio", {}),
              "visual": values.get("visual", {}), "captions": values.get("captions", {}),
              "narrative_loop": "not_applicable" if format == "long" else values.get("narrative_loop", "unresolved"),
              "end_screen_seconds": values.get("end_screen_seconds")}
    # New ordinary whole-frame recipes opt in through the pinned ChannelSpec.
    # Keep historical requirements (including their digest) unchanged when absent.
    montage = profile.get("montage", {})
    if isinstance(result["visual"], dict) and result["visual"].get("motion") == "whole_frame" and isinstance(montage, dict):
        camera = {}
        if "directions" in montage:
            directions = montage["directions"]
            if (not isinstance(directions, list) or not directions
                    or any(not isinstance(value, str) or value not in MONTAGE_DIRECTIONS for value in directions)):
                raise WorkflowError("montage.directions must list supported camera directions")
            camera["directions"] = list(directions)
        if "allow_static" in montage:
            if type(montage["allow_static"]) is not bool:
                raise WorkflowError("montage.allow_static must be boolean")
            camera["allow_static"] = montage["allow_static"]
        if camera:
            result["montage_camera"] = camera
    if profile.get("recipe") == "music_first":
        result["music_edit"] = values.get("music_edit", {})
        result["speech_mode"] = values.get("speech_mode")
        from .music_contract import policy_blockers
        unresolved.extend(policy_blockers(result["music_edit"]))
        if result["speech_mode"] not in {"source", "none"}:
            unresolved.append("speech_mode")
    if not isinstance(result["narrative_loop"], str) or result["narrative_loop"] not in {"required", "not_applicable"}:
        unresolved.append("narrative_loop")
        result["narrative_loop"] = "unresolved"
    for name in ("video", "audio", "visual", "captions"):
        if not isinstance(result[name], dict):
            raise WorkflowError("production." + name + " must be an object")
    video = result["video"]
    canvas = video.get("canvas")
    if (not isinstance(canvas, list) or len(canvas) != 2
            or any(type(v) is not int or v < 2 or v % 2 for v in canvas)):
        unresolved.append("video.canvas")
    else:
        width, height = canvas
        if (format == "short" and width >= height) or (format == "long" and width <= height):
            raise WorkflowError("production canvas orientation contradicts format")
    try:
        fps = Fraction(str(video.get("fps")))
        if fps <= 0:
            raise ValueError
    except (ValueError, ZeroDivisionError):
        unresolved.append("video.fps")
    for name in ("codec", "pix_fmt", "sample_aspect_ratio", "color_primaries",
                 "color_transfer", "color_space", "color_range"):
        if not isinstance(video.get(name), str) or not video[name].strip():
            unresolved.append("video." + name)
    minimum_shot_seconds = video.get("minimum_shot_seconds", 0)
    if type(minimum_shot_seconds) is not int or minimum_shot_seconds < 0:
        unresolved.append("video.minimum_shot_seconds")
    if type(result["audio"].get("required")) is not bool:
        unresolved.append("audio.required")
    if not isinstance(result["audio"].get("codec"), str) or not result["audio"]["codec"].strip():
        unresolved.append("audio.codec")
    for name in ("channels", "sample_rate"):
        if name in result["audio"] and (type(result["audio"][name]) is not int or result["audio"][name] <= 0):
            unresolved.append("audio." + name)
    if type(result["visual"].get("source_interval_review", False)) is not bool:
        unresolved.append("visual.source_interval_review")
    choices = {("audio", "music"): {"required", "optional", "none"},
               ("visual", "motion"): {"whole_frame", "source_motion", "authored", "none"},
               ("visual", "transitions"): {"direct_cuts", "recipe_defined"},
               ("visual", "decorative_frame"): {"required", "optional", "forbidden"},
               ("captions", "mode"): {"word_highlight", "when_speech", "lyrics", "none"},
               ("captions", "srt"): {"required", "when_speech", "none"}}
    for (group, name), allowed in choices.items():
        if result[group].get(name) not in allowed:
            unresolved.append(group + "." + name)
    if result["captions"].get("mode") in {"word_highlight", "lyrics"}:
        face = result["captions"].get("font", {})
        for key in ("family", "style"):
            if not isinstance(face, dict) or not isinstance(face.get(key), str) or not face[key].strip():
                unresolved.append("captions.font." + key)
    end_screen = result["end_screen_seconds"]
    if type(end_screen) not in (int, float) or not math.isfinite(end_screen) or end_screen < 0:
        unresolved.append("end_screen_seconds")
    if result["visual"].get("decorative_frame") == "required":
        asset = result["visual"].get("frame_asset")
        if not isinstance(asset, dict) or not asset.get("sha256") or not asset.get("path"):
            unresolved.append("visual.frame_asset")
    checks = {"visual_review", "listening", "subtitles", "rights", "delivery_contract", "decorative_frame"}
    if result["visual"].get("motion") != "none":
        checks.add("motion")
    if result["audio"].get("music") != "none":
        checks.add("music")
    if result["captions"].get("mode") != "none":
        checks.add("captions")
    if end_screen:
        checks.add("end_screen")
    if format == "short":
        checks.add("av_loop")
    result.update(configured=not unresolved, unresolved=list(dict.fromkeys(unresolved)),
                  review_checks=sorted(checks))
    result["sha256"] = digest(result)
    return result


def require_configured(requirements):
    if not requirements["configured"]:
        raise WorkflowError("production requirements unresolved: " + ", ".join(requirements["unresolved"]))


def validate_delivery_summary(summary, requirements):
    """Compare measured streams with channel policy, independent of renderer choice."""
    require_configured(requirements)
    videos = summary.get("video", [])
    if len(videos) != 1:
        raise WorkflowError("production delivery requires exactly one video stream")
    actual, expected = videos[0], requirements["video"]
    if [actual.get("width"), actual.get("height")] != expected["canvas"]:
        raise WorkflowError("production video dimensions differ from the pinned canvas")
    for name in ("codec", "pix_fmt", "sample_aspect_ratio", "color_primaries",
                 "color_transfer", "color_space", "color_range"):
        if actual.get(name) != expected[name]:
            raise WorkflowError("production video differs from required " + name)
    try:
        if any(Fraction(str(actual.get(name))) != Fraction(expected["fps"])
               for name in ("avg_frame_rate", "r_frame_rate")):
            raise ValueError
    except (ValueError, ZeroDivisionError):
        raise WorkflowError("production video cadence differs from the pinned fps") from None
    if requirements["audio"]["required"] and not summary.get("audio"):
        raise WorkflowError("production delivery requires audio, including a video without speech")
    if len(summary.get("audio", [])) > 1 or any(stream.get("codec") != requirements["audio"]["codec"]
                                               for stream in summary.get("audio", [])):
        raise WorkflowError("production delivery needs one final mix in the required audio codec")
    for stream in summary.get("audio", []):
        for name in ("channels", "sample_rate"):
            if name in requirements["audio"] and stream.get(name) != requirements["audio"][name]:
                raise WorkflowError("production audio differs from required " + name)
        if requirements["audio"]["required"]:
            try:
                start, duration = float(stream.get("start_time") or 0), float(stream["duration"])
                video_duration = float(actual["duration"])
                container_duration = float(summary["duration_seconds"])
                tolerance = max(1 / float(Fraction(expected["fps"])), 1024 / stream["sample_rate"]) + .001
                if (not all(math.isfinite(value) for value in (start, duration, video_duration, container_duration))
                        or duration <= 0 or abs(start) > tolerance or abs(start + duration - video_duration) > tolerance
                        or abs(container_duration - video_duration) > tolerance):
                    raise ValueError
            except (TypeError, ValueError, KeyError, ZeroDivisionError):
                raise WorkflowError("production audio and container must match the complete video timeline") from None
    return summary


def _intervals_cover(intervals, duration):
    cursor = 0
    for start, end in sorted(intervals):
        if start > cursor or end <= start:
            return False
        cursor = max(cursor, end)
    return cursor >= duration


def _frame_interval(value, total, label):
    start, end = value.get("start_frame"), value.get("end_frame")
    if type(start) is not int or type(end) is not int or not 0 <= start < end <= total:
        raise WorkflowError(label + " needs an exact in-timeline frame interval")
    return start, end


def _fragment_contracts(plan, requirements):
    """Describe the exact source/crop/visible range a manual fragment review must inspect."""
    total = plan["scenes"][-1]["end_frame"]
    contracts, seen = [], set()
    for scene in plan["scenes"]:
        identity = require_text(scene.get("id"), "reviewed fragment id")
        if identity in seen:
            raise WorkflowError("reviewed fragment IDs must be unique")
        seen.add(identity)
        source = scene.get("source")
        if not isinstance(source, dict) or set(source) != {"path", "sha256", "start_seconds", "end_seconds"}:
            raise WorkflowError("reviewed fragment needs its exact original source and full interval")
        if not Path(require_text(source.get("path"), "fragment original source path")).is_absolute():
            raise WorkflowError("fragment original source path must be absolute")
        for value in (source.get("sha256"), scene.get("clip_sha256")):
            if not isinstance(value, str) or not re.fullmatch(r"[0-9a-f]{64}", value):
                raise WorkflowError("reviewed fragment needs exact original and prepared clip hashes")
        start, end = source["start_seconds"], source["end_seconds"]
        if (any(type(value) not in (int, float) or not math.isfinite(value) for value in (start, end))
                or not 0 <= start < end):
            raise WorkflowError("reviewed fragment source interval is invalid")
        first, stop = scene.get("visible_start_frame"), scene.get("visible_end_frame")
        if (type(first) is not int or type(stop) is not int
                or not 0 <= first <= scene["start_frame"] < scene["end_frame"] <= stop <= total):
            raise WorkflowError("fragment visible interval must include both transition overlaps")
        crop = scene.get("crop")
        if not isinstance(crop, dict) or set(crop) != {"interpolation", "keyframes"}:
            raise WorkflowError("reviewed fragment needs the exact crop trajectory")
        require_text(crop["interpolation"], "crop interpolation")
        keyframes = crop["keyframes"]
        if not isinstance(keyframes, list) or not keyframes:
            raise WorkflowError("crop trajectory requires bounded keyframes")
        previous = first - 1
        for keyframe in keyframes:
            if not isinstance(keyframe, dict) or set(keyframe) != {"frame", "box"}:
                raise WorkflowError("crop keyframe requires exact frame and source-pixel box")
            frame, box = keyframe["frame"], keyframe["box"]
            if (type(frame) is not int or not previous < frame < stop or frame < first
                    or not isinstance(box, list) or len(box) != 4
                    or any(type(value) not in (int, float) or not math.isfinite(value) for value in box)
                    or not 0 <= box[0] < box[2] or not 0 <= box[1] < box[3]):
                raise WorkflowError("crop keyframes must be ordered in the full visible interval")
            previous = frame
        if keyframes[0]["frame"] != first or keyframes[-1]["frame"] != stop - 1:
            raise WorkflowError("crop trajectory must include the first and last visible frame")
        contracts.append({"id": identity, "source": source, "clip_sha256": scene["clip_sha256"],
            "timeline": {key: scene[key] for key in ("start_frame", "end_frame", "visible_start_frame", "visible_end_frame")},
            "crop": crop})
    return contracts


def _finite_review_number(value):
    try:
        return type(value) in (int, float) and math.isfinite(value)
    except OverflowError:
        return False


def _fragment_coverage(coverage, *, first, stop, label):
    if not isinstance(coverage, list) or not coverage:
        raise WorkflowError("fragment review requires full " + label + " motion coverage, not three stills")
    intervals = []
    for interval in coverage:
        if not isinstance(interval, dict):
            raise WorkflowError("fragment " + label + " coverage must contain actual intervals")
        start, end = interval.get("start_seconds"), interval.get("end_seconds")
        if (any(not _finite_review_number(value) for value in (start, end))
                or not first <= start < end <= stop):
            raise WorkflowError("fragment " + label + " coverage falls outside the accepted interval")
        intervals.append((start - first, end - first))
    if not _intervals_cover(intervals, stop - first):
        raise WorkflowError("fragment " + label + " motion coverage omits part of the used interval")
    return intervals


def _fragment_probe_duration(probe):
    if not isinstance(probe, dict) or not isinstance(probe.get("video"), list) or len(probe["video"]) != 1:
        raise WorkflowError("fragment review requires measured source and final video probes")
    duration = probe.get("duration_seconds")
    if not _finite_review_number(duration) or duration <= 0:
        raise WorkflowError("fragment review requires a finite positive measured duration")
    return duration


def validate_fragment_review(document, *, plan, requirements, media_sha256, reviewer, sources, media_probe=None):
    """Check complete manual observations, never infer motion/crop quality from a detector."""
    if not requirements["visual"].get("source_interval_review", False):
        return []
    validate_render_manifest(plan, requirements)
    final_duration = _fragment_probe_duration(media_probe)
    if (not isinstance(document, dict) or document.get("schema") != "ytv-source-fragment-review-v1"
            or document.get("artifact_sha256") != media_sha256 or document.get("reviewer") != reviewer):
        raise WorkflowError("fragment review must bind the exact MP4 and independent reviewer")
    contracts = _fragment_contracts(plan, requirements)
    rows = document.get("fragments")
    if not isinstance(rows, list) or len(rows) != len(contracts) or len(sources) != len(contracts):
        raise WorkflowError("fragment review must cover every accepted source interval")
    checks = {"source_motion", "crop", "internal_cuts", "final_motion", "transitions"}
    records = []
    for row, contract, accepted in zip(rows, contracts, sources):
        if not isinstance(row, dict) or any(row.get(key) != value for key, value in contract.items()):
            raise WorkflowError("fragment review differs from the exact source/timeline/crop contract")
        source, timeline = contract["source"], contract["timeline"]
        if any(accepted.get(key) != value for key, value in {
                "id": contract["id"], "clip_sha256": contract["clip_sha256"], "source_sha256": source["sha256"],
                "start_seconds": source["start_seconds"], "end_seconds": source["end_seconds"]}.items()):
            raise WorkflowError("fragment review source differs from the accepted storyboard and clip")
        require_text(row.get("method"), "full source and final motion review method")
        observed = row.get("checks")
        if not isinstance(observed, dict) or set(observed) != checks:
            raise WorkflowError("fragment review needs source motion, crop, internal cuts, final motion and transitions")
        for name, observation in observed.items():
            if not isinstance(observation, dict) or observation.get("status") != "PASS":
                raise WorkflowError("fragment " + name + " remains FAIL or UNVERIFIED")
            require_text(observation.get("notes"), "fragment " + name + " observations")
        source_probe = accepted.get("source_probe")
        if source["end_seconds"] > _fragment_probe_duration(source_probe) + .05:
            raise WorkflowError("fragment source interval exceeds the measured original media")
        intervals = _fragment_coverage(row.get("source_coverage"), first=source["start_seconds"],
                                       stop=source["end_seconds"], label="source")
        _review_inspection({"inspection": row.get("source_inspection")}, "motion",
                           source["end_seconds"] - source["start_seconds"], intervals, source_probe)
        fps = Fraction(requirements["video"]["fps"])
        final_first = float(Fraction(timeline["visible_start_frame"]) / fps)
        final_stop = float(Fraction(timeline["visible_end_frame"]) / fps)
        if final_stop > final_duration + .05:
            raise WorkflowError("fragment final interval exceeds the measured rendered media")
        final_intervals = _fragment_coverage(row.get("final_coverage"), first=final_first, stop=final_stop, label="final")
        _review_inspection({"inspection": row.get("final_inspection")}, "motion",
                           final_stop - final_first, final_intervals, media_probe)
        anchors = row.get("source_anchors_seconds")
        expected_anchors = accepted.get("source_anchors_seconds")
        if (not isinstance(anchors, list) or len(anchors) != 3
                or any(type(value) not in (int, float) or not math.isfinite(value) for value in anchors)
                or not isinstance(expected_anchors, list) or len(expected_anchors) != 3
                or any(abs(value - expected) > 1e-6 for value, expected in zip(anchors, expected_anchors))):
            raise WorkflowError("fragment review needs first, middle and last used source-frame anchors")
        first, last = timeline["visible_start_frame"], timeline["visible_end_frame"] - 1
        if row.get("final_anchors_frames") != [first, (first + last) // 2, last]:
            raise WorkflowError("fragment review needs exact first, middle and last final-frame anchors")
        expected_seams = sorted({first, timeline["start_frame"], timeline["end_frame"] - 1, last})
        if row.get("checked_transition_frames") != expected_seams:
            raise WorkflowError("fragment review must identify both ends and overlaps of its transitions")
        records.append({key: source[key] for key in ("path", "sha256")})
    return records


def validate_render_manifest(plan, requirements):
    """Check explicit choices and required elements before encoding or accepting MP4."""
    require_configured(requirements)
    if not isinstance(plan, dict) or plan.get("purpose", "production") != "production":
        raise WorkflowError("technical probes cannot be completed as production delivery")
    for name in ("channel", "format"):
        if plan.get(name) != requirements[name]:
            raise WorkflowError("render manifest uses another " + name)
    if plan.get("production_variant") != requirements["variant"]:
        raise WorkflowError("render manifest uses another production variant")
    expected = requirements["video"]
    if plan.get("canvas", expected["canvas"]) != expected["canvas"]:
        raise WorkflowError("render manifest canvas differs from the production requirements")
    try:
        if Fraction(str(plan.get("fps", expected["fps"]))) != Fraction(expected["fps"]):
            raise ValueError
    except (ValueError, ZeroDivisionError):
        raise WorkflowError("render manifest fps differs from the production requirements") from None
    scenes = plan.get("scenes")
    if not isinstance(scenes, list) or not scenes:
        raise WorkflowError("production render manifest requires scene intervals")
    cursor = 0
    minimum_shot_seconds = expected.get("minimum_shot_seconds", 0)
    minimum_shot_frames = minimum_shot_seconds * Fraction(expected["fps"])
    for index, scene in enumerate(scenes, start=1):
        if (not isinstance(scene, dict) or type(scene.get("start_frame")) is not int
                or type(scene.get("end_frame")) is not int or scene["start_frame"] != cursor
                or scene["end_frame"] <= cursor):
            raise WorkflowError("production scenes must cover one continuous frame timeline")
        if scene["end_frame"] - scene["start_frame"] < minimum_shot_frames:
            raise WorkflowError(f"production shot {index} must last at least {minimum_shot_seconds} seconds")
        if "motion_clip" in scene or ("image" in scene and "clip" in scene):
            raise WorkflowError("mixed image/video scenes require a supported bound renderer; unsupported motion inputs must not be ignored")
        cursor = scene["end_frame"]
        if requirements["visual"]["motion"] == "whole_frame" and scene.get("role") != "end_screen":
            direction, zoom = scene.get("direction"), scene.get("zoom")
            camera = requirements.get("montage_camera", {})
            if (direction not in camera.get("directions", LEGACY_MONTAGE_DIRECTIONS)
                    or zoom not in ("in", "out", "none")
                    or (direction == zoom == "none" and camera.get("allow_static") is not True)):
                raise WorkflowError("whole-frame direction/zoom must match the pinned montage camera policy")
    if requirements["visual"]["transitions"] == "direct_cuts":
        if plan.get("transitions", "direct_cuts") != "direct_cuts":
            raise WorkflowError("production requires direct cuts")
    has_speech = plan.get("has_speech", True)
    if type(has_speech) is not bool:
        raise WorkflowError("render manifest has_speech must be boolean")
    speech_mode = requirements.get("speech", {}).get("mode")
    if speech_mode is not None and has_speech != (speech_mode != "none"):
        raise WorkflowError("render has_speech must match the accepted script")
    if speech_mode == "none" and (plan.get("srt") or plan.get("subtitles", {}).get("mode") != "none"):
        raise WorkflowError("no-speech edits require explicit subtitles.mode=none and no fabricated SRT")
    captions = requirements["captions"]
    needs_captions = captions["mode"] == "word_highlight" or (captions["mode"] == "when_speech" and has_speech)
    if needs_captions and plan.get("subtitles", {}).get("mode") != "words":
        raise WorkflowError("production requires burned-in word captions")
    if captions["mode"] == "lyrics" and plan.get("subtitles", {}).get("mode") != "lyrics":
        raise WorkflowError("production requires the canonical burned-in lyric captions")
    needs_srt = captions["srt"] == "required" or (captions["srt"] == "when_speech" and has_speech)
    if needs_srt and not plan.get("srt"):
        raise WorkflowError("production manifest must bind the manual SRT")
    end_seconds = requirements["end_screen_seconds"]
    end_scenes = [index for index, scene in enumerate(scenes) if scene.get("role") == "end_screen"]
    if end_seconds:
        expected_frames = Fraction(str(end_seconds)) * Fraction(expected["fps"])
        last = scenes[-1]
        if end_scenes != [len(scenes) - 1] or last["end_frame"] - last["start_frame"] != expected_frames:
            raise WorkflowError("production requires its exact final end-screen interval")
    elif end_scenes:
        raise WorkflowError("this production format has no end-screen interval")
    visual = requirements["visual"]
    overlays = plan.get("overlays", [])
    if not isinstance(overlays, list) or any(not isinstance(item, dict) for item in overlays):
        raise WorkflowError("production overlays must be explicit file-backed layers")
    frames = [layer for layer in overlays if layer.get("role") in {"decorative_frame", "paper_frame", "frame"}]
    if visual["decorative_frame"] == "forbidden" and frames:
        raise WorkflowError("pinned channel policy forbids a decorative frame")
    if visual["decorative_frame"] == "required" and not frames:
        raise WorkflowError("production is missing the approved decorative frame asset")
    for layer in overlays:
        require_text(layer.get("role"), "overlay role")
        require_text(layer.get("path"), "overlay source asset path")
        require_text(layer.get("sha256"), "overlay source asset hash")
        _frame_interval(layer, cursor, "overlay")
    for layer in frames:
        asset = visual.get("frame_asset", {})
        if layer.get("sha256") != asset.get("sha256") or not asset.get("sha256"):
            raise WorkflowError("decorative frame must use the exact approved asset; drawn substitutes are not assets")
    music = plan.get("music", {})
    if not isinstance(music, dict):
        raise WorkflowError("production music decision must be an object")
    if requirements["audio"]["music"] == "required" and music.get("status") != "present":
        raise WorkflowError("production requires an audible music mix with source evidence")
    if music.get("status") == "present":
        tracks = music.get("tracks")
        if not isinstance(tracks, list) or not tracks:
            raise WorkflowError("present music requires actual source tracks")
        intervals = []
        for track in tracks:
            if not isinstance(track, dict):
                raise WorkflowError("music track must be an object")
            require_text(track.get("path"), "music source path")
            require_text(track.get("sha256"), "music source hash")
            intervals.append(_frame_interval(track, cursor, "music track"))
        for silence in music.get("silences", []):
            require_text(silence.get("reason"), "intentional music pause reason")
            intervals.append(_frame_interval(silence, cursor, "music pause"))
        if requirements["audio"]["music"] == "required" and not _intervals_cover(intervals, cursor):
            raise WorkflowError("music and intentional pauses must cover the complete timeline")
        if not isinstance(music.get("mix_evidence"), dict):
            raise WorkflowError("music needs exact mix execution evidence")
    elif requirements["audio"]["music"] == "optional":
        if music.get("status") != "not_used" or not isinstance(music.get("reason"), str) or not music["reason"].strip():
            raise WorkflowError("optional music requires an explicit decision and reason")
    if requirements["visual"].get("source_interval_review", False):
        _fragment_contracts(plan, requirements)
    return {"frames": cursor, "duration_seconds": float(Fraction(cursor) / Fraction(expected["fps"])),
            "has_speech": has_speech, "requires_srt": needs_srt}


def _review_inspection(observed, name, duration, intervals, media_probe):
    """Validate declared observation mode, not the truth of a reviewer's perception."""
    inspection = observed.get("inspection")
    if not isinstance(inspection, dict):
        raise WorkflowError("review requires a typed inspection method")
    mode = inspection.get("mode")
    modes = {"frame_inspection", "video_playback", "audio_listening", "av_playback",
             "media_probe", "document_inspection"}
    if not isinstance(mode, str) or mode not in modes:
        raise WorkflowError("unsupported review inspection mode")
    require_text(inspection.get("tool"), "actual inspection tool or surface")
    allowed = ({"av_playback"} if name == "av_loop" else
               {"audio_listening", "av_playback"} if name in {"listening", "music", "no_speech"} else
               {"video_playback", "av_playback"} if name in {"motion", "subtitles", "captions"} else
               {"frame_inspection", "video_playback", "av_playback"} if name == "visual_review" else modes)
    if mode not in allowed:
        raise WorkflowError("inspection mode cannot establish " + str(name))
    if mode in {"video_playback", "audio_listening", "av_playback"}:
        if set(inspection) != {"mode", "tool", "playback_speed"}:
            raise WorkflowError("playback inspection requires its actual speed, not frame sampling")
        speed = inspection["playback_speed"]
        if not _finite_review_number(speed) or speed <= 0:
            raise WorkflowError("playback speed must be a finite positive number")
        if name in {"motion", "av_loop"} and speed != 1:
            raise WorkflowError(str(name) + " acceptance requires normal-speed playback; slow motion is supplementary")
        return
    if mode != "frame_inspection":
        if set(inspection) != {"mode", "tool"}:
            raise WorkflowError("non-playback inspection must not claim playback or frame coverage")
        return
    if set(inspection) != {"mode", "tool", "sampling", "source_fps", "frame_count", "inspected_frames", "display_size"}:
        raise WorkflowError("frame inspection requires exact sampling and displayed dimensions")
    fps, count = inspection["source_fps"], inspection["frame_count"]
    frames, size = inspection["inspected_frames"], inspection["display_size"]
    if (not _finite_review_number(fps) or fps <= 0
            or type(count) is not int or not _finite_review_number(count) or count <= 0
            or abs(count / fps - duration) > .05):
        raise WorkflowError("frame inspection metadata differs from the exact media duration")
    try:
        video = media_probe["video"]
        if len(video) != 1:
            raise ValueError
        actual_count = int(video[0]["nb_frames"])
        actual_fps = float(Fraction(video[0]["avg_frame_rate"]))
        if actual_count != count or not math.isclose(actual_fps, fps, rel_tol=1e-9):
            raise ValueError
    except (TypeError, KeyError, ValueError, ZeroDivisionError, OverflowError):
        raise WorkflowError("frame inspection must match measured video frame count and FPS") from None
    if (not isinstance(frames, list) or not frames or any(type(x) is not int or not 0 <= x < count for x in frames)
            or frames != sorted(set(frames))):
        raise WorkflowError("inspected frames must be sorted unique in-range frame indices")
    if (not isinstance(size, list) or len(size) != 2 or any(type(x) is not int or x <= 0 for x in size)):
        raise WorkflowError("frame inspection needs the actual displayed width and height")
    sampling = inspection["sampling"]
    if not isinstance(sampling, str) or sampling not in {"all_frames", "sampled_frames"} or (sampling == "all_frames") != (len(frames) == count):
        raise WorkflowError("frame sampling claim differs from inspected frame indices")
    # Coverage describes inspected frames, never the span between sparse samples.
    expected_ranges = []
    for frame in frames:
        if expected_ranges and expected_ranges[-1][1] == frame:
            expected_ranges[-1][1] += 1
        else:
            expected_ranges.append([frame, frame + 1])
    covered_ranges = []
    for start, end in sorted(intervals):
        first = max(0, math.floor(start * fps + 1e-7))
        last = min(count, math.ceil(end * fps - 1e-7))
        if covered_ranges and first <= covered_ranges[-1][1]:
            covered_ranges[-1][1] = max(last, covered_ranges[-1][1])
        else:
            covered_ranges.append([first, last])
    if covered_ranges != expected_ranges:
        raise WorkflowError("frame coverage differs from actual inspected samples")
    if name == "visual_review" and sampling != "all_frames":
        raise WorkflowError("sampled frames do not establish complete visual review")


def validate_review_observation(check, *, media_sha256, duration, media_probe=None):
    """Require inspectable coverage; this cannot authenticate a listener's perception."""
    if not _finite_review_number(duration) or duration <= 0:
        raise WorkflowError("review requires a finite positive media duration")
    observed = check.get("observed", {})
    if not isinstance(observed, dict):
        raise WorkflowError("review observation must be an object")
    if observed.get("artifact_sha256") != media_sha256:
        raise WorkflowError("review evidence must identify the exact rendered media hash")
    require_text(observed.get("reviewer"), "review evidence reviewer")
    require_text(observed.get("notes"), "review observations")
    coverage = observed.get("coverage")
    if not isinstance(coverage, list) or not coverage:
        raise WorkflowError("review evidence requires actual interval coverage")
    intervals = []
    for item in coverage:
        if not isinstance(item, dict):
            raise WorkflowError("review coverage must contain time intervals")
        start, end = item.get("start_seconds"), item.get("end_seconds")
        if (not _finite_review_number(start) or not _finite_review_number(end)
                or not 0 <= start < end <= duration + .05):
            raise WorkflowError("review coverage falls outside the exact media")
        intervals.append((start, end))
    _review_inspection(observed, check.get("name"), duration, intervals, media_probe)
    if check.get("name") in {"listening", "visual_review", "subtitles", "music", "motion", "captions", "no_speech"}:
        if not _intervals_cover(intervals, duration - .05):
            raise WorkflowError("review coverage does not cover the complete " + check["name"])
    evidence = observed.get("evidence")
    if not isinstance(evidence, dict) or set(evidence) != {"path", "sha256"}:
        raise WorkflowError("review needs a hash-bound evidence file, not an unchecked PASS")
    return evidence
