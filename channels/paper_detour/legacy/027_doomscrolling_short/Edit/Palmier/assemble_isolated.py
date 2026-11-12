#!/usr/bin/env python3
"""Assemble 027 in an isolated Palmier session, without export.

Run only after explicit confirmation that the captions are final. Never retry
after a receipt has been created without inspecting Palmier's actual state.
"""
import argparse
import hashlib
import json
import math
import os
import sys
from pathlib import Path

ROOT = Path('/Users/diplomat/ytvideos')
EPISODE = ROOT / 'channels/paper_detour/legacy/027_doomscrolling_short'
MANIFEST = EPISODE / 'Edit/short_manifest.json'
RECEIPT = EPISODE / 'Edit/Palmier/assembly_receipt.json'
LOCK = ROOT / 'channels/paper_detour/.rarovista-timeline-lock'
JOURNAL = ROOT / 'channels/paper_detour/RAROVISTA_TIMELINE_COORDINATION.md'
PROJECT_NAME = '027 Nuviko Doomscrolling Short 20261031'
sys.path.insert(0, str(ROOT / 'automation/palmier'))
from inspect_connection import PalmierConnection


def digest(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for part in iter(lambda: f.read(4 * 1024 * 1024), b''):
            h.update(part)
    return h.hexdigest()


def call(c, name, args):
    data = c.request('tools/call', {'name': name, 'arguments': args})
    if data.get('isError'):
        raise RuntimeError(f'{name}: {data.get("content")}')
    blocks = [x['text'] for x in data.get('content', []) if x.get('type') == 'text']
    if len(blocks) != 1:
        raise RuntimeError(f'{name}: unexpected result')
    return json.loads(blocks[0])


def save(receipt):
    tmp = RECEIPT.with_suffix('.tmp')
    with tmp.open('w') as f:
        json.dump(receipt, f, ensure_ascii=False, indent=2)
        f.write('\n')
        f.flush()
        os.fsync(f.fileno())
    tmp.replace(RECEIPT)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--execute-confirmed', action='store_true')
    p.add_argument('--captions', type=Path, required=True,
                   help='Exact, separately confirmed final caption overlay')
    args = p.parse_args()
    if not args.execute_confirmed:
        raise RuntimeError('No edits: run only after separate final-caption confirmation.')
    if RECEIPT.exists():
        raise RuntimeError('Existing receipt: inspect actual state before continuing, never retry blindly.')
    m = json.loads(MANIFEST.read_text())
    if m.get('fps') != 30 or m.get('frames') != 1132 or m.get('voice_speed_applied') != 1.05:
        raise RuntimeError('Unexpected manifest properties')
    scenes = m['scenes']
    start = 0
    for scene in scenes:
        if scene['start'] != start or scene['end'] <= start:
            raise RuntimeError('Scene coverage is not contiguous')
        start = scene['end']
    if start != m['frames']:
        raise RuntimeError('Scene coverage differs from audio')
    captions = args.captions.resolve()
    paths = [Path(m['voice']), Path(m['srt']), captions] + [Path(s['path']) for s in scenes]
    for path in paths:
        if not path.resolve().is_relative_to(EPISODE.resolve()) or not path.is_file():
            raise RuntimeError(f'Missing episode asset: {path}')
    files = {str(path): digest(path) for path in paths}
    # The shared lock serializes this session with other Palmier editors.
    os.mkdir(LOCK)
    owner = ('# Владелец общей блокировки Palmier\n\n'
             '- Сессия: `01a193c7-3518-7e61-82ec-b6da193c2153`, агент `/root/palmier_editor`.\n'
             '- Цель: собрать отдельный проект Nuviko 027; Rarovista и другие проекты не изменять.\n')
    (LOCK / 'owner.md').write_text(owner)
    receipt = {'status': 'started', 'manifest': str(MANIFEST), 'manifest_sha256': digest(MANIFEST),
               'assets': files, 'steps': [], 'project_name': PROJECT_NAME}
    save(receipt)
    def begin(name, **kw):
        receipt['pending'] = {'action': name, **kw}
        save(receipt)
    def done(**kw):
        receipt['steps'].append({**receipt.pop('pending'), **kw})
        save(receipt)
    try:
        with JOURNAL.open('a') as f:
            f.write('\n**31 октября — отдельный проект Nuviko 027.** Сессия '
                    '`01a193c7-3518-7e61-82ec-b6da193c2153`, агент `/root/palmier_editor`, '
                    'получила общий lock для изолированной сборки. Rarovista и другие проекты не редактируются.\n')
        c = PalmierConnection(); c.connect()
        prior = call(c, 'manage_project', {'action': 'list'})
        initial_timeline = call(c, 'get_timeline', {})
        exports = call(c, 'manage_exports', {'action': 'list'}).get('exports')
        if not prior.get('active') or not prior.get('visible') or not isinstance(exports, list):
            raise RuntimeError('Visible project or export state unknown')
        if any(e.get('status') not in ('completed', 'failed', 'cancelled', 'canceled') for e in exports):
            raise RuntimeError('Another export is running')
        if any(project.get('name') == PROJECT_NAME for project in prior.get('projects', [])):
            raise RuntimeError('Project already exists; inspect before any creation')
        receipt.update(prior_project=prior['visible'], prior_timeline_id=initial_timeline.get('id'))
        save(receipt)
        begin('create_project')
        created = call(c, 'manage_project', {'action': 'create', 'name': PROJECT_NAME,
                                             'aspectRatio': '9:16', 'fps': 30, 'quality': '1080p'})
        done(result=created)
        own = call(c, 'manage_project', {'action': 'list'})
        own_tl = call(c, 'get_timeline', {})
        observer = PalmierConnection(); observer.connect()
        observed = call(observer, 'manage_project', {'action': 'list'})
        observed_tl = call(observer, 'get_timeline', {})
        if observed.get('visible') != prior.get('visible') or observed_tl.get('id') != initial_timeline.get('id'):
            raise RuntimeError('Visible project/timeline changed; stop without restoring or touching other project')
        if own.get('active', {}).get('name') != PROJECT_NAME:
            raise RuntimeError('New session target not confirmed')
        project_path = own['active']['path']
        timeline_id = own_tl['id']
        if (own_tl.get('width'), own_tl.get('height'), own_tl.get('fps')) != (1080, 1920, 30):
            raise RuntimeError('Wrong project geometry')
        if own_tl.get('totalFrames') or any(t.get('clips') for t in own_tl.get('tracks', [])):
            raise RuntimeError('New timeline is not empty')
        receipt.update(isolation_confirmed=True, project_path=project_path,
                       timeline_id=timeline_id, timeline_name=own_tl.get('name'))
        save(receipt)
        def guard():
            if not (LOCK / 'owner.md').is_file() or (LOCK / 'owner.md').read_text() != owner:
                raise RuntimeError('Lost the shared lock')
            now = call(c, 'manage_project', {'action': 'list'})
            tl = call(c, 'get_timeline', {})
            probe = call(observer, 'manage_project', {'action': 'list'})
            probe_tl = call(observer, 'get_timeline', {})
            if now.get('active', {}).get('path') != project_path or tl.get('id') != timeline_id:
                raise RuntimeError('Our session target changed')
            if probe.get('visible') != prior.get('visible') or probe_tl.get('id') != initial_timeline.get('id'):
                raise RuntimeError('Foreign visible project changed; stop')
            if digest(MANIFEST) != receipt['manifest_sha256']:
                raise RuntimeError('Manifest changed')
            return tl
        refs = {}
        # SRT stays external; import only the corresponding visual overlay.
        for path in [Path(m['voice'])] + [Path(s['path']) for s in scenes] + [captions]:
            guard()
            if digest(path) != files[str(path)]:
                raise RuntimeError(f'Asset changed: {path}')
            begin('import_media', path=str(path))
            result = call(c, 'import_media', {'source': {'path': str(path)}, 'folder': '027'})
            ref = result['mediaRef']
            assets = call(c, 'get_media', {'ids': [ref]}).get('assets', [])
            if len(assets) != 1 or assets[0].get('generationStatus'):
                raise RuntimeError(f'Unconfirmed import: {path}')
            refs[str(path)] = ref
            done(mediaRef=ref)
        def add(label, entries):
            guard(); begin(label)
            clips = call(c, 'add_clips', {'entries': entries})['clips']
            if len(clips) != len(entries):
                raise RuntimeError('Unexpected clip count')
            tl = guard()
            actual = {x['id']: x for track in tl.get('tracks', []) for x in track.get('clips', [])}
            for entry, clip in zip(entries, clips):
                item = actual.get(clip['id'])
                if not item or item.get('mediaRef') != entry['mediaRef'] or item['frames'][0] != entry['startFrame']:
                    raise RuntimeError(f'Incorrect {label} placement')
                if 'endFrame' in entry and item['frames'][1] != entry['endFrame']:
                    raise RuntimeError(f'Incorrect {label} ending')
            done(clip_ids=[clip['id'] for clip in clips])
            return clips
        clips = add('add_scenes', [{'mediaRef': refs[s['path']], 'startFrame': s['start'], 'endFrame': s['end']}
                                   for s in scenes])
        for i, (scene, clip) in enumerate(zip(scenes, clips)):
            guard()
            span = scene['end'] - scene['start']
            a, b = ((1.02, 1.07) if i % 2 == 0 else (1.07, 1.02))
            keys = [[0, a, a], [span - 1, b, b]]
            begin('set_scale', clip_id=clip['id'], keys=keys)
            call(c, 'set_keyframes', {'clipId': clip['id'], 'property': 'scale', 'keyframes': keys})
            guard(); done()
        add('add_voice', [{'mediaRef': refs[m['voice']], 'startFrame': 0}])
        add('add_captions', [{'mediaRef': refs[str(captions)], 'startFrame': 0,
                              'endFrame': m['frames'], 'includeAudio': False}])
        final = guard()
        if final.get('totalFrames') != m['frames']:
            raise RuntimeError('Unexpected timeline duration')
        receipt.update(status='assembled_not_exported', tracks=final.get('tracks'),
                       duration=final.get('durationSeconds'), media_refs=refs)
        save(receipt)
        # Close only our confirmed session project to force save. Never close Rarovista.
        begin('close_own_project')
        call(c, 'manage_project', {'action': 'close', 'path': project_path})
        done()
        if call(observer, 'manage_project', {'action': 'list'}).get('visible') != prior.get('visible'):
            raise RuntimeError('Visible project changed after close')
        receipt['status'] = 'assembled_saved_not_exported'
        save(receipt)
        print(json.dumps({'status': receipt['status'], 'project_path': project_path,
                          'timeline_id': timeline_id, 'receipt': str(RECEIPT)}, ensure_ascii=False), flush=True)
    except BaseException as exc:
        receipt['error'] = repr(exc)
        receipt['status'] = 'stopped_inspect_before_retry'
        save(receipt)
        raise
    finally:
        # Remove only our own lock; do not touch another session's owner record.
        if (LOCK / 'owner.md').is_file() and (LOCK / 'owner.md').read_text() == owner:
            with JOURNAL.open('a') as f:
                f.write('\n**31 октября — проект Nuviko 027, завершение окна.** Сессия '
                        '`01a193c7-3518-7e61-82ec-b6da193c2153` завершила действия; '
                        'результат и возможные ошибки записаны в '
                        '`channels/paper_detour/legacy/027_doomscrolling_short/Edit/Palmier/assembly_receipt.json`. '
                        'Rarovista и другие проекты не редактировались.\n')
            (LOCK / 'owner.md').unlink()
            LOCK.rmdir()


if __name__ == '__main__':
    main()
