"""Resolve pinned channel requirements and reject incomplete production manifests.

This is a technical/coverage contract. It does not judge a story, hear a mix or
prove that a reviewer actually watched a file. Those observations stay explicit.
"""
import copy
from fractions import Fraction
import math

from .errors import WorkflowError
from .util import digest, require_text


SCHEMA = "ytv-production-requirements-v1"
DELIVERY_SCHEMA = "ytv-production-delivery-v1"


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
    if type(result["audio"].get("required")) is not bool:
        unresolved.append("audio.required")
    if not isinstance(result["audio"].get("codec"), str) or not result["audio"]["codec"].strip():
        unresolved.append("audio.codec")
    choices = {("audio", "music"): {"required", "optional", "none"},
               ("visual", "motion"): {"whole_frame", "source_motion", "authored", "none"},
               ("visual", "transitions"): {"direct_cuts", "recipe_defined"},
               ("visual", "decorative_frame"): {"required", "optional", "forbidden"},
               ("captions", "mode"): {"word_highlight", "when_speech", "none"},
               ("captions", "srt"): {"required", "when_speech", "none"}}
    for (group, name), allowed in choices.items():
        if result[group].get(name) not in allowed:
            unresolved.append(group + "." + name)
    if result["captions"].get("mode") == "word_highlight":
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
    for scene in scenes:
        if (not isinstance(scene, dict) or type(scene.get("start_frame")) is not int
                or type(scene.get("end_frame")) is not int or scene["start_frame"] != cursor
                or scene["end_frame"] <= cursor):
            raise WorkflowError("production scenes must cover one continuous frame timeline")
        cursor = scene["end_frame"]
        if requirements["visual"]["motion"] == "whole_frame" and scene.get("role") != "end_screen":
            direction, zoom = scene.get("direction"), scene.get("zoom")
            if (direction not in {"left_to_right", "right_to_left", "none"}
                    or zoom not in {"in", "out", "none"} or direction == zoom == "none"):
                raise WorkflowError("every scene requires the approved whole-frame horizontal motion/zoom")
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
    return {"frames": cursor, "duration_seconds": float(Fraction(cursor) / Fraction(expected["fps"])),
            "has_speech": has_speech, "requires_srt": needs_srt}


def validate_review_observation(check, *, media_sha256, duration):
    """Require inspectable coverage; this cannot authenticate a listener's perception."""
    observed = check.get("observed", {})
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
        if (type(start) not in (int, float) or type(end) not in (int, float)
                or not math.isfinite(start) or not math.isfinite(end) or not 0 <= start < end <= duration + .05):
            raise WorkflowError("review coverage falls outside the exact media")
        intervals.append((start, end))
    if check.get("name") in {"listening", "visual_review", "subtitles", "music", "motion", "captions", "no_speech"}:
        if not _intervals_cover(intervals, duration - .05):
            raise WorkflowError("review coverage does not cover the complete " + check["name"])
    evidence = observed.get("evidence")
    if not isinstance(evidence, dict) or set(evidence) != {"path", "sha256"}:
        raise WorkflowError("review needs a hash-bound evidence file, not an unchecked PASS")
    return evidence
