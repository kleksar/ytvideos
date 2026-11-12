#!/usr/bin/env python3
"""Render English one-line word-highlight captions for Palmier timeline 1_en.

Canonical wording is user-approved text. Palmier's English word timestamps are
used only for timing; one-to-one ASR spelling differences are resolved to the
canonical text. All caption styling/plan data stays beside this script.
"""
import bisect
import difflib
import json
import re
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).parent
FPS = 30
FRAMES = 3123
W, H = 1080, 1920
FONT = "/System/Library/Fonts/HelveticaNeue.ttc"
FONT_INDEX = 9  # Helvetica Neue Condensed Black
BASE_SIZE = 105
MIN_SIZE = 55
TRACKING = 1.5
WORD_GAP = 32.5
ACTIVE_SCALE = 1.05
Y = round(H * 0.40)
SOURCE_TEXT = ROOT / "voice_en_original.txt"
TIMESTAMPS = ROOT / "voice_en_word_timestamps.json"
PLAN_FILE = ROOT / "CAPTION_PLAN_1_EN.txt"
OUTPUT = ROOT / "voice_word_highlight_overlay_1_en_v2.mov"
SRT_OUTPUT = ROOT / "voice_word_captions_1_en_v2.srt"
SIZE_REPORT = ROOT / "caption_sizes_1_en_v2.tsv"

TEXT = SOURCE_TEXT.read_text(encoding="utf-8").strip()
data = json.loads(TIMESTAMPS.read_text(encoding="utf-8"))
src = [{"word": row[0], "start": float(row[1]), "end": float(row[2])} for row in data["words"]]
# Apostrophes and orthographic hyphens are retained inside English words.
target = re.findall(r"[A-Za-z0-9]+(?:[-'][A-Za-z0-9]+)*", TEXT)

NUMBER_EQUIVALENTS = {"twelve": "12", "first": "1st"}
def norm(s):
    value = re.sub(r"[^a-z0-9]", "", s.lower())
    return NUMBER_EQUIVALENTS.get(value, value)

sm = difflib.SequenceMatcher(None, [norm(w["word"]) for w in src], [norm(t) for t in target], autojunk=False)
words = []
for op, a, b, c, d in sm.get_opcodes():
    S, T = src[a:b], target[c:d]
    if op == "equal" or (op == "replace" and len(S) == len(T)):
        # The approved text supplies spelling and contractions; ASR supplies timing.
        words.extend({"word": tw, "start": sw["start"], "end": sw["end"]} for sw, tw in zip(S, T))
    else:
        raise ValueError(f"Unresolved text/timing alignment: {op}: {[x['word'] for x in S]} -> {T}")
if len(words) != len(target):
    raise ValueError((len(words), len(target)))

plan = [line.strip() for line in PLAN_FILE.read_text(encoding="utf-8").splitlines() if line.strip()]
expected = [w["word"].upper() for w in words]
actual = [token for line in plan for token in line.split()]
if actual != expected:
    i = next((i for i, (a, b) in enumerate(zip(actual, expected)) if a != b), min(len(actual), len(expected)))
    raise ValueError(f"Caption plan differs at token {i}: plan={actual[i:i+6]} text={expected[i:i+6]} ({len(actual)} vs {len(expected)})")

chunks = []
offset = 0
for line in plan:
    count = len(line.split())
    chunks.append(words[offset:offset + count])
    offset += count

starts = [c[0]["start"] for c in chunks]
ends = [starts[i + 1] if i + 1 < len(starts) else c[-1]["end"] for i, c in enumerate(chunks)]
short = [(plan[i], ends[i] - starts[i]) for i in range(len(plan)) if ends[i] - starts[i] < 0.26]
if short:
    raise ValueError(f"Caption below 260 ms; merge it into a readable adjacent group: {short}")
font_cache = {}
def font(size):
    if size not in font_cache:
        font_cache[size] = ImageFont.truetype(FONT, size, index=FONT_INDEX)
    return font_cache[size]
def width_of(text, f):
    return f.getlength(text) + TRACKING * max(0, len(text) - 1)
