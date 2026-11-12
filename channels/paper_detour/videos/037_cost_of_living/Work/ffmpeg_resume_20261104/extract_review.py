import json,pathlib,subprocess,concurrent.futures
w=pathlib.Path(__file__).resolve().parent;p=json.loads((w/'plan_review_v01.json').read_text());o=w/'upload_visual_frames';video=w.parents[1]/'Deliverables/037_EN_review_20261104.mp4';
frames=[]
for s in p['scenes']:frames.extend([s['start_frame'],(s['start_frame']+s['end_frame'])//2,s['end_frame']-1])
def run(k):
 start=k*30; group=frames[start:start+30]; out=o/f'batch_{k:02}';out.mkdir(); vf='select='+"'"+'+'.join('eq(n,'+str(n)+')' for n in group)+"',scale=400:225"; subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-i',str(video),'-vf',vf,'-fps_mode','vfr','-q:v','3',str(out/'frame_%03d.jpg')],check=True); return len(list(out.glob('*.jpg')))
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as x:print('extracted',sum(x.map(run,range((len(frames)+29)//30))),'of',len(frames))
