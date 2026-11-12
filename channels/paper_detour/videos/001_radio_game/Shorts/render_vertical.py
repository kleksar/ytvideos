#!/usr/bin/env python3
"""Render a scratch-voice Short from approved still illustrations.

This is a simple pan/zoom edit, not full character animation. Defaults to a
read-only plan. Explicit --render starts one encode and never overwrites a
deliverable. Captions remain external; machine alignment needs human review.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
import re
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
FPS = 30
WIDTH, HEIGHT = 1080, 1920


def probe(path: Path) -> dict:
    proc = subprocess.run(
        ["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(path)],
        check=True, capture_output=True, text=True,
    )
    return json.loads(proc.stdout)


def tokens(s: str) -> list[str]:
    return [x.casefold() for x in re.findall(r"\b[\w]+(?:['’\-][\w]+)*\b", s)]


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def revision_paths(slug: str, revision: str) -> tuple[Path, Path, Path, Path, Path]:
    base = ROOT / slug
    if revision == "pro_v2":
        voice_dir = base / "Source/Voice/pro_v2"
        return (base / "narration_pro_v2.txt", voice_dir / "voice_en.mp3",
                voice_dir / "voice_en.words.json", voice_dir / "voice_en.draft.srt",
                ROOT / "shorts_edit_plan_pro_v2.json")
    voice_dir = base / "Source/Voice"
    return (base / "narration_en.txt", voice_dir / "voice_en.mp3",
            voice_dir / "voice_en.words.json", voice_dir / "voice_en.draft.srt",
            ROOT / "shorts_edit_plan.json")


def timeline(slug: str, revision: str) -> tuple[list[dict], float]:
    text_path, audio, words_path, _, plan_path = revision_paths(slug, revision)
    plan = json.loads(plan_path.read_text())
    spec = plan["shorts"][slug]
    info = probe(audio)
    duration = float(info["format"]["duration"])
    data = json.loads(words_path.read_text())
    text_hash = sha(text_path)
    if data["source_sha256"] != text_hash:
        raise ValueError("Spoken text differs from the timing file; re-record/re-align before rendering")
    words = data["words"]
    word_strings = [tokens(x["text"])[0] for x in words]
    shots = []
    for item in spec["shots"]:
        if "start" in item:
            start = float(item["start"])
        else:
            needle = tokens(item["anchor"])
            matches = [i for i in range(len(words) - len(needle) + 1)
                       if word_strings[i:i + len(needle)] == needle]
            if len(matches) != 1:
                raise ValueError(f"Anchor {item['anchor']!r} occurs {len(matches)} times")
            start = float(words[matches[0]]["start_seconds"])
        shots.append({"start": start, "image": str(ROOT / "Shared/Images" / item["image"]),
                      "anchor": item.get("anchor", "beginning")})
    frames = [round(s["start"] * FPS) for s in shots] + [math.ceil(duration * FPS)]
    if frames[0] != 0 or any(b <= a for a, b in zip(frames, frames[1:])):
        raise ValueError("Shot boundaries must be strictly increasing and start at zero")
    for i, shot in enumerate(shots):
        shot["start_frame"] = frames[i]
        shot["end_frame"] = frames[i + 1]
        shot["frames"] = frames[i + 1] - frames[i]
        shot["start_seconds_snapped"] = frames[i] / FPS
    return shots, duration


def render(slug: str, revision: str, shots: list[dict], duration: float) -> None:
    base = ROOT / slug
    _, voice, _, srt, _ = revision_paths(slug, revision)
    label = ROOT / "Shared/Graphics/reconstruction_en.png"
    for path in [voice, srt, label, *(Path(s["image"]) for s in shots)]:
        if not path.is_file():
            raise FileNotFoundError(path)
    suffix = "v2" if revision == "pro_v2" else "v1"
    output = ROOT.parents[3] / "channels/paper_detour/legacy/020_rarovista_radio_game/Deliverables" / f"{slug}_en_shorts_{suffix}.mp4"
    subtitles = output.with_suffix(".en.srt")
    report_path = output.with_suffix(".verification.json")
    part = output.with_name(output.stem + ".partial.mp4")
    if any(p.exists() for p in (output, subtitles, report_path, part)):
        raise FileExistsError("A deliverable or partial already exists; refusing to overwrite")
    output.parent.mkdir(parents=True, exist_ok=True)
    cmd = ["ffmpeg", "-nostdin", "-hide_banner", "-v", "warning", "-filter_complex_threads", "2"]
    for shot in shots:
        # Bound every looped image input; otherwise upstream can remain infinite
        # even when a downstream trim is in place.
        cmd += ["-loop", "1", "-framerate", str(FPS), "-t", f"{shot['frames'] / FPS:.9f}",
                "-i", shot["image"]]
    cmd += ["-i", str(voice), "-loop", "1", "-framerate", str(FPS), "-t", "4", "-i", str(label)]
    filters = []
    labels = []
    for i, shot in enumerate(shots):
        n = shot["frames"]
        # A restrained scale change provides movement within each shot. Alternate
        # zoom direction and framing so a repeated image does not hold still.
        z = f"1+0.045*on/{n}" if i % 2 == 0 else f"1.045-0.045*on/{n}"
        x = (0.40, 0.60, 0.50)[i % 3]
        y = (0.42, 0.55, 0.48)[i % 3]
        filters.append(
            f"[{i}:v]scale={WIDTH}:{HEIGHT}:force_original_aspect_ratio=increase,"
            f"crop={WIDTH}:{HEIGHT},setsar=1,"
            f"zoompan=z='{z}':x='(iw-iw/zoom)*{x}':y='(ih-ih/zoom)*{y}':"
            f"d=1:s={WIDTH}x{HEIGHT}:fps={FPS},trim=end_frame={n},"
            f"setpts=PTS-STARTPTS,format=yuv420p[v{i}]"
        )
        labels.append(f"[v{i}]")
    filters.append("".join(labels) + f"concat=n={len(shots)}:v=1:a=0[vbase]")
    filters.append(f"[vbase][{len(shots) + 1}:v]overlay=x=(W-w)/2:y=100:"
                   "enable='lt(t,4)':eof_action=pass[vout]")
    cmd += ["-filter_complex", ";".join(filters), "-map", "[vout]", "-map", f"{len(shots)}:a:0",
            "-t", f"{duration:.6f}", "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
            "-threads", "2", "-pix_fmt", "yuv420p", "-r", str(FPS), "-c:a", "aac", "-profile:a", "aac_low",
            "-b:a", "192k", "-ar", "44100", "-ac", "1", "-movflags", "+faststart", str(part)]
    try:
        subprocess.run(cmd, check=True)
        p = probe(part)
        streams = p["streams"]
        video = next(s for s in streams if s["codec_type"] == "video")
        audio = next(s for s in streams if s["codec_type"] == "audio")
        actual = float(p["format"]["duration"])
        if (video["width"], video["height"]) != (WIDTH, HEIGHT):
            raise ValueError("Unexpected dimensions")
        if video["codec_name"] != "h264" or audio["codec_name"] != "aac" or audio["channels"] != 1:
            raise ValueError("Unexpected video/audio codecs or channel count")
        if abs(actual - duration) > 0.15:
            raise ValueError(f"Unexpected duration: {actual} versus {duration}")
        subprocess.run(["ffmpeg", "-v", "error", "-xerror", "-i", str(part), "-f", "null", "-"], check=True)
        part.rename(output)
        shutil.copyfile(srt, subtitles)
        report = {
            "status": "draft render; no listening/full visual review", "video": str(output),
            "source_voice": str(voice), "source_voice_sha256": sha(voice), "video_sha256": sha(output),
            "srt_sha256": sha(subtitles), "output_duration_seconds": actual,
            "voice_duration_seconds": duration, "streams": streams, "shots": shots,
            "limitations": ["Still-image pan/zoom, not frame-by-frame animation",
                            "No music or effects added", "No subtitles embedded",
                            "English SRT uses machine alignment, not verified by ear",
                            "All images are illustrative; exact historical visuals not verified; English reconstruction label shown at start",
                            "Audio source is MP3 at 128 kbps; 192 kbps AAC does not restore source quality"],
        }
        report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n")
        print(json.dumps({"output": str(output), "duration": actual, "subtitles": str(subtitles),
                          "verification": str(report_path)}, ensure_ascii=False))
    except BaseException:
        if part.exists():
            part.unlink()
        raise


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("slug", choices=("01_radio_signal", "02_decoder", "03_stereo_text"))
    p.add_argument("--revision", choices=("scratch_v1", "pro_v2"), default="scratch_v1")
    p.add_argument("--render", action="store_true", help="run one FFmpeg encode")
    args = p.parse_args()
    shots, duration = timeline(args.slug, args.revision)
    if args.render:
        render(args.slug, args.revision, shots, duration)
    else:
        print(json.dumps({"slug": args.slug, "duration_seconds": duration, "shots": shots}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
