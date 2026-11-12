import subprocess,numpy as np
from scipy.signal import correlate,correlation_lags
sources=['Source/Voice/voice_en.mp3','Work/audio_trial_v01/mix_EXPERIMENT_NOT_REVIEWED.wav']
for t in (10,120,240,360,475):
 samples=[]
 for path in sources:
  raw=subprocess.check_output(['ffmpeg','-v','error','-ss',str(t),'-t','5','-i',path,'-ac','1','-ar','8000','-f','f32le','-'])
  samples.append(np.frombuffer(raw,dtype='<f4'))
 x,y=samples; n=min(len(x),len(y));x=x[:n];y=y[:n]
 corr=correlate(y,x,mode='full',method='fft');lag=correlation_lags(n,n,'full');m=(lag>=-1600)&(lag<=1600); lag0=int(lag[m][np.argmax(corr[m])]);norm=float(np.max(corr[m])/(np.linalg.norm(x)*np.linalg.norm(y)+1e-12))
 print(f'{t}s: estimated mix delay {lag0/8000:.4f} s, normalized peak {norm:.3f}')
