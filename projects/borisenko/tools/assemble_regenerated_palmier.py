#!/usr/bin/env python3
"""Place regenerated speech on a duplicate Palmier timeline.

Default is a read-only dry run. --execute creates a timeline copy and imports
local media through Palmier's public MCP operations; it does not export media.
If any action fails or its result is unknown, the exclusive receipt records the
phase. Do not repeat the command blindly: first inspect the project and receipt.
"""
import argparse
import hashlib
import json
import math
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'automation/palmier'))
from inspect_connection import PalmierConnection

PROJECT = '/Users/diplomat/Documents/Palmier Pro/Borisenko English Pilot 001.palmier'
TIMELINE = 'B791704C'
MEDIA_ROOT = ROOT / 'projects/borisenko/pilot_001/Source/Voice'


def tool(c, name, args):
    response = c.request('tools/call', {'name': name, 'arguments': args})
    if response.get('isError'):
        raise RuntimeError(f'{name}: {response.get("content")}')
    texts = [x['text'] for x in response.get('content', []) if x.get('type') == 'text']
    if len(texts) != 1:
        raise RuntimeError(f'{name}: unexpected response; inspect project before retry')
    return json.loads(texts[0])


def project_guard(c, path, timeline):
    project = tool(c, 'manage_project', {'action': 'list'})
    for key in ('active', 'visible'):
        if not project.get(key) or Path(project[key]['path']).resolve() != path.resolve():
            raise RuntimeError(f'Wrong {key} project; refusing to mutate.')
    state = tool(c, 'get_timeline', {})
    if state['id'] != timeline:
        raise RuntimeError(f'Active timeline is {state["id"]}, expected {timeline}; refusing.')
    return state


def media_info(path):
    result = subprocess.run(
        ['ffprobe', '-v', 'error', '-show_entries',
         'format=duration:stream=codec_name,channels,sample_rate', '-of', 'json', str(path)],
        capture_output=True, text=True, timeout=30, check=True)
    parsed = json.loads(result.stdout)
    streams = parsed.get('streams', [])
    if len(streams) != 1 or not str(streams[0].get('codec_name', '')).startswith('pcm_'):
        raise RuntimeError(f'Expected a single PCM WAV audio stream: {path}')
    seconds = float(parsed['format']['duration'])
    if not math.isfinite(seconds) or seconds <= 0:
        raise RuntimeError(f'Invalid duration: {path}')
    return {'duration': seconds, 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}


def validate(plan, media_root, expected_count):
    clips = plan.get('clips')
    if (not isinstance(clips, list) or len(clips) != expected_count or plan.get('fps') != 30
            or plan.get('tempo') != 0.95 or plan.get('videoEndFrame') != 16093):
        raise RuntimeError('Unexpected plan clip count, frame rate, tempo, or original video length.')
    if plan.get('overrunFrames', 0) > 0:
        raise RuntimeError('Plan extends beyond the original video; resolve that conflict first.')
    ids = set()
    records = []
    previous_end = -1
    for clip in clips:
        ident, start, end = clip['id'], clip['startFrame'], clip['conservativeEndFrame']
        if not isinstance(ident, str) or not ident or ident in ids:
            raise RuntimeError('Missing or duplicated phrase ID.')
        ids.add(ident)
        if not isinstance(start, int) or not isinstance(end, int) or start < 0 or end <= start:
            raise RuntimeError(f'{ident}: invalid frame interval.')
        if start < previous_end:
            raise RuntimeError(f'{ident}: conservative frame intervals overlap.')
        if end > plan['videoEndFrame']:
            raise RuntimeError(f'{ident}: conservative duration extends beyond video.')
        path = Path(clip['path'])
        if not path.is_absolute() or not path.is_file() or path.suffix.lower() != '.wav':
            raise RuntimeError(f'{ident}: expected an existing absolute WAV path.')
        try:
            path.resolve().relative_to(media_root.resolve())
        except ValueError:
            raise RuntimeError(f'{ident}: WAV is not in the permanent voice source folder.') from None
        info = media_info(path)
        predicted = float(clip['durationSeconds'])
        if not math.isfinite(predicted) or abs(info['duration'] - predicted) > 0.04:
            raise RuntimeError(f'{ident}: WAV duration differs from placement plan.')
        if end - start < math.ceil(info['duration'] * 30 - 1e-6):
            raise RuntimeError(f'{ident}: insufficient allocated frames for the complete phrase.')
        previous_end = end
        records.append({'id': ident, 'text': clip['text'], 'path': str(path),
                        'startFrame': start, 'conservativeEndFrame': end, **info})
    return records


