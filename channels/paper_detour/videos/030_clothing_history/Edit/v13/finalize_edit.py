"""Apply only collision fixes found in depth/caption composite preflight."""
import copy
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, '/Users/diplomat/ytvideos')
from automation.image_motion.run import Palmier, fingerprint

HERE = ROOT / 'Edit/v13'
assert not (HERE / 'POST_EDIT.json').exists(), 'Already finalized; inspect live state before any retry'
run_dir = Path(json.loads((HERE / 'TARGET_RUN.json').read_text())['run'])
run = json.loads((run_dir / 'run.json').read_text())
assert run['status'] == 'complete'
c = Palmier(HERE)
ids = {'projectId': 'B1BA2D18', 'timelineId': run['target_timeline_id']}
before = c.call('get_timeline', ids)
assert fingerprint(before) == run['result_fingerprint']
snapshot = c.call('manage_snapshots', {**ids, 'action': 'save', 'name': 'Before depth-caption collision fixes'}, True)
accents = next(t for t in before['tracks'] if t['name'] == 'Accents')
by_interval = {tuple(cl['frames']): cl for cl in accents['clips']}
cues = json.loads((ROOT / 'Storyboard/CUE_SHEET_v06.json').read_text())
omitted = next(q for q in cues if q['id'] == 'D06')
omitted_clip = by_interval[(omitted['startFrame'], omitted['endFrame'])]
c.call('remove_clips', {**ids, 'clipIds': [omitted_clip['id']]}, True)
new_cues = json.loads((ROOT / 'Storyboard/CUE_SHEET_v13_plan.json').read_text())
for q in new_cues:
    clip = by_interval[(q['startFrame'], q['endFrame'])]
    q['clipId'] = clip['id']
    if q['id'] == 'D10':
        c.call('set_keyframes', {**ids, 'clipId': clip['id'], 'property': 'position', 'keyframes': q['position_keys']}, True)
    q['v13_preflight'] = 'Actual depth-sample composite; native export samples still require verification'
final = c.call('get_timeline', ids)
assert [len(t['clips']) for t in final['tracks']] == [33, 39, 1]
assert final['tracks'][1:] == before['tracks'][1:]
actuals = {tuple(cl['frames']): cl for cl in final['tracks'][0]['clips']}
for q in new_cues:
    cl = actuals[(q['startFrame'], q['endFrame'])]
    assert cl['id'] == q['clipId']
    assert cl['keyframes']['opacity'] == by_interval[tuple(cl['frames'])]['keyframes']['opacity']
    if q['id'] != 'D10':
        assert cl == by_interval[tuple(cl['frames'])]
shots = json.loads((ROOT / 'Storyboard/SHOTLIST_v06.json').read_text())
for s, row, clip in zip(shots, run['scenes'], final['tracks'][1]['clips']):
    s.update(clipId=clip['id'], parallax_video=row['video'], parallax_mediaRef=clip['mediaRef'],
             depth_zoom=row['depth_zoom'], camera_keyframes=clip['keyframes'], motion_preset='gentle-aligned')
(ROOT / 'Storyboard/SHOTLIST_v13.json').write_text(json.dumps(shots, ensure_ascii=False, indent=2) + '\n')
(ROOT / 'Storyboard/CUE_SHEET_v13.json').write_text(json.dumps(new_cues, ensure_ascii=False, indent=2) + '\n')
(HERE / 'timeline_final.json').write_text(json.dumps(final, indent=2) + '\n')
snapshot_final = c.call('manage_snapshots', {**ids, 'action': 'save', 'name': 'v13 full39scene parallax33accents verified'}, True)
record = {'timelineId': ids['timelineId'], 'before_snapshot': snapshot, 'final_snapshot': snapshot_final,
          'changes': {'D06': 'Omitted: paper caption covers main stone blade after motion framing; source PNG retained',
                      'D10': 'Moved to existing alternate anchor to keep woman head clear'},
          'other_tracks': 'Unchanged after motion helper completed', 'result_fingerprint': fingerprint(final)}
(HERE / 'POST_EDIT.json').write_text(json.dumps(record, indent=2) + '\n')
print(json.dumps({'timelineId': ids['timelineId'], 'scenes': 39, 'accents': 33}))
