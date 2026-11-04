"""Hash bindings for prepared subtitles, a rendered file and its release checks.

Hashes establish identity/freshness, never listening or user acceptance. Review
records must be supplied from work actually performed; machine defaults stay open.
This module uses only the standard library so the uploader can validate offline.
"""
from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SCHEMA = 'ytv-delivery-v1'
REVIEW_CHECKS = ('semantic_grouping', 'audible_sync', 'visual_placement')


def sha256(path):
    digest = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(chunk)
    return digest.hexdigest()


def fingerprint(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True,
                                     separators=(',', ':'), allow_nan=False).encode()).hexdigest()


def resolve(base, value):
    path = Path(value).expanduser()
    return (path if path.is_absolute() else Path(base) / path).resolve()


def file_record(path):
    path = Path(path).resolve(strict=True)
    if not path.is_file():
        raise ValueError('Expected a regular file: ' + str(path))
    return {'path': str(path), 'sha256': sha256(path)}


def check_record(record):
    if file_record(record['path']) != record:
        raise ValueError('Stale delivery input: ' + str(record['path']))


def profile_paths(channel, form):
    style = HERE / 'profiles' / (channel + '.json')
    geometry = HERE / 'profiles' / (channel + '_' + form + '.json')
    if not geometry.is_file():
        geometry = HERE / 'profiles' / (form + '.json')
    return style, geometry


def audio_binding(plan, base):
    """Require the final, already conformed mix, including evidenced voice speed."""
    audio = file_record(resolve(base, plan['audio']))
    contract = plan.get('audio_contract', {})
    if contract.get('final_audio_sha256') != audio['sha256']:
        raise ValueError('audio_contract must bind the exact final audio SHA-256')
    policy_path = ROOT / '.agents/skills/ytv-audio-delivery/references/speed.json'
    policy = json.loads(policy_path.read_text())
    required = policy[plan['channel']]
    applied = contract.get('applied_speed')
    if (isinstance(applied, bool) or not isinstance(applied, (int, float))
            or not math.isfinite(applied) or not math.isclose(applied, required, abs_tol=1e-8)):
        raise ValueError(f'Final voice speed must be {required:.2f}x, applied once before alignment')
    # The evidence identifies the source, operation (or already-retimed source),
    # and final mix. The number alone cannot establish actual playback speed.
    evidence = file_record(resolve(base, contract['speed_evidence']))
    return {'audio': audio, 'applied_speed': applied, 'speed_policy': file_record(policy_path),
            'speed_evidence': evidence}


def validate_words(plan, base, total, fps=30):
    binding = audio_binding(plan, base)
    sub = plan['subtitles']
    if sub.get('style') or any(key in sub for key in ('width', 'y')):
        raise ValueError('Subtitle style and geometry are defined by the shared format profile')
    transcript_path = resolve(base, sub['transcript'])
    transcript = transcript_path.read_text(encoding='utf-8').strip()
    source = json.loads(resolve(base, sub['words']).read_text())
    if not isinstance(source, dict) or source.get('audio_sha256') != binding['audio']['sha256']:
        raise ValueError('Word map must bind the final audio; realign or explicitly conform first')
    if source.get('transcript_sha256') != hashlib.sha256(transcript.encode()).hexdigest():
        raise ValueError('Word map transcript SHA-256 is stale')
    words = source.get('words')
    if not isinstance(words, list) or not words:
        raise ValueError('word map is empty')
    if any(not isinstance(word, dict) for word in words):
        raise ValueError('word map entries must be objects')
    # Quotes are an on-screen formatting choice; apostrophes remain literal.
    display = str.maketrans('', '', '\"“”„‟«»')
    tokens = [token.translate(display) for token in transcript.split()]
    tokens = [token for token in tokens if token]
    if [word.get('text') for word in words] != tokens:
        raise ValueError('Word map changes, omits or reorders the retained transcript')
    previous_end = -1.0
    previous_frame = -1
    for word in words:
        if not isinstance(word.get('text'), str) or not word['text'].strip() or any(c.isspace() for c in word['text']):
            raise ValueError('each word text must be a single token')
        if any(isinstance(word[key], bool) for key in ('start', 'end')):
            raise ValueError('Word timings must be numeric seconds, not booleans')
        start, end = float(word['start']), float(word['end'])
        if not (math.isfinite(start) and math.isfinite(end) and 0 <= start < end <= total / fps + 1e-6 and start >= previous_end):
            raise ValueError('invalid or overlapping word timings')
        frame = math.ceil(start * fps - 1e-7)
        if frame >= total or frame <= previous_frame:
            raise ValueError('Word starts collide on a frame or fall outside the timeline; reconcile timings')
        previous_end, previous_frame = end, frame
    return words, binding


