#!/usr/bin/env python3
"""Create independent transparent graphic layers for the Rarovista 001 edit."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).resolve().parent
FONT = '/System/Library/Fonts/Supplemental/Arial Bold.ttf'
MAIN = ImageFont.truetype(FONT, 72)
SMALL = ImageFont.truetype(FONT, 43)
PANELS = [
    ('01_show.png', 'CLIP INFORMÁTICA', 'RÁDIO USP  ·  SÃO PAULO'),
    ('02_archive.png', 'ARCHIVE COPY: 1987', 'SOFTWARE AUDIO FOR MSX'),
    ('03_two_recordings.png', 'TWO RECORDINGS', 'IDENTITY NOT ESTABLISHED'),
    ('04_tape_audio_data.png', 'TAPE  →  SOUND  →  DATA', 'COMPATIBLE COMPUTER'),
    ('05_delivery.png', 'RADIO  →  CASSETTE  →  COMPUTER', 'SOFTWARE AS AUDIO'),
    ('06_speed.png', 'QUIET AUDIO', 'PLAYBACK TOO FAST'),
    ('07_six_files.png', 'SIX DATA FILES', 'KAI’S DECODING INSTRUCTIONS'),
    ('08_reported_match.png', 'DATA MATCH REPORTED', 'WEBER KAI  ·  AVENGER'),
]

for filename, main, sub in PANELS:
    im = Image.new('RGBA', (1920, 1080), (0, 0, 0, 0))
    draw = ImageDraw.Draw(im)
    x, y = 96, 86
    main_w = draw.textlength(main, font=MAIN)
    sub_w = draw.textlength(sub, font=SMALL)
    width = int(max(main_w, sub_w) + 100)
    draw.rounded_rectangle((x, y, x+width, y+178), radius=22, fill=(18, 17, 16, 225), outline=(234, 136, 52, 230), width=3)
    draw.rounded_rectangle((x+22, y+26, x+30, y+152), radius=4, fill=(243, 149, 57, 255))
    draw.text((x+52, y+24), main, font=MAIN, fill=(255, 247, 228, 255), stroke_width=0)
    draw.text((x+54, y+111), sub, font=SMALL, fill=(255, 190, 115, 255), stroke_width=0)
    im.save(OUT / filename, optimize=True)
