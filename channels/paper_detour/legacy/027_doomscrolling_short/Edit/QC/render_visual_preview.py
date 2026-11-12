#!/usr/bin/env python3
"""Render silent, half-resolution QC preview, without modifying Palmier."""
import json
import subprocess
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
QC=ROOT/'Edit/QC'
MANIFEST=ROOT/'Edit/short_manifest.json'
SEGMENTS=QC/'preview_segments'
OUTPUT=QC/'visual_preview_silent.mp4'
FPS=30

def run(cmd):
    subprocess.run(cmd,check=True)

def main():
    manifest=json.loads(MANIFEST.read_text())
    assert manifest['fps']==FPS and len(manifest['scenes'])==7
    assert manifest['captions'].endswith('captions_105_upper_scene05_v2.mov')
    assert not OUTPUT.exists(),f'Will not overwrite {OUTPUT}'
    SEGMENTS.mkdir(parents=True,exist_ok=True)
    pieces=[]; prior=0
    for i,scene in enumerate(manifest['scenes']):
        assert scene['start']==prior and scene['end']>prior
        frames=scene['end']-scene['start']; prior=scene['end']
        source=Path(scene['path']); assert source.is_file()
        segment=SEGMENTS/f'scene_{i+1:02}.mp4'; assert not segment.exists()
        zoom="min(1.0+on*0.00025,1.045)" if i%2==0 else "max(1.045-on*0.00025,1.0)"
        filt=f"scale=600:1067:force_original_aspect_ratio=increase,crop=600:1066,zoompan=z='{zoom}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=540x960:fps=30,format=yuv420p"
        run(['ffmpeg','-nostdin','-hide_banner','-loglevel','error','-n','-loop','1','-framerate','30','-i',str(source),'-vf',filt,'-frames:v',str(frames),'-an','-c:v','h264_videotoolbox','-b:v','2500k',str(segment)])
        pieces.append(segment)
    assert prior==manifest['frames']==1132
    listing=QC/'preview_segments.ffconcat'; assert not listing.exists()
    listing.write_text('ffconcat version 1.0\n'+''.join(f"file '{p}'\n" for p in pieces))
    captions=Path(manifest['captions']);assert captions.is_file()
    filt='[1:v]scale=540:960:flags=lanczos[cap];[0:v][cap]overlay=0:0:shortest=1:format=auto,format=yuv420p[v]'
    run(['ffmpeg','-nostdin','-hide_banner','-loglevel','error','-n','-f','concat','-safe','0','-i',str(listing),'-i',str(captions),'-filter_complex',filt,'-map','[v]','-frames:v',str(manifest['frames']),'-an','-c:v','h264_videotoolbox','-b:v','3000k','-movflags','+faststart',str(OUTPUT)])
    print(json.dumps({'output':str(OUTPUT),'width':540,'height':960,'fps':FPS,'frames':manifest['frames'],'audio':False,'purpose':'temporary visual QC preview'}))

if __name__=='__main__': main()
