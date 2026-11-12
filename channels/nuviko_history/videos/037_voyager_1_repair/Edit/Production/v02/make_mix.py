from pathlib import Path
import subprocess,json,hashlib,wave
import numpy as np
EP=Path(__file__).resolve().parents[3]
OUT=EP/'Source/Audio/en_v02';OUT.mkdir(parents=True,exist_ok=True)
VOICE=EP/'Source/Voice/en_v01_nuviko/voice_en.mp3'
sr=48000;dur=6353/30;n=round(dur*sr)
voice=np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(VOICE),'-f','f32le','-ac','1','-ar',str(sr),'-']),dtype='<f4')
voice=np.pad(voice,(0,max(0,n-len(voice))))[:n].astype(np.float64)
t=np.arange(n)/sr
# Smooth original nonmelodic drone. No external recording or library audio.
bed=(np.sin(2*np.pi*55*t)+.32*np.sin(2*np.pi*110*t+.12*np.sin(2*np.pi*t/39))+.15*np.sin(2*np.pi*164.81*t))
warm=(1+np.tanh((t-174)/2))/2
bed+=.13*warm*np.sin(2*np.pi*220*t)
knots=[0,3,5.6,20.17,28.87,33.37,43.3,67.6,83.2,95.2,109.37,151.13,159.2,168,173.67,178,196.97,204,211.7667]
gain=[0,.2,.55,.35,.1,.3,.5,.25,.4,.35,.4,.25,.08,.06,.1,.48,.36,.3,0]
env=np.interp(t,knots,gain)*np.minimum(1,np.maximum(0,(dur-t)/7))
voice_rms=np.sqrt(np.mean(voice**2));bed*=voice_rms*10**(-32/20)/np.sqrt(np.mean(bed**2))
bed*=env
tone=np.zeros(n);start=round(95.2*sr);length=round(.35*sr);tt=np.arange(length)/sr
tone[start:start+length]=np.sin(2*np.pi*440*tt)*np.sin(np.pi*np.arange(length)/(length-1))**2*voice_rms*10**(-26/20)
music=bed+tone
music*=voice_rms*10**(-32/20)/np.sqrt(np.mean(music**2))
mix=voice+music
assert np.max(np.abs(mix))<1,'Clipping: adjust only music'
def wav(path,a):
 with wave.open(str(path),'wb') as f:f.setnchannels(1);f.setsampwidth(3);f.setframerate(sr);v=np.rint(np.clip(a,-1,1)*8388607).astype(np.int32);f.writeframes(np.stack((v&255,(v>>8)&255,(v>>16)&255),axis=1).astype(np.uint8).tobytes())
wav(OUT/'original_ambient_v01.wav',music);wav(OUT/'mix_en_v02.wav',mix)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
record={'voice':str(VOICE),'voice_sha256':sha(VOICE),'mix':str(OUT/'mix_en_v02.wav'),'mix_sha256':sha(OUT/'mix_en_v02.wav'),'sample_rate':sr,'channels':1,'duration':dur,'voice_gain':1,'speed_applied_here':False,'source_speed':1.1,'peak_dbfs':float(20*np.log10(np.max(np.abs(mix)))),'music_rms_db_relative_to_voice':float(20*np.log10(np.sqrt(np.mean(music**2))/voice_rms)),'source_note':'Original deterministic local synthesis, no third-party sample; artistic background, not real Voyager radio','audible_review':'UNVERIFIED'}
(OUT/'mix_en_v02.evidence.json').write_text(json.dumps(record,indent=2)+'\n')
(OUT/'speed_evidence.md').write_text('Source narration was synthesized at speed 1.1 once; see ../../Voice/en_v01_nuviko/voice_en.request.json.\nVoice SHA256: '+sha(VOICE)+'\nMix retains all voice samples at unity gain and unchanged timing; resampled to 48000Hz, padded 0.0067s to the final video frame. No tempo filter.\nFinal mix SHA256: '+sha(OUT/'mix_en_v02.wav')+'\n')
print(json.dumps(record,indent=2))
