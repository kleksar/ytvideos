"""Signal comparison on existing audio only; no audio output files."""
import hashlib,json,subprocess
from pathlib import Path
import numpy as np
from scipy.signal import fftconvolve
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent
voice=ROOT/'Source/Voice/v05/voice_en.mp3';mix=ROOT/'Deliverables/PAPER_DETOUR_030_CLOTHING_HISTORY_EN_v13.mp4'
def decoded(path):
 return np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(path),'-map','0:a:0','-ac','1','-ar','8000','-f','f32le','-']),dtype='<f4').astype(float)
a,b=decoded(voice),decoded(mix);rows=[]
for sec in [2,35,70,105,140,175,182]:
 start=int(sec*8000);sample=a[start:start+4*8000];sample-=sample.mean();left=max(0,start-2000);area=b[left:start+4*8000+2000]
 num=fftconvolve(area,sample[::-1],mode='valid');ones=np.ones(len(sample));sm=fftconvolve(area,ones,mode='valid');ss=fftconvolve(area*area,ones,mode='valid');corr=num/np.sqrt(np.maximum(ss-sm*sm/len(sample),1e-10)*np.sum(sample*sample));i=int(corr.argmax());rows.append({'voice_start_seconds':sec,'source_to_final_lag_seconds':(left+i-start)/8000,'normalized_correlation':float(corr[i])})
assert max(abs(x['source_to_final_lag_seconds']) for x in rows)<.01
assert min(x['normalized_correlation'] for x in rows)>.9
q=json.loads((ROOT/'Source/Voice/v05/VOICE_QA_v05.json').read_text());assert hashlib.sha256(voice.read_bytes()).hexdigest()==q['mp3_sha256']
report={'status':'PASS','voice_sha256':q['mp3_sha256'],'source_map':{'source_in':0,'final_start':0,'speed':1,'retained_speech_seconds':187.6,'final_mix_seconds':190},'evidence':'Live Mix spans0-5700 with no clip retime; accepted AAC bit-identical; seven signal landmarks verify unretimed voice at same positions within10ms; no subjective hearing inferred.','landmarks':rows,'alignment_terminal_overrun':'Raw question-mark punctuation ends187.76; spoken us letters end187.44 within187.6voice. Existing words/SRT end187.6. No new clamping or text modification.','subjective_listening':'UNVERIFIED'}
(HERE/'AUDIO_TIMING_MAP.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(rows,indent=2))
