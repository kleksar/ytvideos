#!/usr/bin/env python3
"""Generate separate, resumable ElevenLabs phrase recordings.

Default mode is a no-network dry run. A real request requires --generate and
creates an exclusive per-phrase state BEFORE sending, so a crash or an unknown
network outcome is never retried automatically. Source timeline placement is
not performed by this tool. Never share API keys or print server error bodies.
"""

import argparse
import base64
import binascii
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

VOICE_ID = 'T5FteTezhjGJLDY1cJiA'
MODEL = 'eleven_v4'
FORMATS = ('mp3_44100_128', 'mp3_44100_192')


class GenerationError(Exception):
    pass


def stamp():
    return datetime.now(timezone.utc).isoformat(timespec='seconds')


def api_key():
    value = os.environ.get('ELEVENLABS_API_KEY', '').strip()
    if value:
        return value
    if sys.platform == 'darwin':
        try:
            result = subprocess.run(
                ['/usr/bin/security', 'find-generic-password', '-a', 'yt-stories',
                 '-s', 'yt-stories-elevenlabs', '-w'],
                text=True, capture_output=True, timeout=30, check=False)
            if result.returncode == 0:
                return result.stdout.strip()
        except (OSError, subprocess.TimeoutExpired):
            pass
    return ''


def exclusive_write(path, data):
    # An exclusive create prevents replacing earlier paid results or states.
    with path.open('xb') as f:
        f.write(data)
        f.flush()
        os.fsync(f.fileno())


def update_state(path, data):
    payload = (json.dumps(data, ensure_ascii=False, indent=2) + '\n').encode('utf-8')
    name = None
    try:
        with tempfile.NamedTemporaryFile(dir=path.parent, prefix='.state-', delete=False) as f:
            name = f.name
            f.write(payload)
            f.flush()
            os.fsync(f.fileno())
        os.replace(name, path)
    finally:
        if name and os.path.exists(name):
            os.unlink(name)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def load_plan(path):
    try:
        data = json.loads(path.read_text(encoding='utf-8'))
    except (OSError, UnicodeError, ValueError) as exc:
        raise GenerationError(f'Cannot read input JSON: {path}: {exc}') from exc
    segments = data.get('segments') if isinstance(data, dict) else data
    if not isinstance(segments, list) or not segments:
        raise GenerationError('Expected a non-empty segments array.')
    seen = set()
    for phrase in segments:
        if not isinstance(phrase, dict):
            raise GenerationError('Each segment must be an object.')
        ident, text = phrase.get('id'), phrase.get('text')
        if not isinstance(ident, str) or not re.fullmatch(r'[A-Za-z0-9_-]{1,64}', ident):
            raise GenerationError('Every id must be a safe, unique alphanumeric string.')
        if ident in seen:
            raise GenerationError(f'Duplicate id: {ident}')
        if not isinstance(text, str) or not text.strip() or len(text) > 10000:
            raise GenerationError(f'Invalid or oversized text in {ident}.')
        seen.add(ident)
    return segments


def verify_mp3(path, output_format):
    cmd = ['ffprobe', '-v', 'error', '-show_entries', 'format=duration:stream=codec_name,sample_rate,channels,bit_rate',
           '-of', 'json', str(path)]
    p = subprocess.run(cmd, capture_output=True, text=True, check=True, timeout=30)
    meta = json.loads(p.stdout)
    streams = meta.get('streams', [])
    if not streams or streams[0].get('codec_name') != 'mp3' or float(meta['format']['duration']) <= 0:
        raise GenerationError(f'Invalid returned MP3: {path}; do not retry before checking ElevenLabs history.')
    wanted = int(output_format.rsplit('_', 1)[1]) * 1000
    actual = int(streams[0].get('bit_rate') or 0)
    if actual and abs(actual - wanted) > wanted * .2:
        raise GenerationError(f'Unexpected source bitrate {actual} for {path}; check history and file before retry.')
    return {'durationSeconds': float(meta['format']['duration']), 'codec': 'mp3',
            'sampleRate': streams[0].get('sample_rate'), 'channels': streams[0].get('channels'),
            'bitRate': actual}


