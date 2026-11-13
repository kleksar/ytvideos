"""Exact inputs and settings for the music-first compositor, without creative verdicts."""
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import re
import sys
import unicodedata

from .errors import WorkflowError
from .media_checks import probe_media, validate_font_face
from .util import file_digest, require_text


MANIFEST_SCHEMA = "ytv-music-render-v1"
RECEIPT_SCHEMA = "ytv-music-render-receipt-v1"
MIX_SCHEMA = "ytv-source-mix-evidence-v1"
ENGINE = ("automation/music_render.py", "automation/music_montage.py", "automation/music_beats.py",
          "automation/music_fragments.py", "automation/captions/music_lyrics.py",
          "src/ytvideos/music_contract.py")


def policy_blockers(policy):
    """Supported compositor settings; artist-selected effect strength stays in the edit."""
    expected = {"zoom": [.95, 1.05], "color": {"contrast": 1.25, "saturation": 1.5},
                "transition": {"duration_frames": 3, "peak_incoming": .7,
                               "components": ["fade", "gaussian_blur", "brightness"]},
                "lyrics": {"font_size_px": 147, "max_words": 1, "tilt_every": 6,
                           "vocal_beat": True, "invert_masks": True, "mask_sigma_px": 1.65,
                           "hold_gap_lt_ms": 500, "beat_pulse_scale": .06}}
    if not isinstance(policy, dict):
        return ["music_edit"]
    return ["music_edit." + key for key, value in expected.items() if policy.get(key) != value]


def file_record(path):
    path = Path(path).resolve(strict=True)
    if not path.is_file():
        raise WorkflowError("music input must be a regular file")
    return {"path": str(path), "sha256": file_digest(path)}


def checked(record):
    if (not isinstance(record, dict) or set(record) != {"path", "sha256"}
            or not isinstance(record.get("path"), str) or not record["path"].strip()
            or not isinstance(record.get("sha256"), str) or not re.fullmatch(r"[0-9a-f]{64}", record["sha256"])):
        raise WorkflowError("music input requires exact path and SHA-256")
    try:
        actual = file_record(record["path"])
    except OSError as exc:
        raise WorkflowError("music input is missing: " + record["path"]) from exc
    if actual != record:
        raise WorkflowError("music input changed or uses a noncanonical path")
    return Path(record["path"])


def document(record):
    try:
        return json.loads(checked(record).read_text(encoding="utf-8"))
    except (ValueError, UnicodeError) as exc:
        raise WorkflowError("music evidence must contain readable JSON") from exc


def helper(project, relative, name):
    path = Path(project) / relative
    if str(Path(project) / "automation") not in sys.path:
        sys.path.insert(0, str(Path(project) / "automation"))
    specification = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def visible_intervals(scenes):
    total = scenes[-1]["end_frame"]
    return [(max(0, scene["start_frame"] - (1 if index else 0)),
             min(total, scene["end_frame"] + (2 if index + 1 < len(scenes) else 0)))
            for index, scene in enumerate(scenes)]


def validate_mix(record, *, audio_sha256, track, project, scenes=None, fps=30):
    """Require the actual canonical source-audio execution, retaining original track time."""
    mix = document(record)
    if (mix.get("schema") != MIX_SCHEMA or mix.get("audio_sha256") != audio_sha256
            or mix.get("track_sha256") != [track["sha256"]] or mix.get("returncode") != 0):
        raise WorkflowError("music mix must bind the accepted audio and one original musical recording")
    execution = document(mix["execution"])
    source_plan = document(mix["source_plan"])
    if (execution.get("kind") != "mix" or execution.get("state") != "completed"
            or execution.get("returncode") != 0 or execution.get("argv") != mix.get("argv")
            or not any(item.get("sha256") == audio_sha256 for item in execution.get("output_artifacts", []))):
        raise WorkflowError("music mix needs the successful native source-audio execution")
    script = Path(project) / "automation/audio_mix.py"
    argv = execution.get("argv", [])
    if (len(argv) != 5 or Path(argv[1]).resolve() != script.resolve()
            or execution.get("script_sha256") != file_digest(script)
            or argv[2] != mix["source_plan"]["path"] or argv[3] != "--output"
            or not any(item.get("path") == argv[4] and item.get("sha256") == audio_sha256
                       for item in execution.get("output_artifacts", []))):
        raise WorkflowError("music mix must identify the exact canonical source-audio command")
    if source_plan.get("schema") != "ytv-source-audio-v1" or not isinstance(source_plan.get("segments"), list):
        raise WorkflowError("music mix requires its exact canonical source plan")
    segments = source_plan["segments"]
    if not segments or (scenes is not None and [item.get("id") for item in segments] != [item["id"] for item in scenes]):
        raise WorkflowError("music source segments differ from the accepted edit order")
    cursor = track["source_in_seconds"]
    for index, segment in enumerate(segments):
        if (segment.get("sha256") != track["sha256"] or segment.get("path") != track["path"]
                or segment.get("gain") != 1 or abs(segment.get("start_seconds", -100) - cursor) > 1e-6):
            raise WorkflowError("music must retain one continuous accepted excerpt without invented gain or gaps")
        if scenes is not None:
            expected = track["source_in_seconds"] + scenes[index]["end_frame"] / fps
            if abs(segment.get("end_seconds", -100) - expected) > 1e-6:
                raise WorkflowError("music segment bounds differ from the exact edit timeline")
        cursor = segment["end_seconds"]
    inputs = execution.get("inputs", [])
    if mix["source_plan"] not in inputs or {"path": track["path"], "sha256": track["sha256"]} not in inputs:
        raise WorkflowError("music execution omitted its actual source or source plan")
    return mix, [mix["execution"], mix["source_plan"]]


