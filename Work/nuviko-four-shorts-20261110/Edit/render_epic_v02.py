import hashlib,json,subprocess
from pathlib import Path
root=Path('/Users/diplomat/ytvideos/Work/nuviko-four-shorts-20261110')
old=json.loads((root/'Edit/epic-v01-contract.json').read_text())
out=root/'Deliverables/Epic-Inspiration-review-v02.mp4'
if out.exists(): raise SystemExit('output exists')
cuts=old['cuts']; transition=0.5
shots=[Path(s['path']) for s in old['shots']]; audio=Path(old['audio']['path'])
g=[]
for i,(start,end) in enumerate(zip(cuts,cuts[1:])):
 duration=(end-start)/30 + (0.25 if i in (0,4) else 0.5)
 motion=f'(1-cos(PI*on/({round(duration*30)}-1)))/2'
 z=f'1+0.02*{motion}' if i%2==0 else f'1.02-0.02*{motion}'
 # Optical interpolation only where the native source is 25 fps.
 fpsfilter='minterpolate=fps=30:mi_mode=mci:mc_mode=aobmc:me_mode=bidir' if i==3 else 'fps=30'
 g.append(f"[{i}:v]trim=start=1:duration={duration+0.12:.6f},setpts=PTS-STARTPTS,scale=1140:2026:force_original_aspect_ratio=increase:flags=bicubic,crop=1140:2026,{fpsfilter},trim=duration={duration:.6f},setpts=PTS-STARTPTS,zoompan=z='{z}':x='(iw-iw/zoom)/2':y='(ih-ih/zoom)/2':d=1:s=1080x1920:fps=30,setsar=1,settb=AVTB,format=yuv420p[v{i}]")
prev='v0'
for i,cut in enumerate(cuts[1:-1],1):
 label=f'x{i}'; offset=cut/30-transition/2
 g.append(f'[{prev}][v{i}]xfade=transition=fade:duration={transition}:offset={offset:.6f}[{label}]'); prev=label
g.append(f'[{prev}]trim=duration=16,setpts=PTS-STARTPTS,eq=contrast=1.25:saturation=1.5,format=yuv420p[video]')
g.append(f'[{len(shots)}:a]atrim=duration=16,asetpts=PTS-STARTPTS,afade=t=in:st=0:d=0.04,afade=t=out:st=15.8:d=0.2[audio]')
graph=root/'Edit/epic-v02.ffgraph';graph.write_text(';\n'.join(g)+'\n')
argv=['ffmpeg','-nostdin','-n','-hide_banner','-loglevel','error','-filter_complex_threads','2']
for p in shots: argv+=['-i',str(p)]
argv+=['-i',str(audio),'-filter_complex_script',str(graph),'-map','[video]','-map','[audio]','-r','30','-fps_mode','cfr','-c:v','libx264','-preset','veryfast','-crf','19','-pix_fmt','yuv420p','-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709','-c:a','aac','-b:a','192k','-ar','44100','-ac','2','-movflags','+faststart',str(out)]
contract=dict(old);contract.update({'revision':'v02','transitions':'0.5 s crossfade centred at original beat frame','motion':'smooth cosine zoom 2% per shot; no glow/blur pulses','25fps_source':'optical interpolation to 30 fps; artifacts require inspection','frames':480,'graph_sha256':hashlib.sha256(graph.read_bytes()).hexdigest(),'command':argv,'output':str(out),'qa':'pending','cut_map_meaning':'transition midpoint frames'})
(root/'Edit/epic-v02-contract.json').write_text(json.dumps(contract,indent=2,ensure_ascii=False)+'\n')
(root/'Edit/epic-v02-cut-map.json').write_text(json.dumps({'fps':30,'cut_frames':cuts[1:-1]},indent=2)+'\n')
subprocess.run(argv,check=True)
