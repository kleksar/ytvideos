#!/usr/bin/env python3
"""Prepare 0.95x phrase WAVs and a conservative, read-only placement plan.

The plan is an estimate based on Russian ASR timing, NOT a verified dub. No
Palmier project or timeline is modified. All audio is retained. Timing conflicts
and an overrun of the reference video are reported rather than hidden.
"""
import argparse
import array
import hashlib
import json
import math
import os
import subprocess
import sys
import tempfile
from pathlib import Path


FPS = 30
RATE = 0.95
VIDEO_END = 16093


def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1048576), b''):
            h.update(chunk)
    return h.hexdigest()


def exclusive_json(path, obj):
    with path.open('x', encoding='utf-8') as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
        f.write('\n')


def prepare_audio(segment, source_dir, output_dir):
    ident = segment['id']
    mp3, state = source_dir / f'{ident}.mp3', source_dir / f'{ident}.state.json'
    wav, meta = output_dir / f'{ident}_095.wav', output_dir / f'{ident}_095.json'
    if not state.exists():
        return None
    job = json.loads(state.read_text(encoding='utf-8'))
    if job.get('status') != 'completed':
        return None
    if not mp3.is_file() or sha(mp3) != job.get('audioSha256'):
        raise RuntimeError(f'{ident}: generated audio missing or hash mismatch')
    expected_text = hashlib.sha256(segment['text'].encode('utf-8')).hexdigest()
    if job.get('textSha256') != expected_text:
        raise RuntimeError(f'{ident}: audio was generated from different text; refusing mismatched variant')
    mp3_hash = job['audioSha256']
    if wav.exists() or meta.exists():
        if not wav.exists() or not meta.exists():
            raise RuntimeError(f'{ident}: incomplete existing WAV preparation; inspect before continuing')
        old = json.loads(meta.read_text(encoding='utf-8'))
        if old.get('inputSha256') != mp3_hash or old.get('wavSha256') != sha(wav) or old.get('tempo') != RATE:
            raise RuntimeError(f'{ident}: prepared audio does not match original; refusing overwrite')
        return old
    output_dir.mkdir(parents=True, exist_ok=True)
    # WAV is created at a temporary path and linked without overwriting an existing file.
    fd, tempname = tempfile.mkstemp(prefix=f'.{ident}-', suffix='.wav', dir=output_dir)
    os.close(fd)
    try:
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(mp3), '-vn',
                        '-af', 'atempo=0.95', '-ac', '1', '-ar', '44100', '-c:a', 'pcm_s24le', tempname],
                       check=True, capture_output=True)
        probe = json.loads(subprocess.run(['ffprobe', '-v', 'error', '-show_entries',
            'format=duration:stream=codec_name,sample_rate,channels', '-of', 'json', tempname],
            check=True, capture_output=True, text=True).stdout)
        stream = probe['streams'][0]
        duration = float(probe['format']['duration'])
        if duration <= 0 or stream.get('codec_name') != 'pcm_s24le' or int(stream.get('channels', 0)) != 1:
            raise RuntimeError(f'{ident}: invalid processed audio')
        pcm = subprocess.run(['ffmpeg', '-v', 'error', '-i', tempname, '-f', 'f32le', '-ac', '1',
                              '-ar', '44100', '-'], check=True, capture_output=True).stdout
        samples = array.array('f'); samples.frombytes(pcm)
        if sys.byteorder != 'little':
            samples.byteswap()
        # 10 ms RMS windows; an approximate onset, not a guarantee that weak consonants are silence.
        window = 441
        threshold = 10 ** (-42 / 20)
        active = []
        for offset in range(0, len(samples), window):
            frame = samples[offset:offset + window]
            if frame and math.sqrt(sum(x*x for x in frame) / len(frame)) >= threshold:
                active.append(offset)
        if not active:
            raise RuntimeError(f'{ident}: no detectable speech; inspect output')
        onset, speech_end = active[0] / 44100, min(len(samples), active[-1] + window) / 44100
        os.link(tempname, wav)
        result = {'id': ident, 'inputSha256': mp3_hash, 'wavSha256': sha(wav), 'tempo': RATE,
                  'path': str(wav.resolve()), 'durationSeconds': duration,
                  'detectedOnsetSeconds': onset, 'detectedSpeechEndSeconds': speech_end,
                  'rmsWindowMs': 10, 'speechThresholdDb': -42}
        exclusive_json(meta, result)
        return result
    finally:
        try:
            os.unlink(tempname)
        except FileNotFoundError:
            pass


