#!/usr/bin/env python3
"""Render transparent, frame-exact Nuviko word-highlight subtitle overlay."""
from __future__ import annotations

import argparse
import bisect
import hashlib
import json
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[6]
DEFAULT_MAP = Path(__file__).with_name("cue_map_candidate_v02.json")
DEFAULT_OUTPUT = ROOT / "channels/nuviko_history/videos/009_black_death/Assets/Generated/remake_v02/captions"
FONT = Path("/System/Library/Fonts/Supplemental/Georgia Bold.ttf")


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def render_state(cue: dict, active: int | None, size: tuple[int, int], style: dict, out: Path) -> None:
    width, height = size
    font_size = int(style["font_size_px"])
    font = ImageFont.truetype(str(FONT), font_size)
    text = cue["text"]
    tokens = text.split()
    if len(tokens) != len(cue["words"]):
        raise ValueError(f"Token mismatch in {cue['cue_id']}: {len(tokens)} != {len(cue['words'])}")
    box = font.getbbox(text)
    text_width = int(round(font.getlength(text)))
    pad_x, pad_y, stripe = 22, 10, 9
    box_h = box[3] - box[1]
    panel_w, panel_h = text_width + 2 * pad_x + stripe, box_h + 2 * pad_y
    if panel_w > width - 96:
        raise ValueError(f"Subtitle exceeds safe one-line width: {cue['cue_id']} ({panel_w}px)")
    x0 = round(style["center_x"] - panel_w / 2)
    cy = round(style["center_y"])
    y0 = cy - panel_h // 2
    im = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(im)
    fill = style["panel_fill"]
    neutral = style["neutral_text"]
    active_color = style["active_text"]
    draw.rectangle((x0, y0, x0 + panel_w, y0 + panel_h), fill=fill)
    draw.rectangle((x0, y0, x0 + stripe - 1, y0 + panel_h), fill=active_color)
    text_x = x0 + stripe + pad_x
    baseline_y = y0 + pad_y - box[1]
    draw.text((text_x, baseline_y), text, font=font, fill=neutral)
    if active is not None:
        if not 0 <= active < len(tokens):
            raise ValueError(f"Bad active word index in {cue['cue_id']}: {active}")
        prefix = " ".join(tokens[:active])
        word_x = text_x + (font.getlength(prefix + " ") if prefix else 0)
        draw.text((round(word_x), baseline_y), tokens[active], font=font, fill=active_color)
    im.save(out, optimize=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--map", type=Path, default=DEFAULT_MAP)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--max-frames", type=int, help="Render a short transparent pilot from frame 0")
    parser.add_argument("--codec", choices=("qtrle", "prores4444"), default="qtrle",
                        help="Transparent overlay format; Palmier requires ProRes 4444")
    parser.add_argument("--verify-existing", action="store_true",
                        help="Verify an already-rendered output and write its receipt without encoding again")
    args = parser.parse_args()
    cue_path = args.map.resolve()
    data = json.loads(cue_path.read_text())
    fps = int(data["fps"])
    width, height = data["canvas"]
    cues = data["cues"]
    starts = [float(c["display_start"]) for c in cues]
    total_frames = round(float(data["audio_duration_seconds"]) * fps)
    frame_count = min(total_frames, args.max_frames) if args.max_frames else total_frames
    if frame_count < 1:
        raise ValueError("No frames requested")

    outdir = args.out_dir.resolve()
    states_dir = outdir / "states"
    states_dir.mkdir(parents=True, exist_ok=True)
    style = data["style"]
    sequence: list[tuple[int, int | None]] = []
    uncovered = 0
    for frame in range(frame_count):
        t = (frame + 0.5) / fps
        ci = max(0, bisect.bisect_right(starts, t) - 1)
        cue = cues[ci]
        active = None
        for wi, word in enumerate(cue["words"]):
            if float(word["start"]) <= t < float(word["end"]):
                active = wi
                break
        # The current phrase remains on screen in neutral styling through pauses.
        if cue["text"].strip():
            sequence.append((ci, active))
        else:
            uncovered += 1
            sequence.append((ci, None))
    if uncovered:
        raise ValueError(f"Caption coverage failed: {uncovered} uncovered frames")

    state_names: dict[tuple[int, int | None], str] = {}
    for state in dict.fromkeys(sequence):
        ci, wi = state
        stem = f"{cues[ci]['cue_id']}_{'neutral' if wi is None else f'word{wi:02d}'}"
        path = states_dir / f"{stem}.png"
        if not args.verify_existing or not path.is_file():
            render_state(cues[ci], wi, (width, height), style, path)
        state_names[state] = path.name

    # Coalesce identical per-frame states to exact integer-frame durations.
    runs: list[tuple[tuple[int, int | None], int]] = []
    for state in sequence:
        if runs and runs[-1][0] == state:
            runs[-1] = (state, runs[-1][1] + 1)
        else:
            runs.append((state, 1))
    ffconcat = outdir / ("caption_pilot.ffconcat" if args.max_frames else "caption_overlay.ffconcat")
    lines = ["ffconcat version 1.0"]
    for state, frames in runs:
        name = state_names[state].replace("'", "'\\''")
        lines.extend((f"file '{(states_dir / name).as_posix()}'", f"duration {frames / fps:.12f}"))
    # concat demuxer uses the last file as a timestamp anchor; the encoder is capped to frame_count.
    last_name = state_names[runs[-1][0]].replace("'", "'\\''")
    lines.append(f"file '{(states_dir / last_name).as_posix()}'")
    ffconcat.write_text("\n".join(lines) + "\n")
    if args.codec == "prores4444":
        output_name = "caption_overlay_pilot_prores4444.mov" if args.max_frames else "black_death_en_word_highlight_overlay_prores4444.mov"
        encoding = ["-c:v", "prores_ks", "-profile:v", "4", "-pix_fmt", "yuva444p10le"]
        expected_codec, expected_pix_fmt = "prores", "yuva444p10le"
    else:
        output_name = "caption_overlay_pilot.mov" if args.max_frames else "black_death_en_word_highlight_overlay.mov"
        encoding = ["-c:v", "qtrle", "-pix_fmt", "argb"]
        expected_codec, expected_pix_fmt = "qtrle", "argb"
    output = outdir / output_name
    cmd = ["ffmpeg", "-hide_banner", "-y", "-f", "concat", "-safe", "0", "-i", str(ffconcat),
           "-an", "-fps_mode", "cfr", "-r", str(fps), "-frames:v", str(frame_count), *encoding, str(output)]
    if args.verify_existing:
        if not output.is_file() or output.stat().st_size == 0:
            raise ValueError(f"No existing output to verify: {output}")
    else:
        subprocess.run(cmd, check=True)
    probe = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                            "stream=codec_name,width,height,r_frame_rate,nb_frames,pix_fmt", "-of", "json", str(output)],
                           check=True, capture_output=True, text=True)
    stream = json.loads(probe.stdout)["streams"][0]
    pix_ok = (stream.get("pix_fmt") == expected_pix_fmt or
              (args.codec == "prores4444" and stream.get("pix_fmt") in {"yuva444p10le", "yuva444p12le"}))
    if (stream.get("codec_name"), stream.get("width"), stream.get("height"),
            int(stream.get("nb_frames", -1))) != (expected_codec, width, height, frame_count) or not pix_ok:
        raise ValueError(f"Overlay stream verification failed: {stream}")
    receipt = {
        "status": "PILOT_RENDERED" if args.max_frames else "RENDERED",
        "cue_map": str(cue_path), "cue_map_sha256": digest(cue_path),
        "audio_sha256": data["source_audio_sha256"], "fps": fps,
        "canvas": [width, height], "frames": frame_count,
        "duration_seconds": frame_count / fps, "cue_count": len(cues),
        "word_count": data["word_count"], "rendered_state_count": len(state_names),
        "run_count": len(runs), "uncovered_frames": uncovered,
        "font": str(FONT), "style": style, "ffmpeg_command": cmd,
        "output": str(output), "output_sha256": digest(output), "stream": stream,
        "timing_limitations": data.get("limitations", []),
        "verified_existing_output": args.verify_existing,
    }
    receipt_path = outdir / (("caption_overlay_pilot_receipt_prores4444.json" if args.codec == "prores4444" else "caption_overlay_pilot_receipt.json") if args.max_frames else ("caption_overlay_receipt_prores4444.json" if args.codec == "prores4444" else "caption_overlay_receipt.json"))
    receipt_path.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"status": receipt["status"], "output": str(output), "frames": frame_count,
                      "states": len(state_names), "runs": len(runs), "receipt": str(receipt_path)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
