#!/usr/bin/env python3
"""Render transparent, frame-exact Nuviko word-highlight subtitle overlay."""
from __future__ import annotations

import argparse
import bisect
import hashlib
import importlib.util
import json
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


FONT = Path("/System/Library/Fonts/Supplemental/Georgia Bold.ttf")
ROOT = Path(__file__).resolve().parents[2]
SEGMENTER_PATH = ROOT / "automation/helpers/paper-subtitles/scripts/semantic_grouping.py"
_segmenter_spec = importlib.util.spec_from_file_location("ytv_semantic_grouping", SEGMENTER_PATH)
if _segmenter_spec is None or _segmenter_spec.loader is None:
    raise RuntimeError(f"Cannot load shared subtitle segmenter: {SEGMENTER_PATH}")
segmenter = importlib.util.module_from_spec(_segmenter_spec)
_segmenter_spec.loader.exec_module(segmenter)


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
    text_width = int(round(font.getlength(text)))
    # Paper's fixed font-metrics baseline: ascenders and descenders never
    # change the line or background geometry from one cue to the next.
    ascent, descent = font.getmetrics()
    pad_x, pad_y = 22, 10
    panel_w, panel_h = text_width + 2 * pad_x, ascent + descent + 2 * pad_y
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
    text_x = x0 + pad_x
    baseline_y = y0 + pad_y + ascent
    draw.text((text_x, baseline_y), text, font=font, fill=neutral, anchor="ls")
    if active is not None:
        if not 0 <= active < len(tokens):
            raise ValueError(f"Bad active word index in {cue['cue_id']}: {active}")
        prefix = " ".join(tokens[:active])
        word_x = text_x + (font.getlength(prefix + " ") if prefix else 0)
        draw.text((round(word_x), baseline_y), tokens[active], font=font, fill=active_color, anchor="ls")
    im.save(out, optimize=True)


