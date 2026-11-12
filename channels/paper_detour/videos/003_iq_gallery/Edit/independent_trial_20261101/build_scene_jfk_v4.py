"""Build a standalone layered JFK scene; no Palmier writes or generated sound.

Scene layout and sources are in the adjacent JSON. Input images are never
modified. This is a creative test and must pass independent visual review.
"""
import json
import pathlib
import subprocess

here = pathlib.Path(__file__).resolve().parent
m = json.loads((here / 'scene_jfk_v4_manifest.json').read_text())
paths = [m['background'], m['midground'], m['foreground'], m['name'], m['iq'], *m['digits']]
args = ['ffmpeg', '-hide_banner', '-loglevel', 'error', '-filter_complex_threads', '1']
for path in paths:
    args += ['-loop', '1', '-framerate', '30', '-t', '4.6', '-i', path]
args += ['-stream_loop', '-1', '-t', '4.6', '-i', m['grain'], '-i', m['audio_reference']]
f = []
def add(s): f.append(s)
add("[0:v]scale=564:1002,crop=540:960:x='12-6*t/4.6':y=21,setsar=1[bg]")
# Each layer has its own trajectory; subject and its table/hand form one unit.
add("[1:v]scale=564:1002,format=rgba[person]")
add("[2:v]scale=564:1002,format=rgba[foreground]")
# Large words start below the left foreground camera and move into clear air;
# draw text before the subject and foreground to make overlap physically real.
add("[3:v]scale=w='trunc(405*(1+0.03*sin(2*PI*t/6.0))/2)*2':h='trunc(138*(1+0.03*sin(2*PI*t/6.0))/2)*2':eval=frame,format=rgba,pad=430:160:(ow-iw)/2:(oh-ih)/2:color=0x00000000,rotate=a='0.0209*sin(2*PI*t/6.0)':ow=450:oh=180:c=none,fade=t=in:st=0.45:d=0.75:alpha=1[name]")
add("[bg][name]overlay=x='30+2*sin(t*0.8)':y='490-385*pow(clip((t-0.45)/0.8,0,1),2)*(3-2*clip((t-0.45)/0.8,0,1))+2*sin(2*PI*t/6.0)':format=auto[bname]")
last = 'bname'
xs = [28,132,185,240]
for j, idx in enumerate([4,5,6,7]):
    w, h = ((132,88) if j == 0 else (91,87))
    # Fixed padding keeps output dimensions stable when the paper glyph breathes.
    pad_w, pad_h = (146,104) if j == 0 else (104,101)
    ow, oh = (160,118) if j == 0 else (118,115)
    phase = j * 0.65
    add(f"[{idx}:v]scale=w='trunc({w}*(1+0.03*sin(2*PI*t/6.0+{phase}))/2)*2':h='trunc({h}*(1+0.03*sin(2*PI*t/6.0+{phase}))/2)*2':eval=frame,format=rgba,pad={pad_w}:{pad_h}:(ow-iw)/2:(oh-ih)/2:color=0x00000000,rotate=a='0.0209*sin(2*PI*t/6.0+{phase})':ow={ow}:oh={oh}:c=none,fade=t=in:st=0.45:d=0.75:alpha=1[g{j}]")
    y = f"570-365*pow(clip((t-0.45)/0.8,0,1),2)*(3-2*clip((t-0.45)/0.8,0,1))+1.5*sin(2*PI*t/6.0+{phase})"
    add(f"[{last}][g{j}]overlay=x='{xs[j]}+1.0*sin(2*PI*t/6.0+{phase})':y='{y}':format=auto[text{j}]")
    last = f'text{j}'
add(f"[{last}][person]overlay=x='-12-7*t/4.6':y=-21:format=auto[withperson]")
add("[withperson][foreground]overlay=x='-12+10*t/4.6':y=-21:format=auto[scene]")
add("[8:v]scale=540:960,format=rgba,colorchannelmixer=aa=0.4[grain]")
add("[scene][grain]overlay=0:0:format=auto,format=yuv420p[video]")
args += ['-filter_complex', ';'.join(f), '-map', '[video]', '-map', '9:a:0',
         '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '22', '-c:a', 'copy',
         '-t', '4.6', '-movflags', '+faststart', '-n', str(here / 'jfk_layered_scene_trial_v4.mp4')]
subprocess.run(args, check=True)
