#!/usr/bin/env python3
"""Render fixed-geometry Nuviko subtitle states for each aligned spoken word."""
from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

EPISODE = Path(__file__).resolve().parents[2]
PROFILE = Path(__file__).resolve().parents[4] / "brand/nuviko/fieldnotes_kit_v02/style.json"
PLAN = EPISODE / "Work/subtitles_nuviko_plan_v01/cue_map_source_v01.json"
SHOT = EPISODE / "Storyboard/SHOT_MAP_v01.json"
OUT = EPISODE / "Assets/Generated/subtitles_word_states_v01"
MANIFEST = EPISODE / "Edit/Captions/word_states_manifest_source_v01.json"
FPS = 30
CANVAS = (1920, 1080)
HIGHLIGHT = "#C28A2C"
HIGHLIGHT_OUTLINE = "#302D27"


def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha_file(path: Path) -> str:
    return sha_bytes(path.read_bytes())


def hex_rgb(value: str) -> tuple[int, int, int]:
    return tuple(bytes.fromhex(value.lstrip("#")))


def render_state(text: str, active_index: int, profile: dict) -> Image.Image:
    native_w, native_h = profile["canvas"]
    scale = CANVAS[1] / native_h
    ss = profile["supersample"]
    font_cfg = profile["fonts"]["subtitle"]
    font = ImageFont.truetype(font_cfg["path"], round(font_cfg["size"] * scale * ss))
    tokens = text.split()
    if not 0 <= active_index < len(tokens):
        raise ValueError("Active word index is outside the subtitle group")
    native = profile["subtitle"]
    pad_x = round(native["pad_x"] * scale)
    pad_y = round(native["pad_y"] * scale)
    center_x = CANVAS[0] / 2
    bottom = round(native["bottom"] * scale)
    max_width = 1180 * scale - 2 * pad_x
    line_width = font.getlength(text) / ss
    if line_width > max_width:
        raise ValueError(f"Subtitle exceeds approved one-line width: {line_width:.1f}px > {max_width:.1f}px: {text}")
    bbox = font.getbbox(text)
    text_h = (bbox[3] - bbox[1]) / ss
    panel_w = math.ceil(line_width + 2 * pad_x)
    panel_h = math.ceil(text_h + 2 * pad_y)
    x0 = round(center_x - panel_w / 2)
    y0 = bottom - panel_h
    layer = Image.new("RGBA", (CANVAS[0] * ss, CANVAS[1] * ss), (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    paper = hex_rgb(profile["palette"]["paper"]) + (255,)
    ink = hex_rgb(profile["palette"]["ink"]) + (255,)
    highlight = hex_rgb(HIGHLIGHT) + (255,)
    draw.rectangle((x0 * ss, y0 * ss, (x0 + panel_w) * ss - 1, (y0 + panel_h) * ss - 1), fill=paper)
    text_top = y0 + pad_y - bbox[1] / ss
    pen = (center_x - line_width / 2) * ss
    space = font.getlength(" ")
    for index, word in enumerate(tokens):
        color = highlight if index == active_index else ink
        draw.text((pen, text_top * ss), word, font=font, fill=color,
                  stroke_width=ss if index == active_index else 0,
                  stroke_fill=ink if index == active_index else None)
        pen += font.getlength(word) + space
    return layer.resize(CANVAS, Image.Resampling.LANCZOS)


def main() -> None:
    profile = json.loads(PROFILE.read_text())
    plan = json.loads(PLAN.read_text())
    shot = json.loads(SHOT.read_text())
    if plan.get("status") != "SOURCE_TIME_DRAFT_REVIEW_REQUIRED":
        raise ValueError("Unexpected subtitle timing status; preserve and review before rendering")
    if plan.get("fps") != FPS or plan.get("target_canvas") != [1672, 941]:
        raise ValueError("Subtitle plan/profile identity mismatch")
    OUT.mkdir(parents=True, exist_ok=True)
    unique_states: dict[str, dict] = {}
    timed_states: list[dict] = []
    previous_end = None
    for cue in plan["cues"]:
        words = cue["group_words"]
        tokens = cue["text"].split()
        if not tokens or len(tokens) == 1:
            raise ValueError(f"Invalid subtitle group {cue['cue']}")
        if words[-1]["text"].strip(".,!?;:").lower() == "who":
            raise ValueError(f"Forbidden who-ending cue {cue['cue']}")
        # A historically hyphenated place can be one displayed word but two
        # spoken alignment tokens; keep the single word highlighted through both.
        aligned_to_display = []
        ai = 0
        for token in tokens:
            if "-" in token and ai + 1 < len(words):
                left = words[ai]["caption_text"].strip(".,!?;:")
                right = words[ai + 1]["caption_text"].strip(".,!?;:")
                if (left + "-" + right).casefold() == token.strip(".,!?;:").casefold():
                    aligned_to_display.extend([len(aligned_to_display), len(aligned_to_display)])
                    ai += 2
                    continue
            if ai >= len(words):
                raise ValueError(f"Text/alignment token mismatch at cue {cue['cue']}")
            aligned_to_display.append(len(aligned_to_display))
            ai += 1
        if ai != len(words):
            raise ValueError(f"Text/alignment token mismatch at cue {cue['cue']}")
        cue_end = cue["source_end_seconds"]
        total_frames = shot["total_frames"]
        end_frame = round((cue_end if cue_end is not None else total_frames / FPS) * FPS)
        starts = [round(float(w["source_start_seconds"]) * FPS) for w in words]
        if starts[0] != round(float(cue["source_start_seconds"]) * FPS):
            raise ValueError(f"Cue start disagrees with first aligned word at cue {cue['cue']}")
        for i, (word, start, display_index) in enumerate(zip(words, starts, aligned_to_display)):
            stop = starts[i + 1] if i + 1 < len(starts) else end_frame
            if (previous_end is not None and start != previous_end) or stop <= start:
                raise ValueError(f"Subtitle has a gap/overlap/zero span at cue {cue['cue']} word {i+1}")
            active_text = tokens[display_index]
            key_data = {"version": "nuviko-word-states-v01", "canvas": CANVAS, "text": cue["text"], "active": display_index,
                        "profile_sha256": sha_file(PROFILE), "highlight": HIGHLIGHT}
            key = sha_bytes(json.dumps(key_data, sort_keys=True, ensure_ascii=False).encode())
            if key not in unique_states:
                path = OUT / f"WS_{key[:20]}.png"
                if not path.exists():
                    image = render_state(cue["text"], display_index, profile)
                    image.save(path, optimize=True)
                else:
                    with Image.open(path) as existing:
                        if existing.size != CANVAS or existing.mode != "RGBA":
                            raise ValueError(f"Cached word-state image has wrong geometry: {path}")
                unique_states[key] = {"id": path.stem, "path": str(path), "sha256": sha_file(path),
                                      "text": cue["text"], "active_index": display_index, "active_word": active_text}
            timed_states.append({"cue": cue["cue"], "word_index": i, "word": word["text"],
                                 "active_display_word": active_text,
                                 "startFrame": start, "endFrame": stop,
                                 "image_id": unique_states[key]["id"], "image": unique_states[key]["path"],
                                 "sha256": unique_states[key]["sha256"]})
            previous_end = stop
    total_frames = shot["total_frames"]
    if previous_end != total_frames:
        raise ValueError(f"Subtitle end {previous_end} does not match expected {total_frames}")
    receipt = {"version": "nuviko-word-states-v01", "status": "SOURCE_TIME_DRAFT_REVIEW_REQUIRED",
               "episode": "016_marseille_1720", "fps": FPS, "canvas": list(CANVAS),
               "sourceAudioSha256": plan["source_audio_sha256"], "cueMapSha256": sha_file(PLAN),
               "styleProfile": str(PROFILE), "styleProfileSha256": sha_file(PROFILE),
               "profileGeometry": {"native": profile["canvas"], "subtitle": profile["subtitle"],
                                  "font": profile["fonts"]["subtitle"], "palette": profile["palette"],
                                  "highlight": HIGHLIGHT, "highlightOutline": HIGHLIGHT_OUTLINE},
               "timingEvidence": plan["alignment_method"], "audibleSync": "UNVERIFIED",
               "cueCount": len(plan["cues"]), "wordStateCount": len(timed_states),
               "uniqueImageCount": len(unique_states), "totalFrames": total_frames,
               "stateFiles": list(unique_states.values()), "timeline": timed_states}
    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"status": receipt["status"], "cues": receipt["cueCount"],
                      "wordStates": receipt["wordStateCount"], "uniqueImages": receipt["uniqueImageCount"],
                      "totalFrames": total_frames, "manifest": str(MANIFEST)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
