#!/usr/bin/env python3
"""Render exact-word Russian captions as a transparent QuickTime overlay.
Source text and word timings are kept in this folder for revision."""
import bisect, difflib, json, re, subprocess, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).parent
FPS, FRAMES = 30, 2489
W, H = 1080, 1920
FONT = '/System/Library/Fonts/HelveticaNeue.ttc'
FONT_BOLD = '/System/Library/Fonts/HelveticaNeue.ttc'
FONT_INDEX = 9  # Helvetica Neue Condensed Black; inspected with Russian Cyrillic
TEXT = (ROOT/'voice_original.txt').read_text(encoding='utf-8').strip()
data=json.loads((ROOT/'voice_115.json').read_text(encoding='utf-8'))
src=[w for seg in data['segments'] for w in seg['words']]
# Keep em dashes attached to the following spoken word so they're punctuation, not a cue word.
# Keep an em dash with the preceding spoken word, so a 3–4-word cue never opens on a dash.
target=re.findall(r'\w+(?:[-‑]\w+)*(?:\s+—)?[.,!?…:;]*|—\s*\w+(?:[-‑]\w+)*[.,!?…:;]*', TEXT, flags=re.UNICODE)
def norm(s): return re.sub(r'[^а-яё0-9]','',s.lower())
sm=difflib.SequenceMatcher(None,[norm(w['word'].strip()) for w in src],[norm(x) for x in target],autojunk=False)
words=[]
for op,a,b,c,d in sm.get_opcodes():
    S,T=src[a:b],target[c:d]
    if op=='equal':
        for sw,tw in zip(S,T): words.append({'word':tw,'start':sw['start'],'end':sw['end']})
    elif op=='replace':
        if len(S)==len(T):
            for sw,tw in zip(S,T): words.append({'word':tw,'start':sw['start'],'end':sw['end']})
        elif len(S)==2 and len(T)==1: # e.g. Whisper split a hyphenated word
            words.append({'word':T[0],'start':S[0]['start'],'end':S[-1]['end']})
        elif len(S)==1 and len(T)==2: # split a fused spoken phrase
            sw=S[0]; cut=sw['start']+(sw['end']-sw['start'])*len(norm(T[0]))/(len(norm(T[0]))+len(norm(T[1])))
            words.extend([{'word':T[0],'start':sw['start'],'end':cut},{'word':T[1],'start':cut,'end':sw['end']}])
        elif len(S)==2 and len(T)==3: # corrected phrase "а на ней" vs ASR "она не"
            st,en=S[0]['start'],S[-1]['end']; weights=[max(1,len(norm(t))) for t in T]; total=sum(weights); cur=st
            for j,(tw,weight) in enumerate(zip(T,weights)):
                nxt=en if j==len(T)-1 else cur+(en-st)*weight/total
                words.append({'word':tw,'start':cur,'end':nxt}); cur=nxt
        else:
            raise ValueError(f'Unresolved text/timing alignment: {op}, {[x["word"] for x in S]} -> {T}')
    elif op=='delete':
        raise ValueError(f'Original wording omits spoken token(s): {[x["word"] for x in S]}')
    elif op=='insert':
        raise ValueError(f'Original wording contains unaligned token(s): {T}')
if len(words)!=len(target): raise AssertionError((len(words),len(target)))
# Keep orthographic hyphens inside compound words; discard punctuation dashes.
# A dash between separate words is never part of the displayed caption.
def display_word(word):
    word=word.replace('‐','-').replace('‑','-')
    word=re.sub(r'[‒–—]', ' ', word)
    word=re.sub(r'[^а-яёА-ЯЁ0-9\s-]', '', word)
    word=re.sub(r'(?<![а-яёА-ЯЁ0-9])-|-(?![а-яёА-ЯЁ0-9])', ' ', word)
    return re.sub(r'\s+', ' ', word).strip()

PREPOSITIONS={'в','во','на','к','ко','с','со','о','об','обо','от','ото','из','изо','у','по','для','за','до','над','под','при','без','между','через','про','ради','около','вокруг','перед','пред','после','вне','внутри','сквозь'}
def is_preposition(word):
    return norm(display_word(word)) in PREPOSITIONS
