from pathlib import Path
import hashlib, importlib.util, json, urllib.request, urllib.error
root=Path('/Users/diplomat/ytvideos'); ep=root/'channels/nuviko_history/videos/039_brest_fortress'; out=ep/'Source/SFX/rebuild_20261107'
spec=importlib.util.spec_from_file_location('tts',root/'automation/elevenlabs/tts.py');tts=importlib.util.module_from_spec(spec);spec.loader.exec_module(tts)
key=tts.get_api_key()
if not key: raise SystemExit('ElevenLabs credential unavailable; no requests sent')
jobs=[('paper','A single close, delicate handling of a thick archival paper folder, quiet paper rustle and soft tap on a wooden table. Natural dry foley. No voices, no music, no dramatic whoosh.',2),('distant_artillery','Distant low muffled artillery report followed by a soft rolling reverberation, restrained and realistic, heard from far away. One isolated impact, no voices, no music, no high-frequency crack.',5),('water','Quiet realistic nighttime river water gently lapping against a stone bank. Subtle small ripples, no voices, no birds, no music.',8),('rubble','One quiet fall of loose brick dust and small masonry fragments in an empty interior, restrained dry stone debris, no voices, no music, no gunfire.',4)]
for name,prompt,duration in jobs:
 dest=out/(name+'.mp3'); request=out/(name+'_request.json')
 if dest.exists(): print(name,'EXISTS; not repeated');continue
 body={'text':prompt,'duration_seconds':duration,'prompt_influence':0.4}; request.write_text(json.dumps(body,indent=2)+'\n')
 req=urllib.request.Request('https://api.elevenlabs.io/v1/sound-generation',data=json.dumps(body).encode(),headers={'xi-api-key':key,'Content-Type':'application/json','Accept':'audio/mpeg'},method='POST')
 try:
  with urllib.request.urlopen(req,timeout=90) as response:data=response.read()
  tts.save_new(dest,data);print(name,'saved',len(data),'bytes sha256',hashlib.sha256(data).hexdigest(),flush=True)
 except (urllib.error.URLError,TimeoutError) as ex:
  print(name,'request outcome failed or unknown:',type(ex).__name__,'do not retry blindly',flush=True);break
