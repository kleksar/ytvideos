"""Prepare the shared FFmpeg plan, model overlays, provenance and export contract."""

import hashlib
import json
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

EP = Path(__file__).resolve().parents[1]
CHANNEL = EP.parents[1]
W, H, FPS = 1080, 1920, 30
IMAGES = EP / "Source/Images"
SOURCE = EP / "Source/Audio/v01"
EDIT = EP / "Edit"
GENERATED = EP / "Assets/Generated/v01"
FONT = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
TOKENS = json.loads((CHANNEL / "brand/tokens.json").read_text())
# Exclusive word boundaries in the retained v01 narration.
CAPTION_ENDS = [4, 10, 15, 18, 23, 26, 33, 36, 40, 43, 47, 53, 57, 61, 65, 69, 75, 79, 83, 86, 91, 96, 100]


def dump(path, payload):
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n")


def file_record(path):
    return {"path": str(path), "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}


def caption_phrases(words):
    if len(words) != CAPTION_ENDS[-1]:
        raise ValueError("caption boundaries require the v01 transcript")
    return [" ".join(w["text"] for w in words[start:end])
            for start, end in zip([0] + CAPTION_ENDS, CAPTION_ENDS)]


def art(name, eyebrow, main=None, left=None, right=None, detail=None):
    """Render a semantic title overlay. Nothing is painted over the shoppers."""
    image = Image.new("RGBA", (W, 250))
    d = ImageDraw.Draw(image)
    center = 516

    def label(s, x, y, px, fill, width=850):
        while px > 20:
            face = ImageFont.truetype(FONT, px)
            if d.textlength(s, font=face) <= width:
                break
            px -= 1
        d.text((x, y), s, font=face, fill=fill, anchor="mm")

    label(eyebrow, center, 78, 33, TOKENS["secondary"])
    if main:
        label(main, center, 155, 84, TOKENS["text"])
    else:
        for x, s, color in ((300, left, "lane_a"), (732, right, "lane_b")):
            d.rounded_rectangle((x-195, 108, x+195, 194), 20, fill=TOKENS["ink"])
            label(s, x, 153, 60, TOKENS[color], 365)
    if detail:
        label(detail, center, 227, 35, TOKENS["result"])
    path = GENERATED / f"{name}.png"
    image.save(path)
    return path


def matched_empty(left, right):
    # Both generated sources share the K02 framing. Use only the naturally
    # empty half of each; blend their common, unoccupied middle tiles.
    with Image.open(left) as a, Image.open(right) as b:
        if a.size != b.size:
            raise ValueError("complementary empty lanes do not match geometry")
        mask = Image.new("L", a.size)
        cut = a.width // 2
        d = ImageDraw.Draw(mask)
        d.rectangle((0, 0, cut-18, a.height), fill=255)
        for i in range(36):
            d.line((cut-17+i, 0, cut-17+i, a.height), fill=round(255*(35-i)/35))
        path = GENERATED / "K00_aligned.png"
        Image.composite(a.convert("RGB"), b.convert("RGB"), mask).save(path)
    return path


def main():
    GENERATED.mkdir(parents=True)
    timing = json.loads((SOURCE / "timing.json").read_text())
    word_map = json.loads((SOURCE / "word_times.json").read_text())["words"]
    total = timing["frames"]
    _, setup, rule, result1, reset, result2, lesson, seam = [
        math.ceil(b["start"]*FPS-1e-6) for b in timing["lines"]
    ]
    def word_start(line_index, word):
        first = timing["lines"][line_index]["word_index"]
        last = timing["lines"][line_index+1]["word_index"]
        matches = [w for w in word_map[first:last] if w["text"] == word]
        match, = matches
        return math.ceil(match["start"]*FPS)

    shots = {p.name[:3]: p for p in IMAGES.glob("K[0-9][0-9]_*.png")}
    shot00 = matched_empty(shots["K06"], shots["K04"])
    image_files = {**shots, "K00": shot00}
    events = json.loads((EP / "experiment/events.json").read_text())
    records = json.loads((IMAGES / "generation.json").read_text())
    for record in records:
        source = IMAGES / (record["name"]+".png")
        with Image.open(source) as im:
            record["native_pixels"] = list(im.size)
        record["file"] = {"path": str(source.relative_to(EP)), "sha256": file_record(source)["sha256"]}
        record["review"] = ("SOURCE_ONLY_FRAMING_DIFFERS"
                            if record["name"] in {"K00_empty", "K00b_trial"} else "CHECKED_FOR_LOCAL_EDIT")
    for record in records:
        parent = next((r for r in records if r["name"].startswith((record["parent"] or "__")+"_")), None)
        record["supplied_reference"] = parent["file"] if parent else None
    dump(EDIT / "image_manifest_v01.json", {
        "revision": "v01",
        "generator": "built-in imagegen; immutable original PNG files",
        "target": [W, H],
        "records": records,
        "cut_K00": {"path": str(shot00.relative_to(EP)), "sha256": file_record(shot00)["sha256"],
                    "source_parents": ["K06_run2_t74", "K04_run1_t48"],
                    "method": "static composite of the empty left and right halves; camera aligned to K02"},
        "cast": {
            "A1": "teal denim jacket, dark bob, pale trousers, large grocery cart; first left",
            "A2": "navy/cream striped jumper, tan trousers, curly hair, large grocery cart; second left",
            "B1": "coral sweater, bob, pale trousers, basket; first right",
            "B2": "yellow sweater, brown hair, navy trousers, basket; second right",
            "B3": "plum hoodie, bun, light trousers, basket; third right",
            "B4": "sage jacket, brown trousers, short hair, basket; fourth right",
            "B5": "cream blouse, coral trousers, dark ponytail, basket; fifth right",
        },
        "modeled_states": events["states"],
    })

    r1, r2 = events["rounds"]
    a, b = (events["item_totals"][lane] for lane in ("A", "B"))
    scan = events["scan_seconds_per_item"]
    p1, p2 = (r["payment_seconds"] for r in events["rounds"])

    def state_caption(key):
        s = events["states"][key]
        return art(key, f"ROUND {s['round']}  /  MODEL CLOCK",
                   main=f"{s['model_seconds']} s")

    def verdict(key, r):
        s = events["states"][key]
        return art(f"result-{s['round']}", f"ROUND {s['round']}  /  MODELED WAIT",
                   left=f"A · {r['clear_seconds']['A']} s", right=f"B · {r['clear_seconds']['B']} s",
                   detail=f"{r['winner']} WINS BY {r['margin_seconds']} s")

    hook = art("hook", "THE CHECKOUT TEST", main="2 PEOPLE OR 5?")
    item_card = art("items", "TOTAL GROCERIES", left=f"A · {a} ITEMS", right=f"B · {b} ITEMS")
    payment_update = word_start(4, "Now")
    schedule = [
        (0, "K02", hook),
        (setup, "K00", art("setup", "THE CHECKOUT TEST", main="SAME STORE")),
        (setup+24, "K01", item_card),
        (setup+83, "K02", item_card),
        (rule, "K02", art("rules", "ROUND 1  /  BOTH LANES", main=f"{scan} s SCAN · {p1} s PAY")),
        (result1-32, "K03", state_caption("K03")),
        (result1, "K04", verdict("K04", r1)),
        (reset, "K02", art("reset", "ROUND 2  /  RESET", main="SAME SHOPPERS")),
        (payment_update, "K02", art("pay", "PAYMENT PER SHOPPER", main=f"{p1} s → {p2} s")),
        (result2-34, "K05", state_caption("K05")),
        (result2, "K06", verdict("K06", r2)),
        (lesson, "K02", art("lesson", "WHAT CHANGED?", main="PAYMENT TIME")),
        (seam, "K02", hook),
    ]
    scenes, overlays = [], []
    for (start, key, overlay), (end, _, _) in zip(schedule, schedule[1:] + [(total, None, None)]):
        if end-start < 2:
            raise ValueError(f"invalid beat interval: {start}..{end}")
        source = image_files[key]
        # Keep the match cut at the start and end; give each result a restrained emphasis.
        zoom = "in" if start in (0, result1, result2) else "none"
        camera = {"focus": [.5, .48], "subject": "checkout comparison",
                  "reason": "Emphasize the visible result without losing either checkout",
                  "start": {"center": [.5, .5], "scale": 1.0},
                  "end": {"center": [.5, .5], "scale": 1.012 if zoom=="in" else 1.0}}
        scenes.append({"image": "../"+str(source.relative_to(EP)), "start_frame": start, "end_frame": end,
                       "direction": "none", "zoom": zoom, "camera": camera})
        overlays.append({"path": "../"+str(overlay.relative_to(EP)), "start_frame": start, "end_frame": end})

    audio = SOURCE / "mix.wav"
    plan = {
        "channel": "two_ways_lab", "format": "short", "fps": FPS, "canvas": [W, H],
        "source_transfer": "srgb", "audio": "../Source/Audio/v01/mix.wav",
        "audio_contract": {"final_audio_sha256": file_record(audio)["sha256"], "applied_speed": 1.0,
                           "speed_evidence": "../Source/Audio/v01/mix-evidence.md"},
        "scenes": scenes, "overlays": overlays,
        "subtitles": {"mode": "words", "transcript": "../Source/Audio/v01/narration.txt",
                      "words": "../Source/Audio/v01/word_times.json", "phrases": caption_phrases(word_map)},
    }
    manifest = EDIT / "timeline_v01.json"
    dump(manifest, plan)
    out = EP / "Deliverables/TWL_E001_review_v01.mp4"
    dump(EDIT / "export_contract_v01.json", {
        "schema": "ytv-export-contract-v1", "status": "READY_TO_RENDER",
        "episode_id": "TWL_E001", "language": "en", "format": "short", "purpose": "local review",
        "edit": {"timeline_id": str(manifest), "revision": "v01", "source": file_record(manifest)},
        "timeline": {"width": W, "height": H, "aspect_ratio": "9:16", "sample_aspect_ratio": "1:1",
                     "fps": "30/1", "frame_count": total, "duration_seconds": total/FPS,
                     "output_color_space": "Rec.709 SDR"},
        "required_delivery": {
            "container": "MP4",
            "video": {"codec_name": "h264", "pix_fmt": "yuv420p", "scan": "progressive",
                      "cadence": "constant 30/1 fps", "color_primaries": "bt709", "color_transfer": "bt709",
                      "color_space": "bt709", "color_range": "tv"},
            "audio_contract": {"owner_handoff": file_record(SOURCE / "mix-evidence.md"),
                               "accepted_complete_mix": file_record(audio),
                               "source_rate_channels": "24000 Hz stereo PCM", "codec_name": "aac",
                               "profile": "LC", "sample_rate": 24000, "channels": 2,
                               "target_bit_rate": "256k"},
        },
        "encoding": {"requested_arguments": {"encoder": "libx264", "video_bitrate": "10M",
                                               "output_pix_fmt": "yuv420p", "fps": "30/1",
                                               "audio_codec": "aac", "audio_bitrate": "256k"},
                     "container_options": "+faststart"},
        "preflight": {"unresolved_required_fields": [], "output_path": str(out),
                      "writer": "local FFmpeg CLI; newly allocated output", "authorization": "one local review pilot"},
    })
    print(f"{manifest} · {total} frames")


if __name__ == "__main__":
    main()