def isotonic(values):
    """Equal-weight least squares projection onto nondecreasing values >= 0."""
    blocks = []
    for value in values:
        blocks.append([float(value), 1])
        while len(blocks) >= 2 and blocks[-2][0] / blocks[-2][1] > blocks[-1][0] / blocks[-1][1]:
            last = blocks.pop()
            blocks[-1][0] += last[0]
            blocks[-1][1] += last[1]
    out = []
    for total, count in blocks:
        out.extend([max(0.0, total / count)] * count)
    return out


def safe_tail_end(audio):
    """Return a source frame end after 0.2s below -50 dBFS peak, or None.

    Full WAV stays unchanged. This is a conservative acoustic heuristic, not
    confirmation that very quiet speech or breaths are expendable.
    """
    pcm = subprocess.run(['ffmpeg', '-v', 'error', '-i', audio['path'], '-f', 'f32le',
                          '-ac', '1', '-ar', '44100', '-'], check=True, capture_output=True).stdout
    samples = array.array('f'); samples.frombytes(pcm)
    if sys.byteorder != 'little':
        samples.byteswap()
    limit = 10 ** (-50 / 20)
    last = next((i for i in range(len(samples) - 1, -1, -1) if abs(samples[i]) >= limit), None)
    if last is None:
        raise RuntimeError(f'{audio["id"]}: no above-threshold peak, cannot classify tail')
    # 200ms *after* last above-threshold sample; round up to a whole source frame.
    cut_frame = math.ceil(((last + 1) / 44100 + 0.2) * FPS)
    full_frames = math.ceil(audio['durationSeconds'] * FPS)
    if cut_frame >= full_frames or cut_frame / FPS >= len(samples) / 44100:
        return None
    cut_sample = round(cut_frame * 44100 / FPS)
    if cut_sample <= last or cut_sample - (last + 1) < 8820:
        raise RuntimeError(f'{audio["id"]}: tail safety margin failed')
    if max(abs(x) for x in samples[last + 1:cut_sample]) >= limit:
        raise RuntimeError(f'{audio["id"]}: above-threshold tail detected')
    return {'sourceEndFrame': cut_frame, 'lastPeakAboveMinus50Seconds': round(last / 44100, 6),
            'tailMarginSeconds': round(cut_frame / FPS - (last + 1) / 44100, 6),
            'removedQuietSeconds': round(audio['durationSeconds'] - cut_frame / FPS, 6)}


def materialize_tail(audio, tail, output_dir):
    """Write a separate WAV; verify exact lossless PCM prefix and both hashes."""
    ident = audio['id']
    source = Path(audio['path'])
    original_sha = sha(source)
    if original_sha != audio['wavSha256']:
        raise RuntimeError(f'{ident}: source WAV hash mismatch')
    target_dir = output_dir / 'trimmed' / ident
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / f'{ident}_095_tail.wav'
    metadata = target_dir / f'{ident}_095_tail.json'
    frame = tail['sourceEndFrame']
    if target.exists() or metadata.exists():
        if not target.is_file() or not metadata.is_file():
            raise RuntimeError(f'{ident}: incomplete tail output; inspect before continuing')
        old = json.loads(metadata.read_text(encoding='utf-8'))
        if old.get('originalSha256') != original_sha or old.get('outputSha256') != sha(target) or old.get('sourceEndFrame') != frame:
            raise RuntimeError(f'{ident}: tail output mismatch; refusing overwrite')
        return old
    fd, tmp = tempfile.mkstemp(prefix=f'.{ident}-', suffix='.wav', dir=target_dir)
    os.close(fd)
    try:
        sample_end = frame * 1470  # 44100 / 30; exact source frame boundary.
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(source), '-af',
                        f'atrim=end_sample={sample_end},asetpts=PTS-STARTPTS', '-ac', '1',
                        '-ar', '44100', '-c:a', 'pcm_s24le', tmp], check=True, capture_output=True)
        def raw(path):
            return subprocess.run(['ffmpeg', '-v', 'error', '-i', str(path), '-f', 's24le',
                                   '-ac', '1', '-ar', '44100', '-'], check=True, capture_output=True).stdout
        original_pcm, cut_pcm = raw(source), raw(tmp)
        expected_bytes = sample_end * 3
        if len(cut_pcm) != expected_bytes or cut_pcm != original_pcm[:expected_bytes]:
            raise RuntimeError(f'{ident}: trimmed WAV is not the exact original PCM prefix')
        if sha(source) != original_sha:
            raise RuntimeError(f'{ident}: source WAV changed during preparation')
        os.link(tmp, target)
        result = {'id': ident, 'originalPath': str(source.resolve()), 'originalSha256': original_sha,
                  'outputPath': str(target.resolve()), 'outputSha256': sha(target),
                  'sourceEndFrame': frame, 'durationSeconds': frame / FPS,
                  'keptPcmSha256': hashlib.sha256(cut_pcm).hexdigest(),
                  'safety': tail, 'note': 'Bit-identical PCM prefix, input WAV unmodified; listening still required.'}
        exclusive_json(metadata, result)
        return result
    finally:
        try:
            os.unlink(tmp)
        except FileNotFoundError:
            pass


