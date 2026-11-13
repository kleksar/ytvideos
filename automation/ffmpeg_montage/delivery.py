"""Hash bindings for prepared subtitles, a rendered file and its release checks.

Hashes establish identity/freshness, never listening or user acceptance. Review
records must be supplied from work actually performed; machine defaults stay open.
This module uses only the standard library so the uploader can validate offline.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
_config_spec = importlib.util.spec_from_file_location('delivery_channel_config', ROOT / 'automation/helpers/channel_config.py')
channel_config = importlib.util.module_from_spec(_config_spec)
_config_spec.loader.exec_module(channel_config)
SCHEMA = 'ytv-delivery-v1'
RECEIPT_SCHEMA = 'ytv-delivery-v2'
REUPLOAD_SCHEMA = 'ytv-owned-reupload-v1'
REVIEW_CHECKS = ('semantic_grouping', 'visual_placement')


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
    name = channel_config.visual_profile(channel)
    if form not in {'long', 'short'}:
        raise ValueError('Unsupported video format')
    style = HERE / 'profiles' / (name + '.json')
    if not style.is_file():
        raise ValueError(f'No montage visual profile configured for {channel}: {name}')
    geometry = HERE / 'profiles' / (name + '_' + form + '.json')
    if not geometry.is_file():
        geometry = HERE / 'profiles' / (form + '.json')
    return style, geometry


def load_style(plan, base):
    """Resolve an explicit font override; never substitute a host's default font."""
    style, _ = profile_paths(plan['channel'], plan['format'])
    profile = json.loads(style.read_text())
    name = channel_config.visual_profile(plan['channel']).upper().replace('-', '_')
    override = plan.get('font_override')
    if override is None and os.environ.get('YTV_FONT_OVERRIDE_' + name):
        try:
            index = int(os.environ.get('YTV_FONT_INDEX_' + name, '0'))
        except ValueError:
            raise ValueError('Font override index must be a nonnegative integer') from None
        override = {'path': os.environ['YTV_FONT_OVERRIDE_' + name], 'index': index}
    if override is not None:
        if (not isinstance(override, dict) or set(override) != {'path', 'index'}
                or not isinstance(override['path'], str) or not override['path'].strip()
                or type(override['index']) is not int or override['index'] < 0):
            raise ValueError('font_override requires an explicit path and nonnegative integer index')
        font = resolve(base, override['path'])
        if not font.is_file() or font.suffix.lower() not in {'.ttf', '.otf', '.ttc'}:
            raise ValueError('Explicit font override must be an existing TTF, OTF or TTC file')
        profile.update(font=str(font), font_index=override['index'])
    if not Path(profile['font']).is_file():
        raise ValueError('Approved profile font is unavailable; supply a verified explicit font_override')
    return profile