def save(receipt_path, data):
    # This file exists exclusively for this run; fsync after each operation so an
    # interrupted MCP call leaves an explicit phase requiring manual recovery.
    payload = (json.dumps(data, ensure_ascii=False, indent=2) + '\n').encode()
    temp = receipt_path.with_name(receipt_path.name + '.tmp')
    with temp.open('wb') as f:
        f.write(payload)
        f.flush()
        os.fsync(f.fileno())
    os.replace(temp, receipt_path)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--plan', required=True, type=Path, help='Placement JSON from the alignment tool.')
    p.add_argument('--receipt', required=True, type=Path, help='New recovery receipt path; must not exist.')
    p.add_argument('--name', default='EN regenerated phrases 095', help='Unique name of the timeline copy.')
    p.add_argument('--project', default=PROJECT, type=Path)
    p.add_argument('--source-timeline-id', default=TIMELINE)
    p.add_argument('--expected-count', default=108, type=int)
    p.add_argument('--execute', action='store_true', help='Create the copy and import/insert the WAVs.')
    a = p.parse_args()
    if a.receipt.exists() or a.receipt.with_name(a.receipt.name + '.tmp').exists():
        raise RuntimeError('Receipt already exists: inspect it and the project, do not repeat blindly.')
    if not a.name.strip() or a.expected_count <= 0:
        raise RuntimeError('Timeline name and positive expected count are required.')
    raw = a.plan.read_bytes()
    plan = json.loads(raw)
    records = validate(plan, MEDIA_ROOT, a.expected_count)
    c = PalmierConnection()
    c.connect()
    state = project_guard(c, a.project, a.source_timeline_id)
    if state['fps'] != 30 or state['totalFrames'] != 16093:
        raise RuntimeError('The source timeline frame rate or video duration has changed.')
    video = [z for track in state['tracks'] for z in track.get('clips', []) if z.get('mediaRef') == '404792DB']
    english = [z for z in state['tracks'] if z.get('name') == 'English095']
    if (len(video) != 1 or video[0].get('trimStartFrame') != 374 or
            video[0].get('audio', {}).get('volumeDb') != -28 or len(english) != 1):
        raise RuntimeError('Original video/trim, Russian level, or existing English track changed.')
    inventory = tool(c, 'get_media', {})
    if any(item.get('name') == a.name for item in inventory.get('timelines', [])):
        raise RuntimeError('Timeline name already exists; inspect before choosing a new run.')
    print(f'Validated {len(records)} complete WAV phrases, non-overlapping plan, and source timeline.', flush=True)
    if not a.execute:
        print('Dry run: no project or filesystem mutation.', flush=True)
        return
    a.receipt.parent.mkdir(parents=True, exist_ok=True)
    with a.receipt.open('x', encoding='utf-8') as f:
        json.dump({'phase': 'reserved', 'plan': str(a.plan.resolve())}, f)
        f.flush()
        os.fsync(f.fileno())
    receipt = {'phase': 'reserved', 'project': str(a.project), 'sourceTimeline': a.source_timeline_id,
               'newTimelineName': a.name, 'plan': str(a.plan.resolve()),
               'planSha256': hashlib.sha256(raw).hexdigest(), 'clips': records, 'imported': []}
    save(a.receipt, receipt)
    receipt['phase'] = 'creating_timeline_outcome_unknown'
    save(a.receipt, receipt)
    created = tool(c, 'create_timeline', {'name': a.name, 'from': a.source_timeline_id})
    new_id = created['timelineId']
    receipt.update({'phase': 'copy_created', 'newTimelineId': new_id})
    save(a.receipt, receipt)
    copied = project_guard(c, a.project, new_id)
    original_track = [x for x in copied['tracks'] if x.get('name') == 'English095']
    if len(original_track) != 1:
        raise RuntimeError('Copied English track was not found; inspect new timeline and receipt.')
    receipt['phase'] = 'muting_original_outcome_unknown'
    save(a.receipt, receipt)
    tool(c, 'manage_tracks', {'set': [{'trackId': original_track[0]['trackId'], 'muted': True}]})
    receipt['phase'] = 'importing'
    save(a.receipt, receipt)
    for i, record in enumerate(records):
        if i % 10 == 0:
            project_guard(c, a.project, new_id)
        if media_info(Path(record['path']))['sha256'] != record['sha256']:
            raise RuntimeError(f'{record["id"]}: WAV changed since validation; stop.')
        receipt['pendingImport'] = record['id']
        save(a.receipt, receipt)
        imported = tool(c, 'import_media', {'source': {'path': record['path']},
                                          'folder': 'Borisenko Regenerated v1', 'name': record['id']})
        if imported.get('status') != 'ready' or imported.get('type') != 'audio':
            raise RuntimeError(f'{record["id"]}: import is not ready; inspect receipt and project.')
        receipt['imported'].append({'id': record['id'], 'mediaRef': imported['mediaRef']})
        receipt.pop('pendingImport', None)
        save(a.receipt, receipt)
        print(f'Imported {i + 1}/{len(records)}: {record["id"]}', flush=True)
    checked = project_guard(c, a.project, new_id)
    current_original_track = next((x for x in checked['tracks'] if x.get('name') == 'English095'), None)
    if not current_original_track or not current_original_track.get('muted'):
        raise RuntimeError('The old English track is not muted; inspect before placement.')
    refs = [item['mediaRef'] for item in receipt['imported']]
    if len(set(refs)) != len(records):
        raise RuntimeError('Imported media refs are not unique; inspect the project and receipt.')
    inventory = tool(c, 'get_media', {'ids': refs})
    assets = {z['id']: z for z in inventory.get('assets', [])}
    for record, ref in zip(records, refs):
        asset = assets.get(ref)
        if not asset or asset.get('generationStatus') or asset.get('type') != 'audio' or abs(float(asset['durationSeconds']) - record['duration']) > 0.05:
            raise RuntimeError(f'{record["id"]}: imported media verification failed.')
    entries = [{'mediaRef': ref, 'startFrame': record['startFrame']} for record, ref in zip(records, refs)]
    receipt['phase'] = 'adding_clips_outcome_unknown'
    save(a.receipt, receipt)
    added = tool(c, 'add_clips', {'entries': entries})
    receipt['phase'] = 'clips_added'
    receipt['added'] = added
    save(a.receipt, receipt)
    state = project_guard(c, a.project, new_id)
    tracks = [x for x in state['tracks'] if {z.get('mediaRef') for z in x.get('clips', [])} == set(refs)]
    if len(tracks) != 1:
        raise RuntimeError('Could not identify full regenerated track; inspect timeline before retry.')
    track = tracks[0]
    found = {z['mediaRef']: z for z in track['clips']}
    if len(track['clips']) != len(records):
        raise RuntimeError('Incorrect number of added clips; inspect before retry.')
    for record, ref in zip(records, refs):
        clip = found[ref]
        expected_frames = round(record['duration'] * 30)
        if (clip['frames'][0] != record['startFrame'] or clip.get('trimStartFrame', 0) or
                clip.get('trimEndFrame', 0) or abs((clip['frames'][1] - clip['frames'][0]) - expected_frames) > 1):
            raise RuntimeError(f'{record["id"]}: clip differs from full source; inspect before retry.')
    if any(x['frames'][1] > y['frames'][0] for x, y in zip(track['clips'], track['clips'][1:])):
        raise RuntimeError('Clip intervals overlap; inspect before retry.')
    receipt['phase'] = 'naming_track_outcome_unknown'
    save(a.receipt, receipt)
    tool(c, 'manage_tracks', {'set': [{'trackId': track['trackId'], 'name': 'EnglishRegen'}]})
    final = project_guard(c, a.project, new_id)
    receipt.update({'phase': 'complete', 'newTrackId': track['trackId'],
                    'clipCount': len(records), 'timelineDuration': final['durationSeconds']})
    save(a.receipt, receipt)
    print(f'Complete: {len(records)} phrases on timeline {new_id}. Receipt: {a.receipt}', flush=True)


if __name__ == '__main__':
    try:
        main()
    except (RuntimeError, OSError, ValueError, KeyError, subprocess.SubprocessError) as exc:
        print(f'Error: {exc}. Inspect any existing receipt/project before retry.', file=sys.stderr)
        sys.exit(1)
