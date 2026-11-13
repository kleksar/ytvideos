#!/usr/bin/env python3
"""Mix explicitly selected local sound layers into an existing montage trial."""
import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import subprocess
import tempfile

RATE = 48000
ROLES = {"narration", "music", "clip", "ambience", "foley"}


def sha(path):
    with path.open("rb") as handle:
        return hashlib.file_digest(handle, "sha256").hexdigest()


def local(path, expected, base):
    path = (base / path).resolve(strict=True)
    if sha(path) != expected:
        raise ValueError(f"input hash mismatch: {path}")
    return path


def execute(argv):
    result = subprocess.run(argv, capture_output=True, text=True)
    if result.returncode:
        raise ValueError(result.stderr[-4000:])
    return result.stdout


def samples(seconds):
    if type(seconds) not in (float, int) or not math.isfinite(seconds) or seconds < 0:
        raise ValueError("expected finite non-negative seconds")
    return round(seconds * RATE)


def mix(manifest_path, output):
    raw = manifest_path.read_bytes()
    m = json.loads(raw)
    if m["schema"] != "ytv.montage_trial_sound.v1":
        raise ValueError("unsupported sound manifest")
    base = manifest_path.parent
    picture = local(m["picture"]["path"], m["picture"]["sha256"], base)
    receipt = local(m["picture_receipt"]["path"], m["picture_receipt"]["sha256"], base)
    picture_record = json.loads(receipt.read_bytes())
    if (picture_record["purpose"] != "montage_trial" or
            picture_record["output"]["sha256"] != m["picture"]["sha256"]):
        raise ValueError("picture must be bound to its montage trial receipt")
    total = samples(picture_record["timeline"]["duration_seconds"])
    fps = picture_record["timeline"]["fps"]
    video_scenes = {s["id"]: s for s in picture_record["timeline"]["scenes"] if s["type"] == "video"}
    required = set(m["required_roles"])
    if not required or not required <= ROLES or not required <= {t["role"] for t in m["layers"]}:
        raise ValueError("missing required sound layer")
    output_receipt = output.with_suffix(".sound.json")
    if output.exists() or output_receipt.exists():
        raise ValueError("output or receipt already exists")
    cmd = ["ffmpeg", "-v", "error", "-nostdin", "-n"]
    inputs = [(picture, m["picture"]["sha256"]), (receipt, m["picture_receipt"]["sha256"])]
    filters = []
    clips = set()
    music = []
    for index, layer in enumerate(m["layers"], 1):
        path = local(layer["path"], layer["sha256"], base)
        inputs.append((path, layer["sha256"]))
        at, start, length, fade_in, fade_out = (
            samples(layer[key]) for key in ("at", "source_in", "duration", "fade_in", "fade_out")
        )
        gain = layer["gain_db"]
        if (layer["role"] not in ROLES or not length or at + length > total
                or fade_in + fade_out > length or type(gain) not in (float, int)
                or not math.isfinite(gain) or not -80 <= gain <= 24):
            raise ValueError(f"invalid layer {index}")
        probe = json.loads(execute([
            "ffprobe", "-v", "error", "-protocol_whitelist", "file,pipe",
            "-format_whitelist", "mov,wav,mp3", "-select_streams", "a:0",
            "-show_entries", "stream=duration", "-of", "json", str(path),
        ]))["streams"]
        if not probe or start + length > samples(float(probe[0]["duration"])):
            raise ValueError(f"layer {index} exceeds its source audio")
        if layer["role"] == "clip":
            scene = video_scenes.get(layer["scene"])
            if (not scene or scene["id"] in clips or path != Path(scene["source"]).resolve()
                    or at != samples(scene["start_frame"] / fps)
                    or start != samples(scene["source_in_seconds"])
                    or length != samples(scene["used_duration_frames"] / fps)):
                raise ValueError(f"clip layer {index} must match the picture interval and source")
            clips.add(scene["id"])
        if layer["role"] == "music":
            music.append((at, at + length))
        cmd += ["-protocol_whitelist", "file,pipe", "-format_whitelist", "mov,wav,mp3", "-i", str(path)]
        chain = (f"[{index}:a:0]aresample={RATE},aformat=channel_layouts=stereo,"
                 f"atrim=start_sample={start}:end_sample={start + length},asetpts=PTS-STARTPTS,"
                 f"volume={gain}dB")
        if fade_in:
            chain += f",afade=t=in:ss=0:ns={fade_in}"
        if fade_out:
            chain += f",afade=t=out:ss={length-fade_out}:ns={fade_out}"
        filters.append(f"{chain},adelay={at}S:all=1[a{index}]")
    labels = "".join(f"[a{i}]" for i in range(1, len(m["layers"]) + 1))
    if "clip" in required and clips != video_scenes.keys():
        raise ValueError("required clip audio does not cover all video scenes")
    if "music" in required:
        covered = 0
        for start, end in sorted(music):
            if start > covered:
                break
            covered = max(covered, end)
        if covered != total:
            raise ValueError("required music has a gap in the timeline")
    filters.append(f"{labels}amix=inputs={len(m['layers'])}:normalize=0:dropout_transition=0,"
                   f"apad=whole_len={total},atrim=end_sample={total},"
                   "alimiter=limit=0.82:level=false:latency=true[a]")
    with tempfile.TemporaryDirectory(dir=output.parent) as work:
        tmp, note = Path(work) / "trial.mp4", Path(work) / "receipt.json"
        cmd[5:5] = ["-protocol_whitelist", "file,pipe", "-format_whitelist", "mov", "-i", str(picture)]
        cmd += ["-filter_complex", ";".join(filters), "-map", "0:v:0", "-map", "[a]", "-c:v", "copy",
                "-c:a", "aac", "-b:a", "256k", "-movflags", "+faststart", str(tmp)]
        execute(cmd)
        decode = ["ffmpeg", "-v", "error", "-xerror", "-i", str(tmp), "-map", "0:v:0", "-map", "0:a:0", "-f", "null", "-"]
        execute(decode)
        probe = json.loads(execute(["ffprobe", "-v", "error", "-show_streams", "-of", "json", str(tmp)]))
        audio = [s for s in probe["streams"] if s["codec_type"] == "audio"]
        if len(audio) != 1 or abs(samples(float(audio[0]["duration"])) - total) > 1024:
            raise ValueError("output audio duration does not match picture")
        if any(sha(p) != h for p, h in inputs) or manifest_path.read_bytes() != raw:
            raise ValueError("inputs changed while mixing")
        result = {"purpose": "montage_trial", "production_acceptance": False,
                  "listening": "UNVERIFIED", "manifest_sha256": hashlib.sha256(raw).hexdigest(),
                  "helper_sha256": sha(Path(__file__)), "command": cmd, "decode_command": decode,
                  "output": {"path": str(output), "sha256": sha(tmp)}, "probe": probe}
        note.write_text(json.dumps(result, indent=2) + "\n")
        os.link(tmp, output)
        try:
            os.link(note, output_receipt)
        except OSError:
            if output.samefile(tmp):
                output.unlink()
            raise
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        print(json.dumps(mix(args.manifest, args.output)["output"]))
    except (OSError, ValueError, KeyError, TypeError) as error:
        parser.exit(2, f"montage_trial_sound: {error}\n")