def audio_binding(plan, base):
    """Require the final, already conformed mix, including evidenced voice speed."""
    audio = file_record(resolve(base, plan['audio']))
    contract = plan.get('audio_contract', {})
    if contract.get('final_audio_sha256') != audio['sha256']:
        raise ValueError('audio_contract must bind the exact final audio SHA-256')
    profile, policy_path = channel_config.channel_profile(plan['channel'])
    required = profile.get('voice', {}).get('speed')
    if type(required) not in (int, float) or not math.isfinite(required) or required <= 0:
        raise ValueError('Channel voice.speed must be configured')
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
    effective_style = load_style(plan, base)
    sub = plan['subtitles']
    return {'schema': SCHEMA, 'channel': plan['channel'], 'format': plan['format'],
            'canvas': list(canvas), 'fps': 30, 'frames': total,
            'caption_end_frame': plan['subtitles'].get('end_frame', total),
            'audio': audio_binding(plan, base),
            'transcript': file_record(resolve(base, sub['transcript'])),
            'word_map': file_record(resolve(base, sub['words'])),
            'profiles': [file_record(style), file_record(geometry),
                         file_record(effective_style['font'])],
            'font': {'path': effective_style['font'], 'index': effective_style['font_index']},
            'engine': [file_record(HERE / 'montage.py'), file_record(Path(__file__)),
                       file_record(ROOT / 'automation/helpers/channel_config.py'),
                       file_record(ROOT / 'automation/helpers/paper-subtitles/scripts/semantic_grouping.py')],
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


def write_receipt(output, channel, contract, inputs, review=None, render=None):
    """Record identity after encoding, without performing or claiming AV QA."""
    if review is not None and review.get('subtitle_contract_sha256') != fingerprint(contract):
        raise ValueError('Pre-render subtitle review is stale')
    validate_render_binding(render, contract, inputs[0]['path'], output)
    value = {'schema': RECEIPT_SCHEMA, 'channel': channel, 'media': file_record(output),
             'inputs': inputs, 'subtitles': contract, 'review': review or review_template(contract),
             'acceptance': {'accepted': False, 'media_sha256': None, 'evidence': None},
             'open_requirements': [], 'render': render}
    write_json(str(output) + '.delivery.json', value)


def protected_channel(channel_id):
    for slug in channel_config.configured_channels():
        profile, _ = channel_config.channel_profile(slug)
        if profile.get('youtube_channel_id') == channel_id and profile.get('recipe') == 'illustrated':
            return slug
    return None


def same_channel(recorded, expected):
    return isinstance(recorded, str) and channel_config.LEGACY_ALIASES.get(recorded, recorded) == expected


def validate_release(video, channel_id, receipt_path=None, *, private_staging=False):
    """Validate the exact media before upload or before leaving private staging."""
    channel = protected_channel(channel_id)
    if channel is None and receipt_path is None:
        return
    path = Path(receipt_path) if receipt_path else Path(str(Path(video).resolve()) + '.delivery.json')
    if not path.is_file():
        raise ValueError('Missing delivery receipt for configured illustrated-channel upload')
    receipt = json.loads(path.read_text())
    if receipt.get('schema') == REUPLOAD_SCHEMA:
        return validate_owned_reupload(receipt, video, channel_id)
    if receipt.get('schema') == 'ytv-audio-replacement-v1':
        return validate_audio_replacement(receipt, video, channel_id, channel, private_staging)
    if receipt.get('schema') == SCHEMA:
        raise ValueError('Historical receipt needs a saved-command audit and frozen export contract; do not automatically rerender')
    if (receipt.get('schema') != RECEIPT_SCHEMA or not same_channel(receipt.get('channel'), channel)
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
    for record in contract['profiles']:
        check_record(record)
    # The executable used for this file is frozen; a later working-tree change
    # is not a change to the accepted edit or media.
    validate_render_binding(receipt.get('render'), contract, receipt['inputs'][0]['path'], video)
    # Revalidate speed/timing/text from the actual current plan, not editable flags.
    manifest = Path(receipt['inputs'][0]['path'])
    plan = json.loads(manifest.read_text())
    if plan['channel'] != receipt['channel'] or plan['subtitles']['mode'] != 'words':
        raise ValueError('Release requires the official word-subtitle route')
    words, binding = validate_words(plan, manifest.parent, contract['frames'])
    # A frozen renderer can record a snapshot path for the speed policy.
    # Both files were independently hash-checked above; compare the policy
    # content, while retaining exact path-and-hash binding for the audio and
    # its speed evidence.
    recorded_binding = dict(contract['audio'])
    current_binding = dict(binding)
    recorded_policy = recorded_binding.pop('speed_policy')
    current_policy = current_binding.pop('speed_policy')
    if (recorded_binding != current_binding
            or recorded_policy['sha256'] != current_policy['sha256']
            or file_record(resolve(manifest.parent, plan['audio'])) != contract['audio']['audio']):
        raise ValueError('Final audio binding differs from rendered subtitles')
    if [w for group in contract['groups'] for w in group] != words:
        raise ValueError('Subtitle contract does not cover the exact word map')
    review = receipt['review']
    if review.get('subtitle_contract_sha256') != fingerprint(contract):
        raise ValueError('Subtitle review is stale')
    if any(review['checks'][key].get('status') == 'FAIL' for key in REVIEW_CHECKS):
        raise ValueError('Confirmed subtitle defect remains open')
    if private_staging:
        technical = receipt.get('technical_review', {})
        if (technical.get('status') != 'PASS' or technical.get('full_decode') != 'PASS'
                or technical.get('media_sha256') != receipt['media']['sha256']):
            raise ValueError('Private staging requires technical QA and full decode of this exact MP4')
        check_record(technical['evidence'])
        return receipt
    playback = receipt.get('playback_review', {})
    owner_viewed = (playback.get('status') == 'ACCEPTED'
                    and playback.get('media_sha256') == receipt['media']['sha256']
                    and playback.get('scope') == 'final_mp4_with_audio_and_burned_in_captions')
    if owner_viewed:
        check_record(playback['evidence'])
    for key in REVIEW_CHECKS:
        check = review['checks'][key]
        if owner_viewed and check.get('status') in ('UNVERIFIED', 'WARNING'):
            continue
        if check.get('status') != 'PASS' or not all(isinstance(check.get(field), str) and check[field].strip() for field in ('reviewer', 'method', 'coverage')):
            raise ValueError('Subtitle review incomplete: ' + key)
        check_record(check['evidence'])
    acceptance = receipt['acceptance']
    if acceptance.get('accepted') is not True or acceptance.get('media_sha256') != receipt['media']['sha256']:
        raise ValueError('User acceptance must bind this exact MP4')
    check_record(acceptance['evidence'])
    return receipt


def validate_owned_reupload(receipt, video, channel_id):
    """Validate a recovered published copy without inventing a production render."""
    import re
    if receipt.get('channel_id') != channel_id or receipt.get('media') != file_record(video):
        raise ValueError('Reupload receipt does not match the video/channel')
    source = receipt.get('source', {})
    if not re.fullmatch(r'[A-Za-z0-9_-]{11}', source.get('video_id', '')):
        raise ValueError('Reupload source video ID is invalid')
    check_record(source['api_snapshot'])
    check_record(source['download_evidence'])
    snapshot = json.loads(Path(source['api_snapshot']['path']).read_text())
    items = [v for v in snapshot.get('items', []) if v.get('id') == source['video_id']]
    if (len(items) != 1 or items[0].get('snippet', {}).get('channelId') != channel_id
            or items[0].get('status', {}).get('privacyStatus') != 'public'):
        raise ValueError('Snapshot does not establish a public source on the expected channel')
    technical = receipt.get('technical_review', {})
    if (technical.get('full_decode') != 'PASS'
            or technical.get('media_sha256') != receipt['media']['sha256']):
        raise ValueError('Reupload requires full decode of the exact file')
    check_record(technical['evidence'])
    return receipt

def validate_audio_replacement(receipt, video, channel_id, channel, private_staging):
    """Validate an audio-only replacement against a previously rendered picture."""
    if (not same_channel(receipt.get('channel'), channel) or receipt.get('media') != file_record(video)
            or receipt.get('open_requirements') != []):
        raise ValueError('Audio replacement receipt does not match media/channel')
    for key in ('source_receipt', 'source_media', 'mix', 'word_map', 'export_contract',
                'audio_evidence', 'video_identity_evidence'):
        check_record(receipt[key])
    source = validate_release(receipt['source_media']['path'], channel_id,
                              receipt['source_receipt']['path'], private_staging=True)
    old_map = json.loads(Path(source['subtitles']['word_map']['path']).read_text())
    new_map = json.loads(Path(receipt['word_map']['path']).read_text())
    if (new_map.get('words') != old_map.get('words')
            or new_map.get('transcript_sha256') != old_map.get('transcript_sha256')
            or new_map.get('audio_sha256') != receipt['mix']['sha256']):
        raise ValueError('Replacement word map or final mix differs from source timing')
    contract = json.loads(Path(receipt['export_contract']['path']).read_text())
    root = Path(contract['working_directory'])
    for record, key in ((receipt['source_media'], contract['picture_source']),
                        (receipt['mix'], contract['audio']['mix']),
                        (receipt['word_map'], contract['audio']['word_map'])):
        if file_record(root / key['path']) != record or key['sha256'] != record['sha256']:
            raise ValueError('Replacement export contract differs from input')
    argv = contract.get('argv')
    if (not isinstance(argv, list) or len(argv) < 2
            or Path(argv[0]).name != 'ffmpeg' or argv.count('-i') != 2
            or argv[argv.index('-i') + 1] != contract['picture_source']['path']
            or argv[argv.index('-i', argv.index('-i') + 1) + 1] != contract['audio']['mix']['path']
            or command_option(argv, '-c:v') != 'copy'
            or argv[-1] != contract['output']):
        raise ValueError('Replacement command does not copy the source picture and use the selected mix')
    if (contract['status'] != 'READY_TO_RENDER'
            or (root / contract['output']).resolve() != Path(video).resolve()):
        raise ValueError('Replacement export contract does not identify output')
    technical = receipt.get('technical_review', {})
    if (technical.get('status') != 'PASS' or technical.get('full_decode') != 'PASS'
            or technical.get('media_sha256') != receipt['media']['sha256']):
        raise ValueError('Replacement requires technical review of exact output')
    check_record(technical['evidence'])
    if not private_staging:
        accepted = receipt.get('acceptance', {})
        if accepted.get('accepted') is not True or accepted.get('media_sha256') != receipt['media']['sha256']:
            raise ValueError('User acceptance must bind this exact MP4')
        check_record(accepted['evidence'])
    return receipt


def command_option(argv, name):
    """Require an unambiguous submitted value; never infer it from a preset."""
    if argv.count(name) != 1:
        raise ValueError('Expected exactly one command option: ' + name)
    return argv[argv.index(name) + 1]


def bitrate(value):
    import re
    match = re.fullmatch(r'([0-9]+(?:\.[0-9]+)?)\s*([kKmM]?)(?:\s*bit/s)?', str(value))
    if not match:
        raise ValueError('Invalid bitrate: ' + str(value))
    result = float(match[1]) * {'': 1, 'k': 1000, 'm': 1000000}[match[2].lower()]
    if result <= 0 or not result.is_integer():
        raise ValueError('Bitrate must be a positive integer')
    return int(result)


def check_export_settings(passport, argv, prepared, audio, manifest, output):
    """Compare the frozen passport with the actual argv before scene encoding.

    This is a settings check, not a measurement or audiovisual QA of the output.
    Fields outside this renderer's contract are rejected rather than ignored.
    """
    from fractions import Fraction
    if not isinstance(argv, list) or not argv or not all(isinstance(value, str) for value in argv):
        raise ValueError('FFmpeg command must be a nonempty argv string list')
    if passport.get('status') != 'READY_TO_RENDER':
        raise ValueError('Export contract must be READY_TO_RENDER')
    if passport['preflight'].get('unresolved_required_fields') != []:
        raise ValueError('Unresolved required export settings')
    if Path(passport['edit']['timeline_id']).resolve() != Path(manifest).resolve():
        raise ValueError('Export contract identifies another manifest')
    if Path(passport['preflight']['output_path']).resolve() != Path(output).resolve() or Path(argv[-1]).resolve() != Path(output).resolve():
        raise ValueError('Export contract/command identifies another output')
    expected_audio = passport['required_delivery']['audio_contract']
    required_video = {'codec_name','pix_fmt','scan','cadence','color_primaries','color_transfer','color_space','color_range'}
    if set(passport['required_delivery']['video']) != required_video:
        raise ValueError('Missing or unsupported required video settings')
    allowed_audio = {'owner_handoff','accepted_complete_mix','source_rate_channels','codec_name','profile','sample_rate','channels','target_bit_rate'}
    if set(expected_audio) - allowed_audio:
        raise ValueError('Unsupported required audio field')
    mix_record = expected_audio['accepted_complete_mix']
    if {key: mix_record[key] for key in ('path', 'sha256')} != file_record(prepared['audio']):
        raise ValueError('Export contract does not bind the accepted complete mix')
    # Commands operate on the same continuous mix, with no resampling/remapping.
    if prepared['audio'] not in [argv[i+1] for i, value in enumerate(argv) if value == '-i']:
        raise ValueError('Command does not use the accepted audio')
    if any(flag in argv for flag in ('-ar', '-ac', '-af', '-filter:a')):
        raise ValueError('Audio resampling/remapping/filtering requires a supported contract mapping')
    def equal(name, expected, actual):
        if expected != actual:
            raise ValueError(f'Export setting mismatch: {name}: contract={expected!r}, command={actual!r}')
    timeline = passport['timeline']
    actual_timeline = dict(width=prepared['canvas'][0], height=prepared['canvas'][1],
                           frame_count=prepared['frames'], sample_aspect_ratio='1:1',
                           aspect_ratio='16:9' if prepared['format']=='long' else '9:16',
                           output_color_space='Rec.709 SDR')
    # Technical probes may have a different aspect, recorded explicitly.
    from math import gcd
    divisor = gcd(*prepared['canvas'])
    actual_timeline['aspect_ratio'] = ':'.join(str(v//divisor) for v in prepared['canvas'])
    for key, value in actual_timeline.items():
        equal('timeline.'+key, timeline[key], value)
    equal('timeline.fps', Fraction(str(timeline['fps'])), Fraction(30))
    equal('timeline.duration', round(float(timeline['duration_seconds']), 8), round(prepared['frames']/30, 8))
    equal('command.duration', round(float(command_option(argv, '-t')), 8), round(prepared['frames']/30, 8))
    equal('container', passport['required_delivery']['container'], 'MP4')
    if Path(output).suffix.lower() != '.mp4':
        raise ValueError('Output must be MP4')
    filters = command_option(argv, '-filter_complex')
    if 'setsar=1' not in filters:
        raise ValueError('Command does not set square pixels')
    if prepared.get('source_transfer') == 'srgb' and 'itrc=srgb:' not in filters:
        raise ValueError('Command lacks required sRGB transfer conversion')
    audio_input = [argv[i+1] for i,value in enumerate(argv) if value=='-i'].index(prepared['audio'])
    mappings = [argv[i+1] for i,value in enumerate(argv) if value=='-map']
    if mappings != ['[vout]', f'{audio_input}:a:0']:
        raise ValueError('Unexpected final video/audio mapping')
    encoder = command_option(argv, '-c:v')
    if encoder not in ('libx264', 'h264_videotoolbox'):
        raise ValueError('Unsupported encoder mapping: ' + encoder)
    video = {'codec_name':'h264', 'pix_fmt':command_option(argv, '-pix_fmt'),
             'scan':'progressive', 'cadence':'constant 30/1 fps',
             'color_primaries':command_option(argv, '-color_primaries'),
             'color_transfer':command_option(argv, '-color_trc'),
             'color_space':command_option(argv, '-colorspace'),
             'color_range':command_option(argv, '-color_range')}
    for key, expected in passport['required_delivery']['video'].items():
        if key not in video:
            raise ValueError('Unsupported required video field: ' + key)
        equal('video.'+key, expected, video[key])
    audio_mode = command_option(argv, '-c:a')
    if audio_mode not in ('aac', 'copy') or (audio_mode=='copy' and audio['codec_name']!='aac'):
        raise ValueError('Unsupported audio codec mapping')
    actual_audio = {'codec_name':'aac', 'profile':audio.get('profile') if audio_mode=='copy' else 'LC',
                    'channels':int(audio['channels']), 'sample_rate':int(audio['sample_rate'])}
    for key in ('codec_name', 'profile', 'channels', 'sample_rate'):
        equal('audio.'+key, expected_audio[key], actual_audio[key])
    target = 'STREAM_COPY' if audio_mode=='copy' else bitrate(command_option(argv, '-b:a'))
    if audio_mode=='copy':
        if '-b:a' in argv:
            raise ValueError('Stream copy must not claim an encoder bitrate')
        equal('audio.target_bit_rate', expected_audio['target_bit_rate'], target)
    else:
        if target < (256000 if actual_audio['channels']>=2 else 192000):
            raise ValueError('Audio target below channel delivery requirement')
        equal('audio.target_bit_rate', bitrate(expected_audio['target_bit_rate']), target)
    requested = {'encoder':encoder, 'video_bitrate':bitrate(command_option(argv, '-b:v')),
                 'output_pix_fmt':video['pix_fmt'], 'fps':'30/1', 'audio_codec':audio_mode,
                 'audio_profile':'aac_low' if actual_audio['profile']=='LC' else actual_audio['profile'],
                 'audio_bitrate':target, 'audio_sample_rate':actual_audio['sample_rate'],
                 'audio_channels':actual_audio['channels']}
    for key, expected in passport['encoding']['requested_arguments'].items():
        if key not in requested:
            raise ValueError('Unsupported requested encoder control: ' + key)
        if key in ('video_bitrate', 'audio_bitrate') and expected != 'STREAM_COPY':
            expected = bitrate(expected)
        if key in ('audio_sample_rate', 'audio_channels'):
            expected = int(expected)
        equal('encoding.'+key, expected, requested[key])
    return {'scope':'pre-render settings only; no encoded-result or AV QA',
            'timeline':actual_timeline, 'video':video, 'audio':{**actual_audio, 'mode':audio_mode, 'target_bit_rate':target},
            'requested_arguments':requested}


def freeze_render(work, passport_path, command_path, engine, prepared, audio, manifest, output):
    """Freeze provenance before encoding; later tool updates are not edit changes."""
    work = Path(work)
    directory = work/'render_provenance'
    directory.mkdir()
    def snapshot(path, name):
        original = file_record(path)
        target = directory/name
        target.write_bytes(Path(path).read_bytes())
        frozen = file_record(target)
        if original['sha256'] != frozen['sha256']:
            raise ValueError('Input changed while freezing render provenance')
        return {'original':original, 'snapshot':frozen}
    passport = snapshot(passport_path, 'export_contract.json')
    command = snapshot(command_path, 'render_command.json')
    expected = json.loads(Path(passport['snapshot']['path']).read_text())
    argv = json.loads(Path(command['snapshot']['path']).read_text())
    settings = check_export_settings(expected, argv, prepared, audio, manifest, output)
    frozen_engine = [snapshot(record['path'], f'engine_{i}_{Path(record["path"]).name}') for i,record in enumerate(engine)]
    if [entry['original'] for entry in frozen_engine] != engine:
        raise ValueError('Renderer changed after subtitle preparation')
    import subprocess
    version = subprocess.check_output([argv[0], '-version'], text=True).splitlines()[0]
    return {'schema':'ytv-render-v1', 'origin':'render', 'export_contract':passport,
            'command':command, 'engine':frozen_engine, 'prepared':prepared, 'audio_source':audio,
            'settings':settings, 'ffmpeg_version':version}


def validate_render_binding(render, subtitle_contract, manifest, output):
    if not isinstance(render, dict) or render.get('schema') != 'ytv-render-v1':
        raise ValueError('Missing frozen render provenance; audit saved command and export contract, do not automatically rerender')
    for key in ('export_contract', 'command'):
        check_record(render[key]['snapshot'])
        if render[key]['original']['sha256'] != render[key]['snapshot']['sha256']:
            raise ValueError('Invalid frozen '+key)
    engine = render['engine']
    if [item['original'] for item in engine] != subtitle_contract['engine']:
        raise ValueError('Render engine differs from subtitle preparation')
    if render.get('origin') == 'render':
        for item in engine:
            check_record(item['snapshot'])
            if item['snapshot']['sha256'] != item['original']['sha256']:
                raise ValueError('Invalid frozen engine snapshot')
    elif render.get('origin') == 'historical_command_audit':
        check_record(render['audit_evidence'])
    else:
        raise ValueError('Unknown render provenance origin')
    passport = json.loads(Path(render['export_contract']['snapshot']['path']).read_text())
    argv = json.loads(Path(render['command']['snapshot']['path']).read_text())
    settings = check_export_settings(passport, argv, render['prepared'], render['audio_source'], manifest, output)
    if settings != render['settings']:
        raise ValueError('Frozen render settings differ from command/contract')
    if render['prepared']['canvas'] != subtitle_contract['canvas'] or render['prepared']['frames'] != subtitle_contract['frames']:
        raise ValueError('Render timeline differs from subtitles')
    if file_record(render['prepared']['audio']) != subtitle_contract['audio']['audio']:
        raise ValueError('Render audio differs from accepted subtitle audio')
