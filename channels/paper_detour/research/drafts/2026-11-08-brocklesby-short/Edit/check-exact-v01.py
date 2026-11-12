import bisect,hashlib,json,math,subprocess
from pathlib import Path
import numpy as np
from PIL import Image
ep=Path(__file__).resolve().parents[1]
work=ep/'Work/render-v02'
video=ep/'Deliverables/Brocklesby-Paper-Detour-en-v01.mp4'
def run(args):return subprocess.check_output(args)
def probe(*args):return json.loads(run(['ffprobe','-v','error',*args,'-of','json',str(video)]))
x=probe('-show_streams','-show_format')
v,a=x['streams']
for key,val in dict(width=1440,height=2560,codec_name='h264',pix_fmt='yuv420p',r_frame_rate='30/1',avg_frame_rate='30/1',nb_frames='1080',color_space='bt709',color_transfer='bt709',color_primaries='bt709',color_range='tv',sample_aspect_ratio='1:1',field_order='progressive').items(): assert v[key]==val,(key,v[key],val)
for key,val in dict(codec_name='aac',profile='LC',sample_rate='48000',channels=2,channel_layout='stereo').items(): assert a[key]==val,(key,a[key],val)
assert float(x['format']['duration'])==36.0
ts=probe('-select_streams','v:0','-show_packets','-show_entries','packet=pts,duration')['packets']
pts=sorted(int(p['pts']) for p in ts)
step=round(1/(30*float(__import__('fractions').Fraction(v['time_base']))))
assert pts==list(range(0,1080*step,step)) and all(int(q['duration'])==step for q in ts)
src=ep/'Assets/Audio/full-mix-v02.wav'
def wav(p):
 return np.frombuffer(run(['ffmpeg','-v','error','-xerror','-i',str(p),'-map','0:a:0','-f','f32le','-c:a','pcm_f32le','-']),dtype=np.float32).reshape(-1,2)
m,y=wav(src),wav(video)
n=len(m)
assert n==36*48000 and 0<=len(y)-n<1024
metrics=[]
for j in range(36):
 u=m[j*48000:(j+1)*48000].astype(np.float64)
 z=y[j*48000:(j+1)*48000].astype(np.float64)
 metrics.append(dict(second=j,corr=[float(np.corrcoef(u[:,c],z[:,c])[0,1]) for c in range(2)],error_rms_dbfs=float(20*np.log10(np.sqrt(np.mean((u-z)**2))))))
assert min(min(q['corr']) for q in metrics)>.985
r=json.loads((work/'caption_groups.json').read_text())
ev=r['word_events']; times=[i['frame'] for i in ev]
expected_words=json.loads((ep/'Work/word-times-final-v01.json').read_text())['words']
assert times==[math.ceil(float(w['start'])*30-1e-7) for w in expected_words]
g=r['display_intervals']
assert g[0]['start_frame']==0 and g[-1]['end_frame']==1080 and all(i['end_frame']==j['start_frame'] for i,j in zip(g,g[1:]))
width,height=360,640
height_small=64
base_y=round(2560*.762-Image.open(ev[0]['path']).height/2)
crop_y=base_y//4-3
cream=np.array([244,232,200]);gold=np.array([255,209,102])
masks=[]
for e in ev:
 im=Image.open(e['path']).convert('RGBA')
 layer=Image.new('RGBA',(1440,height_small*4))
 layer.paste(im,(0,base_y-crop_y*4))
 source=np.asarray(layer.resize((width,height_small),Image.Resampling.BOX),dtype=np.int16)
 def mask(color):
  return (source[:,:,3]>246)&(np.max(np.abs(source[:,:,:3]-color),axis=2)<7)
 masks.append((mask(cream),mask(gold)))
stream=subprocess.Popen(['ffmpeg','-v','error','-xerror','-i',str(video),'-map','0:v:0','-vf',f'scale=360:640:flags=area,crop=360:{height_small}:0:{crop_y}', '-pix_fmt','rgb24','-f','rawvideo','-'],stdout=subprocess.PIPE)
fails=[]; mins=[1.0,1.0]; over=[]
for frame in range(1080):
 data=stream.stdout.read(width*height_small*3)
 if len(data)!=width*height_small*3: raise ValueError(f'decoded only {frame} frames')
 rgb=np.frombuffer(data,dtype=np.uint8).reshape((height_small,width,3)).astype(np.int16)
 ci,gi=masks[bisect.bisect_right(times,frame)-1]
 for index,(mask,color) in enumerate(((ci,cream),(gi,gold))):
  if mask.any():
   pix=rgb[mask]; tol=np.abs(pix-color)
   frac=float((np.max(tol,axis=1)<=48).mean())
   mins[index]=min(mins[index],frac)
   if frac<.64: fails.append(dict(frame=frame,state='cream' if index==0 else 'gold',match=frac))
 if ci.any():
  pix=rgb[ci]; closer_gold=(np.linalg.norm(pix-gold,axis=1)+24<np.linalg.norm(pix-cream,axis=1)).mean()
  if closer_gold>.18: over.append(dict(frame=frame,rate=float(closer_gold)))
assert not stream.stdout.read(1) and stream.wait()==0
evidence=dict(media=str(video),sha256=hashlib.sha256(video.read_bytes()).hexdigest(),stream_metadata='PASS',cadence='PASS',fps='30/1',decoded_caption_frames=1080,caption_expected_events=len(times),caption_match_min=dict(cream=mins[0],gold=mins[1]),caption_mismatch_candidates=fails,extra_gold_candidates=over,caption_method='Compare decoded, area-downsampled caption interiors to exact scheduled cream and gold renderer states. Thresholds 48 RGB units, 64% minimum matched interiors; targeted visual review of any candidates.',audio_method='Sample-aligned first 36 seconds, exact 48k stereo; per-channel 1s correlation source versus AAC decoded; allowed less than one AAC frame of end padding.',audio_padding_samples=len(y)-n,audio_comparison=metrics,signal_peak_dbfs=float(20*np.log10(np.max(np.abs(y)))),subjective_listening='UNVERIFIED')
(ep/'Edit/QA/exact-check-v01.json').write_text(json.dumps(evidence,indent=2)+'\n')
print({k:v for k,v in evidence.items() if k not in ('audio_comparison','caption_mismatch_candidates','extra_gold_candidates')})
print('Candidates',len(fails),len(over),fails[:20],over[:20])
