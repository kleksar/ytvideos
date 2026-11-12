#!/usr/bin/env python3
"""Build ten Paper Detour Shorts cover candidates from the episode's accepted portraits."""

from __future__ import annotations

import json
import math
import random
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps

ROOT = Path('/Users/diplomat/ytvideos/channels/paper_detour/videos/003_iq_gallery')
SOURCE = ROOT / 'Source/Images/iq_gallery_full_scene_v22'
OUT = ROOT / 'Packaging/Thumbnail/Concepts/v03'
PHONE = ROOT / 'Packaging/Thumbnail/QA/v03_phone'
W, H = 1080, 1920
FONT_PATH = '/System/Library/Fonts/Supplemental/Arial Rounded Bold.ttf'
CREAM = (247, 223, 178)
PAPER = (231, 197, 139)
TERRA = (192, 75, 42)
NAVY = (16, 31, 51)
NAMES = [
    ('s01_jfk.png', 'John F. Kennedy'),
    ('s02_kasparov.png', 'Garry Kasparov'),
    ('s03_feynman.png', 'Richard Feynman'),
    ('s04_kanye.png', 'Kanye West'),
    ('s05_logan.png', 'Logan Paul'),
    ('s06_rm.png', 'RM / Kim Nam-joon'),
    ('s07_nolan.png', 'Nolan Gould'),
    ('s08_lampard.png', 'Frank Lampard'),
    ('s09_kate.png', 'Kate Beckinsale'),
    ('s10_sharon.png', 'Sharon Stone'),
    ('s11_lee.png', 'Lee Byung-hun'),
    ('s12_tarantino.png', 'Quentin Tarantino'),
    ('s13_marilyn.png', 'Marilyn vos Savant'),
]

OUT.mkdir(parents=True, exist_ok=True)
PHONE.mkdir(parents=True, exist_ok=True)