def bad_ending(word):
    return is_preposition(word) or norm(display_word(word)) in {'я','а','и','но','он','что','не'}

# Use punctuation in the source text only as hidden phrase boundaries so a
# following sentence's opening word never trails the previous phrase on screen.
sentences=[]; sentence=[]
for w in words:
    sentence.append(w)
    if re.search(r'[.!?…]$',w['word']):
        sentences.append(sentence); sentence=[]
if sentence: sentences.append(sentence)

# Full editorial cue plan: every line was reviewed against the entire spoken
# passage, not generated greedily and repaired one dangling word at a time.
TRACKING=1.5  # slightly increased letter spacing in 1080p canvas pixels
ACTIVE_SCALE=1.05  # smooth active-word pulse peaks at +5%; inactive words stay 105 px
WORD_GAP=32.5  # slightly wider than the preceding 27.5 px gap
measure_font=ImageFont.truetype(FONT,105,index=FONT_INDEX)
SPECIAL_SIZE={
    'КАК СТАРШАЯ СЕСТРА': 100,
    'НА СЛЕДУЮЩИЙ ДЕНЬ': 95,
    'И ПЫТАЛСЯ СДЕЛАТЬ': 100,
    'С ЕЁ ЛУЧШЕЙ ПОДРУГОЙ': 89,
    'СОБИРАЕТСЯ УЕЗЖАТЬ': 98,
}
def tracked_width(text,font):
    return font.getlength(text)+TRACKING*max(0,len(text)-1)
def cue_text(c):
    return ' '.join(display_word(w['word']).upper() for w in c)
plan=[line.strip() for line in (ROOT/'CAPTION_PLAN_v4.txt').read_text(encoding='utf-8').splitlines() if line.strip()]
expected=[display_word(w['word']).upper() for w in words]
actual=[token for line in plan for token in line.split()]
if actual!=expected:
    i=next((i for i,(a,b) in enumerate(zip(actual,expected)) if a!=b),min(len(actual),len(expected)))
    raise ValueError(f'Cue plan changes source word at position {i}: plan={actual[i:i+5]}, source={expected[i:i+5]} ({len(actual)} vs {len(expected)} words)')
chunks=[]; offset=0
for line in plan:
    tokens=line.split()
    c=words[offset:offset+len(tokens)]; offset+=len(tokens)
    if len(tokens)>3 and line not in {'С ЕЁ ЛУЧШЕЙ ПОДРУГОЙ','ДЕЛО НЕ В НЕЙ'}:
        raise ValueError(f'More than three words: {line}')
    cue_font=ImageFont.truetype(FONT,SPECIAL_SIZE.get(line,105),index=FONT_INDEX)
    widths=[tracked_width(token,cue_font) for token in tokens]
    peak=sum(widths)+WORD_GAP*(len(widths)-1)+(ACTIVE_SCALE-1)*max(widths)
    if peak>1000:
        raise ValueError(f'Cue exceeds safe width: {line} ({peak:.1f}px)')
    chunks.append(c)
# Consecutive cues touch exactly; the next cue starts on its first spoken word.
starts=[c[0]['start'] for c in chunks]
ends=[starts[i+1] if i+1<len(chunks) else c[-1]['end'] for i,c in enumerate(chunks)]
font=ImageFont.truetype(FONT,105,index=FONT_INDEX)
font_cache={105:font}
def scaled_font(size):
    size=max(89,min(111,size))
    if size not in font_cache:
        font_cache[size]=ImageFont.truetype(FONT,size,index=FONT_INDEX)
    return font_cache[size]
for c in chunks:
    line=' '.join(display_word(w['word']).upper() for w in c)
max_width=max(sum(tracked_width(display_word(w['word']).upper(),scaled_font(SPECIAL_SIZE.get(cue_text(c),105))) for w in c)+WORD_GAP*max(0,len(c)-1)+(ACTIVE_SCALE-1)*max(tracked_width(display_word(w['word']).upper(),scaled_font(SPECIAL_SIZE.get(cue_text(c),105))) for w in c) for c in chunks)
print(f'Words: {len(words)}; captions: {len(chunks)}; font: 105px Helvetica Neue Condensed Black (five local fit sizes); active scale: +5% smooth (orange word only); tracking: {TRACKING}px; word gap: {WORD_GAP}px; max line width: {max_width:.0f}px',flush=True)
# Save the exact cue map beside the renderer as a revisable, readable timing map.
def stamp(t):
    n=round(t*1000); h,n=divmod(n,3600000); m,n=divmod(n,60000); s,n=divmod(n,1000)
    return f'{h:02d}:{m:02d}:{s:02d},{n:03d}'
