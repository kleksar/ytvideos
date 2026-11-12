#!/usr/bin/env python3
"""Compose existing silent QC scene renders with the v3 caption layer."""
import subprocess
from pathlib import Path

QC=Path(__file__).resolve().parent
ROOT=QC.parents[1]
listing=QC/'preview_segments.ffconcat'
captions=ROOT/'Edit/Captions/captions_105_scenes05_06_v3.mov'
out=QC/'visual_preview_silent_v2.mp4'
assert listing.is_file() and captions.is_file() and not out.exists()
filt='[1:v]scale=540:960:flags=lanczos[cap];[0:v][cap]overlay=0:0:shortest=1:format=auto,format=yuv420p[v]'
subprocess.run(['ffmpeg','-nostdin','-hide_banner','-loglevel','error','-n','-f','concat','-safe','0','-i',str(listing),'-i',str(captions),'-filter_complex',filt,'-map','[v]','-frames:v','1132','-an','-c:v','h264_videotoolbox','-b:v','3000k','-movflags','+faststart',str(out)],check=True)
print(out)