def paper_texture(seed: int, size=(W, H), base=NAVY):
    rng = np.random.default_rng(seed)
    w, h = size
    coarse = Image.fromarray(rng.integers(0, 256, (max(2, h // 34), max(2, w // 34)), dtype=np.uint8)).resize(size, Image.Resampling.BICUBIC).filter(ImageFilter.GaussianBlur(9))
    fine = Image.fromarray(rng.integers(0, 256, (h, w), dtype=np.uint8)).filter(ImageFilter.GaussianBlur(0.45))
    c = np.asarray(coarse, dtype=np.float32) - 127.5
    f = np.asarray(fine, dtype=np.float32) - 127.5
    grad_y = np.linspace(4, -7, h, dtype=np.float32)[:, None]
    grad_x = np.linspace(-4, 4, w, dtype=np.float32)[None, :]
    arr = np.empty((h, w, 3), dtype=np.uint8)
    for i, channel in enumerate(base):
        value = channel + c * 0.18 + f * 0.045 + grad_y + grad_x
        arr[:, :, i] = np.clip(value, 0, 255).astype(np.uint8)
    im = Image.fromarray(arr)
    d = ImageDraw.Draw(im, 'RGBA')
    rr = random.Random(seed + 100)
    for _ in range(310):
        x, y = rr.randrange(w), rr.randrange(h)
        length = rr.randrange(3, 18)
        d.line((x, y, x + length, y + rr.choice([-1, 0, 1])), fill=(206, 191, 163, rr.randrange(5, 16)), width=1)
    return im


def torn_mask(size, seed, amplitude=4, step=22):
    w, h = size
    rng = random.Random(seed)
    pts = []
    for x in range(0, w, step): pts.append((x, rng.randrange(0, amplitude + 1)))
    pts.append((w, rng.randrange(0, amplitude + 1)))
    for y in range(0, h, step): pts.append((w - rng.randrange(0, amplitude + 1), y))
    pts.append((w - rng.randrange(0, amplitude + 1), h))
    for x in range(w, 0, -step): pts.append((x, h - rng.randrange(0, amplitude + 1)))
    pts.append((0, h - rng.randrange(0, amplitude + 1)))
    for y in range(h, 0, -step): pts.append((rng.randrange(0, amplitude + 1), y))
    mask = Image.new('L', size, 0)
    ImageDraw.Draw(mask).polygon(pts, fill=255)
    return mask


def make_title_panel(width, height, seed, lines):
    panel = Image.new('RGBA', (width + 54, height + 54), (0, 0, 0, 0))
    x0 = y0 = 27
    mask = torn_mask((width, height), seed, amplitude=8, step=27)
    shadow = Image.new('RGBA', panel.size, (0, 0, 0, 0))
    shadow_alpha = Image.new('L', panel.size, 0)
    shadow_alpha.paste(mask, (x0, y0))
    shadow.putalpha(shadow_alpha.filter(ImageFilter.GaussianBlur(15)))
    shade = Image.new('RGBA', panel.size, (0, 0, 0, 135))
    shade.putalpha(shadow.getchannel('A'))
    panel.alpha_composite(shade, (7, 14))
    edge = Image.new('RGBA', (width, height), (*PAPER, 255))
    edge.putalpha(mask)
    panel.alpha_composite(edge, (x0, y0))
    inner = Image.new('RGBA', (width - 16, height - 16), (0, 0, 0, 0))
    inner_mask = torn_mask(inner.size, seed + 7, amplitude=5, step=25)
    texture = paper_texture(seed + 31, inner.size, NAVY).convert('RGBA')
    texture.putalpha(inner_mask)
    panel.alpha_composite(texture, (x0 + 8, y0 + 8))

    pad_x = max(26, int(width * 0.055))
    pad_y = max(18, int(height * 0.08))
    usable_w = width - pad_x * 2 - 24
    usable_h = height - pad_y * 2
    font = ImageFont.truetype(FONT_PATH, 128)
    while True:
        widths = [ImageDraw.Draw(panel).textbbox((0, 0), line, font=font)[2] for line in lines]
        heights = [ImageDraw.Draw(panel).textbbox((0, 0), line, font=font)[3] for line in lines]
        gap = int(font.size * 0.08)
        total_h = sum(heights) + gap * (len(lines) - 1)
        if max(widths) <= usable_w and total_h <= usable_h: break
        font = ImageFont.truetype(FONT_PATH, font.size - 2)
        if font.size < 40: break
    text_layer = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    td = ImageDraw.Draw(text_layer)
    y = (height - total_h) // 2 - 1
    for line, box_h in zip(lines, heights):
        bbox = td.textbbox((0, 0), line, font=font)
        tw = bbox[2] - bbox[0]
        x = (width - tw) // 2
        # A soft shadow under the paper lettering.
        td.text((x + 7, y + 10), line, font=font, fill=(2, 9, 18, 180), stroke_width=5, stroke_fill=(2, 9, 18, 170))
        # Thick terracotta paper edge beneath the cream cut-paper face.
        td.text((x + 2, y + 5), line, font=font, fill=(*TERRA, 255), stroke_width=12, stroke_fill=(*TERRA, 255))
        td.text((x, y), line, font=font, fill=(*CREAM, 255), stroke_width=5, stroke_fill=(*TERRA, 255))
        y += box_h + gap
    # Subtle paper fibers clipped to the letter mask.
    alpha = text_layer.getchannel('A')
    fiber = paper_texture(seed + 57, (width, height), CREAM).convert('RGBA')
    fiber.putalpha(alpha)
    panel.alpha_composite(fiber, (x0, y0))
    panel.alpha_composite(text_layer, (x0, y0))
    return panel


def portrait_card(filename, width, height, seed):
    src = Image.open(SOURCE / filename).convert('RGB')
    # Use the upper, face-centered portion of the episode's already accepted full-scene artwork.
    card_img = ImageOps.fit(src, (width - 22, height - 22), method=Image.Resampling.LANCZOS, centering=(0.5, 0.37))
    card_img = ImageEnhanceColor(card_img, 1.04)
    card = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    outer = torn_mask((width, height), seed, amplitude=4, step=19)
    matte = Image.new('RGBA', (width, height), (*PAPER, 255))
    matte.putalpha(outer)
    card.alpha_composite(matte)
    inner_size = (width - 22, height - 22)
    inner_mask = torn_mask(inner_size, seed + 11, amplitude=2, step=17)
    pic = card_img.convert('RGBA')
    pic.putalpha(inner_mask)
    card.alpha_composite(pic, (11, 11))
    d = ImageDraw.Draw(card)
    d.line([(13, 12), (width - 13, 12)], fill=(255, 239, 207, 170), width=2)
    return card


def ImageEnhanceColor(img, factor):
    from PIL import ImageEnhance
    return ImageEnhance.Color(img).enhance(factor)


def add_card(canvas, idx, cx, cy, cw, ch, angle, seed):
    filename, _ = NAMES[idx]
    card = portrait_card(filename, cw, ch, seed + idx * 17).rotate(angle, resample=Image.Resampling.BICUBIC, expand=True)
    shadow = Image.new('RGBA', card.size, (0, 0, 0, 0))
    shadow.putalpha(card.getchannel('A').filter(ImageFilter.GaussianBlur(10)))
    shadow = Image.new('RGBA', card.size, (0, 0, 0, 110))
    shadow.putalpha(card.getchannel('A').filter(ImageFilter.GaussianBlur(10)))
    x = max(0, min(canvas.width - card.width, int(cx - card.width / 2)))
    y = max(0, min(canvas.height - card.height, int(cy - card.height / 2)))
    sx = max(0, min(canvas.width - shadow.width, x + 5))
    sy = max(0, min(canvas.height - shadow.height, y + 13))
    canvas.alpha_composite(shadow, (sx, sy))
    canvas.alpha_composite(card, (x, y))


def add_panel(canvas, cx, cy, width, height, seed, lines=('THINK YOU\'RE', 'SMARTER', 'THAN THEM?')):
    p = make_title_panel(width, height, seed, lines)
    canvas.alpha_composite(p, (int(cx - p.width / 2), int(cy - p.height / 2)))


def centered_row(count, y, cw, ch, gap, order, seed, angles=None):
    total = count * cw + (count - 1) * gap
    left = (W - total) / 2 + cw / 2
    placements = []
    for n in range(count):
        a = (angles[n] if angles else ((n * 7 + seed) % 7 - 3))
        placements.append((order[n], left + n * (cw + gap), y, cw, ch, a))
    return placements


def render_variant(number, layout):
    seed = 9700 + number * 73
    canvas = paper_texture(seed).convert('RGBA')
    # small scattered scraps anchor the pieces in the same tactile world without competing with faces.
    d = ImageDraw.Draw(canvas, 'RGBA')
    rng = random.Random(seed)
    for _ in range(18):
        x = rng.randrange(-40, W - 20)
        y = rng.randrange(0, H)
        ww, hh = rng.randrange(20, 68), rng.randrange(9, 22)
        color = rng.choice([(228, 187, 123, 70), (190, 83, 50, 55), (80, 105, 129, 85)])
        poly = [(x, y + 2), (x + ww - 4, y), (x + ww, y + hh - 3), (x + 5, y + hh)]
        d.polygon(poly, fill=color)

    order = list(range(13))
    # Distinct, mixed order on every cover; no portrait is singled out as a score leader.
    random.Random(seed + 2).shuffle(order)
    placements = []
    if layout == 'gallery_rows':
        cw, ch = 190, 280
        placements += centered_row(4, 250, cw, ch, 42, order[0:4], seed)
        placements += centered_row(5, 590, cw, ch, 22, order[4:9], seed + 1)
        placements += centered_row(4, 930, cw, ch, 42, order[9:13], seed + 2)
        panel = (540, 1480, 940, 430, ('THINK YOU\'RE', 'SMARTER', 'THAN THEM?'))
    elif layout == 'center_bridge':
        cw, ch = 176, 245
        placements += centered_row(4, 210, cw, ch, 58, order[0:4], seed)
        placements += centered_row(5, 500, cw, ch, 25, order[4:9], seed + 1)
        placements += centered_row(4, 1410, cw, ch, 58, order[9:13], seed + 2)
        panel = (540, 930, 960, 390, ('THINK YOU\'RE', 'SMARTER THAN', 'THEM?'))
    elif layout == 'side_columns':
        cw, ch = 216, 218
        for j, idx in enumerate(order[:6]): placements.append((idx, 122, 145 + j * 304, cw, ch, (-2 + j % 5)))
        for j, idx in enumerate(order[6:]): placements.append((idx, 958, 112 + j * 278, cw, ch, (2 - j % 5)))
        panel = (540, 960, 590, 650, ('THINK', 'YOU\'RE', 'SMARTER', 'THAN THEM?'))
    elif layout == 'halo':
        cw, ch = 174, 234
        for j, idx in enumerate(order):
            a = -math.pi / 2 + 2 * math.pi * j / 13
            cx = 540 + 411 * math.cos(a)
            cy = 960 + 738 * math.sin(a)
            placements.append((idx, cx, cy, cw, ch, (-5 + (j * 7) % 11)))
        panel = (540, 960, 640, 500, ('THINK YOU\'RE', 'SMARTER', 'THAN THEM?'))
    elif layout == 'fan_rows':
        cw, ch = 192, 282
        placements += centered_row(5, 550, cw, ch, 18, order[0:5], seed, [-4, -2, 1, 2, 4])
        placements += centered_row(4, 880, cw, ch, 45, order[5:9], seed + 1, [-3, -1, 1, 3])
        placements += centered_row(4, 1210, cw, ch, 45, order[9:13], seed + 2, [-4, -1, 2, 4])
        panel = (540, 220, 900, 420, ('THINK YOU\'RE', 'SMARTER', 'THAN THEM?'))
    elif layout == 'portrait_wall':
        cw, ch = 202, 254
        placements += centered_row(4, 200, cw, ch, 32, order[0:4], seed)
        placements += centered_row(5, 500, cw, ch, 10, order[4:9], seed + 1)
        placements += centered_row(4, 800, cw, ch, 32, order[9:13], seed + 2)
        panel = (540, 1370, 930, 450, ('THINK YOU\'RE', 'SMARTER', 'THAN THEM?'))
    elif layout == 'split_gallery':
        cw, ch = 210, 240
        left_ids, right_ids = order[:6], order[6:]
        for j, idx in enumerate(left_ids): placements.append((idx, 128, 170 + j * 316, cw, ch, (-3 + j % 6)))
        for j, idx in enumerate(right_ids): placements.append((idx, 952, 90 + j * 286, cw, ch, (3 - j % 6)))
        panel = (540, 960, 520, 560, ('THINK', 'YOU\'RE', 'SMARTER', 'THAN THEM?'))
    elif layout == 'window_rows':
        cw, ch = 240, 270
        placements += centered_row(3, 170, cw, ch, 60, order[0:3], seed)
        placements += centered_row(3, 480, cw, ch, 60, order[3:6], seed + 1)
        placements += centered_row(3, 1330, cw, ch, 60, order[6:9], seed + 2)
        placements += centered_row(4, 1640, 210, 230, 18, order[9:13], seed + 3)
        panel = (540, 905, 960, 430, ('THINK YOU\'RE', 'SMARTER', 'THAN THEM?'))
    elif layout == 'zigzag':
        cw, ch = 190, 240
        # Two balanced tracks; the alternating offsets create movement without suggesting rank.
        for j, idx in enumerate(order):
            side = -1 if j % 2 == 0 else 1
            row = j // 2
            cx = 260 if side < 0 else 820
            cy = 145 + row * 242 + (42 if side > 0 else 0)
            placements.append((idx, cx, cy, cw, ch, (-4 + (j * 5) % 9)))
        panel = (540, 960, 620, 510, ('THINK', 'YOU\'RE', 'SMARTER', 'THAN THEM?'))
    else:  # 'loose_mosaic'
        cw, ch = 200, 265
        rows = [(3, 160), (4, 470), (3, 780), (3, 1090)]
        pos = 0
        for count, y in rows:
            ids = order[pos:pos + count]
            pos += count
            gap = 28 if count == 4 else 64
            placements += centered_row(count, y, cw, ch, gap, ids, seed + pos,
                                       [(-4 + (n * 7 + pos) % 9) for n in range(count)])
        panel = (540, 1510, 920, 420, ('THINK YOU\'RE', 'SMARTER', 'THAN THEM?'))

    # Add cards in a deterministic shuffled order while keeping all thirteen visible.
    for j, placement in enumerate(placements):
        idx, cx, cy, cw, ch, angle = placement
        add_card(canvas, idx, cx, cy, cw, ch, angle, seed + j * 3)
    add_panel(canvas, panel[0], panel[1], panel[2], panel[3], seed + 88, panel[4])

    png = OUT / f'iq_gallery_cover_{number:02d}.png'
    canvas.convert('RGB').save(png, optimize=True)
    # Phone review at exactly the on-device preview scale.
    phone = ImageOps.fit(canvas.convert('RGB'), (360, 640), method=Image.Resampling.LANCZOS)
    phone.save(PHONE / f'iq_gallery_cover_{number:02d}_360x640.jpg', quality=94, optimize=True)
    # Upload-ready 9:16 review copy; source PNG remains 1080x1920.
    review = ImageOps.fit(canvas.convert('RGB'), (2160, 3840), method=Image.Resampling.LANCZOS)
    jpg = OUT / f'iq_gallery_cover_{number:02d}_2160x3840.jpg'
    review.save(jpg, quality=94, subsampling=0, optimize=True)
    return {'number': number, 'layout': layout, 'people': [NAMES[i][1] for i in order], 'png': str(png), 'jpg': str(jpg), 'phone': str(PHONE / f'iq_gallery_cover_{number:02d}_360x640.jpg')}


LAYOUTS = [
    'gallery_rows', 'center_bridge', 'side_columns', 'halo', 'fan_rows',
    'portrait_wall', 'split_gallery', 'window_rows', 'zigzag', 'loose_mosaic',
]
results = [render_variant(i + 1, layout) for i, layout in enumerate(LAYOUTS)]
(OUT / 'variants.json').write_text(json.dumps(results, ensure_ascii=False, indent=2) + '\n')
print(json.dumps(results, ensure_ascii=False, indent=2))
