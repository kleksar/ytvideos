import numpy as np,subprocess,json
from pathlib import Path
p=Path(__file__).resolve().parent

def read(path,rate=8000):
 return np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(path),'-vn','-ac','1','-ar',str(rate),'-f','f32le','-']),dtype='<f4')
a=read(p/'Deliverables/review_v02.mp4'); b=read(p/'voice/mix_draft_v01.wav'); v=read(p/'voice/voice_en_speed110.wav'); music=read(p/'music/Constance_Kevin_MacLeod.mp3')
print('samples',len(a),len(b),len(v),len(music),'music_seconds',len(music)/8000)
for t in [10,70,140,210,280]:
 i=int(t*8000); x=b[i:i+24000]; y=a[i-400:i+24400]; c=np.correlate(y,x,mode='valid'); k=int(np.argmax(c)); yy=y[k:k+len(x)]; print('mix_to_mp4',t,'lag_seconds',(k-400)/8000,'corr',float(np.corrcoef(x,yy)[0,1]))
# Music repeat seam in decoded source and final mix; compare start/end discontinuity against signal.
print('source_end_start_sample_jump',float(music[0]-music[-1]),'source_rms',float(np.sqrt(np.mean(music**2))))
for t in [len(music)/8000,2*len(music)/8000]:
 i=round(t*8000); x=b[max(0,i-8000):i+8000]; d=np.abs(np.diff(x)); print('mix_near_repeat',round(t,3),'max_adjacent_diff',float(d.max()),'p999_adjacent_diff',float(np.quantile(d,.999)))
print('mono_mix_integrated_rms',float(np.sqrt(np.mean(b*b))))
