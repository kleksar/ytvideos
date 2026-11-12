import json
import time
from client_v06 import ROOT, call

ids={'projectId':'B1BA2D18','timelineId':'A7C273C5'}
t=call('get_timeline',ids)
assert t['totalFrames']==5700
assert [len(next(x for x in t['tracks'] if x['name']==name)['clips']) for name in ['Accents','Grain','Scenes','Mix']]==[34,1,39,1]
staging=json.loads((ROOT/'Edit/v06/RAM_STAGING.json').read_text())
job=call('export_project',{**ids,'mode':'video','codec':'H.264','resolution':'1080p','outputPath':staging['path']+'/Palmier_v06.mp4','overwrite':False})
(ROOT/'Edit/v06/export_job.json').write_text(json.dumps(job,indent=2))
print(json.dumps(job),flush=True)
job_id=job.get('jobId')
assert job_id,job
for _ in range(600):
    status=call('manage_exports',{'projectId':ids['projectId'],'action':'list'})
    (ROOT/'Edit/v06/export_status.json').write_text(json.dumps(status,indent=2))
    match=next(x for x in status['exports'] if x['jobId']==job_id)
    print(match['status'],match.get('progress'),flush=True)
    if match['status']=='completed':break
    if match['status'] in ['failed','cancelled','error']:raise RuntimeError(match)
    time.sleep(3)
else:raise RuntimeError('export polling timeout; inspect native job before retry')
