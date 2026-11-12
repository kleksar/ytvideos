"""Offline narration of the exact user script in the existing Kokoro voice."""
import os,wave,json,hashlib,math,re,subprocess
from pathlib import Path
os.environ['HF_HOME']='/private/tmp/twl-e001-hf';os.environ['HF_HUB_OFFLINE']='1';os.environ['HF_HUB_DISABLE_IMPLICIT_TOKEN']='1'
import numpy as np
import torch
from kokoro import KPipeline
p=Path(__file__).resolve().parents[1];out=p/'Source/Audio/v05';rate=24000
h=lambda q:hashlib.sha256(q.read_bytes()).hexdigest()
def wav(q,a):
 with wave.open(str(q),'wb') as f:f.setparams((a.shape[1] if a.ndim==2 else 1,2,rate,0,'NONE',''));f.writeframes(np.rint(np.clip(a,-1,1)*32767).astype('<i2').tobytes())
def groups(tokens):
 buf=[];res=[]
 for t in tokens:
  buf.append(t)
  if t.whitespace:
   valid=[x for x in buf if x.start_ts is not None and x.end_ts is not None]
   if valid:res.append((''.join(x.text for x in buf).strip(),valid[0].start_ts,valid[-1].end_ts))
   buf=[]
 if buf:
  valid=[x for x in buf if x.start_ts is not None and x.end_ts is not None]
  if valid:res.append((''.join(x.text for x in buf).strip(),valid[0].start_ts,valid[-1].end_ts))
 return res
script=(out/'narration.txt').read_text().strip();lines=[x.strip() for x in script.split('\n') if x.strip()];assert len(lines)==8
torch.set_num_threads(3);pipe=KPipeline('a',repo_id='hexgrad/Kokoro-82M',device='cpu')
def render(text):
 parts=list(pipe(text,voice='af_heart',speed=1.0,split_pattern=None));assert len(parts)==1
 r=parts[0];return r.audio.detach().cpu().numpy().copy(),groups(r.tokens)
seam,toks=render(lines[-1]+' '+lines[0]); ix=next(i for i,t in enumerate(toks) if t[0].lower()=='two');split=round(toks[ix][1]*rate);assert split>0
chunks=[seam[split:]]
for line in lines[1:-1]:
 a,t=render(line);assert t
 start=max(0,round((t[0][1]-.04)*rate));end=min(len(a),round((t[-1][2]+.07)*rate));chunks.append(a[start:end])
chunks.append(seam[:split]);speech=[];line_times=[];cursor=0
for i,chunk in enumerate(chunks):
 line_times.append(cursor/rate);speech.append(chunk);cursor+=len(chunk)
 if i not in (len(chunks)-1,):speech.append(np.zeros(round(.10*rate)));cursor+=round(.10*rate)
voice=np.concatenate(speech);peak=np.max(np.abs(voice));voice=voice*(.72/peak);wav(out/'voice_untrimmed.wav',voice)
# Shorten low-level silence, preserving endings. Seam itself remains directly adjacent on playback.
r=subprocess.run(['ffmpeg','-hide_banner','-i',str(out/'voice_untrimmed.wav'),'-af','silencedetect=noise=-40dB:d=0.18','-f','null','-'],capture_output=True,text=True,check=True)
starts=[float(x) for x in re.findall(r'silence_start: ([\d.]+)',r.stderr)];ends=[float(x) for x in re.findall(r'silence_end: ([\d.]+)',r.stderr)];cuts=[]
for x,y in zip(starts,ends):
 if y-x>.18:
  mid=(x+y)/2;half=(y-x-.10)/2;cuts.append((round((mid-half)*rate),round((mid+half)*rate)))
pieces=[];at=0
for x,y in cuts:pieces.append(voice[at:x]);at=y
pieces.append(voice[at:]);voice=np.concatenate(pieces)
frames=math.ceil(len(voice)/rate*30);samples=round(frames*rate/30);voice=np.pad(voice,(0,samples-len(voice)))
with wave.open(str(p/'Source/Audio/v01/music.wav'),'rb') as f:assert f.getframerate()==rate;music=np.frombuffer(f.readframes(f.getnframes()),dtype='<i2').reshape(-1,2).astype(float)/32767
if len(music)<samples:music=np.tile(music,(math.ceil(samples/len(music)),1))
music=music[:samples].copy();fade=round(.25*rate);music[-fade:]*=np.linspace(1,0,fade)[:,None]
mix=voice[:,None]+music;wav(out/'voice.wav',voice);wav(out/'mix.wav',mix)
(out/'audio_build.json').write_text(json.dumps({'voice':'Kokoro af_heart','speed':1.0,'model':'hexgrad/Kokoro-82M','user_script_sha256':h(out/'narration.txt'),'speech_initial_raw_line_starts':line_times,'seam_synthesis':lines[-1]+' | '+lines[0], 'removed_low_level_gaps_samples':cuts,'frames':frames,'sample_rate':rate,'peak':float(np.max(np.abs(mix)))},indent=2)+'\n')
(out/'mix-evidence.md').write_text('# TWL E001 audio v05\n\nExact user-provided English narration, new local Kokoro synthesis with the same af_heart voice as v01, at synthesis speed 1.0. End and opening are generated together and split at the onset of Two; low-level gaps shortened. No new paid calls. Original project music v01 retains its original speed and is trimmed with a short end fade; prior SFX not reused. Story text is unchanged. Signal-based trimming and a textual seam do not prove naturalness; listening remains unverified. Rights/source of existing voice and music: [v01](../v01/mix-evidence.md).\n\n'+''.join(f'- {f}: `{h(out/f)}`\n' for f in ['narration.txt','voice.wav','mix.wav','audio_build.json']))
print('frames',frames,'seconds',frames/30,'voice_sha',h(out/'voice.wav'))
