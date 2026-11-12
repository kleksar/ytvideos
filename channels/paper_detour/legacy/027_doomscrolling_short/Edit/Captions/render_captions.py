#!/usr/bin/env python3
"""Generate 30 fps transparent captions and SRT from ElevenLabs word alignment.

The source voice has already been sped up once using atempo=1.05.  This script
maps original alignment times by 1/1.05; auditory sync still needs review.
"""
import json
import math
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'Edit/Captions'
VOICE = ROOT / 'Source/Voice'
FPS, SPEED = 30, 1.05
W, H = 1080, 1920
FONT = '/System/Library/Fonts/Supplemental/Arial Bold.ttf'
SPEECH = VOICE / 'voice_en_105.wav'
GROUP_TEXT = '''You open the|news for one|minute|Twenty minutes later|you’re still scrolling|But the urge|to check|is older|than your phone|In seventeen ten|the English|satirical magazine|The Tatler|described a man|who rose|before dawn|to read|political news|He was a|character in a|satire|But the question|feels familiar|what happened|while I wasn’t|looking|Today the updates|never seem to|end|So try this|before you scroll|choose one question|you want answered|Find a reliable|source|Then decide|when to check|again|The world will|keep making news|Your life will|keep happening too'''

def stamp(seconds):
    ms = round(seconds * 1000)
    return f'{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02},{ms%1000:03}'

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    frames_dir = OUT / 'frames'
    frames_dir.mkdir(exist_ok=True)
    words = json.loads((VOICE / 'voice_en.words.json').read_text())['words']
    spec = [s.split() for s in GROUP_TEXT.split('|')]
    flat = [w for g in spec for w in g]
    assert flat == [w['text'] for w in words], 'Manual group plan differs from alignment'
    assert all(1 <= len(g) <= 3 for g in spec)
    p = subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','default=nw=1:nk=1',str(SPEECH)],capture_output=True,text=True,check=True)
    duration = float(p.stdout)
    frames = math.ceil(duration * FPS)
    # Each displayed run starts at the closest 30 fps frame to its aligned word.
    groups, seq, wi = [], [], 0
    blank = frames_dir / 'blank.png'
    if not blank.exists():
        Image.new('RGBA',(W,H),(0,0,0,0)).save(blank)
    if round(words[0]['start_seconds'] / SPEED * FPS) > 0:
        seq.append((blank,round(words[0]['start_seconds'] / SPEED * FPS)))
    for gi, tokens in enumerate(spec):
        count = len(tokens)
        start = max(0,round(words[wi]['start_seconds'] / SPEED * FPS))
        # Caption disappears near last spoken word; short intra-group gaps remain visible.
        end = min(frames,max(start+1,round((words[wi+count-1]['end_seconds'] / SPEED + 0.09)*FPS)))
        next_start = min(frames,round(words[wi+count]['start_seconds'] / SPEED * FPS)) if wi+count < len(words) else frames
        end = min(end,next_start)
        assert end > start, (gi,tokens,start,end,next_start)
        groups.append({'text':' '.join(tokens),'start_frame':start,'end_frame':end,'words':[]})
        # Fix all word origins for the full group; changing active word never moves neighbors.
        font_size = 76
        while True:
            font=ImageFont.truetype(FONT,font_size)
            widths=[font.getlength(t.upper()) for t in tokens]
            space=font.getlength(' ')
            total=sum(widths)+space*(len(tokens)-1)
            if total<=960 or font_size<=42: break
            font_size-=2
        assert total<=960
        left=(W-total)/2
        positions=[]
        for width in widths:
            positions.append(left)
            left += width+space
        for j,token in enumerate(tokens):
            current = max(start,round(words[wi+j]['start_seconds'] / SPEED * FPS))
            finish = end if j==count-1 else max(current+1,round(words[wi+j+1]['start_seconds'] / SPEED * FPS))
            finish=min(finish,end)
            if finish<=current: continue
            image=Image.new('RGBA',(W,H),(0,0,0,0)); draw=ImageDraw.Draw(image)
            for k,tok in enumerate(tokens):
                draw.text((round(positions[k]),1410),tok.upper(),font=font,fill=(255,223,38,255) if j==k else (255,255,255,255),stroke_width=5,stroke_fill=(0,0,0,240))
            target=frames_dir / f'{gi:02}_{j}.png'
            if not target.exists(): image.save(target)
            seq.append((target,finish-current))
            groups[-1]['words'].append({'word':token,'start_frame':current,'end_frame':finish})
        if next_start>end: seq.append((blank,next_start-end))
        wi += count
    assert sum(n for _,n in seq)==frames, (sum(n for _,n in seq),frames)
    srt=VOICE / 'voice_en_105.en.srt'
    # Frames 515..754 correspond to the telephone shot; 755..978 to writing.
    # Move the whole text region to each shot's safe band, retaining active
    # word and each word's X coordinate. Split runs on scene boundaries.
    upper_dir = OUT / 'frames_upper_scene05'
    upper_dir.mkdir(exist_ok=True)
    upper_cache = {}
    def upper(path):
        if path == blank:
            return blank
        if path not in upper_cache:
            original = Image.open(path).convert('RGBA')
            moved = Image.new('RGBA',(W,H),(0,0,0,0))
            moved.paste(original.crop((0,1360,W,1600)),(0,700))
            target = upper_dir / path.name
            if not target.exists(): moved.save(target)
            upper_cache[path] = target
        return upper_cache[path]
    middle_dir = OUT / 'frames_middle_scene06'
    middle_dir.mkdir(exist_ok=True)
    middle_cache = {}
    def middle(path):
        if path == blank:
            return blank
        if path not in middle_cache:
            original = Image.open(path).convert('RGBA')
            moved = Image.new('RGBA',(W,H),(0,0,0,0))
            moved.paste(original.crop((0,1360,W,1600)),(0,950))
            target = middle_dir / path.name
            if not target.exists(): moved.save(target)
            middle_cache[path] = target
        return middle_cache[path]
    reflowed=[]
    current=0
    for path,count in seq:
        finish=current+count
        stops=sorted({current,finish,*[b for b in (515,755,979) if current < b < finish]})
        for a,b in zip(stops,stops[1:]):
            shot_path=upper(path) if 515 <= a < 755 else middle(path) if 755 <= a < 979 else path
            reflowed.append((shot_path,b-a))
        current=finish
    seq=reflowed
    assert sum(n for _,n in seq)==frames
    (OUT/'caption_plan_scenes05_06_v3.json').write_text(json.dumps({'fps':FPS,'frames':frames,'duration_audio':duration,'speed':SPEED,'font':FONT,'font_colour_active':'yellow','caption_top_px':1410,'shot_position_overrides':[{'start_frame':515,'end_frame':755,'caption_top_px':750},{'start_frame':755,'end_frame':979,'caption_top_px':1000}],'groups':groups},ensure_ascii=False,indent=2)+'\n')
    concat=OUT/'runs_scenes05_06_v3.ffconcat'
    concat.write_text('ffconcat version 1.0\n'+''.join(f"file '{p}'\noption framerate 30\nduration {n/FPS:.9f}\n" for p,n in seq)+f"file '{seq[-1][0]}'\noption framerate 30\n")
    out=OUT/'captions_105_scenes05_06_v3.mov'
    subprocess.run(['ffmpeg','-nostdin','-hide_banner','-loglevel','error','-n','-f','concat','-safe','0','-i',str(concat),'-an','-vf','fps=30,format=yuva444p10le','-frames:v',str(frames),'-c:v','prores_ks','-profile:v','4444',str(out)],check=True)
    print(json.dumps({'frames':frames,'duration_audio':duration,'groups':len(groups),'words':wi,'srt':str(srt),'overlay':str(out)}))

if __name__=='__main__': main()
