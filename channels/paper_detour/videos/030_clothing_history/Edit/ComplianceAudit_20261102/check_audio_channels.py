from pathlib import Path
import subprocess,json,numpy as np
p=Path('/Users/diplomat/ytvideos/channels/paper_detour/videos/030_clothing_history'); a=p/'Edit/ComplianceAudit_20261102'
f=p/'Deliverables/PAPER_DETOUR_030_CLOTHING_HISTORY_EN_v13.mp4'
b=subprocess.run(['ffmpeg','-v','error','-i',str(f),'-map','0:a:0','-ar','8000','-f','f32le','pipe:1'],capture_output=True,check=True).stdout
x=np.frombuffer(b,dtype='<f4').reshape(-1,2); l=x[:,0];r=x[:,1]; m=(l+r)*.5;d=(l-r)*.5
rms=lambda y:float(np.sqrt(np.mean(y.astype('float64')**2)))
db=lambda v:float(20*np.log10(max(v,1e-12)))
res={'method':'Read-only existing mix decode to memory, 8kHz float32 stereo. Arithmetic mono (L+R)/2, no audio file created. This does not prove subjective balance.','channels':2,'seconds':len(x)/8000,'left_rms_dbfs':db(rms(l)),'right_rms_dbfs':db(rms(r)),'lr_correlation':float(np.corrcoef(l,r)[0,1]),'mono_rms_dbfs':db(rms(m)),'side_rms_dbfs':db(rms(d)),'mono_peak_dbfs':db(float(abs(m).max())),'signal_status':'PASS: both channels nonzero, no global mono cancellation observed','subjective_fold_down_listening':'UNVERIFIED'}
(a/'AUDIO_CHANNELS.json').write_text(json.dumps(res,indent=2));print(json.dumps(res,indent=2))