def line_size(line):
    size = BASE_SIZE
    tokens = line.split()
    while size >= MIN_SIZE:
        f = font(size)
        widths = [width_of(token, f) for token in tokens]
        peak = sum(widths) + WORD_GAP * max(0, len(tokens) - 1) + (ACTIVE_SCALE - 1) * max(widths, default=0)
        if peak <= 1000:
            return size, peak
        size -= 1
    raise ValueError(f"Caption cannot fit the safe width at {MIN_SIZE}px: {line}")

sizes = [line_size(line) for line in plan]
with SIZE_REPORT.open("w", encoding="utf-8") as f:
    f.write("cue\twords\tbase_size_px\tpeak_width_px\n")
    for i, (line, (size, peak)) in enumerate(zip(plan, sizes), 1):
        f.write(f"{i}\t{line}\t{size}\t{peak:.1f}\n")

def stamp(seconds):
    n = round(seconds * 1000)
    h, n = divmod(n, 3600000)
    m, n = divmod(n, 60000)
    s, ms = divmod(n, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

srt = []
for i, line in enumerate(plan, 1):
    srt.extend([str(i), f"{stamp(starts[i-1])} --> {stamp(ends[i-1])}", line, ""])
SRT_OUTPUT.write_text("\n".join(srt), encoding="utf-8")

print(f"Aligned words: {len(words)}; cues: {len(chunks)}; frames: {FRAMES}; "
      f"size range: {min(s for s, _ in sizes)}–{max(s for s, _ in sizes)} px; "
      f"max active width: {max(w for _, w in sizes):.1f}px", flush=True)

cmd = [
    "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
    "-f", "rawvideo", "-pixel_format", "rgba", "-video_size", f"{W}x{H}",
    "-framerate", str(FPS), "-i", "pipe:0", "-an", "-c:v", "qtrle",
    "-pix_fmt", "argb", "-movflags", "+faststart", str(OUTPUT)
]
p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
white = (255, 255, 255, 255)
yellow = (255, 213, 79, 255)
outline = (0, 0, 0, 210)

for frame in range(FRAMES):
    t = frame / FPS
    ci = bisect.bisect_right(starts, t) - 1
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    if ci >= 0 and t < ends[ci]:
        c = chunks[ci]
        shown = [w["word"].upper() for w in c]
        size = sizes[ci][0]
        base_font = font(size)
        active = next((j for j, w in enumerate(c) if w["start"] <= t < w["end"]), -1)
        draw = ImageDraw.Draw(im)
        base_widths = [width_of(word, base_font) for word in shown]
        total = sum(base_widths) + WORD_GAP * max(0, len(c) - 1)
        x = (W - total) / 2
        for j, w in enumerate(c):
            active_here = (j == active)
            if active_here:
                duration = max(0.001, w["end"] - w["start"])
                progress = max(0.0, min(1.0, (t - w["start"]) / duration))
                ramp = min(0.12, duration * 0.45)
                if duration <= 2 * ramp:
                    q = min(1.0, progress * 2) if progress <= 0.5 else min(1.0, (1 - progress) * 2)
                    eased = q * q * (3 - 2 * q)
                elif progress < ramp / duration:
                    q = progress * duration / ramp
                    eased = q * q * (3 - 2 * q)
                elif progress > 1 - ramp / duration:
                    q = (1 - progress) * duration / ramp
                    eased = q * q * (3 - 2 * q)
                else:
                    eased = 1.0
                active_font = font(round(size * (1 + 0.05 * eased)))
                color = yellow
            else:
                active_font = base_font
                color = white
            # Fixed base layout: the active word changes only its own glyph size.
            center = x + base_widths[j] / 2
            char_x = center - width_of(shown[j], active_font) / 2
            for char in shown[j]:
                cw = active_font.getlength(char)
                draw.text((char_x + cw / 2, Y), char, font=active_font, fill=color,
                          anchor="mm", stroke_width=5, stroke_fill=outline)
                char_x += cw + TRACKING
            x += base_widths[j] + WORD_GAP
    p.stdin.write(im.tobytes())
    if frame % 300 == 0:
        print(f"Rendered {frame}/{FRAMES}", flush=True)

p.stdin.close()
code = p.wait()
if code:
    raise SystemExit(code)
print(OUTPUT)

