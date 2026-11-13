#!/usr/bin/env python3
"""Render a centered, word-timed lyric overlay as a transparent MOV."""

import argparse
from functools import lru_cache
import itertools
import json
import math
from pathlib import Path
import random
import re
import subprocess
import unicodedata

from PIL import Image, ImageColor, ImageDraw, ImageFont


WIDTH, HEIGHT = 896, 384
SAFE_WIDTH = 796
FONT_SIZE = 98
SUPERSAMPLE = 3
TRACKING = 5 / FONT_SIZE
LETTER_SCALE_VARIATION = 0.035
TILT_DEGREES = 2.5
LINE_TILT_DEGREES = 2.5
DEFAULT_MOTION_SEED = 17
DEFAULT_ACCENT = '#FFB879'
NEUTRAL_INK = (244, 236, 221)
MAX_GROUP_CHARS = 20
MAX_GAP_SECONDS = 0.23
VOCAL_HOLD_GAP_SECONDS = 0.5
BEAT_SNAP_FRAMES = 2
BEAT_PULSE_SCALE = 0.06
INVERT_INK = (255, 0, 0)
REINVERT_INK = (0, 255, 0)


def load_words(data, offset, fps, frames, *, keep_source_times=False):
    if 'segments' in data:
        entries = [
            {'text': word['word'], 'start_seconds': word['start'], 'end_seconds': word['end']}
            for segment in data['segments']
            for word in segment.get('words', [])
        ]
    else:
        entries = data['words']

    previous_start = -math.inf
    words = []
    for entry in entries:
        text = entry['text'].strip()
        start, end = entry['start_seconds'], entry['end_seconds']
        if not text or re.search(r'\s', text):
            raise ValueError(f'Expected one word per entry, got {text!r}')
        if not math.isfinite(start) or not math.isfinite(end) or start < previous_start or end <= start:
            raise ValueError(f'Invalid word timing for {text!r}: {start}–{end}')
        previous_start = start
        letters = ''.join(char for char in unicodedata.normalize('NFC', text) if char.isalnum())
        start_frame = max(0, math.ceil((start - offset) * fps - 1e-9))
        end_frame = min(frames, math.ceil((end - offset) * fps - 1e-9))
        if letters and start_frame < end_frame:
            word = {
                'text': letters, 'start_frame': start_frame, 'end_frame_exclusive': end_frame,
                'break_before': bool(entry.get('break_before')),
                'break_after': text.endswith(('.', '!', '?', ',')),
            }
            if keep_source_times:
                word.update(source_start_seconds=start, source_end_seconds=end)
            if 'accent_color' in entry:
                color = entry['accent_color']
                if not isinstance(color, str) or not re.fullmatch(r'#[0-9a-fA-F]{6}', color):
                    raise ValueError(f'Invalid accent color for {text!r}: {color!r}')
                word['accent_color'] = color.upper()
            words.append(word)
    return words


def line_width(font, text):
    return (sum(font.getlength(char) for char in text) + font.size * TRACKING * (len(text) - 1)) / SUPERSAMPLE


def group_words(words, fps, font, cut_starts=(), max_words=3):
    groups = []
    group = []
    for word in words:
        joined = ' '.join(item['text'] for item in [*group, word])
        if group:
            previous = group[-1]
            pause = word['start_frame'] - previous['end_frame_exclusive']
            if (len(group) >= max_words or len(joined) > MAX_GROUP_CHARS
                    or line_width(font, joined) > SAFE_WIDTH
                    or pause / fps > MAX_GAP_SECONDS or previous['break_after']
                    or word['break_before'] or word['start_frame'] in cut_starts):
                groups.append(group)
                group = []
        group.append(word)
    if group:
        groups.append(group)
    return groups


