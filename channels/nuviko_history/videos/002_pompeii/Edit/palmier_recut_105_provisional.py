#!/usr/bin/env python3
"""Build a new Palmier recut timeline from an approved CSV; dry-run by default.

Uses Palmier's local MCP bridge. Never edits the .palmier package directly.
See palmier_recut_README.md. Do not run alongside another Palmier editor.
"""
import argparse
import csv
import hashlib
import json
import math
import os
from pathlib import Path
import sys
import time
from datetime import datetime, timezone
from uuid import uuid4

BRIDGE = Path('/Users/diplomat/ytvideos/automation/palmier')
sys.path.insert(0, str(BRIDGE))
from inspect_connection import PalmierConnection  # noqa: E402

PROJECT = Path('/Users/diplomat/ytvideos/channels/nuviko_stories/videos/001_brother_ex_best_friend/1.palmier')
STORYBOARD = Path('/Users/diplomat/ytvideos/channels/nuviko_history/videos/002_pompeii/Source/Storyboard')
EDIT = Path(__file__).resolve().parent
DEFAULT_MAP = EDIT / 'dynamic_recut_105_provisional.csv'
FPS, WIDTH, HEIGHT, START, TOTAL = 30, 1920, 1080, 1024, 26914
VOICE_REF = 'CEC13D41'
FOLDER = 'Stories/002/Edit/DynamicRecutImports'


def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def check(condition, message):
    if not condition:
        raise ValueError(message)


def keyframes_match(actual, expected):
    """Allow Palmier's observed 3-decimal serialization; frames remain exact."""
    if not isinstance(actual, list) or not isinstance(expected, list) or len(actual) != len(expected):
        return False
    for got, want in zip(actual, expected):
        if not isinstance(got, list) or not isinstance(want, list):
            return False
        gi = got[-1] if got and isinstance(got[-1], str) else None
        wi = want[-1] if want and isinstance(want[-1], str) else None
        gv = got[:-1] if gi is not None else got
        wv = want[:-1] if wi is not None else want
        if len(gv) != len(wv) or not gv or type(gv[0]) is not int or gv[0] != wv[0]:
            return False
        if gi != wi and not (gi is None and wi == 'smooth'):
            return False
        if any(type(a) not in (int, float) or not math.isfinite(a) or abs(a-b) > 0.000500001 for a,b in zip(gv[1:],wv[1:])):
            return False
    return True


def read_map(path):
    rows = []
    with open(path, encoding='utf-8-sig', newline='') as f:
        reader = csv.DictReader(f)
        required = {'clip', 'start_frame', 'end_frame_exclusive', 'duration_frames', 'image_path', 'review'}
        check(required.issubset(reader.fieldnames or []), 'CSV is missing required columns')
        for r in reader:
            row = {k: r[k] for k in required}
            row['shot'] = row.pop('clip')
            row['status'] = (r.get('status') or '').strip().lower() if 'status' in reader.fieldnames else 'available'
            for k in ('shot', 'start_frame', 'end_frame_exclusive', 'duration_frames'):
                row[k] = int(row[k])
            check(row['status'] in ('available', 'provisional'), f"shot {row['shot']}: unknown status")
            p = Path(row['image_path'])
            check(p.is_absolute() and p.is_file(), f"shot {row['shot']}: missing absolute image path: {p}")
            p = p.resolve(strict=True)
            check(p.is_relative_to(STORYBOARD.resolve(strict=True)), f"shot {row['shot']}: file outside Storyboard")
            check(p.suffix.lower() in ('.png', '.jpg', '.jpeg', '.tiff', '.heic'), f"shot {row['shot']}: unsupported image")
            row['image_path'] = str(p)
            check(row['end_frame_exclusive'] > row['start_frame'] >= 0, f"shot {row['shot']}: invalid frame range")
            check(row['duration_frames'] == row['end_frame_exclusive'] - row['start_frame'], f"shot {row['shot']}: wrong duration")
            check(row['shot'] == len(rows) + 1, 'Shot numbers must be consecutive starting at 1')
            check(row['start_frame'] == (rows[-1]['end_frame_exclusive'] if rows else START), f"shot {row['shot']}: gap or overlap")
            rows.append(row)
    check(rows and rows[-1]['end_frame_exclusive'] == TOTAL, f'Map must cover [{START},{TOTAL}) exactly')
    return rows


