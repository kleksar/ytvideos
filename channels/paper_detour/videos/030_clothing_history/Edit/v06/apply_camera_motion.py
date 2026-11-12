import json
from client_v06 import ROOT, call

target = json.loads((ROOT / 'Edit/v06/target.json').read_text())
ids = {'projectId': target['projectId'], 'timelineId': target['created']['timelineId']}
timeline = call('get_timeline', ids)
shots = json.loads((ROOT / 'Storyboard/SHOTLIST_v05.json').read_text())
scene_track = next(t for t in timeline['tracks'] if t['name'] == 'Scenes')
assert len(scene_track['clips']) == len(shots) == 39
pan = {2, 5, 10, 12, 15, 31, 33, 38}
pull = {4, 13, 16, 18, 22, 23, 27, 29, 32, 39}
human = set(range(13, 15)) | set(range(16, 31)) | {32, 34}
plan = []
for index, (shot, clip) in enumerate(zip(shots, scene_track['clips']), 1):
    assert clip['frames'] == [shot['startFrame'], shot['endFrame']]
    d = shot['endFrame'] - shot['startFrame']
    if index in pan:
        scale = 1.065
        start, end = ((-0.004, -0.0325), (-0.061, -0.0325))
        if index % 2:
            start, end = end, start
        scale_keys = [[0, scale, scale, 'linear'], [d - 1, scale, scale]]
        pos_keys = [[0, *start, 'linear'], [d - 1, *end]]
        kind = 'lateral camera drift'
    else:
        z = 1.055 if index in human else 1.09
        a, b = (z, 1.0) if index in pull else (1.0, z)
        focus = [0.5, 0.53]
        scale_keys = [[0, a, a, 'linear'], [d - 1, b, b]]
        pos_keys = [[0, (1-a)*focus[0], (1-a)*focus[1], 'linear'],
                    [d-1, (1-b)*focus[0], (1-b)*focus[1]]]
        kind = 'camera pull-out' if index in pull else 'camera push-in'
    for row in pos_keys:
        s = scale_keys[0 if row[0] == 0 else 1][1]
        assert 1-s-0.00001 <= row[1] <= 0.00001
        assert 1-s-0.00001 <= row[2] <= 0.00001
    call('set_keyframes', {**ids, 'clipId': clip['id'], 'property': 'scale', 'keyframes': scale_keys})
    call('set_keyframes', {**ids, 'clipId': clip['id'], 'property': 'position', 'keyframes': pos_keys})
    plan.append({**shot, 'clipId': clip['id'], 'camera_motion': kind,
                 'scale_keys': scale_keys, 'position_keys': pos_keys,
                 'scope': 'Explicit user direction for030; full-image camera transform, not a channel standard change.'})
(ROOT / 'Storyboard/SHOTLIST_v06.json').write_text(json.dumps(plan, ensure_ascii=False, indent=2) + '\n')
final = call('get_timeline', ids)
(ROOT / 'Edit/v06/timeline_camera.json').write_text(json.dumps(final, indent=2))
for clip in next(t for t in final['tracks'] if t['name'] == 'Scenes')['clips']:
    assert len(clip['keyframes']['scale']) == len(clip['keyframes']['position']) == 2
print('39 complete-scene camera moves applied and read back; no timing/audio changes.')
