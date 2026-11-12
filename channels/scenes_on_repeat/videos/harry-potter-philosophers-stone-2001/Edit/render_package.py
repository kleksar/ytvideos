"""Render one frozen Scenes on Repeat edit from its source ranges."""
import json
import math
import sys
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

import numpy as np

EPISODE = Path(__file__).resolve().parents[1]
ROOT = EPISODE.parents[3]
sys.path[:0] = [str(ROOT/'channels/scenes_on_repeat/automation/pipeline'),
                str(ROOT/'automation/ffmpeg_montage')]
import render_clip as clip
from caption_groups import resolve_groups
from montage import draw_caption_state

FPS, RATE = 24, 48000
MASTERS_AUDIO_FILTER = 'acompressor=threshold=0.16:ratio=3:attack=5:release=130,volume=1.55,alimiter=limit=0.82:attack=5:release=60:level=false:latency=true'
FILM = Path.home()/'Downloads'/'Harry.Potter.and.the.Sorcerer’s.Stone.2001.Extended.Cut.BDRip.1080p-SOFCJ.mkv'
POSTER = EPISODE/'Assets/poster.jpg'
PICTURE_LAYERS = clip.live_picture_layers

def layers(picture):
    graph = PICTURE_LAYERS(picture)
    graph[1] = graph[1].replace('brightness=-0.18', 'brightness=-0.035')
    graph.insert(-1, '[foreground]eq=saturation=1.25[grade]')
    graph[-1] = graph[-1].replace('[foreground]', '[grade]')
    return graph