def read_keyframes(path, rows):
    if not path:
        return {}
    data = json.loads(Path(path).read_text(encoding='utf-8'))
    check(isinstance(data, dict), 'Keyframes JSON must be an object keyed by shot number')
    result = {}
    sizes = {'scale': 3, 'position': 3, 'crop': 5, 'rotation': 2, 'opacity': 2, 'blur': 2}
    for key, props in data.items():
        check(str(key).isdigit() and 1 <= int(key) <= len(rows), f'Unknown shot {key}')
        check(isinstance(props, dict), f'shot {key}: keyframes must be an object')
        duration = rows[int(key)-1]['duration_frames']
        for prop, points in props.items():
            check(prop in sizes and isinstance(points, list) and len(points) >= 2, f'shot {key}: at least two keyframes required')
            previous = -1
            for point in points:
                check(isinstance(point, list), 'Keyframe must be an array')
                has_interp = bool(point and isinstance(point[-1], str))
                vals = point[:-1] if has_interp else point
                check(len(vals) == sizes[prop], f'shot {key}: invalid {prop} point')
                check(not has_interp or point[-1] in ('smooth', 'linear', 'hold'), 'Invalid interpolation')
                check(all(type(x) in (int, float) and math.isfinite(x) for x in vals), 'Non-finite keyframe')
                check(type(vals[0]) is int and previous < vals[0] < duration, f'shot {key}: invalid frame offset')
                previous = vals[0]
                if prop == 'opacity': check(0 <= vals[1] <= 1, 'Invalid opacity')
                if prop == 'blur': check(0 <= vals[1] <= 100, 'Invalid blur')
                if prop == 'crop': check(all(0 <= x <= 1 for x in vals[1:]), 'Invalid crop')
                if prop == 'scale': check(all(x > 0 for x in vals[1:]), 'Invalid scale')
            def values(point):
                return point[1:-1] if isinstance(point[-1], str) else point[1:]
            check(any(values(p) != values(points[0]) for p in points[1:]), f'shot {key}: constant {prop} keyframes are not supported by this checker')
        result[int(key)] = props
    return result


def tool(c, name, args):
    result = c.request('tools/call', {'name': name, 'arguments': args})
    if result.get('isError'):
        raise RuntimeError(f'{name} refused: {result.get("content")}')
    text = [x['text'] for x in result.get('content', []) if x.get('type') == 'text']
    check(len(text) == 1, f'{name}: unexpected MCP response')
    return json.loads(text[0])


def state(c, expected_id):
    projects = tool(c, 'manage_project', {'action': 'list'})
    for role in ('active', 'visible'):
        p = (projects.get(role) or {}).get('path')
        check(p and os.path.samefile(p, PROJECT), f'{role} project is not the expected project')
    timeline = tool(c, 'get_timeline', {})
    check(timeline.get('id') == expected_id, f'Active timeline changed: {timeline.get("id")}')
    check((timeline.get('fps'), timeline.get('width'), timeline.get('height'), timeline.get('totalFrames')) == (FPS, WIDTH, HEIGHT, TOTAL), 'Unexpected canvas or duration')
    matching = [x for x in timeline.get('timelines', []) if x.get('timelineId') == expected_id and x.get('active')]
    check(len(matching) == 1, 'Active timeline identity is ambiguous')
    return timeline


def voice(t):
    tracks = [x for x in t.get('tracks', []) if x.get('type') == 'audio']
    check(len(tracks) == 1 and tracks[0].get('name') == 'Voice', 'Expected exactly one Voice audio track')
    clips = tracks[0].get('clips', [])
    check(len(clips) >= 2, 'Expected intro clips and one main Voice clip')
    clips = sorted(clips, key=lambda x: x.get('frames', [-1])[0])
    check(clips[-1].get('mediaRef') == VOICE_REF and clips[-1].get('frames') == [START, TOTAL], 'Main Voice source/range differs')
    check(clips[-1].get('speed', 1) == 1.05, 'Main Voice speed differs from the 1.05x provisional map')
    check(not clips[-1].get('trimStartFrame') and not clips[-1].get('trimEndFrame'), 'Main Voice was trimmed; recalculate the map')
    previous_end = 0
    for clip in clips[:-1]:
        frames = clip.get('frames') or []
        check(len(frames) == 2 and 0 <= frames[0] < frames[1] <= START and frames[0] >= previous_end and clip.get('mediaType') == 'audio' and clip.get('mediaRef'), 'Intro Voice clips overlap or extend outside intro')
        previous_end = frames[1]
    # IDs change on duplication, so compare the remaining audio settings and content.
    return {'clips': [{k: v for k, v in clip.items() if k != 'id'} for clip in clips], 'track': {k: v for k, v in tracks[0].items() if k not in ('clips', 'trackId', 'index', 'label')}}


