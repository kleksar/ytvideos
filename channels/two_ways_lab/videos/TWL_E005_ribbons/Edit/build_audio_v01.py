import json, re, wave, subprocess, hashlib, math
from pathlib import Path
import numpy as np
p=Path(__file__).resolve().parents[1]; d=p/'Source/Audio/v01'; rate=24000
h=lambda x:hashlib.sha256(x.read_bytes()).hexdigest()
def readwav(path):
 with wave.open(str(path),'rb') as w:
  assert w.getframerate()==rate and w.getsampwidth()==2
  n=w.getnchannels(); a=np.frombuffer(w.readframes(w.getnframes()),dtype='<i2').astype(np.float64)/32768
  return a.reshape(-1,n) if n>1 else a
def writewav(path,a):
 with wave.open(str(path),'wb') as w:
  w.setparams((a.shape[1] if a.ndim==2 else 1,2,rate,0,'NONE',''));w.writeframes(np.rint(np.clip(a,-1,1)*32767).astype('<i2').tobytes())
a=json.loads((d/'voice_raw.alignment.json').read_text())['alignment'];t=''.join(a['characters']); st=a['character_start_times_seconds'];en=a['character_end_times_seconds']; assert t==(d/'request_text.txt').read_text().strip()
words=[{'text':m.group(),'start':st[m.start()],'end':en[m.end()-1]} for m in re.finditer(r'\S+',t)]
transcript=(d/'narration.txt').read_text().strip();expected=transcript.split(); start_index=next(i for i,w in enumerate(words) if w['text']=='Three'); assert [w['text'] for w in words[start_index:]+words[:start_index]]==expected
voice=readwav(d/'voice_raw.wav'); voice*=.68/max(np.max(np.abs(voice)),1e-9); writewav(d/'voice_normalized.wav',voice); res=subprocess.run(['ffmpeg','-hide_banner','-i',str(d/'voice_normalized.wav'),'-af','silencedetect=noise=-40dB:d=0.25','-f','null','-'],text=True,capture_output=True,check=True)
starts=[float(x) for x in re.findall(r'silence_start: ([\d.]+)',res.stderr)]; ends=[float(x) for x in re.findall(r'silence_end: ([\d.]+)',res.stderr)]; assert len(starts)==len(ends)
cuts=[]
for x,y in zip(starts,ends):
 if y-x>.25:
  mid=(x+y)/2; cuts.append((round((mid-(y-x-.16)/2)*rate),round((mid+(y-x-.16)/2)*rate)))
def mapped(sample):
 return sample-sum(max(0,min(sample,b)-a) for a,b in cuts if sample>a)
parts=[]; cursor=0
for x,y in cuts: parts.append(voice[cursor:x]);cursor=y
parts.append(voice[cursor:]); short=np.concatenate(parts)
# Preserve the full with → Eight transition on the wrap. Split in the silent gap just before Two.
seam_src=round((words[start_index]['start']-.01)*rate); seam=mapped(seam_src); speech=np.concatenate((short[seam:],short[:seam]));raw_len=len(short)
# Check the rotated and normalized signal as delivered; normalize can expose a longer threshold interval.
writewav(d/'voice_pre_final.wav',speech)
r2=subprocess.run(['ffmpeg','-hide_banner','-i',str(d/'voice_pre_final.wav'),'-af','silencedetect=noise=-40dB:d=0.25','-f','null','-'],text=True,capture_output=True,check=True)
s2=[float(x) for x in re.findall(r'silence_start: ([\d.]+)',r2.stderr)]; e2=[float(x) for x in re.findall(r'silence_end: ([\d.]+)',r2.stderr)]; assert len(s2)==len(e2)
secondary=[]
for x,y in zip(s2,e2):
 if y-x>.25:
  mid=(x+y)/2; secondary.append((round((mid-(y-x-.15)/2)*rate),round((mid+(y-x-.15)/2)*rate)))
chunks=[]; pos=0
for x,y in secondary: chunks.append(speech[pos:x]);pos=y
chunks.append(speech[pos:]);speech=np.concatenate(chunks)

def target_time(seconds):
 v=mapped(round(seconds*rate));v=((v-seam) if v>=seam else (raw_len-seam+v));v-=sum(max(0,min(v,b)-a) for a,b in secondary if v>a);return v/rate
ordered=words[start_index:]+words[:start_index]
for w in ordered:
 w['start']=round(max(0,target_time(w['start'])),6);w['end']=round(min(len(speech)/rate,target_time(w['end'])),6)
# Provider final-word estimate extends 80 ms beyond the decoded source; clamp to the actual splice boundary.
for current, following in zip(ordered,ordered[1:]):
 if current['end']>following['start']: current['end']=following['start']
assert all(w['end']>=w['start'] for w in ordered)
frames=math.ceil(len(speech)*30/rate); n=round(frames*rate/30);speech=np.pad(speech,(0,n-len(speech)));speech*=.68/max(np.max(np.abs(speech)),1e-9);writewav(d/'voice.wav',speech)
music=readwav(d/'music_source.wav');music=np.tile(music,(math.ceil(n/len(music)),1))[:n].copy();fade=round(.25*rate);music[-fade:]*=np.linspace(1,0,fade)[:,None]
mix=speech[:,None]+music; peak=float(np.max(np.abs(mix)));assert peak<1;writewav(d/'mix.wav',mix)
(d/'word_times.json').write_text(json.dumps({'status':'PROVIDER_ALIGNMENT_REMAPPED','source':'ElevenLabs character timestamps mapped through detected-silence cuts and seam rotation','audio_sha256':h(d/'mix.wav'),'voice_sha256':h(d/'voice.wav'),'transcript_sha256':hashlib.sha256(transcript.encode()).hexdigest(),'words':ordered},indent=2)+'\n')
(d/'audio_build.json').write_text(json.dumps({'model':'eleven_v4','voice_id':'zfc8CJQpe8Kqyl0vvCzo','speed':1.1,'sample_rate':rate,'frames':frames,'raw_silence_cuts_samples':cuts,'seam_source_sample':seam_src,'peak':peak,'music':'music_source.wav','tts_alignment':'voice_raw.alignment.json','note':'Machine silence and provider timing are estimates; naturalness and actual word boundaries not verified by listening'},indent=2)+'\n')
(d/'mix-evidence.md').write_text('# TWL E005 v01 audio\n\nElevenLabs `eleven_v4`, selected voice `zfc8CJQpe8Kqyl0vvCzo` (Mike), speed 1.10 once at synthesis. One completed request with the user-selected channel voice. Exact script; final line and opening were synthesized adjacent and rotated to original narrative order. FFmpeg -40 dB silence intervals above 250 ms were shortened to 160 ms; the same transformations were mapped onto provider alignment. These estimates do not establish audibility or naturalness. Original project v01 music looped and faded at the end, no new SFX.\n\n'+''.join(f'- {x}: `{h(d/x)}`\n' for x in ['request.json','narration.txt','voice_raw.mp3','voice_raw.alignment.json','voice.wav','mix.wav','word_times.json','audio_build.json']))
print('Built audio',frames,'frames; seconds',round(frames/30,2),'cuts',len(cuts),'peak',round(peak,3));print('word boundaries');
for i,w in enumerate(ordered):print(i,w['text'],w['start'],w['end'])
