import json, subprocess, sys
from pathlib import Path
work=Path('/Users/diplomat/ytvideos/Work/nuviko-videos-short-batch-20261110')
source=Path('/Users/diplomat/ytvideos/Work/satisfying-runaway-pilot/Source')
name=sys.argv[1]
configs={
'notion': {'cuts':[0,39,73,107,197,242,286,331,376,421,450], 'shots':['35867202.mp4','36974946.mp4',str(work/'pexels-35179742.mp4'),'34535413.mp4',str(work/'pexels-37362542.mp4'),'6316369.mp4','10001446.mp4','36974946.mp4','35867202.mp4',str(work/'pexels-35179742.mp4')]},
'atlantis': {'cuts':[0,51,111,151,211,251,291,351,392,450], 'shots':[str(work/'pexels-35179742.mp4'),'36974946.mp4','35867202.mp4','34535413.mp4',str(work/'pexels-37362542.mp4'),'6316369.mp4','10001446.mp4','36974946.mp4','35867202.mp4']}}
p=configs[name]; cuts=p['cuts']; shots=p['shots']; filters=[]
for i,(a,b) in enumerate(zip(cuts,cuts[1:])):
 f=b-a
 # Base framing at 100% has a 1/0.95 safety margin, so zoompan=1 corresponds to 95%, zoompan=1.1053 to 105%.
 phase=f'(1-cos(PI*on/{f-1}))/2'
 z=f'1+0.1052631579*{phase}' if i%2==0 else f'1.1052631579-0.1052631579*{phase}'
 x=f'(iw-iw/zoom)*(0.3+0.4*{phase})'
 filters.append(f"[{i}:v]fps=30,trim=start=2:end={2+f/30:.8f},setpts=PTS-STARTPTS,scale=1080:1920:force_original_aspect_ratio=increase:flags=lanczos,crop=1080:1920,format=yuv444p,zoompan=z='{z}':x='{x}':y='(ih-ih/zoom)/2':d=1:s=540x960:fps=30,setsar=1,setpts=PTS-STARTPTS[v{i}]")
filters.append(''.join(f'[v{i}]' for i in range(len(shots)))+f'concat=n={len(shots)}:v=1:a=0,eq=contrast=1.25:saturation=1.5,unsharp=5:5:0.75:5:5:0,split[base][high]')
filters.append("[high]lutyuv=y='max(0,val-190)*3':u=128:v=128,gblur=sigma=12[glow]")
glow='+'.join(f'pow((1+cos(PI*min(abs(T*30-{n})/3.75,1)))/2,2)' for n in cuts[1:-1])
blur='+'.join(f'((1+cos(PI*min(abs(T*30-{n})/7.5,1)))/2)' for n in cuts[1:-1])
filters.append(f"[base][glow]blend=c0_expr='min(235,A+B*0.5*({glow}))':c1_expr='A':c2_expr='A',split[clean][blur_source]")
filters.append('[blur_source]gblur=sigma=6[blurred]')
filters.append(f"[clean][blurred]blend=all_expr='A+(B-A)*0.30*({blur})',format=yuv420p[video]")
graph=work/f'{name}-new-draft.ffgraph';graph.write_text(';\n'.join(filters)+'\n')
output=work/f'{name}-new-visual-draft.mp4';assert not output.exists()
args=['ffmpeg','-nostdin','-hide_banner','-loglevel','error','-filter_complex_threads','2']
for shot in shots: args+=['-i',str(source/shot)]
args+=['-filter_complex_script',str(graph),'-map','[video]','-an','-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p','-movflags','+faststart',str(output)]
(work/f'{name}-new-cut-map.json').write_text(json.dumps({'fps':30,'cut_frames':cuts[1:-1],'shots':shots,'purpose':'test only; timings and source use unverified'},indent=2))
subprocess.run(args,check=True)
