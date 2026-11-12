import json, subprocess, sys
from pathlib import Path
w=Path(__file__).parent
name=sys.argv[1]
visual='notion_fresh-new-visual-draft.mp4' if name=='notion' else 'atlantis_fresh-new-visual-draft.mp4'
cutfile='notion_rise-new-cut-map.json' if name=='notion' else 'atlantis-new-cut-map.json'
mask=f'{name}-aligned-mask.mov'
audio='notion-rise-excerpt.wav' if name=='notion' else 'atlantis-excerpt-draft.wav'
cuts=json.loads((w/cutfile).read_text())['cut_frames']
bloom='+'.join(f'pow(max(0,1-abs(T*30-{c})/3.75),0.8)' for c in cuts)
blur='+'.join(f'if(lt(T*30,{c}),0.85*max(0,1-abs(T*30-{c})/7.5),0.22*max(0,1-abs(T*30-{c})/3))' for c in cuts)
shake='+'.join(f'max(0,1-abs(t*30-{c})/3.75)*sin((t*30-{c})*1.5)' for c in cuts)
graph=f"""[0:v]scale=546:970:flags=lanczos,crop=540:960:x='3+2*({shake})':y='5+1.5*({shake})',format=yuv444p,split=3[base][bright][soft];
[bright]lutyuv=y='max(0,val-127)*1.8':u=128:v=128,gblur=sigma=13[glow];
[base][glow]blend=c0_expr='min(235,A+B*0.88*({bloom}))':c1_expr='A':c2_expr='A'[lit];
[soft]gblur=sigma=12[blurred];
[lit][blurred]blend=all_expr='A+(B-A)*({blur})',format=yuv444p[vbase];
"""
overlay=Path('/private/tmp/nuviko-preview.ffgraph').read_text().replace('[0:v]format=yuv444p,split[base][area];','[vbase]split[base][area];')
graph+=overlay
path=w/f'{name}-restored-transition.ffgraph';path.write_text(graph)
out=w/f'{name}-fresh-scenes-review.mp4'
subprocess.run(['ffmpeg','-nostdin','-hide_banner','-loglevel','error','-i',str(w/visual),'-i',str(w/mask),'-i',str(w/audio),'-filter_complex_script',str(path),'-map','[v]','-map','2:a:0','-t','15','-c:v','libx264','-preset','veryfast','-crf','19','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart','-y',str(out)],check=True)
