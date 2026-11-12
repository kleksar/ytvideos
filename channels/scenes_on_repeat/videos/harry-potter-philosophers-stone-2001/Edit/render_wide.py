"""Reframe the final trailer for the compilation using the same source edit."""
import json
import sys
from pathlib import Path
from tempfile import TemporaryDirectory
from concurrent.futures import ThreadPoolExecutor
from render_package import EPISODE, FILM, FPS, clip, captions

slug = sys.argv[1]
work = EPISODE/'Work'/slug
delivery = EPISODE/'Deliverables'/slug
plan = json.loads((work/'timeline.json').read_text())
shots, groups, frames = (plan[k] for k in ('shots','groups','frames'))
out = delivery/f'{slug}-compilation-block.mp4'

def render(shot, temp, overlays):
    first, last = shot['start_frame'], shot['end_frame']
    seek = shot['in']-.08
    graph = [f'[0:v:0]trim=start=0.0795:end={shot["out"]-seek-.0005:.8f},setpts=PTS-STARTPTS,'
             f'fps={FPS},tpad=stop=2:stop_mode=clone,setsar=1,pad=1920:1080:0:140,'
             'eq=saturation=1.25[wide]']
    args = [*clip.FFMPEG,'-threads','2','-ss',f'{seek:.8f}','-i',FILM]
    label='wide'
    index=0
    for a,b,_,_,path in overlays:
        a,b=max(0,a-first),min(last-first,b-first)
        if a>=b:
            continue
        args.extend(['-i',path])
        index+=1
        new=f'overlay{index}'
        graph.append(f"[{label}][{index}:v]overlay=x=420:y=812:enable='between(n,{a},{b-1})'[{new}]")
        label=new
    graph.append(f'[{label}]format=yuv420p[v]')
    target=temp/f"shot-{shot['number']:03}.mp4"
    clip.run([*args,'-filter_complex_threads','2','-filter_complex',';'.join(graph),'-map','[v]',
              '-an','-frames:v',last-first,'-c:v','libx264','-threads','2','-preset','veryfast','-crf','18',
              '-video_track_timescale','24000','-color_primaries','bt709','-color_trc','bt709',
              '-colorspace','bt709',target])
    assert int(clip.probe(target)['streams'][0]['nb_frames'])==last-first
    return target

with TemporaryDirectory(prefix='wide-',dir=work) as directory:
    temp=Path(directory)
    overlays=captions(groups,temp,frames)
    with ThreadPoolExecutor(max_workers=3) as pool:
        clips=list(pool.map(lambda shot:render(shot,temp,overlays),shots))
    concat=temp/'shots.ffconcat'
    concat.write_text('ffconcat version 1.0\n'+''.join(
        f"file '{path.name}'\nduration {(shot['end_frame']-shot['start_frame'])/FPS:.9f}\n"
        for path,shot in zip(clips,shots)))
    clip.run([*clip.FFMPEG,'-n','-f','concat','-i',concat,'-i',delivery/(slug+'.mp4'),
              '-map','0:v:0','-map','1:a:0','-c','copy','-movflags','+faststart+write_colr',out])
    clip.run([*clip.FFMPEG,'-i',out,'-map','0:v:0','-map','0:a:0','-f','null','-'])
print(out)
