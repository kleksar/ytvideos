from pathlib import Path
import json, math, subprocess, wave, numpy as np
root=Path('/Users/diplomat/ytvideos/channels/paper_detour/videos/001_radio_game')
out=root/'Shorts/02_decoder/Source/Audio/Director_trial_20261031'
base=out/'preview_mix_36p6_no_sfx_stereo.wav'
sources=[root/'Source/Audio/paper_motion_cc0_20261030/book-page-01.wav',root/'Source/Audio/paper_motion_cc0_20261030/book-page-02.wav']
rate=44100; dur=36.6; total=round(dur*rate)
intervals=[(0.10,1.25),(1.35,2.50),(23.30,25.00),(27.35,29.00),(32.95,34.35),(34.82,36.30)]
def load(p):
 raw=subprocess.run(['ffmpeg','-v','error','-i',str(p),'-f','f32le','-ac','2','-ar',str(rate),'-'],check=True,stdout=subprocess.PIPE).stdout
 return np.frombuffer(raw,dtype='<f4').reshape(-1,2).copy()
voice=load(base); clips=[load(p) for p in sources]
if len(voice)!=total:raise ValueError('Unexpected base duration')
sfx=np.zeros_like(voice); schedule=[]
gain01=10**(-26/20); gain02=10**(-25/20)
for start,end in intervals:
 a=max(0,start-.10); b=min(dur,end+.12); scratch=np.zeros((round((b-a)*rate),2),dtype=np.float32)
 for i,trim,offset,gain in [(0,.12,0.0,gain01)]+[(1,.10,k*.50,gain02) for k in range(math.ceil((b-a)/.50))]:
  src=clips[i][round(trim*rate):]; off=round(offset*rate); length=min(len(src),len(scratch)-off)
  if length<=0:continue
  scratch[off:off+length] += src[:length]*gain
  schedule.append({'source':sources[i].name,'source_trim_s':trim,'start_s':round(a+offset,5),'end_s':round(a+offset+length/rate,5),'gain_db':-26 if i==0 else -25,'region_start_s':a,'region_end_s':b})
 # Envelope spans preparation and tail beyond the visible title.
 m=len(scratch); env=np.ones(m,dtype=np.float32); fi=min(m,round(.035*rate)); fo=min(m,round(.12*rate))
 env[:fi]=np.linspace(0,1,fi,dtype=np.float32);env[-fo:]=np.linspace(1,0,fo,dtype=np.float32)
 sfx[round(a*rate):round(a*rate)+m] += scratch*env[:,None]

def write_wav(name,data):
 path=out/name
 if path.exists():raise RuntimeError('Refusing overwrite: '+str(path))
 p=subprocess.run(['ffmpeg','-v','error','-f','f32le','-ar',str(rate),'-ac','2','-i','-','-c:a','pcm_s24le','-n',str(path)],input=data.astype('<f4').tobytes())
 if p.returncode:raise RuntimeError('ffmpeg encode failed')
 return path
mix=voice+sfx
if np.max(np.abs(mix))>=1:raise ValueError('Mix clips')
sfxfile=write_wav('accent_foley_36p6_stereo.wav',sfx)
mixfile=write_wav('preview_mix_36p6_accent_foley_stereo.wav',mix)
report=[]
for start,end in intervals:
 part=sfx[round(start*rate):round(end*rate)]; peak=float(np.max(np.abs(part))); block=round(.01*rate); rms=[]
 for i in range(0,len(part)-block+1,block):rms.append(float(np.sqrt(np.mean(part[i:i+block]**2))))
 report.append({'visible_start':start,'visible_end':end,'min_10ms_rms_dbfs':round(20*math.log10(max(min(rms),1e-15)),2),'max_10ms_rms_dbfs':round(20*math.log10(max(max(rms),1e-15)),2),'peak_dbfs':round(20*math.log10(max(peak,1e-15)),2),'zero_10ms_windows':sum(x==0 for x in rms)})
recipe={'sample_rate':rate,'length_seconds':dur,'base':str(base),'sources':[str(p) for p in sources],'source_provenance':'CC0, Fantasy Sound Effects (Tinysized SFX), Vehicle; see ../paper_motion_cc0_20261030/README.md','sfx_file':str(sfxfile),'mix_file':str(mixfile),'sfx_automation':'For each title interval: region begins 0.10 s early and ends 0.12 s late; one book-page-01 from source 0.12 s at -26 dB, then book-page-02 from source 0.10 s at -25 dB every 0.50 s while region lasts. All clips are summed; region envelope fade in 35 ms, fade out 120 ms; clips truncated at region end. Overlapping regions are summed without normalisation. Base mix unchanged and added at 0 dB.','events':schedule,'coverage_checks_10ms':report,'mix_sample_peak_dbfs':round(20*math.log10(float(np.max(np.abs(mix)))),2),'sfx_sample_peak_dbfs':round(20*math.log10(float(np.max(np.abs(sfx)))),2),'listening_performed':False}
(out/'accent_foley_36p6_recipe.json').write_text(json.dumps(recipe,indent=2)+'\n')
print(json.dumps({'coverage':report,'peak_mix_dbfs':recipe['mix_sample_peak_dbfs'],'peak_sfx_dbfs':recipe['sfx_sample_peak_dbfs'],'mix':str(mixfile)},indent=2))