srt=[]
for i,c in enumerate(chunks,1): srt.extend([str(i),f'{stamp(starts[i-1])} --> {stamp(ends[i-1])}',' '.join(display_word(w['word']).upper() for w in c),''])
(ROOT/'voice_original_word_captions_safe_ui_v5.srt').write_text('\n'.join(srt),encoding='utf-8')
if __import__('os').environ.get('PLAN_ONLY')=='1': raise SystemExit(0)
# Transparent RGBA frames: white phrase, exact spoken word in warm yellow; smooth +5% active-word pulse.
cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-f','rawvideo','-pixel_format','rgba','-video_size',f'{W}x{H}','-framerate',str(FPS),'-i','pipe:0','-an','-c:v','qtrle','-pix_fmt','argb','-movflags','+faststart',str(ROOT/'voice_word_highlight_overlay_safe_ui_v5.mov')]
p=subprocess.Popen(cmd,stdin=subprocess.PIPE)
white=(255,255,255,255); yellow=(255,213,79,255); outline=(0,0,0,210)
y=round(H*0.40)  # above Shorts' right-hand action column and lower metadata
for frame in range(FRAMES):
    t=frame/FPS
    ci=bisect.bisect_right(starts,t)-1
    im=Image.new('RGBA',(W,H),(0,0,0,0))
    if ci>=0 and t<ends[ci]:
        c=chunks[ci]
        base_size=SPECIAL_SIZE.get(cue_text(c),105)
        base_font=scaled_font(base_size)
        active=-1
        for j,w in enumerate(c):
            if w['start']<=t<w['end']:
                active=j; break
        word_fonts=[]
        for j,w in enumerate(c):
            f=base_font
            if active==j:
                duration=max(0.001,w['end']-w['start'])
                progress=max(0.0,min(1.0,(t-w['start'])/duration))
                ramp=min(0.12,duration*0.45)
                if duration <= 2*ramp:
                    q=min(1.0,progress*2) if progress<=0.5 else min(1.0,(1-progress)*2)
                    eased=q*q*(3-2*q)
                elif progress < ramp/duration:
                    q=progress*duration/ramp
                    eased=q*q*(3-2*q)
                elif progress > 1-ramp/duration:
                    q=(1-progress)*duration/ramp
                    eased=q*q*(3-2*q)
                else:
                    eased=1.0
                f=scaled_font(int(base_size*(1+0.05*eased)+0.5))
            word_fonts.append(f)
        shown_words=[display_word(w['word']).upper() for w in c]
        # Layout is fixed from the base font for the entire cue. Only the orange
        # word changes its own glyph size; white words never scale or drift.
        base_widths=[tracked_width(shown_words[j],base_font) for j in range(len(c))]
        total=sum(base_widths)+WORD_GAP*(len(c)-1)
        x=(W-total)/2
        d=ImageDraw.Draw(im)
        for j,w in enumerate(c):
            f=word_fonts[j]
            center=x+base_widths[j]/2
            color=yellow if active==j else white
            shown=shown_words[j]
            total_word=tracked_width(shown,f)
            char_x=center-total_word/2
            for char in shown:
                cw=f.getlength(char)
                char_center=char_x+cw/2
                d.text((char_center,y),char,font=f,fill=color,anchor='mm',stroke_width=5,stroke_fill=outline)
                char_x+=cw+TRACKING
            x+=base_widths[j]+WORD_GAP
    try: p.stdin.write(im.tobytes())
    except BrokenPipeError: raise RuntimeError('ffmpeg closed the video pipe')
    if frame%300==0: print(f'Rendered {frame}/{FRAMES}',flush=True)
p.stdin.close()
code=p.wait()
if code: raise SystemExit(code)
print(ROOT/'voice_word_highlight_overlay_safe_ui_v5.mov')
