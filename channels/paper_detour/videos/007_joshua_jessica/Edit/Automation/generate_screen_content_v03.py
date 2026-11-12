#!/usr/bin/env python3
"""Build registered paper-screen overlays and screen-state masters for Paper Detour 007."""

from __future__ import annotations

import json
import shutil
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont


EPISODE = Path(__file__).resolve().parents[2]
QUICK = EPISODE / "Source" / "Images" / "QUICK_IMPORT_CURRENT"
OUT = EPISODE / "Source" / "Graphics" / "SCREEN_CONTENT_V03"
MASTERS = EPISODE / "Storyboard" / "ScreenMasters_v03"
CANVAS = (941, 1672)
DESIGN = (1000, 620)

FONT_A = "/System/Library/Fonts/Avenir Next.ttc"
FONT_B = "/System/Library/Fonts/Supplemental/Baskerville.ttc"
ASSETS = EPISODE / "Source" / "Graphics" / "Final_v01"

INK = (63, 48, 39, 235)
INK_SOFT = (89, 68, 52, 205)
PAPER = (247, 237, 219, 228)
PAPER_LIGHT = (255, 248, 233, 235)
PAPER_MID = (231, 218, 197, 220)
ORANGE = (177, 85, 47, 236)
MUTED = (119, 92, 71, 180)


def font(path: str, size: int, index: int = 0) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(path, size=size, index=index)


def crop_alpha(image: Image.Image) -> Image.Image:
    image = image.convert("RGBA")
    box = image.getchannel("A").getbbox()
    return image.crop(box) if box else image


