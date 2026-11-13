from pathlib import Path
import subprocess,json,sys
root=Path('/Users/diplomat/ytvideos/Work/homelander-edit-research/revisions'); qa=root/'v6-qa'
for name in sys.argv[1:]:
 p=json.loads((qa/f'{name}-plan-v6.json').read_text()); shots=p['source_shots']; beats=p['beats_output']; end=beats[-1]+.95
 old=root/f'homelander_{name}_v5_audio_fix.mp4'; out=root/f'homelander_{name}_v6_variety.mp4'
 cmd=['ffmpeg','-hide_banner','-loglevel','error','-filter_complex_threads','2','-i',p['intro']]
 for s in shots: cmd+=['-ss',str(s['time']),'-i',s['path']]
 cmd+=['-i',str(old)]
 f=['[0:v]trim=start=0:duration=6.25,setpts=PTS-STARTPTS,fps=24,scale=720:1280,setsar=1,format=yuv420p[v0]']
 for i,s in enumerate(shots):
  a,b,c=s['focus']; pre='crop=1920:816:0:132,' if 'BluRay' in s['path'] else ''
  x=f'min(max(iw*(if(lt(t,0.5),{a}+({b}-{a})*t/0.5,{b}+({c}-{b})*min((t-0.5)/0.5,1)))-ow/2,0),iw-ow)'
  z='max(1.025,1.12-0.014*on)' if i==0 else 'min(1.025,1+0.0012*on)'
  f.append(f"[{i+1}:v]trim=duration={s['duration']:.5f},setpts=PTS-STARTPTS,fps=24,{pre}crop=ih*9/16:ih:x='{x}':y=0,scale=720:1280,zoompan=z='{z}':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':d=1:s=720x1280:fps=24,setsar=1,format=yuv420p[s{i}]")
  f.append(f'[ {"v0" if i==0 else "x"+str(i-1)} ][s{i}]xfade=transition={"smoothright" if i==0 else "fade"}:duration={.25 if i==0 else .16}:offset={beats[i]-(.125 if i==0 else .08):.6f}[x{i}]'.replace('[ ','[').replace(' ]',']'))
 pulses=f'0.30*max(0,1-abs(t-{beats[0]:.6f})/0.07)+'+'+'.join(f'0.10*max(0,1-abs(t-{b:.6f})/0.08)' for b in beats[1:])
 f.append(f"[x13]eq=brightness='{pulses}':contrast=1.08:saturation=1.15:eval=frame,scale=1080:1920,format=yuv420p,trim=duration={end:.4f}[video]")
 cmd+=['-filter_complex',';'.join(f),'-map','[video]','-map','15:a:0','-c:v','libx264','-preset','veryfast','-crf','19','-r','24','-c:a','copy','-colorspace','bt709','-color_primaries','bt709','-color_trc','bt709','-movflags','+faststart','-y',str(out)]
 subprocess.run(cmd,check=True); print('RENDERED',out,flush=True)
