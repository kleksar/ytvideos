import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, '/Users/diplomat/ytvideos')
from automation.image_motion.run import Palmier, fingerprint

HERE = ROOT / 'Edit/v13'
run_dir = Path(json.loads((HERE / 'TARGET_RUN.json').read_text())['run'])
run = json.loads((run_dir / 'run.json').read_text())
assert run['status'] == 'complete' and len(run['scenes']) == 39
c = Palmier(HERE)
ids = {'projectId': 'B1BA2D18', 'timelineId': run['target_timeline_id']}
timeline = c.call('get_timeline', ids)
assert fingerprint(timeline) == json.loads((HERE / 'POST_EDIT.json').read_text())['result_fingerprint']
assert timeline['totalFrames'] == 5700
assert [(t['name'], len(t['clips'])) for t in timeline['tracks']] == [('Accents', 33), ('Scenes', 39), ('Mix', 1)]
(HERE / 'timeline_final.json').write_text(json.dumps(timeline, indent=2) + '\n')
job_path = HERE / 'export_job.json'
assert not job_path.exists(), 'Export request already recorded; inspect it instead of resubmitting'
job = c.call('export_project', {**ids, 'mode': 'video', 'codec': 'H.264',
             'resolution': '1080p', 'outputPath': str(HERE / 'Palmier_export.mp4'), 'overwrite': False}, True)
job_path.write_text(json.dumps(job, indent=2) + '\n')
print(json.dumps(job), flush=True)
job_id = job['jobId']
last = None
for _ in range(600):
    result = c.call('manage_exports', {'projectId': 'B1BA2D18', 'action': 'list'})
    status = next(x for x in result['exports'] if x['jobId'] == job_id)
    (HERE / 'export_status.json').write_text(json.dumps(status, indent=2) + '\n')
    current = (status['status'], round(status.get('progress', 0), 2))
    if current != last:
        print(json.dumps({'status': current[0], 'progress': current[1]}), flush=True)
        last = current
    if status['status'] == 'completed':
        break
    if status['status'] in ['failed', 'cancelled', 'error']:
        raise RuntimeError(status)
    time.sleep(3)
else:
    raise RuntimeError('Export remains pending; inspect recorded job before retrying')