@lru_cache(maxsize=256)
def glyph_image(font, char, ink, invert_masks):
    left, top, right, bottom = font.getbbox(char, anchor='ls')
    stroke = 0 if invert_masks else 3 * SUPERSAMPLE
    padding = max(stroke, SUPERSAMPLE)
    glyph = Image.new('RGBA', (right - left + 2 * padding, bottom - top + 2 * padding))
    ImageDraw.Draw(glyph).text(
        (padding - left, padding - top), char, font=font, anchor='ls',
        fill=ink,
        stroke_width=stroke, stroke_fill=(18, 17, 20, 230),
    )
    return glyph, (left + right) / 2, (top + bottom) / 2


def line_motion(rng, direction):
    amplitude = rng.uniform(0.045, 0.08)
    scale = [1 - amplitude, 1 + amplitude] if direction != 'hold' else [1, 1]
    if direction == 'out':
        scale.reverse()
    return {
        'direction': direction, 'scale': scale,
        'tilt_degrees': [rng.uniform(-LINE_TILT_DEGREES, LINE_TILT_DEGREES) for _ in range(2)],
    }


def interpolate(pair, progress):
    first, last = pair
    return first + (last - first) * progress


def beat_pulse(frame, beats, attack, release):
    return max((max(0, 1 - abs(frame - beat) / (attack if frame < beat else release)) ** 2
                for beat in beats), default=0)


