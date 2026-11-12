#!/usr/bin/env python3
"""Render a review draft from illustrated stills and narration without Palmier.

The output is a motion-of-stills draft, not character or frame-by-frame
animation. Original sound effects and reconstruction labels are separate input
assets. The narration timing is unchanged. No existing output is overwritten.
"""
import argparse, json, math, os, subprocess
from pathlib import Path

def run(args):
    subprocess.run(args, check=True, stdin=subprocess.DEVNULL)

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--manifest',type=Path,required=True)
    p.add_argument('--output-dir',type=Path,required=True)
    a=p.parse_args(); m=json.loads(a.manifest.read_text())
    root=a.manifest.resolve().parents[2]
    out=a.output_dir.resolve(); out.mkdir(parents=True,exist_ok=True)
    segments=out/'segments'; segments.mkdir(exist_ok=False)
    video=out/'001_review_video_only.mp4'; result=out/'001_review_draft.mp4'; files=out/'segments.ffconcat'
    if any(x.exists() for x in (video,result,files)):raise ValueError('Output exists; use a new draft directory')
    voice=Path(m['voice']); label=Path(m['label']); shots=m['shots']; total=m['total_frames']; fps=m['fps']
    if fps!=30 or not voice.is_file() or not label.is_file() or not isinstance(total,int) or total<=0:raise ValueError('Invalid media or timeline')
    if not voice.resolve().is_relative_to(root/'Source') or not label.resolve().is_relative_to(root/'Source'):raise ValueError('Media must be permanent episode source')
    frame=0
    for shot in shots:
        image=Path(shot['image']).resolve()
        if not image.is_file() or not image.is_relative_to(root/'Source') or shot['start']!=frame or shot['end']<=frame:raise ValueError('Invalid or non-contiguous shot')
        frame=shot['end']
    if frame!=total:raise ValueError('Shots do not cover whole timeline')
    for i,shot in enumerate(shots):
        frames=shot['end']-shot['start']; divisor=max(1,frames-1)
        z=(f'1.035+0.060*on/{divisor}' if i%2==0 else f'1.095-0.060*on/{divisor}')
        pan=(f'0.35+0.30*on/{divisor}' if i%2==0 else f'0.65-0.30*on/{divisor}')
        base=f"scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,zoompan=z='{z}':x='(iw-iw/zoom)*({pan})':y='(ih-ih/zoom)/2':d=1:s=1920x1080:fps=30,format=yuv420p"
        target=segments/f'{i:03}.mp4'; cmd=['ffmpeg','-hide_banner','-loglevel','error','-n','-loop','1','-framerate','30','-i',shot['image']]
        if i==0:
            cmd+=['-loop','1','-framerate','30','-i',str(label),'-filter_complex',f"[0:v]{base}[base];[base][1:v]overlay=0:0:enable='between(t,0.2,3.15)'[v]",'-map','[v]']
        else: cmd+=['-vf',base]
        cmd+=['-frames:v',str(frames),'-an','-c:v','h264_videotoolbox','-b:v','6M','-pix_fmt','yuv420p',str(target)]
        print(json.dumps({'stage':'shot','index':i+1,'count':len(shots),'frames':frames}),flush=True);run(cmd)
    with files.open('x',encoding='utf8') as f:
        f.write('ffconcat version 1.0\n')
        for segment in sorted(segments.glob('*.mp4')): f.write("file '"+str(segment).replace("'","'\\''")+"'\n")
    run(['ffmpeg','-hide_banner','-loglevel','error','-n','-f','concat','-safe','0','-i',str(files),'-c','copy',str(video)])
    # A quiet, original illustrative electronic tone under the first 3 seconds.
    # No archival broadcast or third-party music is used. Overall timing remains unchanged.
    run(['ffmpeg','-hide_banner','-loglevel','error','-n','-i',str(video),'-i',str(voice),'-f','lavfi','-i',"aevalsrc=0.035*sin(2*PI*(1100*t+30*sin(2*PI*3*t))):s=44100:d=3",'-filter_complex','[2:a]afade=t=in:st=0:d=0.15,afade=t=out:st=2.4:d=0.6,volume=0.45[fx];[1:a][fx]amix=inputs=2:duration=first:normalize=0[a]','-map','0:v:0','-map','[a]','-c:v','copy','-c:a','aac','-b:a','192k','-ar','44100','-ac','1','-movflags','+faststart',str(result)])
    print(json.dumps({'status':'rendered','video':str(result),'shots':len(shots),'frames':total,'fps':fps,'narration':str(voice),'illustrative_effect':'original synthetic tone first 3s','music':False,'visual':'moving still illustrations; not character animation'}),flush=True)
if __name__=='__main__':main()
