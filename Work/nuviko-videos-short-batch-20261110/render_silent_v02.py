import json
import subprocess
from pathlib import Path

root = Path('/Users/diplomat/ytvideos')
work = root / 'Work/nuviko-videos-short-batch-20261110'
source = root / 'Work/satisfying-runaway-pilot/Source'
shots = ['32509235.mp4', '6316369.mp4', '8859850.mp4', '34535413.mp4', '35867202.mp4', '36974946.mp4', '33353416.mp4']
frames_per_shot = 60
filters = []
for index, shot in enumerate(shots):
    filters.append(
        f"[{index}:v]fps=30,trim=start=1:duration=2,setpts=PTS-STARTPTS,"
        "scale=2160:3840:force_original_aspect_ratio=increase:flags=lanczos,"
        "crop=2160:3840,"
        f"zoompan=z='1+0.1*(1-cos(PI*on/{frames_per_shot - 1}))/2':"
        "x='(iw-iw/zoom)/2':y='(ih-ih/zoom)/2':d=1:s=1080x1920:fps=30,"
        f"setsar=1,setpts=PTS-STARTPTS[v{index}]"
    )
filters.append(''.join(f'[v{i}]' for i in range(len(shots))) + f'concat=n={len(shots)}:v=1:a=0,eq=contrast=1.25,unsharp=5:5:0.75:5:5:0.0,split[base][high]')
filters.append("[high]lutyuv=y='max(0,val-190)*3':u=128:v=128,gblur=sigma=24[glow]")
pulses = '+'.join(f'pow((1+cos(PI*min(abs(T*30-{n})/3.75,1)))/2,2)' for n in range(frames_per_shot, frames_per_shot * len(shots), frames_per_shot))
filters.append(f"[base][glow]blend=all_expr='min(255,A+B*0.8*({pulses}))',split[clean][blur_source]")
filters.append('[blur_source]gblur=sigma=12[blur]')
blur_pulses = '+'.join(f'((1+cos(PI*min(abs(T*30-{n})/7.5,1)))/2)' for n in range(frames_per_shot, frames_per_shot * len(shots), frames_per_shot))
filters.append(f"[clean][blur]blend=all_expr='A+(B-A)*0.55*({blur_pulses})',scale=1108:1936:flags=lanczos,crop=1080:1920:x='14+7*sin(n*4.3)*({blur_pulses.replace('T*30','n')})':y='8+4*cos(n*3.1)*({blur_pulses.replace('T*30','n')})',setsar=1[video]")
filter_path = work / 'silent-preview-v02.ffgraph'
filter_path.write_text(';\n'.join(filters) + '\n')
output = work / 'silent-preview-v02.mp4'
assert not output.exists()
argv = ['ffmpeg', '-nostdin', '-hide_banner', '-loglevel', 'error']
for shot in shots:
    argv += ['-i', str(source / shot)]
argv += ['-filter_complex_script', str(filter_path), '-map', '[video]', '-an', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', str(output)]
(work / 'silent-preview-v02.json').write_text(json.dumps({'kind':'draft silent preview', 'reason':'user requested no music for this clip', 'shots':shots, 'fps':30, 'frames_per_shot':frames_per_shot, 'output':str(output), 'transition':'highlight glow 125 ms each side; draft; no beat alignment without music', 'limitations':['subtitle animations not applicable to silent draft','transition timing is a visual rhythm without music'], 'argv':argv}, ensure_ascii=False, indent=2) + '\n')
subprocess.run(argv, check=True)
