import time,json,sys,subprocess
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from palmier_client import call
E=Path('/Users/diplomat/ytvideos/channels/paper_detour/videos/032_galveston_1900');D=E/'Edit/Export/full_v04';J='DBEDD6B8-56E7-4984-8495-407E1C16B0D1'
while True:
 r=call('manage_exports',{'projectId':'25533909','action':'list'},'full_v04_wait_export')
 x=next(x for x in r['exports'] if x['jobId']==J)
 print(json.dumps(x),flush=True)
 if x['status']=='completed':break
 if x['status'] not in ('queued','rendering','started'):raise RuntimeError(x)
 time.sleep(30)
(D/'native_job_completed.json').write_text(json.dumps(x,indent=2))
for name in ['finalize_candidate_v04.py','prepare_final_qa_v04.py']:
 subprocess.run(['python3',str(Path(__file__).resolve().parent/name)],check=True)
print('CANDIDATE_AND_QA_PLAN_READY',flush=True)
