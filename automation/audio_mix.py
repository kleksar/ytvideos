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
    if not isinstance(plan, dict) or set(plan) != {"schema", "segments"} or plan["schema"] != SCHEMA:
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
    return result


def render(manifest, output):
    manifest, output = Path(manifest).resolve(), Path(output).resolve()
    segments = validate_plan(json.loads(manifest.read_text()), manifest.parent)
    if output.exists():
        raise ValueError("output exists; preserve it and reconcile before retrying")
    command = ["ffmpeg", "-nostdin", "-v", "error", "-n"]
    filters = []
    for index, segment in enumerate(segments):
        probe = subprocess.run(["ffprobe", "-v", "error", "-protocol_whitelist", "file,pipe", "-select_streams", "a:0",
                                "-show_entries", "stream=codec_name:format=duration", "-of", "json", str(segment["path"])],
                               check=True, capture_output=True, text=True, timeout=30)
        actual = json.loads(probe.stdout)
        if not actual.get("streams") or segment["end_seconds"] > float(actual["format"]["duration"]) + .001:
            raise ValueError("source interval requires actual audio within its duration")
        command += ["-protocol_whitelist", "file,pipe", "-i", str(segment["path"])]
        filters.append(f"[{index}:a:0]atrim=start={segment['start_seconds']}:end={segment['end_seconds']},"
                       f"asetpts=PTS-STARTPTS,aresample=48000,aformat=channel_layouts=stereo,volume={segment['gain']}[a{index}]")
    filters.append("".join(f"[a{i}]" for i in range(len(segments))) + f"concat=n={len(segments)}:v=0:a=1[out]")
    output.parent.mkdir(parents=True, exist_ok=True)
    command += ["-filter_complex", ";".join(filters), "-map", "[out]", "-c:a", "pcm_s16le", "-f", "wav", str(output)]
    subprocess.run(command, check=True, stdin=subprocess.DEVNULL, timeout=900)
    return {"output": str(output), "sha256": file_hash(output), "segments": len(segments), "speed": 1.0}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    print(json.dumps(render(args.manifest, args.output)))


if __name__ == "__main__":
    main()