def validate_plan(plan, requirements, *, base, project, script):
    try:
        return _validate_plan(plan, requirements, project=project, script=script)
    except (KeyError, TypeError, ValueError, OSError) as exc:
        raise WorkflowError("incomplete or invalid music manifest: " + str(exc)) from exc


def _validate_plan(plan, requirements, *, project, script):
    """Check exact policy and canonical planner/word inputs before any encoding."""
    from .production_contract import validate_render_manifest

    timeline = validate_render_manifest(plan, requirements)
    if plan.get("schema") != MANIFEST_SCHEMA or requirements.get("music_edit") is None:
        raise WorkflowError("music rendering requires its registered music-edit policy")
    policy = requirements["music_edit"]
    transition = plan.get("transition", {})
    fixed = {key: value for key, value in transition.items() if key not in {"blur_sigma_px", "brightness"}}
    if plan.get("color") != policy["color"] or fixed != policy["transition"]:
        raise WorkflowError("music color and transition settings must match the pinned policy")
    for key, maximum in (("blur_sigma_px", 100), ("brightness", 1)):
        value = transition.get(key)
        if type(value) not in (int, float) or not math.isfinite(value) or not 0 < value <= maximum:
            raise WorkflowError("every musical cut requires positive finite " + key)
    if plan.get("overlays"):
        raise WorkflowError("music picture uses only the canonical lyric-mask overlay")
    fps = 30
    if str(requirements["video"]["fps"]) not in {"30", "30/1"}:
        raise WorkflowError("the registered music compositor requires 30 fps")
    if script["kind"] != "edit_script" or script["mode"] not in {"source", "none"}:
        raise WorkflowError("music-first rendering needs an accepted vocal/instrumental edit script, never narration")
    sub = plan.get("subtitles")
    allowed_subtitles = {"mode", "words", "font", "settings", "beats"} if script["mode"] == "source" else {"mode"}
    if not isinstance(sub, dict) or set(sub) - allowed_subtitles:
        raise WorkflowError("music subtitles contain unsupported settings; no caption intent may be silently ignored")
    if file_digest(Path(plan["script"])) != script["artifact_sha256"]:
        raise WorkflowError("music manifest script differs from the accepted edit")
    scenes = plan["scenes"]
    if [item.get("id") for item in scenes] != script["segment_ids"] or len(scenes) < 2:
        raise WorkflowError("music scenes must preserve the accepted ordered shot plan, including its cuts")
    inputs = [file_record(plan["audio"]), file_record(plan["script"])]
    intervals = visible_intervals(scenes)
    seen_sources = set()
    for scene, (first, stop) in zip(scenes, intervals):
        if scene["end_frame"] - scene["start_frame"] < 4:
            raise WorkflowError("music shots must leave room for the three-frame transition")
        expected_zoom = policy["zoom"] if scene.get("zoom") == "in" else list(reversed(policy["zoom"]))
        if (scene.get("zoom") not in {"in", "out"} or scene.get("direction") != "none"
                or scene.get("scale") != expected_zoom or scene.get("easing") != "smoothstep"):
            raise WorkflowError("each music shot needs continuous pinned 95–105% smoothstep motion")
        source = scene.get("source")
        if not isinstance(source, dict):
            raise WorkflowError("music shot needs its original source identity and interval")
        original = {key: source.get(key) for key in ("path", "sha256")}
        checked(original)
        if source["sha256"] in seen_sources:
            raise WorkflowError("one original footage source may appear only once in the edit")
        seen_sources.add(source["sha256"])
        seconds = (stop - first) / fps
        start, end = source.get("start_seconds"), source.get("end_seconds")
        if (type(start) not in (int, float) or type(end) not in (int, float)
                or not math.isfinite(start) or not math.isfinite(end) or start < 0
                or abs(end - start - seconds) > 1e-6):
            raise WorkflowError("music shot source range must include its exact transition overlap")
        clip = file_record(scene["clip"])
        actual = probe_media(clip["path"])
        if not actual["video"] or abs(actual["duration_seconds"] - seconds) > 1 / fps + .001:
            raise WorkflowError("prepared music clip does not contain its full visible interval")
        if end > probe_media(original["path"])["duration_seconds"] + .001:
            raise WorkflowError("music footage range exceeds its actual original source")
        checked(source.get("rights_evidence"))
        inputs.extend([clip, original, source["rights_evidence"]])
    tracks = plan["music"]["tracks"]
    if len(tracks) != 1 or plan["music"].get("silences"):
        raise WorkflowError("music-first renders one continuous approved musical excerpt")
    track = tracks[0]
    if (type(track.get("source_in_seconds")) not in (int, float) or not math.isfinite(track["source_in_seconds"])
            or track["source_in_seconds"] < 0 or track["start_frame"] != 0 or track["end_frame"] != timeline["frames"]):
        raise WorkflowError("music must cover the complete timeline and retain its original excerpt offset")
    original_track = {key: track[key] for key in ("path", "sha256")}
    checked(original_track)
    mix, mix_inputs = validate_mix(plan["music"]["mix_evidence"], audio_sha256=file_digest(plan["audio"]),
                                   track=track, scenes=scenes, project=project)
    checked(plan["music"].get("rights_evidence"))
    inputs.extend([original_track, plan["music"]["rights_evidence"], plan["music"]["mix_evidence"], *mix_inputs])
    planner_inputs = plan.get("planner", {})
    if set(planner_inputs) != {"input", "output"}:
        raise WorkflowError("music rendering needs the canonical planner input and output")
    planner_plan = document(planner_inputs["input"])
    planned = document(planner_inputs["output"])
    if (Path(planner_plan.get("media", "")).resolve() != Path(plan["audio"]).resolve()
            or planner_plan.get("fps") != fps or planner_plan.get("frames") != timeline["frames"]):
        raise WorkflowError("music planner must use the exact final audio and edit duration")
    for accent in planner_plan.get("approved_accents", []):
        require_text(accent.get("reason"), "manually confirmed musical accent reason")
        checked(accent.get("evidence"))
        inputs.append(accent["evidence"])
    planner = helper(project, "automation/music_montage.py", "ytv_music_planner")
    if planned != planner.plan_timeline(planner_plan):
        raise WorkflowError("music planner output is stale or was edited outside the canonical planner")
    cuts = [scene["start_frame"] for scene in scenes[1:]]
    if ([item["frame"] for item in planned["accents"]] != cuts or len(planned["clips"]) != len(scenes)
            or [item["id"] for item in planned["clips"]] != script["segment_ids"]):
        raise WorkflowError("music cuts and scene order differ from the bound accent plan")
    for chosen, scene in zip(planned["clips"], scenes):
        if Path(chosen["path"]).resolve() != Path(scene["source"]["path"]).resolve() or chosen["source_in"] != scene["source"]["start_seconds"]:
            raise WorkflowError("music edit does not use the exact planner source excerpt")
    inputs.extend(planner_inputs.values())
    lyrics, beat_frames = None, []
    if script["mode"] == "source":
        if sub.get("mode") != "lyrics":
            raise WorkflowError("a vocal music edit requires canonical lyric captions")
        words = document(sub.get("words"))
        if (words.get("audio_sha256") != file_digest(plan["audio"])
                or words.get("transcript_sha256") != hashlib.sha256(script["text"].encode()).hexdigest()):
            raise WorkflowError("lyric word map must bind the accepted music and every accepted lyric word")
        entries = words.get("words")
        def letters(word):
            return "".join(character for character in unicodedata.normalize("NFC", word) if character.isalnum())
        expected = [letters(word) for word in script["text"].split()]
        if (not isinstance(entries, list) or not entries or not all(expected)
                or [letters(item.get("text", "")) for item in entries] != expected):
            raise WorkflowError("lyric timings omit, change or invent accepted sung words")
        previous = -1
        for entry in entries:
            start, end = entry.get("start_seconds"), entry.get("end_seconds")
            if (type(start) not in (int, float) or type(end) not in (int, float)
                    or not math.isfinite(start) or not math.isfinite(end)
                    or not 0 <= start < end <= timeline["duration_seconds"] or start <= previous):
                raise WorkflowError("lyric words need complete ordered times in the final excerpt")
            previous = start
        font = sub.get("font")
        if not isinstance(font, dict) or set(font) != {"path", "sha256", "index"}:
            raise WorkflowError("vocal captions require the exact selected font file and face")
        checked({key: font[key] for key in ("path", "sha256")})
        validate_font_face(font["path"], font["index"], requirements["captions"]["font"])
        if sub.get("settings") != policy["lyrics"]:
            raise WorkflowError("vocal caption settings differ from the pinned one-word inversion recipe")
        inputs.extend([sub["words"], {key: font[key] for key in ("path", "sha256")}])
        lyric_helper = helper(project, "automation/captions/music_lyrics.py", "ytv_lyric_words")
        loaded = lyric_helper.load_words(words, 0, fps, timeline["frames"], keep_source_times=True)
        if len(loaded) != len(entries):
            raise WorkflowError("canonical lyric conversion would drop accepted words; fix their timings first")
        if "beats" in sub:
            beats = document(sub["beats"])
            if (not isinstance(beats, dict) or beats.get("sha256") != file_digest(plan["audio"])
                    or beats.get("fps") != fps or beats.get("frames") != timeline["frames"]
                    or beats.get("source_start_seconds") != 0
                    or type(beats.get("duration_seconds")) not in (int, float)
                    or not math.isfinite(beats["duration_seconds"])
                    or abs(beats["duration_seconds"] - timeline["duration_seconds"]) > 1 / 22050 + 1e-9):
                raise WorkflowError("lyric beat map must bind the exact accepted audio, fps and complete frame timeline")
            candidates = beats.get("candidates")
            if (not isinstance(candidates, list) or any(not isinstance(item, dict)
                    or type(item.get("frame")) is not int or not 0 <= item["frame"] < timeline["frames"]
                    for item in candidates)):
                raise WorkflowError("lyric beat candidates require in-timeline integer frames")
            beat_frames = [item["frame"] for item in candidates]
            if beat_frames != sorted(set(beat_frames)):
                raise WorkflowError("lyric beat candidate frames must be unique and increasing")
            inputs.append(sub["beats"])
        lyrics = {"entries": entries, "font": font, "settings": sub["settings"]}
    elif plan.get("subtitles", {}).get("mode") != "none":
        raise WorkflowError("instrumental edits must not invent lyric captions")
    if timeline["requires_srt"]:
        inputs.append(file_record(plan["srt"]))
    return {**timeline, "cuts": cuts, "beat_frames": beat_frames, "visible_intervals": intervals, "inputs": inputs,
            "planned": planned, "lyrics": lyrics, "track": track, "mix": mix}


