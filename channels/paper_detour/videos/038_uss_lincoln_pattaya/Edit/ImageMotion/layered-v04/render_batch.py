from pathlib import Path
import json,subprocess,sys
root=Path('/Users/diplomat/ytvideos'); ep=root/'channels/paper_detour/videos/038_uss_lincoln_pattaya'; out=ep/'Work/layered-motion-v04/render'; scene=json.loads((ep/'Edit/ImageMotion/948de00cd7dfa621939e/run.json').read_text())['scenes']; py=root/'automation/image_motion/.venv/bin/python'; render=root/'automation/image_motion/layered_render.py'; grain=root/'automation/image_motion/apply_g08_layered.py'
ids={'S01_v03':'S01','S07_v04':'S07','S02_v03':'S02','S06_v03':'S06','S04_v02':'S04','S12_v02':'S12a','S12_v03':'S12b','S09_v02':'S09','S10_v04':'S10','S13_v02':'S13','S14_v03':'S14'}
for i,s in enumerate(scene,1):
 key=ids[Path(s['image']).stem]; layer=ep/'Work/layered-motion-v04/layers'/key; n=s['frames']; stem=f'{i:02d}'; clean=out/f'{stem}_clean.mp4'; grained=out/f'{stem}_grain.mp4'; final=out/f'{stem}_palmier.mp4'; direction='parallax-left-camera-right' if i%2 else 'parallax-right-camera-left'
 if not clean.exists(): subprocess.run([str(py),str(render),'--foreground',str(layer/'foreground.png'),'--background',str(layer/'background.png'),'--direction',direction,'--frames',str(n),'--output-width','1440','--output-height','2560','--output',str(clean)],check=True,stdout=subprocess.DEVNULL)
 if not grained.exists(): subprocess.run([str(py),str(grain),'--input',str(clean),'--output',str(grained),'--image-sha256',s['image_hash'],'--frames',str(n)],check=True,stdout=subprocess.DEVNULL)
 if not final.exists(): subprocess.run(['ffmpeg','-v','error','-i',str(grained),'-vf','tpad=stop_mode=clone:stop=2','-an','-c:v','libx264','-preset','fast','-crf','16','-pix_fmt','yuv420p','-movflags','+faststart',str(final)],check=True)
 print(f'{i}/{len(scene)} {key} {n} {direction} complete',flush=True)