def resegment_map(data: dict, font: ImageFont.FreeTypeFont, preserve_groups: bool,
                  keep_together: list[str]) -> dict:
    """Build phrase cues from the exact timed words, keeping source timings."""
    source_cues = data["cues"]
    words: list[dict] = []
    for cue in source_cues:
        cue_words = cue.get("words", [])
        surfaces = cue.get("text", "").split()
        if len(surfaces) != len(cue_words):
            raise ValueError(f"Token mismatch in source cue {cue.get('cue_id')}: {len(surfaces)} != {len(cue_words)}")
        for surface, word in zip(surfaces, cue_words):
            copied = dict(word)
            if copied.get("text") != surface:
                raise ValueError(f"Word text mismatch in source cue {cue.get('cue_id')}: {copied.get('text')!r} != {surface!r}")
            copied["source_cue_id"] = cue.get("cue_id")
            words.append(copied)
    if len(words) != int(data["word_count"]):
        raise ValueError(f"Word count mismatch: {len(words)} != {data['word_count']}")

    width, _ = data["canvas"]
    # Panel width is text plus 44 px padding and must stay 96 px inside canvas.
    max_text_width = width - 140
    if preserve_groups:
        phrases = [cue["text"] for cue in source_cues]
        groups = segmenter.plan_phrases(words, phrases, font, max_text_width, keep_together)
        mode = "preserved_reviewed_groups"
    else:
        groups = segmenter.group_words(words, font, max_text_width, keep_together)
        mode = "automatic_sentence_syntax_width"

    audio_duration = float(data["audio_duration_seconds"])
    cues: list[dict] = []
    group_starts = [float(group[0]["start"]) for group in groups]
    if not group_starts or group_starts[0] < 0 or group_starts[0] > audio_duration:
        raise ValueError("Invalid first word start in cue map")
    for i, group in enumerate(groups):
        start = 0.0 if i == 0 else group_starts[i]
        end = group_starts[i + 1] if i + 1 < len(groups) else audio_duration
        spoken_end = float(group[-1]["end"])
        if end < spoken_end:
            raise ValueError(f"Next subtitle group begins before current words finish: {i + 1}")
        cues.append({
            "cue_id": f"C{i + 1:04d}",
            "text": " ".join(str(word["text"]) for word in group),
            "display_start": start,
            "display_end": end,
            "words": [{k: v for k, v in word.items() if k != "source_cue_id"} for word in group],
        })
    result = dict(data)
    result["cues"] = cues
    result["segmentation"] = {
        "algorithm": segmenter.VERSION,
        "mode": mode,
        "source_cue_count": len(source_cues),
        "result_cue_count": len(cues),
        "max_text_width_px": max_text_width,
        "keep_together": keep_together,
        "display_rule": "First cue starts at 0; each cue remains through the next cue start; last cue remains through audio duration.",
        "review_required": True,
    }
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--map", type=Path, required=True, help="Reviewed Nuviko word-timed cue map")
    parser.add_argument("--out-dir", type=Path, required=True, help="New output directory")
    parser.add_argument("--max-frames", type=int, help="Render a short transparent pilot from frame 0")
    parser.add_argument("--preserve-groups", action="store_true",
                        help="Keep the map's existing reviewed groups; validate against width and syntax rules")
    parser.add_argument("--plan-only", action="store_true",
                        help="Write the automatically segmented cue map and receipt without rendering the overlay")
    parser.add_argument("--keep-together", action="append", default=[],
                        help="Keep a known two-word name or term together; may be repeated")
    parser.add_argument("--codec", choices=("qtrle", "prores4444"), default="qtrle",
                        help="Transparent overlay format; Palmier requires ProRes 4444")
    parser.add_argument("--verify-existing", action="store_true",
                        help="Verify an already-rendered output and write its receipt without encoding again")
    args = parser.parse_args()
    cue_path = args.map.resolve()
    data = json.loads(cue_path.read_text())
    fps = int(data["fps"])
    width, height = data["canvas"]
    font = ImageFont.truetype(str(FONT), int(data["style"]["font_size_px"]))
    data = resegment_map(data, font, args.preserve_groups, args.keep_together)
    cues = data["cues"]
    starts = [float(c["display_start"]) for c in cues]
    total_frames = round(float(data["audio_duration_seconds"]) * fps)
    frame_count = min(total_frames, args.max_frames) if args.max_frames else total_frames
    if frame_count < 1:
        raise ValueError("No frames requested")

    outdir = args.out_dir.resolve()
    outdir.mkdir(parents=True, exist_ok=True)
    segmented_map = outdir / "segmented_cue_map.json"
    segmented_map.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
    if args.plan_only:
        plan_receipt = {
            "status": "PLAN_READY_REVIEW_REQUIRED", "source_map": str(cue_path),
            "source_map_sha256": digest(cue_path), "segmented_cue_map": str(segmented_map),
            "segmented_cue_map_sha256": digest(segmented_map), "fps": fps,
            "canvas": [width, height], "cue_count": len(cues), "word_count": data["word_count"],
            "segmentation": data["segmentation"], "review_required": True,
        }
        receipt_path = outdir / "segmentation_plan_receipt.json"
        receipt_path.write_text(json.dumps(plan_receipt, ensure_ascii=False, indent=2) + "\n")
        print(json.dumps({"status": plan_receipt["status"], "segmented_cue_map": str(segmented_map),
                          "groups": len(cues), "words": data["word_count"], "receipt": str(receipt_path)}, ensure_ascii=False))
        return
    states_dir = outdir / "states"
    states_dir.mkdir(parents=True, exist_ok=True)
    style = dict(data["style"], stripe=False, geometry="fixed_font_metrics_baseline")
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
        "segmented_cue_map": str(segmented_map), "segmented_cue_map_sha256": digest(segmented_map),
        "audio_sha256": data["source_audio_sha256"], "fps": fps,
        "canvas": [width, height], "frames": frame_count,
        "duration_seconds": frame_count / fps, "cue_count": len(cues),
        "word_count": data["word_count"], "rendered_state_count": len(state_names),
        "run_count": len(runs), "uncovered_frames": uncovered,
        "font": str(FONT), "style": style, "ffmpeg_command": cmd,
        "output": str(output), "output_sha256": digest(output), "stream": stream,
        "timing_limitations": data.get("limitations", []),
        "segmentation": data.get("segmentation"),
        "verified_existing_output": args.verify_existing,
    }
    receipt_path = outdir / (("caption_overlay_pilot_receipt_prores4444.json" if args.codec == "prores4444" else "caption_overlay_pilot_receipt.json") if args.max_frames else ("caption_overlay_receipt_prores4444.json" if args.codec == "prores4444" else "caption_overlay_receipt.json"))
    receipt_path.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"status": receipt["status"], "output": str(output), "frames": frame_count,
                      "states": len(state_names), "runs": len(runs), "receipt": str(receipt_path)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