def validate_lyric_plan(value, plan, prepared, project):
    """Check every rounded/snapped word and held gap against the canonical source map."""
    module = helper(project, "automation/captions/music_lyrics.py", "ytv_lyric_plan_check")
    words = module.load_words(document(plan["subtitles"]["words"]), 0, 30, prepared["frames"], keep_source_times=True)
    beats = sorted(set(prepared["cuts"] + prepared["beat_frames"]))
    snapped = module.sync_vocal_starts(words, beats, set(prepared["cuts"]), 30, prepared["frames"])
    if (value.get("fps") != 30 or value.get("frames") != prepared["frames"]
            or value.get("raster") != [module.WIDTH, module.HEIGHT]
            or value.get("font_index") != plan["subtitles"]["font"]["index"]
            or value.get("font_size_px") != plan["subtitles"]["settings"]["font_size_px"]
            or value.get("max_words") != 1 or value.get("stroke_px") != 0
            or value.get("color_mode") != "inversion_masks" or value.get("hold_gap_lt_ms") != 500
            or value.get("beat_transition_scale") != .06
            or value.get("beat_snaps") != {str(key): number for key, number in snapped.items()}
            or value.get("line_motion", {}).get("tilt_every") != 6
            or value.get("line_motion", {}).get("seed") != 17):
        raise WorkflowError("canonical lyric plan changes the actual font, timing or animation recipe")
    groups = value.get("groups", [])
    if len(groups) != len(words):
        raise WorkflowError("canonical lyric output omitted accepted words")
    for index, (group, word) in enumerate(zip(groups, words)):
        following = words[index + 1] if index + 1 < len(words) else None
        next_start = following["start_frame"] if following else prepared["frames"]
        natural_end = min(word["end_frame_exclusive"], next_start)
        gap = following["source_start_seconds"] - word["source_end_seconds"] if following else None
        stop = next_start if gap is not None and 0 <= gap < .5 - 1e-9 else natural_end
        if (group.get("words") != [word] or group.get("start_frame") != word["start_frame"]
                or group.get("end_frame_exclusive") != stop
                or group.get("natural_end_frame_exclusive") != natural_end
                or group.get("held_gap_frames") != stop - natural_end
                or group.get("tilt_enabled") != ((index + 1) % 6 == 0)):
            raise WorkflowError("canonical lyrics must preserve every exact word and its rounded vocal/hold interval")
