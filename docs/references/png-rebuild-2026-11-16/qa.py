import json,subprocess,pathlib,hashlib
R=pathlib.Path(__file__).resolve().parent;B=R.parent
out={}
for name,old,n in [('MIND_READING','mind-sound-v2/MIND_READING_FINAL_SOUND_V2_1080p30.mp4',6252),('EVERYONE_WANTS_YOU','desire-sound-v9/EVERYONE_WANTS_YOU_SOUND_V9_1080p30.mp4',6198)]:
 p=R/(name+'_UPLOAD_READY_1080p30.mp4');v=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(p)]));s=v['streams'][0]
 assert(s['width'],s['height'],s['r_frame_rate'],int(s['nb_frames']))==(1920,1080,'30/1',n)
 hashes=[]
 for f in [p,B/old]:
  hashes.append(subprocess.check_output(['ffmpeg','-v','error','-i',str(f),'-map','0:a:0','-c','copy','-f','hash','-hash','sha256','-']).decode().strip())
 assert hashes[0]==hashes[1],hashes
 subprocess.run(['ffmpeg','-v','error','-i',str(p),'-f','null','-'],check=True,stderr=open(R/(name+'-decode.log'),'w'))
 out[name]={'bytes':p.stat().st_size,'sha256':hashlib.file_digest(open(p,'rb'),'sha256').hexdigest(),'probe':v,'audio_identical_to_approved_master':True,'audio_sha256':hashes[0]}
(R/'QA.json').write_text(json.dumps(out,indent=2));print(json.dumps({k:{x:y for x,y in v.items() if x!='probe'} for k,v in out.items()},indent=2))
