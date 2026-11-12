import importlib.util
import json
import subprocess
from pathlib import Path

root = Path('/Users/diplomat/ytvideos')
episode = root / 'new_channel/videos/038_uss_lincoln_pattaya'
run = episode / 'Work/nuviko-background-transparency-20-review'
picture = episode / 'Work/ffmpeg-subtitles-auto-v11/scratch/render/picture.mp4'
audio = episode / 'Work/ffmpeg-short-v05/accepted_mix_1.1x.wav'
words = episode / 'Edit/ffmpeg/words_auto_v07_1p1.json'
spec = importlib.util.spec_from_file_location('montage', root / 'automation/ffmpeg_montage/montage.py')
montage = importlib.util.module_from_spec(spec)
spec.loader.exec_module(montage)

for form, canvas in [('short', (1440, 2560)), ('long', (2560, 1440))]:
    for channel in ('nuviko',):
        name = f'{channel}_{form}'
        work = run / 'scratch' / name
        work.mkdir(exist_ok=True)
        plan = {'channel': channel, 'format': form, 'subtitles': {'mode': 'words', 'words': str(words), 'style': {'background': '#20252BCC'}}}
        output = run / 'previews' / f'{name}.mp4'
        if output.exists():
            continue
        subtitles, top = montage.caption_sequence(plan, root, work, canvas, 1800)
        # In the horizontal comparison, extend the vertical picture with a
        # blurred full-frame copy while retaining the complete original view.
        if form == 'long':
            background = '[0:v]split=2[base][portrait];[base]scale=320:568,crop=320:180,boxblur=5:2,scale=2560:1440[blur];[portrait]scale=810:1440[center];[blur][center]overlay=875:0[scene];'
        else:
            background = '[0:v]null[scene];'
        filters = background + f'[1:v]fps=30,format=rgba[subs];[scene][subs]overlay=0:{top}:eof_action=pass:format=auto,setsar=1,format=yuv420p[vout]'
        cmd = ['ffmpeg', '-hide_banner', '-loglevel', 'error', '-n', '-i', str(picture), '-f', 'concat', '-safe', '0', '-i', str(subtitles), '-i', str(audio), '-filter_complex', filters, '-map', '[vout]', '-map', '2:a:0', '-c:v', 'h264_videotoolbox', '-b:v', '20M', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k', '-t', '60', '-movflags', '+faststart', str(output)]
        (work / 'command.json').write_text(json.dumps(cmd, indent=2) + '\n')
        print(f'RENDERING {name}', flush=True)
        subprocess.run(cmd, check=True)
        print(f'RENDERED {output}', flush=True)