def build_plan(segments, prepared, timeline_end, margin, trim_safe_tail=False, trim_audio_pad_frame=False):
    # Reserve a frame margin after each clip. Using ceil guards against a clip
    # extending by rounding in Palmier; retain the full WAV and avoid overlaps.
    cumulative, desired, durations, tail_choices = [], [], [], []
    total = 0
    for seg, audio in zip(segments, prepared):
        cumulative.append(total)
        tail = safe_tail_end(audio) if trim_safe_tail else None
        tail_choices.append(tail)
        # ffprobe prints only six decimal places for frame-aligned WAVs. Its
        # rounded value can appear microscopically above an exact frame count;
        # reserve one extra frame for materialized files to satisfy conservative
        # downstream checks without ever clipping audio.
        frames = tail['sourceEndFrame'] + int(trim_audio_pad_frame) if tail else math.ceil(audio['durationSeconds'] * FPS)
        durations.append(frames)
        ideal = float(seg['timeline_start']) * FPS - audio['detectedOnsetSeconds'] * FPS
        desired.append(ideal - total)
        total += frames + margin
    y = isotonic(desired)
    rows = []
    for seg, audio, base, duration, val, tail in zip(segments, prepared, cumulative, durations, y, tail_choices):
        start = base + round(val)
        spoken_start = start / FPS + audio['detectedOnsetSeconds']
        spoken_end = start / FPS + audio['detectedSpeechEndSeconds']
        rows.append({'id': seg['id'], 'text': seg['text'], 'path': audio['path'],
                     'startFrame': start, 'conservativeEndFrame': start + duration,
                     'durationSeconds': audio['durationSeconds'],
                     'sourceEndFrame': tail['sourceEndFrame'] if tail else None,
                     'safeTailEvidence': tail,
                     'russianStartSeconds': seg['timeline_start'], 'russianEndSeconds': seg['timeline_end'],
                     'estimatedSpeechStartSeconds': round(spoken_start, 3),
                     'estimatedSpeechEndSeconds': round(spoken_end, 3),
                     'startErrorSeconds': round(spoken_start - float(seg['timeline_start']), 3),
                     'endOverrunSeconds': round(max(0, spoken_end - float(seg['timeline_end'])), 3)})
    if any(a['conservativeEndFrame'] + margin > b['startFrame'] for a,b in zip(rows, rows[1:])):
        raise RuntimeError('Planner produced overlapping clips')
    return {'fps': FPS, 'tempo': RATE, 'videoEndFrame': timeline_end, 'frameMargin': margin,
            'trimSafeTail': trim_safe_tail,
            'quietTailTrimmedCount': sum(bool(x) for x in tail_choices),
            'quietTailRemovedSeconds': round(sum(x['removedQuietSeconds'] for x in tail_choices if x), 3),
            'method': 'least-squares non-overlap placement, approximate RMS speech onset and Russian ASR starts',
            'warning': 'Estimated timing only. Must review full text, voice, meaning, pauses and sync by listening; do not trim words. If overrunFrames > 0, video does not cover full narration.',
            'overrunFrames': max(0, rows[-1]['conservativeEndFrame'] - timeline_end),
            'maxStartDeviationSeconds': round(max(abs(x['startErrorSeconds']) for x in rows), 3),
            'phrasesOutsideRussianEnd': sum(x['endOverrunSeconds'] > 0.1 for x in rows),
            'clips': rows}


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--input', required=True, type=Path, help='Phrase script JSON with segments array and timeline_start/end seconds')
    parser.add_argument('--source-dir', required=True, type=Path, help='Directory of generated MP3s and completed state JSONs')
    parser.add_argument('--wav-dir', required=True, type=Path, help='Permanent destination for processed WAVs; existing matching files reused')
    parser.add_argument('--output', type=Path, help='New output JSON report, required except in --prepare-only mode')
    parser.add_argument('--overrides', type=Path, help='Optional JSON overrides: {"overrides":{"ID":{"source_dir":"...","text":"..."}}}; preserve original audio')
    parser.add_argument('--video-end-frame', type=int, default=VIDEO_END, help='Reference timeline length in frames; default 16093')
    parser.add_argument('--frame-margin', type=int, default=1, help='Safety frames between clips, default 1')
    parser.add_argument('--prepare-only', action='store_true', help='Prepare completed phrases only; skip incomplete and do not create placement report')
    parser.add_argument('--trim-safe-tail', action='store_true', help='Plan cuts only in tails below -50 dBFS peak with 0.2s safety margin; WAVs remain intact; listening required')
    parser.add_argument('--materialize-tails', action='store_true', help='With --trim-safe-tail, create separate verified trimmed WAVs, preserving originals')
    args = parser.parse_args()
    if not args.prepare_only and not args.output:
        parser.error('--output is required unless --prepare-only is set')
    if args.output and args.output.exists():
        parser.error('Output already exists; select a new path')
    if args.video_end_frame <= 0 or args.frame_margin < 0:
        parser.error('Invalid frame settings')
    if args.materialize_tails and not args.trim_safe_tail:
        parser.error('--materialize-tails requires --trim-safe-tail')
    segments = json.loads(args.input.read_text(encoding='utf-8'))['segments']
    if not segments:
        raise RuntimeError('No segments')
    overrides = {}
    if args.overrides:
        overrides = json.loads(args.overrides.read_text(encoding='utf-8'))['overrides']
        if not isinstance(overrides, dict) or set(overrides) - {s['id'] for s in segments}:
            raise RuntimeError('Overrides must be an object keyed by existing phrase IDs')
        for ident, override in overrides.items():
            if not isinstance(override, dict) or not isinstance(override.get('text'), str) or not override['text'].strip() or not override.get('source_dir'):
                raise RuntimeError(f'{ident}: override needs text and source_dir')
    prepared, missing = [], []
    chosen = []
    for seg in segments:
        seg = dict(seg)
        override = overrides.get(seg['id'])
        if override:
            seg['text'] = override['text']
            input_dir = Path(override['source_dir'])
            output_dir = args.wav_dir / 'variants' / seg['id']
        else:
            input_dir, output_dir = args.source_dir, args.wav_dir
        chosen.append(seg)
        audio = prepare_audio(seg, input_dir, output_dir)
        if audio is None:
            missing.append(seg['id'])
        else:
            prepared.append(audio)
    print(f'Prepared {len(prepared)}/{len(segments)}; missing or not completed: {len(missing)}', flush=True)
    if args.prepare_only:
        return
    if missing:
        raise RuntimeError('Generation incomplete; cannot build plan. Missing: ' + ', '.join(missing))
    report = build_plan(chosen, prepared, args.video_end_frame, args.frame_margin, args.trim_safe_tail, args.materialize_tails)
    report['overrides'] = str(args.overrides.resolve()) if args.overrides else None
    if args.materialize_tails:
        for row, audio in zip(report['clips'], prepared):
            if row['safeTailEvidence']:
                item = materialize_tail(audio, row['safeTailEvidence'], args.wav_dir)
                row['originalPath'] = row['path']
                row['path'] = item['outputPath']
                row['durationSeconds'] = item['durationSeconds']
                row['materializedTailMetadata'] = str(Path(item['outputPath']).with_suffix('.json'))
                row['sourceEndFrame'] = None  # Whole new WAV is intended for add_clips.
        report['tailsMaterialized'] = True
    args.output.parent.mkdir(parents=True, exist_ok=True)
    exclusive_json(args.output, report)
    print('Plan:', args.output, 'end overrun frames:', report['overrunFrames'],
          'phrases longer than Russian windows:', report['phrasesOutsideRussianEnd'],
          'max start deviation seconds:', report['maxStartDeviationSeconds'])


if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError, KeyError, RuntimeError, subprocess.SubprocessError) as exc:
        print('Error:', str(exc), file=sys.stderr)
        sys.exit(1)
