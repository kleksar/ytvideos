import json, subprocess, sys
from pathlib import Path
work=Path('/Users/diplomat/ytvideos/Work/nuviko-videos-short-batch-20261110')
source=Path('/Users/diplomat/ytvideos/Work/satisfying-runaway-pilot/Source')
name=sys.argv[1]
configs={
'notion_fresh': {'cuts':[0,52,96,141,186,231,276,322,366,411,450], 'shots':['35091927','28891505','37898716','33871227','20568097','26346980','29645507','32120722','35065432','36029898']},
'atlantis_fresh': {'cuts':[0,51,111,151,211,251,291,351,392,450], 'shots':['13830672','7076544','7366444','15367486','29393034','10411103','5619693','36410669','35970539']}}
for cfg in configs.values(): cfg['shots']=[str(work/'new-footage'/f'{s}.mp4') for s in cfg['shots']]

p=configs[name]; cuts=p['cuts']; shots=p['shots']; filters=[]
for i,(a,b) in enumerate(zip(cuts,cuts[1:])):
 f=b-a
 # Base framing at 100% has a 1/0.95 safety margin, so zoompan=1 corresponds to 95%, zoompan=1.1053 to 105%.
 phase=f'(1-cos(PI*on/{f-1}))/2'
 z=f'1+0.1052631579*{phase}' if i%2==0 else f'1.1052631579-0.1052631579*{phase}'
 x=f'(iw-iw/zoom)*(0.3+0.4*{phase})'
 filters.append(f"[{i}:v]fps=30,trim=start=2:end={2+f/30:.8f},setpts=PTS-STARTPTS,scale=720:1280:force_original_aspect_ratio=increase:flags=bicubic,crop=720:1280,format=yuv444p,zoompan=z='{z}':x='{x}':y='(ih-ih/zoom)/2':d=1:s=540x960:fps=30,setsar=1,setpts=PTS-STARTPTS[v{i}]")
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
