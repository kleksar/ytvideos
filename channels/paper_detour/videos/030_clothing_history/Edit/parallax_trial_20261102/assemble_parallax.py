"""Insert the verified scene videos into the isolated Palmier timeline."""
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PROJECT = "B1BA2D18"
TIMELINE = "58E4A048"
CLIENT = Path('/Users/diplomat/ytvideos/automation/palmier/inspect_connection.py')
spec = importlib.util.spec_from_file_location('palmier_read', CLIENT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
conn = module.PalmierConnection()
conn.connect()


def call(name, args):
    response = conn.request('tools/call', {'name': name, 'arguments': args})
    with (ROOT / 'assembly_receipts.jsonl').open('a') as out:
        out.write(json.dumps({'name': name, 'arguments': args, 'response': response}, ensure_ascii=False) + '\n')
    if response.get('isError'):
        raise RuntimeError(f'{name}: {response}')
    return json.loads(response['content'][0]['text'])


def timeline():
    return conn.read_tool('get_timeline', {'projectId': PROJECT, 'timelineId': TIMELINE})


def scenes(state):
    tracks = [t for t in state['tracks'] if t['name'] == 'Scenes']
    if len(tracks) != 1:
        raise ValueError('Scenes track is not unique')
    return tracks[0]


before = json.loads((ROOT / 'timeline_before.json').read_text())
pilot = json.loads((ROOT / 'timeline_pilot.json').read_text())
current = timeline()
if {k: v for k, v in current.items() if k != 'timelines'} != {k: v for k, v in pilot.items() if k != 'timelines'}:
    raise RuntimeError('Timeline changed since pilot; inspect before continuing')
old = scenes(before)['clips']
cur = scenes(current)
assert len(old) == len(cur['clips']) == 39
assert cur['index'] == 2
for i, (original, actual) in enumerate(zip(old, cur['clips'])):
    assert original['frames'] == actual['frames']
    if i:
        assert original['mediaRef'] == actual['mediaRef']
    assert original.get('keyframes', {}) == actual.get('keyframes', {})

entries = []
missing = [str(ROOT / 'scene_01.mp4')] if not (ROOT / 'scene_01.mp4').is_file() else []
missing += [str(ROOT / f'padded_{i:02}.mp4') for i in range(2, 40)
            if not (ROOT / f'padded_{i:02}.mp4').is_file()]
if missing:
    raise FileNotFoundError(f'One or more rendered clips are missing: {missing}')
for i, clip in enumerate(old[1:], 2):
    path = ROOT / f'padded_{i:02}.mp4'
    if not path.is_file():
        raise FileNotFoundError(path)
    imported = call('import_media', {'projectId': PROJECT, 'source': {'path': str(path)},
                                   'folder': 'Parallax trial'})
    entries.append({'mediaRef': imported['mediaRef'], 'startFrame': clip['frames'][0],
                    'endFrame': clip['frames'][1], 'trackIndex': cur['index'],
                    'includeAudio': False})

call('add_clips', {'projectId': PROJECT, 'timelineId': TIMELINE, 'entries': entries})
state = timeline()
new = scenes(state)['clips']
if len(new) != 39:
    raise RuntimeError('Unexpected scene count after insertion')
for original, inserted, entry in zip(old[1:], new[1:], entries):
    if inserted['frames'] != original['frames'] or inserted['mediaRef'] != entry['mediaRef']:
        raise RuntimeError('Unexpected inserted clip; inspect before continuing')
    for prop, keys in original.get('keyframes', {}).items():
        call('set_keyframes', {'projectId': PROJECT, 'timelineId': TIMELINE,
                               'clipId': inserted['id'], 'property': prop, 'keyframes': keys})

state = timeline()
final = scenes(state)['clips']
for original, inserted in zip(old, final):
    if inserted['frames'] != original['frames'] or inserted.get('keyframes', {}) != original.get('keyframes', {}):
        raise RuntimeError('Scene timing or keyframes do not match original')
for name in ('Accents', 'Grain', 'Mix'):
    a = next(t for t in before['tracks'] if t['name'] == name)
    b = next(t for t in state['tracks'] if t['name'] == name)
    if a != b:
        raise RuntimeError(f'Unintended change to {name}')
(ROOT / 'timeline_after.json').write_text(json.dumps(state, ensure_ascii=False, indent=2))
snapshot = call('manage_snapshots', {'projectId': PROJECT, 'timelineId': TIMELINE,
                                     'action': 'save', 'name': 'Parallax trial with original camera keys'})
print(json.dumps({'sceneCount': len(final), 'totalFrames': state['totalFrames'],
                  'snapshot': snapshot}, ensure_ascii=False))