def synthesize(key, segment, previous, following, voice_id, model, output_format, timeout):
    params = urllib.parse.urlencode({'output_format': output_format})
    url = f'https://api.elevenlabs.io/v1/text-to-speech/{voice_id}/with-timestamps?{params}'
    payload = {'text': segment['text'], 'model_id': model, 'voice_settings': {
        'stability': 0.5, 'similarity_boost': 0.75}}
    # Context can improve phrase-to-phrase continuity, while output is only text.
    if previous:
        payload['previous_text'] = previous['text']
    if following:
        payload['next_text'] = following['text']
    req = urllib.request.Request(url, data=json.dumps(payload, ensure_ascii=False).encode('utf-8'),
        headers={'xi-api-key': key, 'Content-Type': 'application/json', 'Accept': 'application/json'}, method='POST')
    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            data = response.read()
            request_id = response.headers.get('request-id') or response.headers.get('x-request-id')
            if response.headers.get_content_type() != 'application/json':
                raise GenerationError('Unexpected content type; request outcome requires manual review.')
    except urllib.error.HTTPError as exc:
        raise GenerationError(f'ElevenLabs HTTP {exc.code}; no retry performed. Check entitlement, history and credits.') from None
    except (urllib.error.URLError, TimeoutError, OSError):
        raise GenerationError('Network error; request outcome and credit usage unknown. Check history before retry.') from None
    try:
        obj = json.loads(data)
        audio = base64.b64decode(obj['audio_base64'], validate=True)
        alignment = {'alignment': obj.get('alignment'), 'normalized_alignment': obj.get('normalized_alignment')}
    except (ValueError, TypeError, KeyError, binascii.Error):
        raise GenerationError('Invalid response; request outcome requires manual review.') from None
    if len(audio) < 100 or not (audio.startswith(b'ID3') or audio[0] == 0xff and audio[1] & 0xe0 == 0xe0):
        raise GenerationError('Response does not contain a valid MP3; request outcome requires manual review.')
    return audio, alignment, request_id


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--input', required=True, type=Path, help='JSON with segments array: id, text, optional timing fields')
    parser.add_argument('--output-dir', required=True, type=Path, help='Permanent directory for audio and job states')
    parser.add_argument('--format', choices=FORMATS, default='mp3_44100_192', help='192 kbps requires Creator or higher; no automatic fallback')
    parser.add_argument('--voice-id', default=VOICE_ID)
    parser.add_argument('--model', default=MODEL)
    parser.add_argument('--ids', help='Optional comma-separated segment IDs')
    parser.add_argument('--max-jobs', type=int, help='Limit number of new requests for this invocation')
    parser.add_argument('--timeout', type=int, default=180)
    parser.add_argument('--generate', action='store_true', help='Send billable requests (default: dry run)')
    args = parser.parse_args()
    if not re.fullmatch(r'[A-Za-z0-9_-]+', args.voice_id) or not re.fullmatch(r'[A-Za-z0-9_-]+', args.model):
        parser.error('Invalid voice or model ID')
    if args.max_jobs is not None and args.max_jobs <= 0 or args.timeout <= 0:
        parser.error('max-jobs and timeout must be positive')
    segments = load_plan(args.input)
    requested = set(args.ids.split(',')) if args.ids else None
    if requested and requested - {s['id'] for s in segments}:
        raise GenerationError('Unknown segment IDs: ' + ', '.join(sorted(requested - {s['id'] for s in segments})))
    selected = [s for s in segments if requested is None or s['id'] in requested]
    config = {'voiceId': args.voice_id, 'modelId': args.model, 'outputFormat': args.format,
              'voiceSettings': {'stability': .5, 'similarity_boost': .75}, 'segments': segments,
              'generationSpeed': 1.0, 'note': 'Generated audio is not time-stretched; edit at 0.95 separately if needed.'}
    immutable = json.dumps(config, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf-8')
    fingerprint = sha(immutable)
    print(f'Segments selected: {len(selected)}; characters: {sum(len(s["text"]) for s in selected)}; '
          f'model: {args.model}; voice: {args.voice_id}; format: {args.format}; plan SHA-256: {fingerprint}')
    if not args.generate:
        print('Dry run: no network request, no filesystem writes, no credits used.')
        return
    key = api_key()
    if not key:
        raise GenerationError('ElevenLabs key not found in environment or yt-stories Keychain entry.')
    args.output_dir.mkdir(parents=True, exist_ok=True)
    plan_path = args.output_dir / 'generation_plan.json'
    if plan_path.exists():
        try:
            plan = json.loads(plan_path.read_text(encoding='utf-8'))
        except (OSError, ValueError) as exc:
            raise GenerationError(f'Cannot read existing plan; do not start: {exc}') from exc
        if plan.get('fingerprint') != fingerprint:
            raise GenerationError('Output directory belongs to a different input/settings; use another directory.')
    else:
        try:
            exclusive_write(plan_path, (json.dumps({'fingerprint': fingerprint, 'config': config}, ensure_ascii=False, indent=2) + '\n').encode())
        except FileExistsError:
            raise GenerationError('Output plan was created concurrently; restart after inspection.') from None
    jobs_started = 0
    for idx, seg in enumerate(segments):
        if requested is not None and seg['id'] not in requested:
            continue
        if args.max_jobs is not None and jobs_started >= args.max_jobs:
            break
        ident = seg['id']
        state_path = args.output_dir / f'{ident}.state.json'
        audio_path = args.output_dir / f'{ident}.mp3'
        alignment_path = args.output_dir / f'{ident}.alignment.json'
        if state_path.exists():
            try:
                state = json.loads(state_path.read_text(encoding='utf-8'))
            except (OSError, ValueError) as exc:
                raise GenerationError(f'{ident}: unreadable state; check history before any retry: {exc}') from exc
            if state.get('status') == 'completed' and audio_path.is_file() and alignment_path.is_file():
                if sha(audio_path.read_bytes()) != state.get('audioSha256'):
                    raise GenerationError(f'{ident}: saved MP3 hash mismatch; stop and inspect')
                print(f'{ident}: already completed; skipped.', flush=True)
                continue
            raise GenerationError(f'{ident}: existing {state.get("status", "unknown")} state; outcome must be investigated before retry.')
        if audio_path.exists() or alignment_path.exists():
            raise GenerationError(f'{ident}: output exists without completed state; investigate before retry.')
        state = {'id': ident, 'status': 'submitted', 'createdAt': stamp(), 'planFingerprint': fingerprint,
                 'textSha256': sha(seg['text'].encode('utf-8')), 'outputFormat': args.format}
        try:
            exclusive_write(state_path, (json.dumps(state, ensure_ascii=False, indent=2) + '\n').encode())
        except FileExistsError:
            raise GenerationError(f'{ident}: request may already be in progress; inspect state and history.') from None
        jobs_started += 1
        print(f'{ident}: sending ({len(seg["text"])} chars).', flush=True)
        try:
            audio, alignment, request_id = synthesize(key, seg, segments[idx-1] if idx else None,
                segments[idx+1] if idx + 1 < len(segments) else None, args.voice_id, args.model,
                args.format, args.timeout)
            exclusive_write(audio_path, audio)
            exclusive_write(alignment_path, (json.dumps(alignment, ensure_ascii=False, indent=2) + '\n').encode())
            audio_meta = verify_mp3(audio_path, args.format)
            state.update({'status': 'completed', 'completedAt': stamp(), 'requestId': request_id,
                          'audioSha256': sha(audio), 'audio': audio_meta,
                          'hasAlignment': alignment['alignment'] is not None})
            update_state(state_path, state)
            print(f'{ident}: saved {audio_meta["durationSeconds"]:.3f} s; alignment={state["hasAlignment"]}.', flush=True)
        except (GenerationError, OSError, ValueError, subprocess.SubprocessError) as exc:
            # Keep a durable marker even for explicit HTTP failure; never resend automatically.
            state.update({'status': 'needs_review', 'failedAt': stamp(), 'error': str(exc)})
            try:
                update_state(state_path, state)
            except OSError:
                pass
            raise GenerationError(f'{ident}: {exc}; job state saved where possible; check ElevenLabs history before retry.') from None
    print(f'New requests started: {jobs_started}', flush=True)


if __name__ == '__main__':
    try:
        main()
    except GenerationError as exc:
        print(f'Error: {exc}', file=sys.stderr)
        sys.exit(1)