def check_body_layers(t):
    """Refuse to cover subtitles or layered artwork with the new top video track."""
    active = []
    for track in t['tracks']:
        if track.get('type') != 'video':
            continue
        for group in track.get('captionGroups', []):
            bounds = group.get('frameRange') or []
            check(len(bounds) == 2, 'Caption group has no readable frame range')
            check(bounds[1] <= START or bounds[0] >= TOTAL, 'Body captions would be covered by the new top track')
        body_clips = [clip for clip in track.get('clips', [])
                      if len(clip.get('frames') or []) == 2 and clip['frames'][1] > START and clip['frames'][0] < TOTAL]
        check(all(clip.get('mediaType') != 'text' for clip in body_clips), 'Body text would be covered by the new top track')
        if body_clips:
            active.append(track.get('trackId'))
    check(len(active) == 1, 'Body uses multiple visual tracks or none; top-track replacement needs manual layer review')


def without_ids(value):
    if isinstance(value, dict):
        return {k: without_ids(v) for k, v in value.items() if k not in ('id', 'trackId')}
    if isinstance(value, list):
        return [without_ids(v) for v in value]
    return value


def check_new_track(t, track_id, expected):
    matches = [x for x in t['tracks'] if x.get('trackId') == track_id and x.get('type') == 'video']
    check(len(matches) == 1, 'Target track missing or ambiguous')
    track = matches[0]
    check(track.get('index') == 0, 'Target track is no longer the top video track')
    actual = sorted((x.get('frames', [None,None])[0], x.get('frames', [None,None])[1], x.get('mediaRef')) for x in track.get('clips', []))
    want = sorted((x['startFrame'], x['endFrame'], x['mediaRef']) for x in expected)
    check(actual == want, 'Target track does not match expected clips; stop, do not retry')
    return track


