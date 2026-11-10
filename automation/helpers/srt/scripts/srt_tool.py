#!/usr/bin/env python3
"""Offline plain-text SRT renderer/validator. No ASR, alignment or media mutation."""
import argparse
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
import hashlib
import json
import math
from pathlib import Path
import re
import sys
import unicodedata


class SrtError(ValueError):
    pass


STAMP = r'(\d{2,}):([0-5]\d):([0-5]\d),(\d{3})'
TIMING = re.compile(STAMP + r' --> ' + STAMP)


def canonical(text):
    return ' '.join(unicodedata.normalize('NFC', text).split())


def seconds(value):
    if isinstance(value, bool) or not isinstance(value, (str, int, float, Decimal)):
        raise SrtError('Timestamp must be a finite number')
    try:
        result = Decimal(str(value))
    except InvalidOperation as exc:
        raise SrtError('Invalid timestamp') from exc
    if not result.is_finite() or result < 0:
        raise SrtError('Timestamp must be finite and nonnegative')
    return result


def milliseconds(value):
    try:
        return int((seconds(value) * 1000).quantize(Decimal('1'), rounding=ROUND_HALF_UP))
    except InvalidOperation as exc:
        raise SrtError('Timestamp cannot be represented in milliseconds') from exc


def stamp(value):
    hours, rem = divmod(value, 3600000)
    minutes, rem = divmod(rem, 60000)
    sec, ms = divmod(rem, 1000)
    return f'{hours:02d}:{minutes:02d}:{sec:02d},{ms:03d}'


def parse_srt(text):
    text = text.lstrip('\ufeff').replace('\r\n', '\n').replace('\r', '\n').strip()
    if not text:
        raise SrtError('Empty SRT')
    cues = []
    for index, block in enumerate(re.split(r'\n[ \t]*\n', text), 1):
        lines = block.split('\n')
        if len(lines) < 3 or lines[0] != str(index):
            raise SrtError(f'Cue {index}: missing text or nonsequential index')
        match = TIMING.fullmatch(lines[1])
        if not match:
            raise SrtError(f'Cue {index}: malformed timestamp')
        nums = list(map(int, match.groups()))
        def total(parts):
            h, m, s, ms = parts
            return Decimal(((h * 60 + m) * 60 + s) * 1000 + ms) / 1000
        cues.append({'start_seconds': total(nums[:4]),
                     'end_seconds': total(nums[4:]), 'text': '\n'.join(lines[2:])})
    return cues


