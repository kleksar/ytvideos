#!/usr/bin/env python3
"""Render a silent, explicitly frame-addressed local montage trial.

This tool is intentionally separate from the production montage adapter. It
does not create production acceptance, delivery, review, or run completion.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import math
import os
import shutil
import subprocess
import sys
import tempfile
import types
from fractions import Fraction
from pathlib import Path
from typing import Any


SCHEMA = "ytv.montage_trial.v1"
PURPOSE = "montage_trial"
HERE = Path(__file__).resolve().parent
CANONICAL_MONTAGE = HERE / "ffmpeg_montage" / "montage.py"
PINNED_ROOT = CANONICAL_MONTAGE.resolve().parents[2]
CANONICAL_MONTAGE_SHA256 = hashlib.sha256(CANONICAL_MONTAGE.read_bytes()).hexdigest()
_spec = importlib.util.spec_from_file_location("canonical_montage", CANONICAL_MONTAGE)
if _spec is None or _spec.loader is None:
    raise RuntimeError(f"Cannot load canonical image motion code: {CANONICAL_MONTAGE}")
_canonical = types.ModuleType("canonical_montage")
_canonical.__file__ = str(CANONICAL_MONTAGE.resolve())
exec(compile(CANONICAL_MONTAGE.read_bytes(), _canonical.__file__, "exec"), _canonical.__dict__)
if hashlib.sha256(CANONICAL_MONTAGE.read_bytes()).hexdigest() != CANONICAL_MONTAGE_SHA256:
    raise RuntimeError("canonical montage dependency changed while loading")
if str(PINNED_ROOT / "src") not in sys.path:
    sys.path.insert(0, str(PINNED_ROOT / "src"))
from ytvideos import media_checks as _media_checks  # noqa: E402 -- pinned checkout path must precede import
CANONICAL_MEDIA_CHECKS = PINNED_ROOT / "src" / "ytvideos" / "media_checks.py"
if Path(_media_checks.__file__).resolve() != CANONICAL_MEDIA_CHECKS.resolve():
    raise RuntimeError(f"Loaded media checks from outside the pinned checkout: {_media_checks.__file__}")
CANONICAL_MEDIA_CHECKS_SHA256 = hashlib.sha256(CANONICAL_MEDIA_CHECKS.read_bytes()).hexdigest()
if hashlib.sha256(CANONICAL_MEDIA_CHECKS.read_bytes()).hexdigest() != CANONICAL_MEDIA_CHECKS_SHA256:
    raise RuntimeError("canonical media checks dependency changed while loading")


class TrialError(ValueError):
    """Invalid trial manifest or an unverifiable render outcome."""


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _exact_keys(value: dict[str, Any], required: set[str], optional: set[str], where: str) -> None:
    missing = required - value.keys()
    extra = value.keys() - required - optional
    if missing or extra:
        raise TrialError(f"{where}: missing keys {sorted(missing)}; unsupported keys {sorted(extra)}")


def _positive_int(value: Any, where: str) -> int:
    if type(value) is not int or value <= 0:
        raise TrialError(f"{where} must be an explicit positive integer")
    return value


def _finite_number(value: Any, where: str, *, minimum: float | None = None) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise TrialError(f"{where} must be a finite number")
    number = float(value)
    if minimum is not None and number < minimum:
        raise TrialError(f"{where} must be at least {minimum}")
    return number


def _digest(value: Any, where: str) -> str:
    if not isinstance(value, str) or len(value) != 64 or any(c not in "0123456789abcdef" for c in value):
        raise TrialError(f"{where} must be a lowercase SHA-256 hex digest")
    return value


def resolve_path(base: Path, value: Any, where: str) -> Path:
    if not isinstance(value, str) or not value:
        raise TrialError(f"{where} must be an explicit non-empty path")
    path = Path(value).expanduser()
    return (path if path.is_absolute() else base / path).resolve()


def ffprobe(path: Path) -> dict[str, Any]:
    command = [
        "ffprobe", "-v", "error", "-protocol_whitelist", "file,pipe",
        "-format_whitelist", "mov,png_pipe", "-count_frames", "-show_streams", "-show_format",
        "-of", "json", str(path),
    ]
    result = subprocess.run(command, check=True, stdin=subprocess.DEVNULL,
                            capture_output=True, text=True)
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise TrialError(f"ffprobe returned invalid JSON for {path}") from exc


def _video_stream(probe: dict[str, Any], where: str) -> dict[str, Any]:
    streams = [stream for stream in probe.get("streams", []) if stream.get("codec_type") == "video"]
    if len(streams) != 1:
        raise TrialError(f"{where} must contain exactly one video stream")
    return streams[0]


def _input_record(path: Path, expected: str, where: str) -> dict[str, Any]:
    if not path.is_file():
        raise TrialError(f"{where} does not exist: {path}")
    observed = sha256_file(path)
    if observed != expected:
        raise TrialError(f"{where} hash mismatch: expected {expected}, observed {observed}")
    return {"path": str(path), "sha256": observed, "size_bytes": path.stat().st_size}


def validate(manifest: Any, manifest_path: Path) -> dict[str, Any]:
    if not isinstance(manifest, dict):
        raise TrialError("manifest root must be an object")
    _exact_keys(manifest, {"schema", "purpose", "provenance", "timing_basis", "canvas", "fps", "audio_policy", "scenes"}, set(), "manifest")
    if manifest["schema"] != SCHEMA or manifest["purpose"] != PURPOSE:
        raise TrialError(f"manifest schema/purpose must be {SCHEMA}/{PURPOSE}")
    provenance = manifest["provenance"]
    if not isinstance(provenance, dict):
        raise TrialError("provenance must be an object")
    _exact_keys(provenance, {"run_id", "script", "storyboard"}, set(), "provenance")
    if not isinstance(provenance["run_id"], str) or not provenance["run_id"].strip():
        raise TrialError("provenance.run_id must be explicit")
    document_records = {}
    for key in ("script", "storyboard"):
        document = provenance[key]
        if not isinstance(document, dict):
            raise TrialError(f"provenance.{key} must contain path and sha256")
        _exact_keys(document, {"path", "sha256"}, set(), f"provenance.{key}")
        doc_path = resolve_path(manifest_path.parent, document["path"], f"provenance.{key}.path")
        expected = _digest(document["sha256"], f"provenance.{key}.sha256")
        document_records[key] = _input_record(doc_path, expected, f"provenance.{key}")
    canvas = manifest["canvas"]
    if not isinstance(canvas, list) or len(canvas) != 2:
        raise TrialError("canvas must explicitly contain [width, height]")
    width, height = (_positive_int(canvas[0], "canvas width"), _positive_int(canvas[1], "canvas height"))
    if width % 2 or height % 2:
        raise TrialError("canvas dimensions must be even for yuv420p")
    fps = manifest["fps"]
    if type(fps) is not int or fps < 1 or fps > 120:
        raise TrialError("fps must be an explicit integer from 1 through 120")
    if manifest["audio_policy"] != "mute":
        raise TrialError("this montage_trial version supports only audio_policy=mute")
    if not isinstance(manifest["timing_basis"], str) or not manifest["timing_basis"].strip():
        raise TrialError("timing_basis must explicitly describe the provisional trial windows")
    scenes = manifest["scenes"]
    if not isinstance(scenes, list) or not scenes:
        raise TrialError("scenes must be a non-empty explicit list")

    base = manifest_path.parent
    normalized: list[dict[str, Any]] = []
    seen_ids: set[str] = set()
    cursor = 0
    for index, scene in enumerate(scenes):
        where = f"scenes[{index}]"
        if not isinstance(scene, dict):
            raise TrialError(f"{where} must be an object")
        scene_type = scene.get("type")
        common = {"id", "type", "source", "source_sha256", "start_frame", "end_frame"}
        scene_id = scene.get("id")
        if not isinstance(scene_id, str) or not scene_id.strip() or scene_id in seen_ids:
            raise TrialError(f"{where}.id must be unique and non-empty")
        seen_ids.add(scene_id)
        if scene_type == "image":
            _exact_keys(scene, common | {"direction", "zoom"}, {"camera"}, where)
            direction, zoom = scene["direction"], scene["zoom"]
            if direction not in _canonical.DIRECTIONS or zoom not in _canonical.ZOOMS:
                raise TrialError(f"{where} has unsupported direction/zoom")
            camera = scene.get("camera")
            if camera is not None:
                try:
                    _canonical.validate_camera(camera, direction, zoom)
                except (KeyError, TypeError, ValueError) as exc:
                    raise TrialError(f"{where}.camera is unsupported or invalid: {exc}") from exc
        elif scene_type == "video":
            _exact_keys(scene, common | {"source_in_seconds", "used_duration_frames", "direction", "zoom"}, set(), where)
            direction, zoom = scene["direction"], scene["zoom"]
            if direction != "none" or zoom != "none":
                raise TrialError(f"{where} video clips must explicitly use direction=none and zoom=none")
            camera = None
            source_in = _finite_number(scene["source_in_seconds"], f"{where}.source_in_seconds", minimum=0)
            used_frames = _positive_int(scene["used_duration_frames"], f"{where}.used_duration_frames")
        else:
            raise TrialError(f"{where}.type must be image or video")
        start = scene["start_frame"]
        end = scene["end_frame"]
        if type(start) is not int or start != cursor or type(end) is not int or end <= start:
            raise TrialError(f"{where} must have explicit, continuous [start_frame, end_frame) bounds")
        frames = end - start
        if scene_type == "video" and used_frames != frames:
            raise TrialError(f"{where}.used_duration_frames must equal the timeline window ({frames})")
        source = resolve_path(base, scene["source"], f"{where}.source")
        expected = _digest(scene["source_sha256"], f"{where}.source_sha256")
        record = _input_record(source, expected, f"{where}.source")
        row = {"id": scene_id, "type": scene_type, "source": source, "source_record": record,
               "start_frame": start, "end_frame": end, "frames": frames}
        if scene_type == "image":
            row.update(direction=direction, zoom=zoom, camera=camera)
        else:
            row.update(source_in_seconds=source_in, used_duration_frames=used_frames,
                       direction=direction, zoom=zoom)
        normalized.append(row)
        cursor = end
    return {"manifest_path": manifest_path.resolve(), "manifest": manifest,
            "document_records": document_records,
            "canvas": [width, height], "fps": fps, "frames": cursor,
            "duration_seconds": cursor / fps, "scenes": normalized}


def _filter_for_scene(scene: dict[str, Any], canvas: list[int], fps: int) -> str:
    width, height = canvas
    frames = scene["frames"]
    if scene["type"] == "image":
        if scene["camera"] is not None:
            motion = _canonical.camera_filter(width, height, frames, scene["camera"])
        else:
            motion = _canonical.motion_filter(width, height, frames, scene["direction"], scene["zoom"])
        if not motion.endswith(",format=yuv420p"):
            raise TrialError("canonical image motion filter shape changed; cannot apply verified color conversion")
        motion = motion.removesuffix(",format=yuv420p")
        # colorspace requires even dimensions even for yuv444p. Fit the same
        # cover canvas in RGB first; do not pad or discard an arbitrary edge.
        color = (f"format=gbrp,scale={width}:{height}:force_original_aspect_ratio=increase:flags=lanczos,"
                 f"crop={width}:{height},format=gbrp,"
                 "scale=out_color_matrix=bt709:out_range=tv,format=yuv444p,"
                 "colorspace=all=bt709:space=bt709:range=tv:iall=bt709:iprimaries=bt709:"
                 "itrc=iec61966-2-1:ispace=bt709:irange=tv")
        return f"{color},{motion},fps={fps},trim=end_frame={frames},setpts=PTS-STARTPTS,format=yuv420p"
    color = scene["source_probe"]
    return ("colorspace=all=bt709:range=tv:iall=bt709:iprimaries=bt709:"
            f"itrc={color['color_transfer']}:ispace={color['color_space']}:irange={color['color_range']},"
            f"scale={width}:{height}:force_original_aspect_ratio=increase:flags=lanczos,"
            f"crop={width}:{height},setsar=1,fps={fps},trim=end_frame={frames},"
            "setpts=PTS-STARTPTS,format=yuv420p")


def _check_video_window(scene: dict[str, Any], fps: int) -> dict[str, Any]:
    probe = ffprobe(scene["source"])
    stream = _video_stream(probe, scene["source"])
    observed_color = {"primaries": stream.get("color_primaries"), "transfer": stream.get("color_transfer"),
                      "matrix": stream.get("color_space"), "range": stream.get("color_range")}
    supported = (observed_color["primaries"] == "bt709"
                 and observed_color["transfer"] in {"bt709", "iec61966-2-1", "smpte170m"}
                 and observed_color["matrix"] in {"bt709", "smpte170m"}
                 and observed_color["range"] in {"tv", "pc"})
    if not supported:
        raise TrialError(f"unsupported or unknown SDR video color metadata: {observed_color}")
    raw_duration = stream.get("duration") or probe.get("format", {}).get("duration", "nan")
    duration = float(raw_duration)
    source_in = scene["source_in_seconds"]
    used = scene["used_duration_frames"] / fps
    try:
        anchors = _media_checks.source_frame_anchors(scene["source"], source_in, source_in + used)
    except _media_checks.WorkflowError as exc:
        raise TrialError(f"source video frame window is not verified: {exc}") from exc
    return {**_stream_metadata(stream, duration), "source_frame_anchors_seconds": anchors}


def _stream_metadata(stream: dict[str, Any], duration: float | None = None) -> dict[str, Any]:
    keys = ("width", "height", "avg_frame_rate", "r_frame_rate", "nb_read_frames",
            "color_primaries", "color_transfer", "color_space", "color_range")
    result = {key: stream.get(key) for key in keys}
    if duration is not None and math.isfinite(duration):
        result["duration_seconds"] = duration
    return result


def _render_command(plan: dict[str, Any], temp_output: Path, inputs: list[dict[str, Any]]) -> list[str]:
    fps = plan["fps"]
    command = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-n"]
    for scene in plan["scenes"]:
        duration = scene["frames"] / fps
        command.extend(["-protocol_whitelist", "file,pipe", "-format_whitelist", "mov,png_pipe"])
        if scene["type"] == "image":
            command.extend(["-loop", "1", "-framerate", str(fps), "-t", f"{duration:.9f}", "-i", str(scene["source"])])
        else:
            command.extend(["-ss", f"{scene['source_in_seconds']:.9f}", "-t", f"{duration:.9f}", "-i", str(scene["source"])])
    filters = []
    labels = []
    for index, scene in enumerate(plan["scenes"]):
        label = f"s{index}"
        filters.append(f"[{index}:v]{_filter_for_scene(scene, plan['canvas'], fps)}[{label}]")
        labels.append(f"[{label}]")
    filters.append(f"{''.join(labels)}concat=n={len(labels)}:v=1:a=0[vout]")
    command.extend(["-filter_complex", ";".join(filters), "-map", "[vout]", "-an",
                    "-frames:v", str(plan["frames"]), "-r", str(fps), "-vsync", "cfr",
                    "-c:v", "libx264", "-crf", "18", "-preset", "medium",
                    "-pix_fmt", "yuv420p", "-color_primaries", "bt709",
                    "-color_trc", "bt709", "-colorspace", "bt709", "-color_range", "tv",
                    "-movflags", "+faststart",
                    str(temp_output)])
    return command


def render(manifest_path: Path, output_path: Path) -> dict[str, Any]:
    manifest_path = manifest_path.expanduser().resolve()
    output_path = output_path.expanduser().resolve()
    receipt_path = Path(str(output_path) + ".montage_trial.json")
    if output_path.exists() or receipt_path.exists():
        raise TrialError("output or receipt already exists; this helper never overwrites trial artifacts")
    if not manifest_path.is_file():
        raise TrialError(f"manifest does not exist: {manifest_path}")
    try:
        manifest_bytes = manifest_path.read_bytes()
        manifest_hash = hashlib.sha256(manifest_bytes).hexdigest()
        manifest = json.loads(manifest_bytes.decode("utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise TrialError(f"cannot read UTF-8 JSON manifest: {exc}") from exc
    plan = validate(manifest, manifest_path)
    for scene in plan["scenes"]:
        scene["source_probe"] = _check_video_window(scene, plan["fps"]) if scene["type"] == "video" else None
    ffmpeg_path = shutil.which("ffmpeg")
    ffprobe_path = shutil.which("ffprobe")
    if not ffmpeg_path or not ffprobe_path:
        raise TrialError("ffmpeg and ffprobe must both be available on PATH")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_record = _input_record(manifest_path, manifest_hash, "manifest")
    dependency_record = _input_record(CANONICAL_MONTAGE, CANONICAL_MONTAGE_SHA256, "canonical montage dependency")
    media_checks_record = _input_record(CANONICAL_MEDIA_CHECKS, CANONICAL_MEDIA_CHECKS_SHA256, "canonical media checks dependency")
    document_records_before = plan["document_records"]
    for scene in plan["scenes"]:
        source_probe = ffprobe(scene["source"])
        source_stream = _video_stream(source_probe, scene["source"])
        raw_duration = source_probe.get("format", {}).get("duration")
        duration = float(raw_duration) if raw_duration is not None else None
        scene["source_metadata"] = _stream_metadata(source_stream, duration)
        scene["source_color_interpretation"] = (
            {"basis": "Probed video stream tags", "primaries": source_stream.get("color_primaries"),
             "transfer": source_stream.get("color_transfer"), "matrix": source_stream.get("color_space"),
             "range": source_stream.get("color_range")}
            if scene["type"] == "video" else
            {"basis": "Explicit local trial assumption for RGB PNG input", "primaries": "bt709",
             "transfer": "iec61966-2-1", "matrix": "gbr", "range": "pc"})
    if sha256_file(manifest_path) != manifest_hash:
        raise TrialError("manifest changed during preflight")
    input_records_before = [scene["source_record"] for scene in plan["scenes"]]
    with tempfile.TemporaryDirectory(prefix="montage-trial-", dir=output_path.parent) as work_dir:
        temp_output = Path(work_dir) / "trial.mp4"
        command = [ffmpeg_path if item == "ffmpeg" else ffprobe_path if item == "ffprobe" else item
                   for item in _render_command(plan, temp_output, input_records_before)]
        # Ensure no manifest values can inject shell syntax; the command is an argv list.
        completed = subprocess.run(command, check=True, stdin=subprocess.DEVNULL,
                                   capture_output=True, text=True)
        if not temp_output.is_file():
            raise TrialError("ffmpeg returned success without creating a video")
        output_probe = ffprobe(temp_output)
        stream = _video_stream(output_probe, temp_output)
        frame_count = int(stream.get("nb_read_frames", -1))
        if frame_count != plan["frames"]:
            raise TrialError(f"render frame count mismatch: expected {plan['frames']}, observed {frame_count}")
        expected_geometry = {"width": plan["canvas"][0], "height": plan["canvas"][1],
                             "sample_aspect_ratio": "1:1", "codec_name": "h264"}
        observed_geometry = {key: stream.get(key) for key in expected_geometry}
        if observed_geometry != expected_geometry:
            raise TrialError(f"render geometry/codec mismatch: expected {expected_geometry}, observed {observed_geometry}")
        expected_output_color = {"pix_fmt": "yuv420p", "color_primaries": "bt709",
                                 "color_transfer": "bt709", "color_space": "bt709", "color_range": "tv"}
        observed_output_color = {key: stream.get(key) for key in expected_output_color}
        if observed_output_color != expected_output_color:
            raise TrialError(f"render color conversion verification failed: expected {expected_output_color}, observed {observed_output_color}")
        if any(item.get("codec_type") == "audio" for item in output_probe.get("streams", [])):
            raise TrialError("silent trial unexpectedly contains an audio stream")
        observed_fps = stream.get("avg_frame_rate")
        if observed_fps is None or Fraction(observed_fps) != Fraction(plan["fps"], 1):
            raise TrialError(f"render frame rate mismatch: expected {plan['fps']}, observed {observed_fps}")
        output_record = {"path": str(output_path), "sha256": sha256_file(temp_output),
                         "size_bytes": temp_output.stat().st_size}
        input_records_after = [_input_record(scene["source"], scene["source_record"]["sha256"], "source after render")
                               for scene in plan["scenes"]]
        if input_records_before != input_records_after:
            raise TrialError("source hashes or sizes changed during render")
        document_records_after = {
            key: _input_record(Path(record["path"]), record["sha256"], f"provenance.{key} after render")
            for key, record in document_records_before.items()
        }
        if document_records_before != document_records_after:
            raise TrialError("script/storyboard provenance hashes or sizes changed during render")
        if sha256_file(manifest_path) != manifest_hash:
            raise TrialError("manifest changed during render")
        if sha256_file(CANONICAL_MONTAGE) != CANONICAL_MONTAGE_SHA256:
            raise TrialError("canonical montage dependency changed during render")
        if sha256_file(CANONICAL_MEDIA_CHECKS) != CANONICAL_MEDIA_CHECKS_SHA256:
            raise TrialError("canonical media checks dependency changed during render")
        receipt = {
            "schema": "ytv.montage_trial_receipt.v1",
            "purpose": PURPOSE,
            "manifest": manifest_record,
            "canonical_dependencies": {"montage": dependency_record, "media_checks": media_checks_record},
            "provenance": {"run_id": manifest["provenance"]["run_id"],
                           "script": document_records_after["script"],
                           "storyboard": document_records_after["storyboard"],
                           "run_id_authority": "declared by manifest; not authenticated by this local helper"},
            "timing_basis": manifest["timing_basis"],
            "inputs": [{"id": scene["id"], "type": scene["type"], **before,
                        "source_in_seconds": scene.get("source_in_seconds"),
                        "used_duration_frames": scene.get("used_duration_frames"),
                        "source_probe": scene.get("source_probe") or scene.get("source_metadata"),
                        "source_color_interpretation": scene["source_color_interpretation"]}
                       for scene, before in zip(plan["scenes"], input_records_after)],
            "timeline": {"canvas": plan["canvas"], "fps": plan["fps"], "frames": plan["frames"],
                         "duration_seconds": plan["duration_seconds"], "audio_policy": "mute",
                         "scenes": [{"id": s["id"], "type": s["type"], "start_frame": s["start_frame"], "end_frame": s["end_frame"],
                                     "source": str(s["source"]),
                                     **({"direction": s["direction"], "zoom": s["zoom"], "camera": s["camera"]}
                                        if s["type"] == "image" else
                                        {"source_in_seconds": s["source_in_seconds"],
                                     "used_duration_frames": s["used_duration_frames"],
                                     "direction": s["direction"], "zoom": s["zoom"]})}
                                    for s in plan["scenes"]]},
            "command": command,
            "ffmpeg_version": subprocess.run([ffmpeg_path, "-version"], check=True, capture_output=True,
                                              text=True).stdout.splitlines()[0],
            "ffprobe_version": subprocess.run([ffprobe_path, "-version"], check=True, capture_output=True,
                                               text=True).stdout.splitlines()[0],
            "encoding": {"video_codec": "libx264", "crf": 18, "preset": "medium",
                          "pixel_format": "yuv420p", "color_primaries": "bt709", "color_transfer": "bt709",
                          "colorspace": "bt709", "color_range": "tv", "color_quality_claim": False,
                          "conversion": "Actual FFmpeg colorspace filter conversion applied; input metadata/assumptions are recorded; output tags alone are not a color quality claim."},
            "process_returncode": completed.returncode,
            "process_stderr": completed.stderr,
            "output": output_record,
            "probe": output_probe,
            "production_acceptance": False,
            "review": "UNVERIFIED",
            "source_unchanged": True,
        }
        receipt_temp = Path(work_dir) / "trial.receipt.json"
        receipt_temp.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        _publish_no_clobber(temp_output, receipt_temp, output_path, receipt_path)
    return receipt


def _publish_no_clobber(temp_output: Path, temp_receipt: Path, output_path: Path, receipt_path: Path) -> None:
    """Publish with atomic links; never replace a concurrent destination."""
    output_linked = False
    try:
        os.link(temp_output, output_path)
        output_linked = True
        os.link(temp_receipt, receipt_path)
    except FileExistsError as exc:
        if output_linked and os.path.samefile(output_path, temp_output):
            output_path.unlink()
        raise TrialError("output or receipt appeared during render; no existing artifact was overwritten") from exc
    except OSError as exc:
        if output_linked and output_path.exists() and os.path.samefile(output_path, temp_output):
            output_path.unlink()
        raise TrialError(f"cannot safely publish trial artifacts with atomic no-clobber links: {exc}") from exc


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    try:
        receipt = render(args.manifest, args.output)
    except subprocess.CalledProcessError as exc:
        parser.exit(2, f"montage_trial: subprocess exited {exc.returncode}\n{exc.stderr or ''}\n")
    except (TrialError, OSError) as exc:
        parser.exit(2, f"montage_trial: {exc}\n")
    print(json.dumps({"output": receipt["output"], "receipt": str(Path(str(args.output.resolve()) + ".montage_trial.json")),
                      "review": receipt["review"], "production_acceptance": receipt["production_acceptance"]},
                     ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