def underlying_tracks(t, target_id=None):
    return [{k: v for k, v in x.items() if k not in ('index', 'label')}
            for x in t['tracks'] if x.get('trackId') != target_id]


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--map', default=str(DEFAULT_MAP), help='Approved CSV map; default is draft')
    ap.add_argument('--source-timeline-id', required=True, help='Exact currently active source timeline ID')
    ap.add_argument('--keyframes', help='Optional JSON keyed by shot, see README')
    ap.add_argument('--voice-manifest', help='Reviewed dry-run JSON whose voice_baseline must match the current source')
    ap.add_argument('--batch-size', type=int, default=10)
    ap.add_argument('--execute', action='store_true', help='Create a copy and import/place media; default is read-only')
    ap.add_argument('--test-first-batch', action='store_true', help='With --execute, stop after verifying the first batch on the new copy')
    args = ap.parse_args()
    check(1 <= args.batch_size <= 20, 'batch-size must be 1–20')
    check(not args.test_first_batch or args.execute, '--test-first-batch requires --execute')
    rows = read_map(Path(args.map)); kf = read_keyframes(args.keyframes, rows)
    hashes = {p: sha256(p) for p in sorted({r['image_path'] for r in rows})}
    provisional = [r['shot'] for r in rows if r['status'] != 'available']
    report = {'mode': 'execute' if args.execute else 'dry-run', 'map': str(Path(args.map).resolve()), 'map_sha256': sha256(args.map), 'shots': len(rows), 'images': len(hashes), 'provisional_shots': provisional, 'review_notes': [{'shot': r['shot'], 'note': r['review']} for r in rows if r['review'].strip()], 'frames': [START,TOTAL], 'intro_preserved': [0,START], 'image_hashes': hashes, 'keyframe_shots': len(kf), 'source_timeline_id': args.source_timeline_id}
    if args.keyframes: report['keyframes_sha256'] = sha256(args.keyframes)
    # Critical: reject provisional inputs before even connecting to Palmier for write mode.
    check(not args.execute or not provisional, 'Execution refused: CSV still contains provisional shots')
    check(not args.execute or args.voice_manifest, 'Execution refused: supply a reviewed dry-run report as --voice-manifest')
    c = PalmierConnection(); c.connect()
    original = state(c, args.source_timeline_id); voice_signature = voice(original)
    check_body_layers(original)
    report['voice_baseline'] = voice_signature
    report['source_track_count'] = len(original['tracks'])
    report['source_video_clips'] = sum(len(x.get('clips', [])) for x in original['tracks'] if x.get('type') == 'video')
    if not args.execute:
        print(json.dumps(report, ensure_ascii=False, indent=2)); return
    approved = json.loads(Path(args.voice_manifest).read_text(encoding='utf-8'))
    for field in ('source_timeline_id', 'map_sha256', 'image_hashes', 'keyframes_sha256', 'voice_baseline'):
        check(approved.get(field) == report.get(field), f'Reviewed dry-run differs: {field}')
    check(approved.get('mode') == 'dry-run', 'Voice manifest must be a reviewed dry-run report')
    runid = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ') + '_' + uuid4().hex[:8]
    log_dir = EDIT / 'palmier_recut_logs' / runid
    log_dir.mkdir(parents=True, exist_ok=False)
    journal = log_dir / 'journal.jsonl'
    def log(kind, data):
        with journal.open('a', encoding='utf-8') as f:
            f.write(json.dumps({'time': datetime.now(timezone.utc).isoformat(), 'kind': kind, 'data': data}, ensure_ascii=False) + '\n'); f.flush(); os.fsync(f.fileno())
    log('preflight', report)
    copy_id = None
    try:
        old_ids = {x['timelineId'] for x in original['timelines']}
        check(state(c, args.source_timeline_id)['tracks'] == original['tracks'], 'Source changed during preflight')
        log('intent', {'operation': 'create_timeline', 'from': args.source_timeline_id})
        receipt = tool(c, 'create_timeline', {'from': args.source_timeline_id, 'name': '002_en_long_dynamic_' + runid})
        log('receipt', {'operation': 'create_timeline', 'result': receipt})
        current = tool(c, 'get_timeline', {})
        copy_id = current.get('id')
        check(copy_id and copy_id not in old_ids, 'Could not identify a new active copy')
        current = state(c, copy_id)
        check(voice(current) == voice_signature, 'Copied voice differs from source')
        check(without_ids(current['tracks']) == without_ids(original['tracks']), 'Copied tracks differ from source; inspect before continuing')
        baseline_tracks = underlying_tracks(current)
        log('copy', {'timeline_id': copy_id})
        selected_rows = rows[:args.batch_size] if args.test_first_batch else rows
        selected_paths = {r['image_path'] for r in selected_rows}
        refs = {}
        for path, digest in hashes.items():
            if path not in selected_paths: continue
            state(c, copy_id); check(sha256(path) == digest, 'Source image changed after preflight')
            request = {'source': {'path': path}, 'folder': FOLDER + '/' + runid}
            log('intent', {'operation': 'import_media', 'args': request, 'sha256': digest})
            receipt = tool(c, 'import_media', request)
            log('receipt', {'operation': 'import_media', 'result': receipt})
            check(receipt.get('status') == 'ready' and receipt.get('mediaRef'), 'Import did not return ready mediaRef')
            refs[path] = receipt['mediaRef']
        library = tool(c, 'get_media', {})
        assets = {a['id']: a for a in library.get('assets', [])}
        check(len(set(refs.values())) == len(refs), 'Imports returned duplicate media IDs')
        for path, ref in refs.items():
            a = assets.get(ref, {})
            check(a.get('type') == 'image' and a.get('folder') == FOLDER + '/' + runid, f'Imported media ID {ref} missing or wrong type/folder')
            check(sha256(path) == hashes[path], f'Image changed: {path}')
        entries = [{'mediaRef': refs[r['image_path']], 'startFrame': r['start_frame'], 'endFrame': r['end_frame_exclusive']} for r in selected_rows]
        inserted = []; target_id = None
        for offset in range(0, len(entries), args.batch_size):
            current = state(c, copy_id); check(voice(current) == voice_signature, 'Voice changed; stop')
            check(underlying_tracks(current, target_id) == baseline_tracks, 'Underlying tracks changed; stop')
            batch = [dict(e) for e in entries[offset:offset+args.batch_size]]
            before = {x['trackId'] for x in current['tracks']}
            if target_id:
                track = check_new_track(current, target_id, inserted)
                for e in batch: e['trackIndex'] = track['index']
            log('intent', {'operation': 'add_clips', 'offset': offset, 'entries': batch})
            receipt = tool(c, 'add_clips', {'entries': batch})
            log('receipt', {'operation': 'add_clips', 'offset': offset, 'result': receipt})
            current = state(c, copy_id); check(voice(current) == voice_signature, 'Voice changed after insertion')
            if not target_id:
                added = [x for x in current['tracks'] if x['trackId'] not in before and x.get('type') == 'video']
                check(len(added) == 1 and added[0]['index'] == 0, 'Expected one new top video track')
                target_id = added[0]['trackId']
            check(underlying_tracks(current, target_id) == baseline_tracks, 'Underlying tracks changed after insertion')
            inserted.extend(batch)
            check_new_track(current, target_id, inserted)
            log('verified_batch', {'offset': offset, 'count': len(batch), 'track_id': target_id})
            if args.test_first_batch:
                log('test_stopped', {'copy_id': copy_id, 'track_id': target_id, 'shots': len(inserted), 'complete': False})
                print(json.dumps({'copy_id': copy_id, 'track_id': target_id, 'shots': len(inserted), 'log': str(log_dir), 'complete': False, 'review_required': True}, ensure_ascii=False))
                return
        # The returned clips are identified by exact nonoverlapping frame ranges and media IDs.
        current = state(c, copy_id); track = check_new_track(current, target_id, inserted)
        clips = {(x['frames'][0], x['frames'][1], x['mediaRef']): x['id'] for x in track['clips']}
        for row in rows:
            shot = row['shot']
            if shot not in kf: continue
            clip_id = clips[(row['start_frame'], row['end_frame_exclusive'], refs[row['image_path']])]
            for prop, points in kf[shot].items():
                current = state(c, copy_id); check(voice(current) == voice_signature, 'Voice changed before keyframes')
                check(underlying_tracks(current, target_id) == baseline_tracks, 'Underlying tracks changed before keyframes')
                check_new_track(current, target_id, inserted)
                params = {'clipId': clip_id, 'property': prop, 'keyframes': points}
                log('intent', {'operation': 'set_keyframes', 'shot': shot, 'args': params})
                receipt = tool(c, 'set_keyframes', params)
                log('receipt', {'operation': 'set_keyframes', 'shot': shot, 'result': receipt})
                updated = state(c, copy_id)
                check(voice(updated) == voice_signature, 'Voice changed after keyframes')
                check(underlying_tracks(updated, target_id) == baseline_tracks, 'Underlying tracks changed after keyframes')
                after = check_new_track(updated, target_id, inserted)
                clip = next(x for x in after['clips'] if x['id'] == clip_id)
                actual = (clip.get('keyframes') or {}).get(prop)
                check(keyframes_match(actual, points), f'shot {shot}: cannot verify {prop} keyframes; inspect before continuing')
        current = state(c, copy_id); check(voice(current) == voice_signature, 'Voice changed at final check')
        check(underlying_tracks(current, target_id) == baseline_tracks, 'Underlying tracks changed at final check')
        check_new_track(current, target_id, inserted)
        check(all(sha256(path) == digest for path, digest in hashes.items()), 'Source images changed during the run')
        (log_dir / 'final_timeline.json').write_text(json.dumps(current, ensure_ascii=False, indent=2), encoding='utf-8')
        log('complete', {'copy_id': copy_id, 'target_track_id': target_id, 'shots': len(inserted), 'review_required': True})
        print(json.dumps({'copy_id': copy_id, 'track_id': target_id, 'shots': len(inserted), 'log': str(log_dir), 'review_required': True}, ensure_ascii=False))
    except Exception as exc:
        log('stopped', {'error': str(exc), 'copy_id': copy_id, 'note': 'Do not retry blindly. Inspect active timeline and journal.'})
        raise


if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        print(f'STOP: {exc}', file=sys.stderr); sys.exit(1)
