"""Independent 9-second layered technical motion trial, no Palmier edits.

Read the JSON manifest beside this script for editable paths, geometry, timing
and motion parameters. This is NOT a reconstructed Palmier project, a final
film, or an approved Paper Detour 004-style composition.
"""
import json
import pathlib
import subprocess

HERE = pathlib.Path(__file__).resolve().parent
M = json.loads((HERE / 'trial_manifest.json').read_text())
inputs = [M['background'], M['foreground'], *[s['portrait'] for s in M['scenes']],
          *[s['name_asset'] for s in M['scenes']], M['iq_asset'], *M['digit_assets'],
          M['grain'], M['audio_reference']]
args = ['ffmpeg', '-hide_banner', '-loglevel', 'error', '-filter_complex_threads', '1']
for p in inputs[:12]:
    args += ['-loop', '1', '-framerate', '30', '-t', '9', '-i', p]
args += ['-stream_loop', '-1', '-t', '9', '-i', inputs[12], '-i', inputs[13]]

filters = []
def add(s): filters.append(s)
# Each plane has independent motion; modest cropping provides safe overscan.
add("[0:v]scale=570:1014,crop=540:960:x='15+4*sin(t*0.32)':y='27+3*sin(t*0.21)',setsar=1[base]")
current = 'base'
transition = "if(lt(t,3.933333),0,if(lt(t,4.633333),(t-3.933333)*771.428571,540))"
tx = [f"-({transition})", f"540-({transition})"]
enabled = ["between(t,0,4.633333)", "gte(t,3.933333)"]
for i in range(2):
    # The paper character is one intact midground layer; no limb animation.
    add(f"[{2+i}:v]scale=400:600,format=rgba[person{i}]")
    add(f"[{current}][person{i}]overlay=x='70+({tx[i]})+3*sin(t*0.7+{i})':y='142+2*sin(t*0.43)':enable='{enabled[i]}':format=auto[personbase{i}]")
    current = f'personbase{i}'

# Preserve IQ and each digit as individual paper image layers. Their positions
# settle into compact rows; gentle independent angle and scale run in hold.
digit_x = [[77,209,273,344],[69,200,273,352]]
digit_indexes = [[6,7,8,9],[6,7,10,11]]
for i in range(2):
    local = f"(t-{4.633333*i})"
    for j in range(4):
        idx = digit_indexes[i][j]
        label = f'g{i}_{j}'
        # IQ uses the established paper glyph; the other three are 1/1/9 or 1/2/3.
        w, h = ((167,125) if j==0 else (113,101))
        angle = f"0.022*sin(2*PI*t/2.35+{j*0.8+i*0.3})"
        scale = f"(1+0.025*sin(2*PI*t/2.65+{j*0.6+i*0.3}))"
        add(f"[{idx}:v]scale=w='trunc({w}*{scale}/2)*2':h='trunc({h}*{scale}/2)*2':eval=frame,format=rgba,rotate=a='{angle}':ow=iw+12:oh=ih+12:c=none,fade=t=in:st={4.633333*i+0.5}:d=0.24:alpha=1[{label}]")
        # A hidden start is held below the foreground ledge and fades in as it rises.
        y = f"if(lt({local},0.5),704,if(lt({local},1.433333),704-224*({local}-0.5)/0.933333,480+2*sin(2*PI*t/2.4+{j*0.7})))"
        add(f"[{current}][{label}]overlay=x='{digit_x[i][j]}+({tx[i]})+2*sin(2*PI*t/2.65+{j*0.6})':y='{y}':enable='{enabled[i]}':format=auto[out{i}_{j}]")
        current = f'out{i}_{j}'

# Foreground covers the real rising layer. Name images are independent from it.
add("[1:v]scale=605:340,format=rgba[front]")
add(f"[{current}][front]overlay=x='-33-4*sin(t*0.32)':y=480:format=auto[withfront]")
current = 'withfront'
for i in range(2):
    # Whole-word labels retain their exact generated typography.
    add(f"[{4+i}:v]scale=w='trunc(378*(1+0.025*sin(2*PI*t/2.8+{i}))/2)*2':h='trunc(129*(1+0.025*sin(2*PI*t/2.8+{i}))/2)*2':eval=frame,format=rgba,rotate=a='0.017*sin(2*PI*t/2.8+{i})':ow=iw+12:oh=ih+12:c=none[name{i}]")
    add(f"[{current}][name{i}]overlay=x='81+({tx[i]})+2*sin(t*0.7+{i})':y='619+2*sin(t*0.85+{i})':enable='{enabled[i]}':format=auto[namebase{i}]")
    current = f'namebase{i}'
add("[12:v]scale=540:960,format=rgba,colorchannelmixer=aa=0.4[grain]")
add(f"[{current}][grain]overlay=0:0:format=auto,format=yuv420p[video]")
args += ['-filter_complex', ';'.join(filters), '-map', '[video]', '-map', '13:a:0',
         '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '22', '-c:a', 'copy',
         '-t', '9', '-movflags', '+faststart', '-n', str(HERE / 'two_scene_motion_trial.mp4')]
print('Rendering a standalone 9-second draft from unchanged sources...', flush=True)
subprocess.run(args, check=True)