def freeze(spec):
    cursor, runs, shots = 0, {}, []
    for i, shot in enumerate(spec['shots'], 1):
        start, end = shot['in'], shot['out']
        frames = round((end-start)*FPS)
        shots.append(dict(shot, number=i, start_frame=cursor, end_frame=cursor+frames,
                          picture_width=1920, picture_height=800, crop_x=shot['x']//2*2, crop_y=shot['y']//2*2))
        label = shot.get('sound')
        if label and 'audio_in' in shot:
            start, end = shot['audio_in'], shot['audio_in']+(end-start)
        if label:
            if label not in runs:
                runs[label] = [start, cursor, frames, end]
            else:
                run = runs[label]
                assert run[3] == start and run[1]+run[2] == cursor
                run[2] += frames
                run[3] = end
        cursor += frames
    groups, lines = [], []
    for label, tokens, phrases in spec['speech']:
        start, pos, frames, end = runs[label]
        words = []
        for token, a, b in tokens:
            assert start <= a < b <= end, (token, a, b, start, end)
            words.append(dict(text=token,start=a-start+pos/FPS,end=b-start+pos/FPS))
        groups.extend(resolve_groups(words,phrases))
        cue = []
        def finish():
            first, last = cue[0]['start'], cue[-1]['end']
            lines.append(dict(start_frame=round(first*FPS),end_frame=round(last*FPS),
                              text=' '.join(w['text'] for w in cue)))
        for word in words:
            text = ' '.join(w['text'] for w in cue+[word])
            if cue and (len(text)>42 or cue[-1]['text'].endswith(('.', '!', '?'))
                        or word['start']-cue[-1]['end']>.65):
                finish()
                cue = []
            cue.append(word)
        if cue:
            finish()
    return shots, runs, groups, lines, cursor

def captions(groups, work, frames):
    profile = dict(background=None, outline='#11151B', highlight='#FF302A', text='#F9EED6')
    font = clip.get_font(66, 'bold')
    overlays = []
    for i, group in enumerate(groups):
        next_frame = round(groups[i+1][0]['start']*FPS) if i+1 < len(groups) else frames
        end_frame = min(next_frame, round((group[-1]['end']+.08)*FPS),frames)
        points = [round(w['start']*FPS) for w in group]+[end_frame]
        for j,(a,b) in enumerate(zip(points,points[1:])):
            assert a<b, (group,a,b)
            path = work/f'caption-{i:03}-{j}.png'
            im = draw_caption_state([w['text'] for w in group], j, size=(1080,160),
                                    center_x=540, baseline=103, font=font, profile=profile, pad_x=0, stroke=3)
            im.save(path,compress_level=1)
            overlays.append((a,b,0,880,path))
    return overlays

def pcm(path, stream, start, seconds):
    raw = clip.run([*clip.FFMPEG,'-ss',f'{start:.6f}','-i',path,'-t',f'{seconds:.6f}',
                    '-map',f'0:{stream}','-ac','2','-ar',RATE,'-f','f32le','-'],capture_output=True).stdout
    return np.frombuffer(raw,dtype='<f4').reshape(-1,2).copy()

def film_only(spec, runs, frames):
    """Keep film audio across each shot and overlap handles at source jumps."""
    size = frames*RATE//FPS
    audio = np.zeros((size, 2), np.float32)
    # A 75 ms overlap is centered at each cut. Audio stays at its timeline position.
    half = round(.0375*RATE)
    fade = np.linspace(0, 1, 2*half, dtype=np.float32)[:, None]
    cursor = 0
    for label, (start, pos, count, _) in runs.items():
        a, b = pos*RATE//FPS, (pos+count)*RATE//FPS
        assert a == cursor, (label, a, cursor)
        pre, post = (half if a else 0), (half if b<size else 0)
        n = b-a+pre+post
        take = pcm(FILM,4,start-pre/RATE,n/RATE+.04)
        assert len(take)>=n, (label, len(take), n)
        take = take[:n] * spec.get('film_gains',{}).get(label,1)
        take[:2*half] *= fade
        if post:
            take[-2*half:] *= fade[::-1]
        else:
            tail = min(len(take),round(.55*RATE))
            take[-tail:] *= np.linspace(1,0,tail,dtype=np.float32)[:,None]
        audio[a-pre:b+post] += take
        cursor = b
    assert cursor == size
    return audio

def mix(spec, runs, groups, frames, work):
    size = frames*RATE//FPS
    if spec.get('film_only'):
        path = work/'mix.f32le'
        film_only(spec,runs,frames).astype('<f4').tofile(path)
        return path
    film = np.zeros((size,2),np.float32)
    fade = int(.075*RATE)
    ramp = np.linspace(0,1,fade,dtype=np.float32)[:,None]
    for start, pos, count, end in runs.values():
        n = count*RATE//FPS
        take = pcm(FILM,4,start,n/RATE)[:n]
        assert len(take) >= n-48
        if len(take) < n:
            take = np.pad(take,((0,n-len(take)),(0,0)))
        take[:fade] *= ramp
        take[-fade:] *= ramp[::-1]
        a = pos*RATE//FPS
        film[a:a+n] = take
    music = spec['music']
    bed = pcm(Path.home()/'Downloads'/music['file'],0,music['start'],size/RATE)[:size]
    assert len(bed) == size
    time = np.arange(size)/RATE
    env = np.ones(size,dtype=np.float32)
    for group in groups:
        a,b = group[0]['start'],group[-1]['end']
        env = np.minimum(env,np.interp(time,[a-.18,a,b,b+.25],[1,.38,.38,1]))
    env *= np.minimum(1,time/.28)*np.minimum(1,(size/RATE-time)/1.15)
    audio = film+bed*(music['gain']*env[:,None])
    peak = float(np.abs(audio).max())
    if peak>.85:
        audio *= .85/peak
    path = work/'mix.f32le'
    audio.astype('<f4').tofile(path)
    return path

def main(spec_file):
    spec = json.loads(spec_file.read_text())
    work = EPISODE/'Work'/spec['slug']
    out_dir = EPISODE/'Deliverables'/spec['slug']
    work.mkdir(parents=True,exist_ok=True)
    out_dir.mkdir(parents=True,exist_ok=True)
    output = out_dir/(spec['slug']+'.mp4')
    assert not output.exists(),output
    shots,runs,groups,lines,frames = freeze(spec)
    (work/'timeline.json').write_text(json.dumps(dict(shots=shots,runs=runs,groups=groups,
             frames=frames,streams={'video':0,'audio':4,'subtitles':9}),ensure_ascii=False,indent=2)+'\n')
    overlays = captions(groups,work,frames)
    clip.live_picture_layers = layers
    def render(shot):
        existing = work/f"shot-{shot['number']:03d}.mp4"
        if existing.exists():
            assert int(clip.probe(existing)['streams'][0]['nb_frames']) == shot['end_frame']-shot['start_frame']
            return existing
        # The outgoing frame can otherwise land on the next native shot after CFR rounding.
        next_shot = shots[shot['number']] if shot['number'] < len(shots) else None
        guard = (next_shot and shot.get('sound') and shot.get('sound') == next_shot.get('sound')
                 and (shot['crop_x'], shot['crop_y']) != (next_shot['crop_x'], next_shot['crop_y']))
        picture = dict(shot, out=shot['out']-1/FPS) if guard else shot
        return clip.render_shot(str(FILM),0,[1920,800,(0,0,1920,800)],picture,overlays,work)
    with ThreadPoolExecutor(max_workers=3) as pool:
        paths = list(pool.map(render,shots))
    concat = work/'shots.ffconcat'
    concat.write_text('ffconcat version 1.0\n'+''.join(
        f"file '{path.name}'\nduration {(shot['end_frame']-shot['start_frame'])/FPS:.9f}\n"
        for path,shot in zip(paths,shots)))
    base = work/'base.mp4'
    mix_file = mix(spec,runs,groups,frames,work)
    clip.run([*clip.FFMPEG,'-y','-f','concat','-i',concat,'-f','f32le','-ar',RATE,'-ac','2','-i',mix_file,
              '-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','aac','-b:a','256k',
              '-af',MASTERS_AUDIO_FILTER,
              '-metadata:s:a:0','language=eng','-video_track_timescale','24000',base])
    for path in paths+[mix_file]:
        path.unlink()
    cta_root = EPISODE/'Work'/'shared-cta'
    cta_root.mkdir(exist_ok=True)
    cta_record = cta_root/'receipt.json'
    if not cta_record.exists():
        cta, record = clip.prepare_cta_motion(clip.DEFAULT_CTA,cta_root)
        cta_record.write_text(json.dumps(record,indent=2))
    else:
        cta, record = cta_root/'cta-motion.mov', json.loads(cta_record.read_text())
    details = work/'details.png'
    clip.make_film_details(details,dict(title="Harry Potter and the Philosopher's Stone",year='2001',
                          genre='Fantasy adventure',runtime='159 min • Extended',cast='Daniel Radcliffe'))
    poster_record = clip.run([sys.executable,clip.POSTER_TOOL,base,output,POSTER,
              '--picture-top',f'{frames-120}:640','--details-overlay',details,
              '--subscribe-overlay',cta,*record['overlay_position']],capture_output=True)
    (work/'poster-receipt.json').write_bytes(poster_record.stdout)
    base.unlink()
    if lines:
        clip.write_srt(output.with_suffix('.en.srt'),lines,frames)
    print(output,flush=True)

if __name__ == '__main__':
    main(Path(sys.argv[1]))
