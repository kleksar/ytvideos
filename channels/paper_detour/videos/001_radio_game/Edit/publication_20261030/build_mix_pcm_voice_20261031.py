import json,sys,subprocess
from pathlib import Path
import numpy as np
sys.path.insert(0,'automation/palmier')
from inspect_connection import PalmierConnection
root=Path('channels/paper_detour/videos/001_radio_game').resolve()
c=PalmierConnection(); c.connect()
def get(name,args):
 r=c.request('tools/call',{'name':name,'arguments':args})
 if r.get('isError'): raise RuntimeError(r)
 return json.loads(r['content'][0]['text'])
p=get('manage_project',{'action':'list'}); t=get('get_timeline',{})
assert p['active']['path']==str(root/'Rarovista_001.palmier') and t['id']=='BD754260' and t['fps']==30
tracks=[x for x in t['tracks'] if x['type']=='audio']
assert [len(t['clips']) for t in tracks]==[5,1,14,1]
paths={
'BD5ACE66':root/'Source/Voice/v3/generated/voice_en.mp3',
'89C74949':root/'Source/Voice/v3/pronunciation_20261030/opening/voice_en.mp3',
'531A8113':root/'Source/Voice/v3/pronunciation_20261030/second_mention/voice_en_pcm16_padded_candidate.wav',
'A6AAC572':root/'Source/Audio/paper_sound_design/music_bed_continuous_260s.wav',
'A4F2D352':root/'Source/Audio/paper_motion_cc0_20261030/book-page-02.wav',
'DE97F1B7':root/'Source/Audio/paper_motion_cc0_20261030/book-page-01.wav'}
for p in paths.values(): assert p.is_file(), p
rate=44100;spf=1470;nframes=t['totalFrames']; mix=np.zeros((nframes*spf,2),dtype=np.float32)
for tr in tracks:
 for clip in tr['clips']:
  start,end=clip['frames']; length=(end-start)*spf; speed=clip.get('speed',1); trim=clip.get('trimStartFrame',0)/30
  cmd=['ffmpeg','-v','error','-ss',str(trim),'-i',str(paths[clip['mediaRef']]),'-af',f'atempo={speed},aresample={rate}', '-t',str((end-start)/30),'-ar',str(rate),'-ac','2','-f','f32le','pipe:1']
  audio=np.frombuffer(subprocess.run(cmd,check=True,stdout=subprocess.PIPE).stdout,dtype=np.float32).copy().reshape(-1,2)
  if len(audio)<length: audio=np.pad(audio,((0,length-len(audio)),(0,0)))
  audio=audio[:length]
  gain=10**(clip.get('volumeDb',0)/20)
  if 'keyframes' in clip and 'volumeDb' in clip['keyframes']:
   frames=np.arange(len(audio),dtype=np.float32)/spf
   keys=clip['keyframes']['volumeDb']; db=np.interp(frames,[x[0] for x in keys],[x[1] for x in keys]); audio*=np.power(10,db/20,dtype=np.float64)[:,None]
  for typ in ('fadeIn','fadeOut'):
   count=clip.get(typ+'Frames',0)*spf
   if not count: continue
   w=np.arange(count,dtype=np.float32)/count
   if clip.get(typ+'Interpolation')=='smooth': w=w*w*(3-2*w)
   if typ=='fadeIn': audio[:count]*=w[:,None]
   else: audio[-count:]*=w[::-1,None]
  mix[start*spf:end*spf]+=audio*gain
  print(clip['id'],clip['mediaRef'],start,end,'gain',gain,flush=True)
output=root/'Edit/publication_20261030/mix_candidate_pcm_voice_20261031.wav'
if output.exists(): raise SystemExit('refusing to overwrite')
p=subprocess.Popen(['ffmpeg','-v','error','-f','f32le','-ar',str(rate),'-ac','2','-i','pipe:0','-c:a','pcm_s24le',str(output)],stdin=subprocess.PIPE)
p.stdin.write(mix.tobytes());p.stdin.close()
if p.wait(): raise SystemExit('ffmpeg failed')
print('peak',float(np.max(np.abs(mix))), 'duration',len(mix)/rate,'output',output)
