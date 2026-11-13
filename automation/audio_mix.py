#!/usr/bin/env python3
"""Extract and concatenate observed source audio without TTS or speed changes."""
import argparse
import hashlib
import json
import math
from pathlib import Path
import subprocess


SCHEMA = "ytv-source-audio-v1"


def file_hash(path):
    with path.open("rb") as incoming:
        return hashlib.file_digest(incoming, "sha256").hexdigest()


def validate_plan(plan, base):
    if (not isinstance(plan, dict) or not {"schema", "segments"} <= set(plan)
            or set(plan) - {"schema", "segments", "fade_out_seconds"} or plan["schema"] != SCHEMA):
        raise ValueError("source audio plan requires schema and ordered segments")
    segments = plan["segments"]
    if not isinstance(segments, list) or not segments:
        raise ValueError("source audio plan requires nonempty segments")
    result, ids = [], set()
    for segment in segments:
        if not isinstance(segment, dict) or set(segment) != {"id", "path", "sha256", "start_seconds", "end_seconds", "gain"}:
            raise ValueError("source segment requires id, path, sha256, bounds and gain")
        identity = segment["id"]
        if not isinstance(identity, str) or not identity.strip() or identity in ids:
            raise ValueError("source segment IDs must be unique")
        ids.add(identity)
        path = Path(segment["path"])
        path = path.resolve() if path.is_absolute() else (base / path).resolve()
        if not path.is_file() or file_hash(path) != segment["sha256"]:
            raise ValueError("source audio segment bytes differ from their hash")
        start, end, gain = (segment[key] for key in ("start_seconds", "end_seconds", "gain"))
        if (any(type(value) not in (int, float) or not math.isfinite(value) for value in (start, end, gain))
                or not 0 <= start < end or not 0 <= gain <= 4):
            raise ValueError("invalid source audio bounds or gain")
        result.append({**segment, "path": path})
    fade = plan.get("fade_out_seconds", 0)
    duration = sum(segment["end_seconds"] - segment["start_seconds"] for segment in result)
    if type(fade) not in (int, float) or not math.isfinite(fade) or not 0 <= fade <= duration:
        raise ValueError("terminal fade must be finite and within the complete mix duration")
    return result


def render(manifest, output):
    manifest, output = Path(manifest).resolve(), Path(output).resolve()
    plan = json.loads(manifest.read_text())
    segments = validate_plan(plan, manifest.parent)
    if output.exists():
        raise ValueError("output exists; preserve it and reconcile before retrying")
    command = ["ffmpeg", "-nostdin", "-v", "error", "-n"]
    filters = []
    for index, segment in enumerate(segments):
        probe = subprocess.run(["ffprobe", "-v", "error", "-protocol_whitelist", "file,pipe", "-select_streams", "a:0",
                                "-show_entries", "stream=codec_name,duration,start_time:format=start_time", "-of", "json", str(segment["path"])],
                               check=True, capture_output=True, text=True, timeout=30)
        actual = json.loads(probe.stdout)
        if not actual.get("streams"):
            raise ValueError("source interval requires actual audio within its duration")
        stream = actual["streams"][0]
        # The container can outlast its audio (for example a silent video tail).
        # Some audio demuxers omit duration; the measured output check below is
        # still mandatory in that case and never trusts container duration.
        if stream.get("duration") not in (None, "N/A"):
            start = float(stream.get("start_time", 0)) - float(actual.get("format", {}).get("start_time", 0))
            end = start + float(stream["duration"])
            if segment["start_seconds"] < start - .001 or segment["end_seconds"] > end + .001:
                raise ValueError("source interval exceeds the actual audio stream")
        command += ["-protocol_whitelist", "file,pipe", "-i", str(segment["path"])]
        filters.append(f"[{index}:a:0]atrim=start={segment['start_seconds']}:end={segment['end_seconds']},"
                       f"asetpts=PTS-STARTPTS,aresample=48000,aformat=channel_layouts=stereo,volume={segment['gain']}[a{index}]")
    duration = sum(segment["end_seconds"] - segment["start_seconds"] for segment in segments)
    fade = plan.get("fade_out_seconds", 0)
    filters.append("".join(f"[a{i}]" for i in range(len(segments))) + f"concat=n={len(segments)}:v=0:a=1[joined]")
    filters.append(f"[joined]afade=t=out:st={duration-fade}:d={fade}[out]" if fade else "[joined]anull[out]")
    output.parent.mkdir(parents=True, exist_ok=True)
    command += ["-filter_complex", ";".join(filters), "-map", "[out]", "-c:a", "pcm_s16le", "-f", "wav", str(output)]
    subprocess.run(command, check=True, stdin=subprocess.DEVNULL, timeout=900)
    measured = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "a:0", "-show_entries",
                               "stream=duration", "-of", "json", str(output)],
                              check=True, capture_output=True, text=True, timeout=30)
    actual_duration = float(json.loads(measured.stdout)["streams"][0]["duration"])
    if not math.isfinite(actual_duration) or abs(actual_duration - duration) > max(.001, len(segments) / 48000):
        raise ValueError("actual mixed audio does not cover the complete requested intervals")
    return {"output": str(output), "sha256": file_hash(output), "segments": len(segments), "speed": 1.0,
            "duration_seconds": actual_duration, "fade_out_seconds": fade}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    print(json.dumps(render(args.manifest, args.output)))


if __name__ == "__main__":
    main()
