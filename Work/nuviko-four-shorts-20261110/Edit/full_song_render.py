"""Render the approved full-song contract in independently verifiable FFmpeg sections."""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import json
import math
import os
import subprocess
import sys

from full_song_plan import batch, edit, repo, run, read, write, sha

FPS = 30
FONT = '/System/Library/Fonts/Supplemental/Bradley Hand Bold.ttf'
name = sys.argv[1]
contract_path = edit/f'{name}-full-song-v01-contract.json'
plan = read(contract_path)
prefix = edit/f'{name}-full-song-v01'
folder = run/name
folder.mkdir(exist_ok=True)
width,height = plan['dimensions']
frames = plan['frames']
cuts = plan['transition_centres']
clips = plan['clips']
bounds = [0,*cuts,frames]
mask = folder/'mask.mov'
caption_plan = prefix.with_name(prefix.name+'-caption-plan.json')

def ffprobe(path):
    return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',path]))

def caption():
    if mask.exists() and caption_plan.exists():
        return
    if mask.exists():
        mask.rename(folder/'incomplete-mask.mov')
    cut_map = folder/'cuts.json'
    beat_map = folder/'beats.json'
    write(cut_map,{'fps':FPS,'cut_frames':cuts})
    beat_frames = {row['frame']:row for row in plan['caption_beats'] if row['strength']>=.70}
    beat_frames.update({row['frame']:row for row in plan['accents']})
    write(beat_map,{'fps':FPS,'candidates':list(beat_frames.values())})
    args=[sys.executable,str(repo/'automation/captions/music_lyrics.py'),plan['words'],
          '--font',FONT,'--font-size',str(plan['font_size']),'--output',str(mask),'--plan',str(caption_plan),
          '--offset','0','--frames',str(frames),'--fps',str(FPS),'--invert-masks','--max-words','1',
          '--tilt-every',str(plan['tilt_every']),'--motion-seed',str(plan['motion_seed']),
          '--beats',str(beat_map),'--cuts',str(cut_map),'--vocal-beat']
    write(folder/'caption-command.json',args)
    subprocess.run(args,check=True)
    print(name,'caption overlay',len(read(caption_plan)['groups']),flush=True)

def geometry(i):
    start,stop=bounds[i:i+2]
    return start-int(i>0),stop+2*int(i+1<len(clips))

def render_part(slot, first, stop, suffix=""):
    begin=bounds[first]-int(first>0)
    end=bounds[stop]-int(stop<len(clips))
    context=max(0,first-1)
    origin=geometry(context)[0]
    stem=f'part-{slot:03d}{suffix}'
    part=folder/f'{stem}.mp4'
    if part.exists():
        stream=ffprobe(part)['streams'][0]
        if int(stream['nb_frames'])!=end-begin:
            raise RuntimeError(f'{part} frame count')
        return part
    args=['ffmpeg','-nostdin','-n','-v','error','-filter_complex_threads','2']
    graph=[]
    for j,i in enumerate(range(context,stop)):
        clip=clips[i]
        head,tail=geometry(i)
        count=tail-head
        span=count/FPS
        args.extend(['-threads','1','-ss',str(clip['source_in']),'-t',f'{span+.16:.6f}','-i',clip['path']])
        horizontal = '(iw-ow)*0.60' if 'deer' in clip['path'] else '(iw-ow)/2'
        a,b = (.95,1.05) if i%2==0 else (1.05,.95)
        u=f'min(on/{count-1},1)'
        z=f'({a}+({b-a:.5f})*(0.7*{u}+0.3*{u}*{u}*(3-2*{u})))/0.95'
        graph.append(
            f"[{j}:v]trim=duration={span+.1:.6f},setpts=PTS-STARTPTS,{clip.get('pre_crop','')}"
            f"fps=30,scale={width}:{height}:force_original_aspect_ratio=increase:flags=bicubic,"
            f"crop={width}:{height}:x='{horizontal}':y='(ih-oh)/2',tpad=stop_mode=clone:stop_duration=0.25,"
            f"format=yuv420p,zoompan=z='{z}':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':d=1:s={width}x{height}:fps=30,"
            f"trim=end_frame={count},setsar=1,settb=1/30[v{i}]")
    active=f'v{context}'
    weight='if(gte(P,2/3),0.70*(1-P)*3,0.70+0.30*sin((1-P-1/3)*3*PI/4))'
    for i in range(context+1,stop):
        offset=(bounds[i]-1-origin)/FPS
        graph.append(f"[{active}][v{i}]xfade=transition=custom:expr='A*(1-({weight}))+B*({weight})':"
                     f"duration=0.1:offset={offset:.8f}[x{i}]")
        active=f'x{i}'
    commands=[]
    windows=[]
    for i in range(max(1,first),stop):
        centre=bounds[i]-begin
        windows.append(f'between(t,{(centre-1.1)/FPS:.8f},{(centre+2.1)/FPS:.8f})')
        for delta in (-1,0,1,2):
            when=max(0,(centre+delta-.5)/FPS)
            amount=.5+.5*math.cos(math.pi*delta/(1 if delta<0 else 2))
            commands += [f'{when:.8f} gblur@transition sigma {max(.01,12*amount):.6f}',
                         f'{when:.8f} eq@transition brightness {.068*amount:.6f}',
                         f'{when:.8f} eq@transition contrast {1-.15*amount:.6f}']
    color='eq=contrast=1.25:saturation=1.5'
    if commands:
        window='+'.join(windows)
        color+=(f",sendcmd=c='{' ; '.join(commands)}',gblur@transition=sigma=0.01:steps=1:enable='{window}',"
                f"eq@transition=contrast=1:brightness=0:enable='{window}'")
    area_w,area_h = (1194,512) if width==1440 else (896,384)
    contrast="127.5+107*(127.5-val)/127.5"
    mask_index=stop-context
    graph.extend([
        f"[{active}]trim=start_frame={begin-origin}:end_frame={end-origin},setpts=PTS-STARTPTS,{color},split[base][area]",
        f"[area]crop={area_w}:{area_h}:(iw-ow)/2:(ih-oh)/2,scale=in_color_matrix=bt709:in_range=tv:out_range=pc,format=gbrp,"
        f"lutrgb=r='{contrast}':g='{contrast}':b='{contrast}'[inversion]",
        '[inversion]scale=out_color_matrix=bt709:in_range=pc:out_range=tv,format=yuv420p[invyuv]',
        f'[{mask_index}:v]format=gbrp,extractplanes=g,scale={area_w}:{area_h}:flags=bicubic,gblur=sigma={1.65*width/1080:.3f}:steps=2,lut=y=val*0.94[alpha]',
        '[invyuv][alpha]alphamerge[layer]',
        '[base][layer]overlay=x=(W-w)/2:y=(H-h)/2:format=yuv420:repeatlast=0[video]',
    ])
    graph_path=folder/f'{stem}.ffgraph'
    graph_path.write_text(';\n'.join(graph)+'\n')
    scratch=folder/f'{stem}.partial.mp4'
    if scratch.exists(): scratch.rename(folder/f'{stem}.failed-{os.getpid()}.mp4')
    args.extend(['-threads','1','-ss',f'{begin/FPS:.8f}','-i',str(mask),'-filter_complex_script',str(graph_path),
                 '-map','[video]','-an','-frames:v',str(end-begin),'-r','30','-fps_mode','cfr','-c:v','libx264',
                 '-threads','3','-preset','superfast','-crf','18','-profile:v','high','-pix_fmt','yuv420p',
                 '-g','15','-bf','2','-color_range','tv','-colorspace','bt709','-color_primaries','bt709',
                 '-color_trc','bt709','-video_track_timescale','30000',str(scratch)])
    write(folder/f'{stem}-command.json',args)
    subprocess.run(args,check=True)
    stream=ffprobe(scratch)['streams'][0]
    if int(stream['nb_frames'])!=end-begin:
        raise RuntimeError(f'{scratch}: actual {stream["nb_frames"]}, expected {end-begin}')
    scratch.replace(part)
    print(name,'section',slot,'frames',begin,end,flush=True)
    return part