def subtitle_contract(plan, base, canvas, total, groups, resolved):
    style, geometry = profile_paths(plan['channel'], plan['format'])
    sub = plan['subtitles']
    return {'schema': SCHEMA, 'channel': plan['channel'], 'format': plan['format'],
            'canvas': list(canvas), 'fps': 30, 'frames': total,
            'audio': audio_binding(plan, base),
            'transcript': file_record(resolve(base, sub['transcript'])),
            'word_map': file_record(resolve(base, sub['words'])),
            'profiles': [file_record(style), file_record(geometry),
                         file_record(json.loads(style.read_text())['font'])],
            'engine': [file_record(HERE / 'montage.py'), file_record(Path(__file__)),
                       file_record(ROOT / '.agents/skills/ytv-paper-subtitles/scripts/semantic_grouping.py')],
            'picture': [{'scene': scene, 'image': file_record(resolve(base, scene['image']))}
                        for scene in plan['scenes']],
            'overlays': [{'layer': layer, 'file': file_record(resolve(base, layer['path']))}
                         for layer in plan.get('overlays', [])],
            'groups': groups, 'resolved': resolved}


def write_json(path, value):
    with Path(path).open('x', encoding='utf-8') as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2, allow_nan=False)
        stream.write('\n')


def review_template(contract):
    return {'subtitle_contract_sha256': fingerprint(contract),
            'checks': {key: {'status': 'UNVERIFIED', 'reviewer': '', 'method': '',
                             'coverage': '', 'evidence': None} for key in REVIEW_CHECKS}}


def render_inputs(manifest, plan, base):
    paths = [manifest, resolve(base, plan['audio'])]
    paths += [resolve(base, scene['image']) for scene in plan['scenes']]
    paths += [resolve(base, layer['path']) for layer in plan.get('overlays', [])]
    if plan['subtitles'].get('review'):
        paths.append(resolve(base, plan['subtitles']['review']))
    return [file_record(path) for path in dict.fromkeys(paths)]


def write_receipt(output, channel, contract, inputs, review=None):
    """Record identity after encoding, without performing or claiming AV QA."""
    if review is not None and review.get('subtitle_contract_sha256') != fingerprint(contract):
        raise ValueError('Pre-render subtitle review is stale')
    value = {'schema': SCHEMA, 'channel': channel, 'media': file_record(output),
             'inputs': inputs, 'subtitles': contract, 'review': review or review_template(contract),
             'acceptance': {'accepted': False, 'media_sha256': None, 'evidence': None},
             'open_requirements': []}
    write_json(str(output) + '.delivery.json', value)


def validate_release(video, channel_id, receipt_path=None):
    """Fail before any API call; unrelated channel upload mechanics stay generic."""
    channels = json.loads((ROOT / 'automation/channels.json').read_text())
    channel_names = {'paper_detour': 'paper', 'nuviko_history': 'nuviko'}
    protected = {channels[key]['channel_id']: name for key, name in channel_names.items()}
    if channel_id not in protected and receipt_path is None:
        return
    path = Path(receipt_path) if receipt_path else Path(str(Path(video).resolve()) + '.delivery.json')
    if not path.is_file():
        raise ValueError('Missing delivery receipt for Paper/Nuviko upload')
    receipt = json.loads(path.read_text())
    if (receipt.get('schema') != SCHEMA or receipt.get('channel') != protected.get(channel_id)
            or receipt.get('media') != file_record(video)):
        raise ValueError('Delivery receipt does not match the video/channel')
    if receipt.get('open_requirements') != []:
        raise ValueError('Required delivery changes remain open')
    for record in receipt['inputs']:
        check_record(record)
    contract = receipt['subtitles']
    if contract.get('schema') != SCHEMA or contract.get('channel') != receipt['channel']:
        raise ValueError('Invalid subtitle contract')
    for record in [contract['audio']['audio'], contract['audio']['speed_policy'],
                   contract['audio']['speed_evidence'], contract['transcript'], contract['word_map']]:
        check_record(record)
    for record in contract['profiles'] + contract['engine']:
        check_record(record)
    # Revalidate speed/timing/text from the actual current plan, not editable flags.
    manifest = Path(receipt['inputs'][0]['path'])
    plan = json.loads(manifest.read_text())
    if plan['channel'] != receipt['channel'] or plan['subtitles']['mode'] != 'words':
        raise ValueError('Release requires the official word-subtitle route')
    words, binding = validate_words(plan, manifest.parent, contract['frames'])
    if binding != contract['audio'] or file_record(resolve(manifest.parent, plan['audio'])) != contract['audio']['audio']:
        raise ValueError('Final audio binding differs from rendered subtitles')
    if [w for group in contract['groups'] for w in group] != words:
        raise ValueError('Subtitle contract does not cover the exact word map')
    review = receipt['review']
    if review.get('subtitle_contract_sha256') != fingerprint(contract):
        raise ValueError('Subtitle review is stale')
    for key in REVIEW_CHECKS:
        check = review['checks'][key]
        if check.get('status') != 'PASS' or not all(isinstance(check.get(field), str) and check[field].strip() for field in ('reviewer', 'method', 'coverage')):
            raise ValueError('Subtitle review incomplete: ' + key)
        check_record(check['evidence'])
    acceptance = receipt['acceptance']
    if acceptance.get('accepted') is not True or acceptance.get('media_sha256') != receipt['media']['sha256']:
        raise ValueError('User acceptance must bind this exact MP4')
    check_record(acceptance['evidence'])
