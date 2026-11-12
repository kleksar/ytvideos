import subprocess,numpy as np,json

from pathlib import Path
root=Path(__file__).resolve().parents[2]; v=root/'Source/Voice/voice_en.mp3';m=root/'Edit/Previews/world_discovery_PREVIEW_1080p_v01.mp4'
def samples(path,start,duration):
 cmd=['ffmpeg','-v','error','-ss',str(start),'-i',str(path),'-t',str(duration),'-ac','1','-ar','8000','-f','f32le','-'];p=subprocess.run(cmd,check=True,stdout=subprocess.PIPE);return np.frombuffer(p.stdout,dtype='<f4')
results=[]
for t in [10,60,120,180,240,300,346,360,420,475]:
 a=samples(v,t,3);b=samples(m,t-0.25,3.5);n=len(a)+len(b)-1; z=1 << (n-1).bit_length(); full=np.fft.irfft(np.fft.rfft(b,z)*np.fft.rfft(a[::-1],z),z)[:n]; c=full[len(a)-1:len(b)]; k=int(np.argmax(np.abs(c)));seg=b[k:k+len(a)];rho=float(np.dot(a,seg)/(np.linalg.norm(a)*np.linalg.norm(seg))) if np.linalg.norm(seg) and np.linalg.norm(a) else 0;results.append({'window_seconds':t,'estimated_offset_seconds':round(k/8000-0.25,6),'normalized_correlation':round(rho,4)})
print(json.dumps(results,indent=2));(root/'Work/compact_preview_v01/voice_correlation.json').write_text(json.dumps(results,indent=2)+'\n')
