from pathlib import Path
import importlib.util,json,urllib.request,concurrent.futures
root=Path('/Users/diplomat/ytvideos')
spec=importlib.util.spec_from_file_location('tts',root/'automation/elevenlabs/tts.py');tts=importlib.util.module_from_spec(spec);spec.loader.exec_module(tts);key=tts.get_api_key()
out=root/'channels/paper_detour/videos/030_clothing_history/Source/SFX/v05'
jobs=[('stone','A single dry flint stone tapping and chipping another stone, two delicate small clicks and a short gritty scrape. Close foley, dry natural sound, no voice, no music, no reverb.',2),('fiber','Gentle close foley of a hand brushing a dry woven grass sandal, soft braided plant fibers creaking and rubbing once. Quiet delicate natural texture, no voice, no music.',2),('cloth','One soft swish of a large fabric skirt and a delicate cloth rustle. Understated close foley, no footsteps, no voices, no music.',2),('river','Soft calm river lapping against a stone bank, gentle natural flowing water. No birds, no wind, no music, no voices.',8)]
def run(job):
 name,prompt,dur=job;dest=out/(name+'.mp3')
 if dest.exists():return name+' exists'
 body={'text':prompt,'duration_seconds':dur,'prompt_influence':0.4}
 (out/(name+'_request.json')).write_text(json.dumps(body,indent=2))
 req=urllib.request.Request('https://api.elevenlabs.io/v1/sound-generation',data=json.dumps(body).encode(),headers={'xi-api-key':key,'Content-Type':'application/json','Accept':'audio/mpeg'},method='POST')
 try:
  with urllib.request.urlopen(req,timeout=180) as r:data=r.read()
  tts.save_new(dest,data);return name+' saved '+str(len(data))
 except Exception as e:return name+' FAILED '+type(e).__name__
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
 for result in pool.map(run,jobs):print(result,flush=True)