def main():
    output=Path(plan['output'])
    if '--replacement' in sys.argv:
        assert mask.is_file() and caption_plan.is_file()
        for slot in map(int,sys.argv[sys.argv.index('--replacement')+1:]):
            first=slot*9
            render_part(slot,first,min(first+9,len(clips)),'-replacement')
        return
    if output.exists():
        raise FileExistsError(output)
    if '--caption-only' in sys.argv:
        caption()
        return
    caption()
    if sha(plan['wav'])!=plan['pcm_sha256']:
        raise RuntimeError('Audio changed after planning')
    for clip in clips:
        if sha(clip['path'])!=clip['sha256']:
            raise RuntimeError(f"{clip['path']} changed after planning")
    chunk=9
    sections=[(i//chunk,i,min(i+chunk,len(clips))) for i in range(0,len(clips),chunk)]
    workers=int(os.environ.get('NUVIKO_FULL_SECTION_WORKERS','1'))
    with ThreadPoolExecutor(max_workers=workers) as pool:
        parts=list(pool.map(lambda args:render_part(*args),sections))
    concat=folder/'sections.ffconcat'
    entries = []
    for part, (_, first, stop) in zip(parts, sections):
        begin = bounds[first] - int(first > 0)
        end = bounds[stop] - int(stop < len(clips))
        entries.append(f"file '{part.name}'\nduration {(end-begin)/FPS:.9f}\n")
    concat.write_text('ffconcat version 1.0\n' + ''.join(entries))
    scratch=folder/'assembled.partial.mp4'
    if scratch.exists(): scratch.rename(folder/f'assembled.failed-{os.getpid()}.mp4')
    cmd=['ffmpeg','-nostdin','-n','-v','error','-f','concat','-safe','0','-i',str(concat),'-i',plan['wav'],
         '-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','aac','-b:a','256k','-ar','44100',
         '-movflags','+faststart','-video_track_timescale','30000',str(scratch)]
    write(folder/'assemble-command.json',cmd)
    subprocess.run(cmd,check=True)
    streams=ffprobe(scratch)['streams']
    if int(streams[0]['nb_frames'])!=frames:
        raise RuntimeError(f"{scratch}: actual {streams[0]['nb_frames']}, expected {frames}")
    scratch.replace(output)
    print(name,'exported',output,flush=True)

if __name__=='__main__':
    main()