def draw_glyph_tile(glyphs, line_angle, line_scale, opacity, invert_masks):
    # The affine and Lanczos operations only need the glyph area plus filter padding.
    # Tile edges stay on the same supersampling grid as the full overlay.
    mid_x, mid_y = WIDTH * SUPERSAMPLE / 2, HEIGHT * SUPERSAMPLE / 2
    left = min(x for _, x, _ in glyphs)
    top = min(y for _, _, y in glyphs)
    right = max(x + glyph.width for glyph, x, _ in glyphs)
    bottom = max(y + glyph.height for glyph, _, y in glyphs)
    cos_angle, sin_angle = math.cos(line_angle), math.sin(line_angle)
    corners = [
        (mid_x + line_scale * (cos_angle * (x-mid_x) + sin_angle * (y-mid_y)),
         mid_y + line_scale * (-sin_angle * (x-mid_x) + cos_angle * (y-mid_y)))
        for x in (left, right) for y in (top, bottom)
    ]
    padding = 5 * SUPERSAMPLE
    x0 = max(0, math.floor((min(left, *(x for x, _ in corners))-padding)/SUPERSAMPLE)*SUPERSAMPLE)
    y0 = max(0, math.floor((min(top, *(y for _, y in corners))-padding)/SUPERSAMPLE)*SUPERSAMPLE)
    x1 = min(WIDTH*SUPERSAMPLE, math.ceil((max(right, *(x for x, _ in corners))+padding)/SUPERSAMPLE)*SUPERSAMPLE)
    y1 = min(HEIGHT*SUPERSAMPLE, math.ceil((max(bottom, *(y for _, y in corners))+padding)/SUPERSAMPLE)*SUPERSAMPLE)
    canvas = Image.new('RGBA', (x1-x0, y1-y0))
    for glyph, x, y in glyphs:
        canvas.alpha_composite(glyph, (x-x0, y-y0))
    c, s = cos_angle / line_scale, sin_angle / line_scale
    cx, cy = mid_x-x0, mid_y-y0
    canvas = canvas.transform(canvas.size, Image.Transform.AFFINE,
                              (c, -s, cx-c*cx+s*cy, s, c, cy-s*cx-c*cy),
                              resample=Image.Resampling.BICUBIC)
    if opacity < 1:
        canvas.putalpha(canvas.getchannel('A').point([round(i*opacity) for i in range(256)]))
    canvas = canvas.resize(((x1-x0)//SUPERSAMPLE, (y1-y0)//SUPERSAMPLE), Image.Resampling.LANCZOS)
    plate = Image.new('RGB' if invert_masks else 'RGBA', (WIDTH, HEIGHT))
    plate.paste(canvas, (x0//SUPERSAMPLE, y0//SUPERSAMPLE),
                mask=canvas.getchannel('A') if invert_masks else None)
    return plate.tobytes()


def render_group(words, font, start, stop, accent, invert_masks, motion, rng, pulse_beats, pulse_window, tilt_enabled, display_hold=False):
    text = ' '.join(word['text'] for word in words)
    x = (WIDTH / 2 - line_width(font, text) / 2) * SUPERSAMPLE
    top, bottom = font.getbbox('Hgy', anchor='ls')[1::2]
    y = (HEIGHT * SUPERSAMPLE - top - bottom) / 2
    tracking = font.size * TRACKING
    letters = []
    for word in words:
        word_end = stop if display_hold and word is words[-1] else word['end_frame_exclusive']
        word_accent = ImageColor.getrgb(word['accent_color']) if 'accent_color' in word else accent
        for char in word['text']:
            scale = [1 + rng.uniform(-LETTER_SCALE_VARIATION, LETTER_SCALE_VARIATION) for _ in range(2)]
            if motion['direction'] == 'hold':
                scale[1] = scale[0]
            tilt = [rng.uniform(-TILT_DEGREES, TILT_DEGREES) for _ in range(2)]
            if not tilt_enabled:
                tilt = [0, 0]
            letters.append((char, x, word['start_frame'], word_end, word_accent, scale, tilt))
            x += font.getlength(char) + tracking
        x += font.getlength(' ') + tracking

    for frame in range(start, stop):
        glyphs = []
        t = (frame - start) / max(1, stop - start - 1)
        eased = t * t * (3 - 2 * t)
        phase = min(1, (frame - start) / 2, (stop - 1 - frame) / 2)
        opacity = 0.76 + 0.24 * (1 - (1 - phase) ** 2)
        pulse = beat_pulse(frame, pulse_beats, *pulse_window)
        opacity += (1 - opacity) * pulse
        for char, x, word_start, word_end, word_accent, scale_range, tilt_range in letters:
            active = word_start <= frame < word_end
            idle_ink, active_ink = (INVERT_INK, REINVERT_INK) if invert_masks else (NEUTRAL_INK, word_accent)
            glyph, cx, cy = glyph_image(font, char, active_ink if active else idle_ink, invert_masks)
            scale, tilt = interpolate(scale_range, eased), interpolate(tilt_range, eased)
            moved = glyph.resize((round(glyph.width * scale), round(glyph.height * scale)),
                                 Image.Resampling.BICUBIC).rotate(tilt, Image.Resampling.BICUBIC, expand=True)
            glyphs.append((moved, round(x+cx-moved.width/2), round(y+cy-moved.height/2)))
        line_angle = math.radians(interpolate(motion['tilt_degrees'], eased))
        line_scale = interpolate(motion['scale'], eased) * (1 + BEAT_PULSE_SCALE * pulse)
        yield draw_glyph_tile(glyphs, line_angle, line_scale, opacity, invert_masks)


def snap_to_beats(words, beats, frames):
    keys = ('start_frame', 'end_frame_exclusive')
    boundaries = sorted({0, frames, *(word[key] for word in words for key in keys)})
    snapped = {}
    for before, frame, after in zip(boundaries, boundaries[1:], boundaries[2:]):
        nearby = [beat for beat in beats if before < beat < after and abs(beat - frame) <= BEAT_SNAP_FRAMES]
        if nearby:
            beat = min(nearby, key=lambda candidate: (abs(candidate - frame), candidate))
            if beat != frame and beat > snapped.get(before, before):
                snapped[frame] = beat
    for word in words:
        for key in keys:
            word[key] = snapped.get(word[key], word[key])
    return snapped


def match_cut_starts(words, cut_frames, fps, frames):
    tolerance = round(fps / 30)
    matches = {}
    for cut in cut_frames:
        candidates = []
        for previous, word, following in zip(words, words[1:], [*words[2:], None]):
            start = word['start_frame']
            next_start = following['start_frame'] if following else frames
            if (abs(cut - start) <= tolerance and previous['start_frame'] < cut < next_start
                    and previous['end_frame_exclusive'] <= cut + tolerance
                    and cut < word['end_frame_exclusive']):
                candidates.append(start)
        if candidates:
            start = min(candidates, key=lambda frame: (abs(frame - cut), frame))
            if start not in matches or abs(cut - start) < abs(matches[start] - start):
                matches[start] = cut
    return matches


def sync_vocal_starts(words, beats, cuts, fps, frames):
    """Align nearby word starts and preserve longer vocal holds and pauses."""
    tolerance = max(1, round(fps / 30))
    aligned = {}
    for index, word in enumerate(words):
        start = word['start_frame']
        previous = words[index - 1] if index else None
        previous_start = previous['start_frame'] if previous else -1
        next_start = words[index + 1]['start_frame'] if index + 1 < len(words) else frames
        nearby = [beat for beat in beats if abs(beat - start) <= tolerance
                  and previous_start < beat < min(next_start, word['end_frame_exclusive'])]
        if not nearby:
            continue
        target = min(nearby, key=lambda beat: (beat not in cuts, abs(beat - start), beat))
        if previous and previous['end_frame_exclusive'] >= min(target, start):
            previous['end_frame_exclusive'] = target
        word['start_frame'] = target
        aligned[start] = target
    return aligned


def make_overlay(words, font_path, font_index, fps, frames, output, accent, invert_masks, motion_seed,
                 transition_beats=(), cut_frames=(), tilt_every=1, max_words=3, font_size=FONT_SIZE,
                 vocal_beat=False):
    font = ImageFont.truetype(str(font_path), font_size * SUPERSAMPLE, index=font_index)
    cut_starts = ({word['start_frame']: word['start_frame'] for word in words
                   if word['start_frame'] in cut_frames} if vocal_beat else
                  match_cut_starts(words, cut_frames, fps, frames))
    groups = group_words(words, fps, font, cut_starts, max_words)
    word_starts = [group[0]['start_frame'] for group in groups]
    starts = [cut_starts.get(start, start) for start in word_starts]
    stops, natural_stops, source_gaps = [], [], []
    for index, (group, next_word, next_start) in enumerate(zip(groups, [*word_starts[1:], frames], [*starts[1:], frames])):
        end = max(word['end_frame_exclusive'] for word in group)
        natural_stop = next_start if end == next_word else min(end, next_start)
        gap = None
        if vocal_beat and index + 1 < len(groups):
            gap = groups[index + 1][0]['source_start_seconds'] - group[-1]['source_end_seconds']
        hold = gap is not None and 0 <= gap < VOCAL_HOLD_GAP_SECONDS - 1e-9
        stops.append(next_start if hold else natural_stop)
        natural_stops.append(natural_stop)
        source_gaps.append(gap)
    anchors = {}
    if vocal_beat:
        anchors = {beat: beat for beat in transition_beats}
    elif cut_frames:
        anchors = {cut: cut for cut in cut_starts.values() if cut in transition_beats}
    elif transition_beats:
        visible_beats = [beat for beat in transition_beats
                         if any(start <= beat < stop for start, stop in zip(starts, stops))]
        transition_window = round(fps * 0.23)
        for start in starts[1:]:
            nearby = [beat for beat in visible_beats if abs(beat - start) <= transition_window]
            if nearby:
                anchors[start] = min(nearby, key=lambda beat: (abs(beat - start), beat))
    pulse_window = max(1, round(fps / 15)), max(1, round(2 * fps / 15))
    transparent = bytes(WIDTH * HEIGHT * (3 if invert_masks else 4))
    input_format, output_format = ('rgb24', 'rgb24') if invert_masks else ('rgba', 'argb')
    cmd = [
        'ffmpeg', '-v', 'error', '-n', '-f', 'rawvideo', '-pixel_format', input_format,
        '-video_size', f'{WIDTH}x{HEIGHT}', '-framerate', str(fps), '-i', 'pipe:0',
        '-c:v', 'qtrle', '-pix_fmt', output_format, str(output),
    ]
    plan = []
    cursor = 0
    rng = random.Random(motion_seed)
    directions = []
    with subprocess.Popen(cmd, stdin=subprocess.PIPE) as encoder:
        with encoder.stdin as pipe:
            for index, (group, start, stop) in enumerate(zip(groups, starts, stops)):
                if stop <= start:
                    raise ValueError('Two groups start on the same frame. Review overlapping word timings.')
                if not directions:
                    directions = ['in', 'out', 'hold']
                    rng.shuffle(directions)
                motion = line_motion(rng, directions.pop())
                tilt_enabled = (index + 1) % tilt_every == 0
                if not tilt_enabled:
                    motion['tilt_degrees'] = [0, 0]
                if vocal_beat:
                    pulse_beats = sorted(beat for beat in anchors if start <= beat < stop)
                else:
                    pulse_beats = sorted({beat for beat in anchors.values()
                                          if start - pulse_window[1] < beat < stop + pulse_window[0] - 1})
                line = ' '.join(word['text'] for word in group)
                width = line_width(font, line)
                pulse_scale = 1 + BEAT_PULSE_SCALE if pulse_beats else 1
                safe_width = SAFE_WIDTH / (max(motion['scale']) * (1 + LETTER_SCALE_VARIATION) * pulse_scale)
                size = max(1, math.floor(font_size * min(1, safe_width / width)))
                group_font = font if size == font_size else font.font_variant(size=size * SUPERSAMPLE)
                for plate in itertools.repeat(transparent, start - cursor):
                    pipe.write(plate)
                for plate in render_group(group, group_font, start, stop, accent, invert_masks, motion, rng,
                                          pulse_beats, pulse_window, tilt_enabled, stop > natural_stops[index]):
                    pipe.write(plate)
                cursor = stop
                entry = {'start_frame': start, 'end_frame_exclusive': stop, 'words': group,
                         'width_px': round(line_width(group_font, line), 2), 'motion': motion,
                         'transition_beat': anchors.get(start), 'pulse_beats': pulse_beats}
                if vocal_beat:
                    entry.update(natural_end_frame_exclusive=natural_stops[index],
                                 held_gap_frames=stop - natural_stops[index],
                                 source_gap_seconds=source_gaps[index])
                if cut_frames:
                    entry['transition_cut'] = cut_starts.get(group[0]['start_frame'])
                if tilt_every > 1:
                    entry['tilt_enabled'] = tilt_enabled
                plan.append(entry)
            for plate in itertools.repeat(transparent, frames - cursor):
                pipe.write(plate)
        if encoder.wait():
            raise RuntimeError('FFmpeg failed to encode the lyric overlay')
    return plan


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('word_timings', type=Path, help='Whisper JSON or words with text, start_seconds and end_seconds')
    parser.add_argument('--font', type=Path, required=True)
    parser.add_argument('--font-index', type=int, default=0, help='Face index for a font collection')
    parser.add_argument('--font-size', type=int, default=FONT_SIZE, help='Nominal font size in overlay pixels')
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--plan', type=Path, required=True)
    parser.add_argument('--offset', type=float, default=0, help='source time at video frame 0')
    parser.add_argument('--fps', type=int, default=30)
    parser.add_argument('--frames', type=int, required=True)
    parser.add_argument('--accent-color', default=DEFAULT_ACCENT, help='Active word color in #RRGGBB format')
    parser.add_argument('--invert-masks', action='store_true', help='Encode ordinary and active glyph coverage in red and green')
    parser.add_argument('--beats', type=Path, help='Optional beat candidates on the edited timeline')
    parser.add_argument('--beat-transitions', action='store_true', help='Accent subtitle changes with a short pulse on nearby beats')
    parser.add_argument('--vocal-beat', action='store_true',
                        help='Align one-word titles within one frame of beats and pulse active words on edit accents')
    parser.add_argument('--cuts', type=Path, help='Optional edit map with fps and cut_frames for scene-aligned line changes')
    parser.add_argument('--motion-seed', type=int, default=DEFAULT_MOTION_SEED)
    parser.add_argument('--tilt-every', type=int, default=1, help='Tilt only every Nth caption group, leaving the others level')
    parser.add_argument('--max-words', type=int, choices=(1, 2, 3), default=3, help='Maximum words visible at a time')
    args = parser.parse_args()
    if args.fps < 1 or args.frames < 1 or not math.isfinite(args.offset):
        parser.error('fps and frames must be positive and offset must be finite')
    if args.tilt_every < 1:
        parser.error('tilt interval must be positive')
    if args.font_size < 1:
        parser.error('font size must be positive')
    if args.output.exists() or args.plan.exists():
        parser.error('output and plan paths must be new')
    if args.beat_transitions and not (args.beats or args.cuts):
        parser.error('beat transitions require a beat map or a map of cuts on the beat')
    if args.vocal_beat and (args.max_words != 1 or not args.cuts):
        parser.error('vocal beat sync requires one word per title and a map of cuts on the beat')
    if not re.fullmatch(r'#[0-9a-fA-F]{6}', args.accent_color):
        parser.error('accent color must use #RRGGBB format')
    words = load_words(json.loads(args.word_timings.read_text(encoding='utf-8')),
                       args.offset, args.fps, args.frames, keep_source_times=args.vocal_beat)
    snapped = {}
    beat_frames = []
    if args.beats:
        beats = json.loads(args.beats.read_text(encoding='utf-8'))
        if beats['fps'] != args.fps:
            parser.error('beat map and overlay must use the same frame rate')
        beat_frames = sorted({event['frame'] for event in beats['candidates']})
        if not args.vocal_beat:
            snapped = snap_to_beats(words, beat_frames, args.frames)
    cut_frames = []
    if args.cuts:
        cut_map = json.loads(args.cuts.read_text(encoding='utf-8'))
        cut_frames = cut_map.get('cut_frames')
        if (cut_map.get('fps') != args.fps or not isinstance(cut_frames, list) or not cut_frames
                or any(type(cut) is not int or not 0 < cut < args.frames for cut in cut_frames)
                or cut_frames != sorted(set(cut_frames))):
            parser.error('cut map needs matching fps and unique, increasing interior cut_frames')
    pulse_frames = (cut_frames or beat_frames) if args.beat_transitions else ()
    if args.vocal_beat:
        snapped = sync_vocal_starts(words, sorted(set(beat_frames + cut_frames)),
                                    set(cut_frames), args.fps, args.frames)
        pulse_frames = sorted(set(cut_frames) | set(snapped.values()))
    plan = make_overlay(words, args.font, args.font_index, args.fps, args.frames, args.output,
                        ImageColor.getrgb(args.accent_color), args.invert_masks, args.motion_seed,
                        pulse_frames, cut_frames, args.tilt_every, args.max_words, args.font_size,
                        vocal_beat=args.vocal_beat)
    args.plan.write_text(json.dumps({'fps': args.fps, 'frames': args.frames,
                                     'raster': [WIDTH, HEIGHT],
                                     'max_words': args.max_words,
                                     'font_index': args.font_index,
                                     'font_size_px': args.font_size,
                                     'stroke_px': 0 if args.invert_masks else 3,
                                     'letter_motion': {'scale_variation': LETTER_SCALE_VARIATION,
                                                       'tilt_degrees': TILT_DEGREES},
                                     'line_motion': {'tilt_degrees': LINE_TILT_DEGREES,
                                                     'tilt_every': args.tilt_every,
                                                     'seed': args.motion_seed,
                                                     'interpolation': 'smoothstep_per_group'},
                                     'color_mode': 'inversion_masks' if args.invert_masks else 'solid',
                                     'accent_color': None if args.invert_masks else args.accent_color.upper(),
                                     'beat_snaps': snapped,
                                     'beat_transition_scale': BEAT_PULSE_SCALE if args.beat_transitions or args.vocal_beat else 0,
                                     **({'hold_gap_lt_ms': round(1000 * VOCAL_HOLD_GAP_SECONDS)}
                                        if args.vocal_beat else {}),
                                     'groups': plan},
                                    ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    main()