def check(cues, transcript, duration, limits=None):
    """Check all cues, never silently clamp, reorder or rewrite their content."""
    duration = seconds(duration)
    if duration <= 0:
        raise SrtError('Duration must be positive')
    if not isinstance(cues, list) or not cues:
        raise SrtError('Expected a nonempty cues array')
    limits = limits or {}
    errors, warnings, measured = [], [], []
    previous_raw_end = Decimal('-1')
    previous_ms_end = -1
    output = []
    for number, cue in enumerate(cues, 1):
        if not isinstance(cue, dict):
            raise SrtError(f'Cue {number}: expected object')
        start, end = seconds(cue.get('start_seconds')), seconds(cue.get('end_seconds'))
        text = cue.get('text')
        if not isinstance(text, str) or not canonical(text) or '\x00' in text:
            raise SrtError(f'Cue {number}: empty/invalid text')
        text = text.replace('\r\n', '\n').replace('\r', '\n')
        lines = text.split('\n')
        if any(not line.strip() for line in lines):
            raise SrtError(f'Cue {number}: blank text line splits the SRT block')
        begin, finish = milliseconds(start), milliseconds(end)
        if end <= start or start < previous_raw_end:
            errors.append(f'Cue {number}: nonpositive duration or overlap before rounding')
        if finish <= begin or begin < previous_ms_end:
            errors.append(f'Cue {number}: nonpositive duration or overlap after rounding')
        if end > duration:
            errors.append(f'Cue {number}: end {end}s exceeds duration {duration}s')
        previous_raw_end, previous_ms_end = end, finish
        span = float(end - start)
        if not math.isfinite(span):
            raise SrtError(f'Cue {number}: duration cannot be represented')
        cps = len(canonical(text)) / span if span > 0 else None
        measured.append({'cue': number, 'lines': len(lines), 'longest_line': max(map(len, lines)),
                         'duration_seconds': span, 'characters_per_second': cps})
        for key, actual, relation in [
            ('max_lines', len(lines), 'max'),
            ('max_line_chars', max(map(len, lines)), 'max'),
            ('max_cps', cps, 'max'),
            ('min_duration', span, 'min'),
            ('max_duration', span, 'max'),
        ]:
            threshold = limits.get(key)
            if threshold is not None and actual is not None:
                if (relation == 'max' and actual > threshold) or (relation == 'min' and actual < threshold):
                    warnings.append({'cue': number, 'criterion': key, 'measured': actual, 'threshold': threshold})
        output.append(f'{number}\n{stamp(begin)} --> {stamp(finish)}\n{text}')
    coverage = canonical(' '.join(c['text'] for c in cues)) == canonical(transcript)
    report = {
        'structure': 'FAIL' if errors else 'PASS',
        'text_coverage': 'PASS' if coverage else 'FAIL',
        'timing_mapping': 'UNVERIFIED',
        'playback': 'UNVERIFIED',
        'readability': ('WARN' if warnings else 'PASS') if limits else 'N_A',
        'limits': limits, 'errors': errors, 'warnings': warnings, 'cues': measured,
        'limits_note': 'Readability metrics do not verify semantic breaks, player layout or hearing sync.',
    }
    return '\n\n'.join(output) + '\n', report


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    for command, flag in [('build', '--cues'), ('validate', '--srt')]:
        p = sub.add_parser(command)
        p.add_argument(flag, type=Path, required=True)
        p.add_argument('--text', type=Path, required=True, help='Expected final transcript; whitespace/NFC only normalized')
        p.add_argument('--duration', required=True, help='Measured duration of the declared timebase in seconds')
        p.add_argument('--timebase', choices=['source', 'final'], default='source')
        p.add_argument('--report', type=Path, help='New JSON report, never overwritten')
        for name in ['max-lines', 'max-line-chars', 'max-cps', 'min-duration', 'max-duration']:
            p.add_argument('--' + name, type=float)
        if command == 'build':
            p.add_argument('--output', type=Path, required=True, help='New SRT, never overwritten')
    args = parser.parse_args(argv)
    try:
        targets = [p for p in [getattr(args, 'output', None), args.report] if p is not None]
        if len({p.resolve() for p in targets}) != len(targets):
            raise SrtError('Output and report paths must differ')
        for p in targets:
            if p.exists() or not p.parent.is_dir():
                raise SrtError(f'Output exists or parent is missing: {p}')
        limits = {k: getattr(args, k) for k in ['max_lines', 'max_line_chars', 'max_cps', 'min_duration', 'max_duration'] if getattr(args, k) is not None}
        for value in limits.values():
            if seconds(value) <= 0:
                raise SrtError('Readability thresholds must be positive and finite')
        transcript = args.text.read_text(encoding='utf-8-sig')
        source = args.cues if args.command == 'build' else args.srt
        if args.command == 'build':
            data = json.loads(source.read_text(encoding='utf-8-sig'))
            cues = data['cues']
        else:
            cues = parse_srt(source.read_text(encoding='utf-8-sig'))
        content, report = check(cues, transcript, args.duration, limits)
        report.update({'timebase': args.timebase, 'duration_seconds': str(seconds(args.duration)),
                       'inputs': {'text': {'path': str(args.text), 'sha256': digest(args.text)},
                                  args.command: {'path': str(source), 'sha256': digest(source)}}})
        passed = report['structure'] == report['text_coverage'] == 'PASS'
        report['result'] = 'MACHINE_CHECKED' if passed else 'FAIL'
        if passed and args.command == 'build':
            # Round-trip checks catch serialization errors as well as input errors.
            _, again = check(parse_srt(content), transcript, args.duration, limits)
            if again['structure'] != 'PASS' or again['text_coverage'] != 'PASS':
                raise SrtError('Serialized SRT fails round-trip checks')
            with args.output.open('x', encoding='utf-8', newline='\n') as handle:
                handle.write(content)
            report['output'] = {'path': str(args.output), 'sha256': digest(args.output)}
        if args.report:
            with args.report.open('x', encoding='utf-8') as handle:
                json.dump(report, handle, ensure_ascii=False, indent=2, allow_nan=False)
                handle.write('\n')
        print(json.dumps(report, ensure_ascii=False, indent=2, allow_nan=False))
        return 0 if passed else 1
    except (SrtError, OSError, UnicodeError, ValueError, KeyError, TypeError, OverflowError) as exc:
        print(f'Error: {exc}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
