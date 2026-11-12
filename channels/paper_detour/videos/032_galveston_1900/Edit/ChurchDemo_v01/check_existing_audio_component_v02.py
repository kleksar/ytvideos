from pathlib import Path
import subprocess,numpy as np,json,hashlib
E=Path('/Users/diplomat/ytvideos/channels/paper_detour/videos/032_galveston_1900');W=Path('/Users/diplomat/ytvideos/channels/nuviko_history/videos/017_galveston_1900/Source/Voice/odom_5vsg/film/voice_en_105.wav');V=E/'Deliverables/032_galveston_en_motion_review_v01.mp4'
def pcm(p,rate=44100,channels=1):return np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(p),'-vn','-ac',str(channels),'-ar',str(rate),'-f','f32le','-']),dtype='<f4')
x=pcm(W);y=pcm(V);n=min(len(x),len(y));sxx=syy=sxy=0.;peaks=[0.,0.];clips=[0,0]
for a in range(0,n,500000):
 u=x[a:min(a+500000,n)].astype(np.float64);v=y[a:min(a+500000,n)].astype(np.float64);sxx+=u@u;syy+=v@v;sxy+=u@v
 peaks=[max(peaks[0],float(np.abs(u).max())),max(peaks[1],float(np.abs(v).max()))];clips=[clips[0]+int((np.abs(u)>=1).sum()),clips[1]+int((np.abs(v)>=1).sum())]
gain=sxy/sxx;res=max(0,syy-2*gain*sxy+gain*gain*sxx);lags=[]
for lag in range(-2,3):
 a=x[44100:44100*31].astype(np.float64);b=y[44100+lag:44100*31+lag].astype(np.float64);lags.append({'samples':lag,'cosine':float((a@b)/np.sqrt((a@a)*(b@b)))})
tail=[]
for a in np.arange(572.9,574.403,.1):
 z=x[int(a*44100):min(len(x),int((a+.1)*44100))]
 if len(z):tail.append({'start':round(float(a),3),'rms_dbfs':float(20*np.log10(max(1e-12,np.sqrt(np.mean(z.astype(float)**2))))),'peak_dbfs':float(20*np.log10(max(1e-12,float(np.abs(z).max()))))})
st=pcm(V,48000,2).reshape(-1,2);maxdiff=0.;l2=r2=lr=0.;stpeaks=[0.,0.];stclips=[0,0]
for a in range(0,len(st),500000):
 z=st[a:a+500000].astype(float);stpeaks=[max(stpeaks[i],float(np.abs(z[:,i]).max())) for i in (0,1)];stclips=[stclips[i]+int((np.abs(z[:,i])>=1).sum()) for i in (0,1)];l2+=z[:,0]@z[:,0];r2+=z[:,1]@z[:,1];lr+=z[:,0]@z[:,1];maxdiff=max(maxdiff,float(np.abs(z[:,0]-z[:,1]).max()))
receipt={'scope':'existing accepted audio component before mux; final exact encoded-audio hash must match this component','source_wav_sha256':hashlib.sha256(W.read_bytes()).hexdigest(),'decoded_rate':44100,'source_samples':len(x),'component_samples':len(y),'source_duration':len(x)/44100,'component_duration':len(y)/44100,'full_common_samples_checked':n,'zero_lag_cosine':sxy/np.sqrt(sxx*syy),'least_squares_gain':gain,'gain_corrected_residual_rms':float(np.sqrt(res/n)),'sample_peaks':peaks,'samples_ge_1':clips,'lag_check_first30seconds':lags,'downmix_gain_note':'Default ffmpeg stereo-to-mono matrix gives aboutsqrt2 boost for centred dual-mono. Values>=1 above refer to this analysis-only downmix, not delivered channels. Gain-correct0.5L+0.5R is equivalent to dividing this downmix bysqrt2.','gain_correct_mono_samples_ge_1':int((np.abs(y)/np.sqrt(2)>=1).sum()),'stereo_full':{'sample_peaks':stpeaks,'samples_ge_1':stclips,'frames':len(st),'left_right_cosine':lr/np.sqrt(l2*r2),'max_abs_channel_difference':maxdiff,'mono_mapping':'ffmpeg standard downmix used only in memory for source correspondence; no audio written'},'last_source_windows':tail,'asr_tail':'inspect_media recognizes the complete final city itself. at573.12-573.72; no word omitted by ASR','subjective_listening':'UNVERIFIED'}
(E/'Edit/ChurchDemo_v01/audio_component_signal_v02.json').write_text(json.dumps(receipt,indent=2));print(json.dumps(receipt,indent=2))
