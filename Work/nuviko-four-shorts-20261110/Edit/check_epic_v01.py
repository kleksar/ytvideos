import hashlib,json,subprocess
from pathlib import Path
root=Path('/Users/diplomat/ytvideos/Work/nuviko-four-shorts-20261110')
mp4=root/'Deliverables/Epic-Inspiration-review-v01.mp4'
receipt=root/'Edit/epic-v01-qa.json'
if receipt.exists(): raise SystemExit('QA receipt exists')
sha=hashlib.sha256(mp4.read_bytes()).hexdigest()
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-show_streams','-show_format','-of','json',str(mp4)]))
subprocess.run(['ffmpeg','-nostdin','-v','error','-xerror','-i',str(mp4),'-map','0:v:0','-map','0:a:0','-f','null','-'],check=True)
subprocess.run(['python3','automation/music_beats.py',str(mp4),'--fps','30','--cut-map',str(root/'Edit/epic-v01-cut-map.json'),'--output',str(root/'Edit/epic-v01-final-beats.json')],check=True)
qa={'sha256':sha,'file':str(mp4),'full_decode':'PASS','ffprobe':probe,'frame_sampling':'PENDING','continuous_playback':'UNVERIFIED','audio_listening':'UNVERIFIED','independent_review':'UNVERIFIED','content_acceptance':'PENDING','music_release_rights':'UNVERIFIED'}
receipt.write_text(json.dumps(qa,ensure_ascii=False,indent=2)+'\n')
print('SHA256',sha)