def paste_fit(canvas: Image.Image, image: Image.Image, box: tuple[int, int, int, int]) -> None:
    x0, y0, x1, y1 = box
    image = crop_alpha(image)
    ratio = min((x1 - x0) / image.width, (y1 - y0) / image.height)
    size = (max(1, round(image.width * ratio)), max(1, round(image.height * ratio)))
    image = image.resize(size, Image.Resampling.LANCZOS)
    canvas.alpha_composite(image, (x0 + (x1 - x0 - size[0]) // 2, y0 + (y1 - y0 - size[1]) // 2))


def paper_block(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], fill=PAPER,
                *, cut: int = 18, outline=(128, 98, 71, 75), width: int = 2) -> None:
    x0, y0, x1, y1 = box
    pts = [(x0 + cut, y0), (x1 - cut // 2, y0 + 2), (x1, y0 + cut),
           (x1 - 2, y1 - cut // 2), (x1 - cut, y1), (x0 + cut // 2, y1 - 2),
           (x0, y1 - cut), (x0 + 2, y0 + cut // 2)]
    draw.polygon(pts, fill=fill)
    if width:
        draw.line(pts + [pts[0]], fill=outline, width=width, joint="curve")


def paper_block_with_shadow(canvas: Image.Image, box: tuple[int, int, int, int], fill=PAPER,
                            *, cut: int = 18) -> None:
    x0, y0, x1, y1 = box
    shadow = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    paper_block(sd, (x0 + 5, y0 + 7, x1 + 5, y1 + 7), (35, 24, 16, 45), cut=cut, outline=(0, 0, 0, 0), width=0)
    canvas.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(7)))
    paper_block(ImageDraw.Draw(canvas), box, fill, cut=cut, width=2)


def ink_lines(draw: ImageDraw.ImageDraw, x: int, y: int, widths: list[int], *, gap: int = 24,
              color=INK_SOFT, thickness: int = 7, angle: int = 0) -> None:
    for i, width in enumerate(widths):
        yy = y + i * gap
        # Short, broken strokes suggest unreadable fragments without inventing dialogue.
        segments = [max(18, width // 3), max(14, width // 4), max(16, width - width // 3 - width // 4)]
        xx = x
        for j, seg in enumerate(segments):
            if xx + seg > x + width:
                seg = x + width - xx
            if seg <= 0:
                break
            draw.line((xx, yy, xx + seg, yy + (j % 2) * 2), fill=color, width=thickness)
            xx += seg + (12 + (i * 5 + j * 7) % 16)


def text_center(draw: ImageDraw.ImageDraw, xy: tuple[int, int], text: str, ft: ImageFont.FreeTypeFont,
                fill=INK, anchor: str = "mm") -> None:
    draw.text(xy, text, font=ft, fill=fill, anchor=anchor, stroke_width=0)


def perspective_coefficients(dst_quad: list[tuple[float, float]], src_size: tuple[int, int]) -> tuple[float, ...]:
    sw, sh = src_size
    src_quad = [(0.0, 0.0), (sw - 1.0, 0.0), (sw - 1.0, sh - 1.0), (0.0, sh - 1.0)]
    rows: list[list[float]] = []
    values: list[float] = []
    for (xd, yd), (xs, ys) in zip(dst_quad, src_quad):
        rows.append([xd, yd, 1, 0, 0, 0, -xs * xd, -xs * yd])
        values.append(xs)
        rows.append([0, 0, 0, xd, yd, 1, -ys * xd, -ys * yd])
        values.append(ys)
    return tuple(float(x) for x in np.linalg.solve(np.asarray(rows), np.asarray(values)))


def warp_to_quad(design: Image.Image, quad: list[tuple[float, float]]) -> Image.Image:
    coeffs = perspective_coefficients(quad, design.size)
    return design.transform(CANVAS, Image.Transform.PERSPECTIVE, coeffs,
                            resample=Image.Resampling.BICUBIC)


def transparent_design(size=DESIGN) -> Image.Image:
    return Image.new("RGBA", size, (0, 0, 0, 0))


def screen_hook(state: str) -> Image.Image:
    w, h = DESIGN
    canvas = transparent_design()
    d = ImageDraw.Draw(canvas)
    if state in {"waiting", "loop"}:
        paper_block_with_shadow(canvas, (36, 34, 490, 142), PAPER_LIGHT, cut=22)
        name_asset = Image.open(ASSETS / "JESSICA_v01.png").convert("RGBA")
        paste_fit(canvas, name_asset, (72, 45, 454, 130))
        d = ImageDraw.Draw(canvas)
        # A clipped remnant of the earlier conversation at the top edge.
        paper_block(d, (-22, 162, 568, 220), PAPER_MID, cut=9, width=1)
        ink_lines(d, 20, 182, [455, 330], gap=18, thickness=8)
        # Empty next-message area; the upright paper cursor is fixed at the loop phase.
        paper_block(d, (36, 440, 964, 584), (247, 238, 224, 205), cut=18, width=2)
        d.line((98, 478, 98, 548), fill=ORANGE, width=8)
    else:
        # The known-but-not-Jessica beat: current dialogue fragments, no new readable claim.
        fragments = [
            ((72, 50, 660, 160), [460, 355, 412]),
            ((320, 205, 930, 315), [485, 392]),
            ((62, 360, 690, 472), [515, 340]),
        ]
        for box, widths in fragments:
            paper_block_with_shadow(canvas, box, PAPER_LIGHT if box[0] < 100 else PAPER, cut=18)
            ink_lines(ImageDraw.Draw(canvas), box[0] + 46, box[1] + 38, widths,
                      gap=25, thickness=8)
    return canvas


def screen_old_messages() -> Image.Image:
    canvas = transparent_design()
    # Three visual groups: source fragments, a description, and Joshua's own introduction.
    groups = [
        ((45, 40, 650, 192), PAPER_LIGHT, [450, 340, 405]),
        ((330, 220, 960, 368), PAPER_MID, [500, 440, 302]),
        ((82, 416, 760, 574), PAPER, [540, 390, 300]),
    ]
    for box, fill, widths in groups:
        paper_block_with_shadow(canvas, box, fill, cut=18)
        ink_lines(ImageDraw.Draw(canvas), box[0] + 36, box[1] + 37, widths, gap=27, thickness=8)
    return canvas


def card_prompt(state: str) -> Image.Image:
    size = (800, 400)
    canvas = transparent_design(size)
    d = ImageDraw.Draw(canvas)
    if state == "prompt":
        text_center(d, (400, 198), "Jessica?", font(FONT_B, 88, 0), fill=(61, 46, 38, 245))
        d.line((205, 266, 595, 266), fill=(177, 85, 47, 90), width=2)
    else:
        d.text((72, 76), "Jessica?", font=font(FONT_B, 51, 0), fill=(61, 46, 38, 245))
        d.line((64, 138, 735, 138), fill=(126, 97, 72, 100), width=2)
        paper_block_with_shadow(canvas, (54, 175, 746, 348), (244, 233, 216, 205), cut=18)
        ink_lines(ImageDraw.Draw(canvas), 92, 218, [540, 468, 350], gap=31,
                  color=(75, 57, 45, 170), thickness=9)
    return canvas


def screen_p10(state: str) -> Image.Image:
    size = (1000, 650)
    canvas = transparent_design(size)
    d = ImageDraw.Draw(canvas)
    # The upper strip is a conditional trace of Joshua's promise, not a quote.
    paper_block(d, (36, 35, 465, 120), (238, 226, 206, 180), cut=15, width=1)
    ink_lines(d, 75, 70, [284, 180], gap=23, thickness=8, color=(82, 60, 44, 150))
    # One long incoming answer; unreadable beginning, exact verified final clause.
    paper_block_with_shadow(canvas, (70, 160, 934, 594), PAPER_LIGHT, cut=22)
    d = ImageDraw.Draw(canvas)
    if state == "unreadable":
        ink_lines(d, 130, 230, [700, 620, 710, 530, 345], gap=52, thickness=12)
    else:
        ink_lines(d, 130, 204, [700, 620, 710], gap=46, thickness=10)
        text_center(d, (504, 454), "I will be here", font(FONT_B, 61, 0), fill=(61, 46, 38, 245))
        text_center(d, (504, 524), "waiting for you.", font(FONT_B, 61, 0), fill=(61, 46, 38, 245))
    return canvas


def screen_resource(state: str) -> Image.Image:
    canvas = transparent_design()
    d = ImageDraw.Draw(canvas)
    if state in {"resource", "lead"}:
        # Echo the previous answer as a quiet paper band.
        paper_block_with_shadow(canvas, (46, 34, 954, 234), PAPER_LIGHT, cut=22)
        text_center(d, (500, 104), "I will be here waiting for you.", font(FONT_B, 46, 0), fill=INK)
        paper_block(d, (82, 276, 918, 386), PAPER_MID, cut=20, width=1)
        d.text((116, 297), "RESOURCE", font=font(FONT_A, 57, 2), fill=INK)
        # An abstract paper strip indicates constraint without asserting a number.
        x0, y0 = 116, 424
        widths = [125, 104, 132, 96, 118, 105, 130]
        for i, width in enumerate(widths):
            fill = ORANGE if i in (0, 2, 4) else (190, 168, 139, 210)
            cut = 10 + (i % 3) * 3
            paper_block(d, (x0, y0, x0 + width, y0 + 67), fill, cut=cut, outline=(100, 67, 46, 65), width=1)
            x0 += width + 10
    else:
        value_asset = Image.open(ASSETS / "55_PERCENT_v01.png").convert("RGBA")
        paste_fit(canvas, value_asset, (94, 68, 600, 365))
        d = ImageDraw.Draw(canvas)
        d.text((120, 380), "REMAINING", font=font(FONT_A, 58, 2), fill=INK)
        paper_block_with_shadow(canvas, (588, 86, 934, 250), PAPER, cut=22)
        text_center(ImageDraw.Draw(canvas), (760, 166), "THIS\nVERSION", font(FONT_A, 47, 2), fill=INK)
        # 55% is the remaining portion of this specific version's resource.
        bx0, by0, bx1, by1 = 120, 492, 910, 566
        paper_block(d, (bx0, by0, bx1, by1), PAPER_MID, cut=14, width=1)
        d.polygon([(bx0 + 15, by0 + 10), (bx0 + int((bx1 - bx0) * .55), by0 + 10),
                   (bx0 + int((bx1 - bx0) * .55) - 4, by1 - 10), (bx0 + 12, by1 - 10)], fill=ORANGE)
    return canvas


def screen_saved(state: str) -> Image.Image:
    canvas = transparent_design()
    fragments = [
        ((40, 36, 670, 166), PAPER_LIGHT, [490, 380]),
        ((325, 210, 960, 332), PAPER, [515, 400]),
        ((65, 372, 635, 484), PAPER_MID, [440, 305]),
    ]
    for box, fill, widths in fragments:
        paper_block_with_shadow(canvas, box, fill, cut=17)
        ink_lines(ImageDraw.Draw(canvas), box[0] + 37, box[1] + 39, widths, gap=25, thickness=8)
    d = ImageDraw.Draw(canvas)
    paper_block(d, (40, 510, 960, 594), (247, 238, 224, 205), cut=15, width=1)
    d.line((94, 524, 94, 578), fill=ORANGE, width=7)
    if state == "sent":
        paper_block_with_shadow(canvas, (520, 405, 930, 492), (250, 240, 224, 220), cut=15)
        ink_lines(ImageDraw.Draw(canvas), 560, 440, [290, 180], gap=22, thickness=7)
    return canvas


def label_on_card(text: str, quad: list[tuple[float, float]], size: int) -> Image.Image:
    design = transparent_design((720, 240))
    d = ImageDraw.Draw(design)
    text_center(d, (360, 120), text, font(FONT_A, size, 2), fill=(64, 46, 33, 238))
    return warp_to_quad(design, quad)


def base_layers(folder: str) -> tuple[Image.Image, Image.Image, Image.Image]:
    source = QUICK / folder
    bg = Image.open(source / "BG.png").convert("RGBA")
    mg = Image.open(source / "MG.png").convert("RGBA")
    fg = Image.open(source / "FG.png").convert("RGBA")
    return bg, mg, fg


def composite(bg: Image.Image, mg: Image.Image, overlay: Image.Image | None,
              fg: Image.Image, fg_label: Image.Image | None = None) -> Image.Image:
    out = Image.alpha_composite(bg, mg)
    if overlay is not None:
        out = Image.alpha_composite(out, overlay)
    out = Image.alpha_composite(out, fg)
    if fg_label is not None:
        out = Image.alpha_composite(out, fg_label)
    return out.convert("RGB")


def save_state(name: str, folder: str, overlay: Image.Image,
               screen_quad: list[tuple[float, float]] | None,
               *, p05: bool = False, fg_label: Image.Image | None = None) -> None:
    bg, mg, fg = base_layers(folder)
    if p05:
        # The existing blank card is in FG. Keep this three-second screen-reading
        # beat static and put its text above the card so nothing slides off it.
        framed = Image.new("RGBA", CANVAS, (0, 0, 0, 0))
        framed.alpha_composite(mg, (-11, 0))
        mg = framed
    full_overlay = warp_to_quad(overlay, screen_quad) if screen_quad else overlay
    OUT.mkdir(parents=True, exist_ok=True)
    MASTERS.mkdir(parents=True, exist_ok=True)
    full_overlay.save(OUT / f"{name}.png")
    if p05:
        result = composite(bg, mg, None, fg, full_overlay)
    else:
        result = composite(bg, mg, full_overlay, fg, fg_label)
    result.save(MASTERS / f"{name}_MASTER.png")


def save_base_master(name: str, folder: str) -> None:
    bg, mg, fg = base_layers(folder)
    composite(bg, mg, None, fg).save(MASTERS / f"{name}_MASTER.png")


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    MASTERS.mkdir(parents=True, exist_ok=True)
    # Four-corner registrations are measured on the zero-offset layer composites.
    quads = {
        "hook": [(508, 876), (748, 892), (724, 1035), (485, 1019)],
        "old_messages": [(342, 550), (797, 578), (763, 829), (299, 793)],
        "p05_card": [(295, 690), (663, 720), (635, 929), (258, 889)],
        "p10_card": [(382, 520), (909, 553), (870, 948), (296, 868)],
        "resource": [(130, 584), (777, 586), (777, 946), (122, 944)],
        "meter": [(239, 601), (849, 628), (820, 975), (207, 944)],
        "saved": [(288, 604), (790, 619), (746, 958), (225, 924)],
    }

    states = [
        ("P01_hook_waiting", "01_14_hook_loop", screen_hook("waiting"), quads["hook"], False, None),
        ("P07_hook_known", "01_14_hook_loop", screen_hook("known"), quads["hook"], False, None),
        ("P04_old_messages", "04_old_messages", screen_old_messages(), quads["old_messages"], False, None),
        ("P05_prompt", "05_reply_card", card_prompt("prompt"), quads["p05_card"], True, None),
        ("P05_reply", "05_reply_card", card_prompt("reply"), quads["p05_card"], True, None),
        ("P10_unreadable", "10_waiting_quote", screen_p10("unreadable"), quads["p10_card"], False, None),
        ("P10_quote", "10_waiting_quote", screen_p10("quote"), quads["p10_card"], False, None),
        ("P11_resource", "11_resource_used", screen_resource("resource"), quads["resource"], False, None),
        ("P12_lead", "12_resource_meter", screen_resource("lead"), quads["meter"], False, None),
        ("P12_55_remaining", "12_resource_meter", screen_resource("remaining"), quads["meter"], False, None),
        ("P13_hold", "13_saved_conversations", screen_saved("hold"), quads["saved"], False, None),
        ("P13_sent", "13_saved_conversations", screen_saved("sent"), quads["saved"], False, None),
    ]

    # P04's two editorial identifiers are physically registered to the two blank FG paper cards.
    p04_labels = Image.new("RGBA", CANVAS, (0, 0, 0, 0))
    gpt_label = label_on_card("GPT-3", [(542, 1145), (691, 1122), (800, 1197), (596, 1243)], 62)
    project_label = label_on_card("PROJECT DECEMBER", [(616, 1255), (842, 1227), (913, 1311), (691, 1382)], 40)
    p04_labels = Image.alpha_composite(p04_labels, gpt_label)
    p04_labels = Image.alpha_composite(p04_labels, project_label)

    for name, folder, design, quad, p05, labels in states:
        if name == "P04_old_messages":
            labels = p04_labels
        save_state(name, folder, design, quad, p05=p05, fg_label=labels)

    # Also lock the five intentional no-screen compositions as full masters.
    for name, folder in (
        ("P02_absence", "02_absence"),
        ("P03_jessica", "03_jessica_name"),
        ("P06_all_night", "06_all_night"),
        ("P08_tears", "08_tears"),
        ("P09_promise_daylight", "09_promise_daylight"),
    ):
        save_base_master(name, folder)

    # P04 labels move with the physical foreground cards, separately from the screen.
    p04_labels.save(OUT / "P04_table_labels.png")

    # P14 uses exactly the same screen art and master pixels as the P01 loop entrance.
    shutil.copy2(OUT / "P01_hook_waiting.png", OUT / "P14_loop_waiting.png")
    shutil.copy2(MASTERS / "P01_hook_waiting_MASTER.png", MASTERS / "P14_loop_waiting_MASTER.png")

    receipt = {
        "version": 3,
        "canvas": list(CANVAS),
        "screen_overlay_assets": [f"{name}.png" for name, *_ in states],
        "p04_foreground_label_asset": "P04_table_labels.png",
        "p05_registration": "static screen-reading hold; FG card and text remain registered; MG framing offset is -11 px",
        "loop_match": "P14_loop_waiting.png and P01_hook_waiting.png are byte-identical",
        "no_screen_plan": "P09 remains unchanged and receives no screen overlay",
        "masters": sorted(p.name for p in MASTERS.glob("*_MASTER.png")),
        "p05_static_composite": "BG + MG(-11 px) + FG + text overlay",
    }
    (OUT / "asset_receipt_v03.json").write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    readme = """# Screen-content assets v03\n\nRegistered, transparent screen-state PNGs for the Paper Detour 007 Short. Each overlay is a full-canvas 941×1672 RGBA image. P01/P14 share identical artwork for the loop. P05 keeps the existing blank paper card in FG; the three-second first-exchange composition is an intentional static reading hold, and its text sits on the card. P04’s two editorial identifiers are a separate overlay registered to the paper cards and must follow FG motion. P09 has no screen overlay because the rear of the laptop lid faces the camera.\n\nTypography inside the display is purpose-fit editorial UI lettering; it is not presented as a verified application screenshot. Existing checked paper PNGs are reused for the JESSICA and 55% accents. Exact readable text is limited to `JESSICA`, `Jessica?`, the verified closing fragment `I will be here waiting for you.`, `RESOURCE`, `55%`, `REMAINING`, `THIS VERSION`, `PROJECT DECEMBER`, and `GPT-3`; all other message fragments are intentionally unreadable.\n\nFull masters in `Storyboard/ScreenMasters_v03/` were composited from the actual zero-offset BG/MG/FG package plus the registered overlays; P05 reflects the timeline’s fixed −11 px MG framing. They are the visual targets for this screen correction. Before import, compare each static overlay composite to its matching master; all text remains on the relevant screen or card plane.\n"""
    (OUT / "README.md").write_text(readme, encoding="utf-8")
    print(json.dumps(receipt, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
