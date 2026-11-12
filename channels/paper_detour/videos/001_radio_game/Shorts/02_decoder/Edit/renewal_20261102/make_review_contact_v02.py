#!/usr/bin/env python3
"""Build compact QA contact sheets from the helper's exact extracted frames."""

import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

EPISODE = Path("/Users/diplomat/ytvideos/channels/paper_detour/videos/001_radio_game")
RUN = "short02-review-v02-qa-20261102"
REPORT = EPISODE / "Edit/QA" / RUN / "report.json"
PLAN = EPISODE / "Shorts/02_decoder/Edit/renewal_20261102/review_qa_plan_v02.json"
OUT = EPISODE / "Work" / RUN / "previews"
OUT.mkdir(parents=True, exist_ok=True)

report = json.loads(REPORT.read_text())
plan = json.loads(PLAN.read_text())
frame_by_index = {
    item["index"]: (REPORT.parent / item["path"]).resolve()
    for item in report["frame_map"]
}
font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 20)
tile_w, tile_h, label_h = 270, 480, 44
columns, page_size = 5, 20

def tile(index, label):
    image = Image.open(frame_by_index[index]).convert("RGB")
    image.thumbnail((tile_w, tile_h), Image.Resampling.LANCZOS)
    card = Image.new("RGB", (tile_w, tile_h + label_h), "#111111")
    card.paste(image, ((tile_w-image.width)//2, 0))
    ImageDraw.Draw(card).text((8, tile_h+7), label, font=font, fill="white")
    return card

cue_tiles = []
for i, cue in enumerate(plan["cues"], 1):
    mid = cue["start"] + (cue["end"] - cue["start"]) // 2
    actual = min(frame_by_index, key=lambda frame: abs(frame-mid))
    if abs(actual-mid) <= 1:
        cue_tiles.append((actual, f"{cue['id']} f{actual}"))

for page_no, offset in enumerate(range(0, len(cue_tiles), page_size), 1):
    page = cue_tiles[offset:offset+page_size]
    rows = (len(page) + columns - 1) // columns
    sheet = Image.new("RGB", (columns*tile_w, rows*(tile_h+label_h)), "#111111")
    for n, (frame, label) in enumerate(page):
        sheet.paste(tile(frame, label), ((n % columns)*tile_w, (n//columns)*(tile_h+label_h)))
    path = OUT / f"cue_mids_{page_no:02d}.jpg"
    sheet.save(path, quality=90)

scene_tiles = []
for scene in plan["scenes"]:
    frames = [scene["start"], (scene["start"]+scene["end"]-1)//2, scene["end"]-1]
    for phase, frame in zip(("start", "mid", "end"), frames):
        if frame in frame_by_index:
            scene_tiles.append((frame, f"{scene['id']} {phase} f{frame}"))
columns = 3
rows = (len(scene_tiles)+columns-1)//columns
sheet = Image.new("RGB", (columns*tile_w, rows*(tile_h+label_h)), "#111111")
for n, (frame, label) in enumerate(scene_tiles):
    sheet.paste(tile(frame, label), ((n % columns)*tile_w, (n//columns)*(tile_h+label_h)))
sheet.save(OUT / "scene_triplets.jpg", quality=90)
print(f"wrote {len(cue_tiles)} cue mids and {len(scene_tiles)} scene samples to {OUT}")
