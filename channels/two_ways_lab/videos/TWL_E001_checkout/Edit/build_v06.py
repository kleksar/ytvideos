"""Conform the retained voice, SFX, visual timeline and cues after silence cuts."""
import hashlib,json,math,re,subprocess,wave
from pathlib import Path
import numpy as np
p=Path(__file__).resolve().parents[1]; old=p/'Source/Audio/v02'; out=p/'Source/Audio/v03';out.mkdir(exist_ok=True)
def sha(q):return hashlib.sha256(q.read_bytes()).hexdigest()
def read(q):
 with wave.open(str(q),'rb') as f:
  rate=f.getframerate();channels=f.getnchannels();return np.frombuffer(f.readframes(f.getnframes()),dtype='<i2').reshape(-1,channels).copy(),rate
def write(q,x,rate):
 with wave.open(str(q),'wb') as f:f.setparams((x.shape[1],2,rate,0,'NONE',''));f.writeframes(np.rint(np.clip(x,-32768,32767)).astype('<i2').tobytes())
v,rate=read(old/'voice.wav');sfx,_=read(old/'sfx.wav'); music,_=read(p/'Source/Audio/v01/music.wav')
r=subprocess.run(['ffmpeg','-hide_banner','-i',str(old/'voice.wav'),'-af','silencedetect=noise=-40dB:d=0.18','-f','null','-'],capture_output=True,text=True,check=True)
a=[float(x) for x in re.findall(r'silence_start: ([\d.]+)',r.stderr)]; b=[float(x) for x in re.findall(r'silence_end: ([\d.]+)',r.stderr)];assert len(a)==len(b)
# Leave 100 ms of measured low-level signal; aligner boundaries can include quiet speech.
cuts=[]
for x,y in zip(a,b):
 if y-x>.18:
  c=(x+y)/2; half=(y-x-.10)/2; cuts.append((round((c-half)*rate),round((c+half)*rate)))
assert all(0<=x<y<=len(v) for x,y in cuts)
def edit(signal):
 chunks=[];start=0
 for x,y in cuts:chunks.append(signal[start:x]);start=y
 chunks.append(signal[start:]);return np.concatenate(chunks)
def remap(t):
 n=t*rate
 for x,y in cuts:
  if n<x:break
  n2=min(n,y)-x
  t-=n2/rate
 return max(0,t)
voice=edit(v);effects=edit(sfx); frames=math.ceil(len(voice)/rate*30); samples=round(frames*rate/30)
voice=np.pad(voice,((0,samples-len(voice)),(0,0)));effects=np.pad(effects,((0,max(0,samples-len(effects))),(0,0)))[:samples];background=music[:samples].astype(float); fade=min(round(.32*rate),len(background));background[-fade:]*=np.linspace(1,0,fade)[:,None]
mix=np.repeat(voice.astype(float),2,axis=1)+effects.astype(float)+background
write(out/'voice.wav',voice,rate);write(out/'sfx.wav',effects,rate);write(out/'mix.wav',mix,rate);(out/'narration.txt').write_bytes((old/'narration.txt').read_bytes())
w=json.loads((old/'word_times.json').read_text());
for token in w['words']:
 token['start']=round(remap(token['start']),6);token['end']=round(remap(token['end']),6)
w.update(audio_sha256=sha(out/'mix.wav'),method='v02 model timings conformed through measured silence cuts; pending fresh alignment',status='REVIEW_REQUIRED');(out/'word_times.json').write_text(json.dumps(w,indent=2)+'\n')
(out/'cuts.json').write_text(json.dumps({'sample_rate':rate,'silence_threshold_db':-40,'max_retained_measured_silence_seconds':.10,'source_voice_sha256':sha(old/'voice.wav'),'cuts_source_samples':cuts,'mix_peak_pcm':float(np.max(np.abs(mix)))},indent=2)+'\n')
e=out/'mix-evidence.md';e.write_text('# TWL_E001 audio v03\n\nExisting v02 1.1x voice and SFX conformed using sample-accurate cuts within measured low-level gaps exceeding 180ms. Each detected gap retains 100ms at -40 dB threshold; music remains at original tempo, trimmed to new duration with 0.32s fade. Cuts are documented in cuts.json. No new speech synthesis. Rights and source: [v02](../v02/mix-evidence.md). Mechanical silence detection and alignment do not establish naturalness or pronunciation.\n\n'+''.join(f'- {f}: `{sha(out/f)}`\n' for f in ['voice.wav','sfx.wav','mix.wav','cuts.json']))
t=json.loads((p/'Edit/timeline_v05.json').read_text());t['audio']='../Source/Audio/v03/mix.wav';t['audio_contract'].update(final_audio_sha256=sha(out/'mix.wav'),speed_evidence='../Source/Audio/v03/mix-evidence.md');t['subtitles'].update(words='../Source/Audio/v03/word_times.json',transcript='../Source/Audio/v03/narration.txt')
for seq in (t['scenes'],t['overlays']):
 for item in seq:
  for k in ('start_frame','end_frame'): item[k]=round(remap(item[k]/30)*30)
  if 'lettering_motion' in item:item['lettering_motion']['rotation_degrees']=2
seq=t['scenes'];seq[-1]['end_frame']=frames;t['overlays'][-1]['end_frame']=frames
m=p/'Edit/timeline_v06.json';m.write_text(json.dumps(t,indent=2)+'\n');c=json.loads((p/'Edit/export_contract_v05.json').read_text());c['edit'].update(timeline_id=str(m),revision='v06',source={'path':str(m),'sha256':sha(m)});c['timeline'].update(frame_count=frames,duration_seconds=frames/30);c['required_delivery']['audio_contract']['owner_handoff']={'path':str(e),'sha256':sha(e)};c['required_delivery']['audio_contract']['accepted_complete_mix']={'path':str(out/'mix.wav'),'sha256':sha(out/'mix.wav')};c['preflight']['output_path']=str(p/'Deliverables/TWL_E001_review_v06.mp4');(p/'Edit/export_contract_v06.json').write_text(json.dumps(c,indent=2)+'\n')
s=(p/'Deliverables/TWL_E001_review_v05.en.srt').read_text()
def conv(m):
 def parse(z):
  a,b,c,d=map(int,re.split('[:,]',z));return a*3600+b*60+c+d/1000
 def fmt(x):
  n=round(x*1000);a,n=divmod(n,3600000);b,n=divmod(n,60000);c,d=divmod(n,1000);return f'{a:02}:{b:02}:{c:02},{d:03}'
 return fmt(remap(parse(m.group(1))))+' --> '+fmt(remap(parse(m.group(2))))
s=re.sub(r'(\d\d:\d\d:\d\d,\d\d\d) --> (\d\d:\d\d:\d\d,\d\d\d)',conv,s);(p/'Deliverables/TWL_E001_review_v06.en.srt').write_text(s)
print(f'{len(cuts)} cuts; {frames} frames; {frames/30:.3f}s; mix max {np.max(np.abs(mix)):.1f}')
