#!/usr/bin/env python3
"""Build fixed-style RU/EN Shorts captions for Story 003.

Canonical spelling comes from Source/Voice/003_*_script.txt. Whisper word timing
is only an alignment reference. Cue text is punctuation-free except apostrophes
and orthographic hyphens. The renderer keeps one fixed base size per language;
only the active yellow word pulses smoothly by +5 percent. White words never
scale. Requires Pillow, FFmpeg, Helvetica Neue TTC at the documented system path.
"""
import argparse, bisect, difflib, json, math, re, subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

BASE = Path(__file__).resolve().parents[2]
VOICE = BASE / 'Source' / 'Voice'
ROOT = Path(__file__).resolve().parent
FPS, W, H = 30, 1080, 1920
FONT = '/System/Library/Fonts/HelveticaNeue.ttc'
FONT_INDEX = 9
TRACKING, WORD_GAP, ACTIVE_SCALE = 1.5, 32.5, 1.05
Y = round(H * .40)


def tokenize(text, lang):
    if lang == 'en':
        raw = re.findall(r"[A-Za-z0-9]+(?:[-'][A-Za-z0-9]+)*[.,!?;:…]*[\"”»]*", text)
        clean = [re.sub(r'[.,!?;:…\"“”«»]+$', '', x) for x in raw]
    else:
        raw = re.findall(r"[А-Яа-яЁё0-9]+(?:[-‑][А-Яа-яЁё0-9]+)*[.,!?;:…]*[\"”»]*", text)
        clean = [re.sub(r'[.,!?;:…\"“”«»]+$', '', x).replace('‐','-').replace('‑','-') for x in raw]
    return raw, clean


def normalize(s, lang):
    allowed = 'a-z0-9' if lang == 'en' else 'а-яёa-z0-9'
    return re.sub(fr'[^ {allowed}]'.replace(' ', ''), '', s.lower())


def read_source_words(path):
    data = json.loads(path.read_text(encoding='utf-8'))
    return [w for seg in data['segments'] for w in seg.get('words', [])]


def align(target_raw, target_clean, source, lang):
    src_text = [str(w['word']).strip() for w in source]
    norm_src = [normalize(w, lang) for w in src_text]
    norm_dst = [normalize(w, lang) for w in target_clean]
    sm = difflib.SequenceMatcher(None, norm_src, norm_dst, autojunk=False)
    aligned = [None] * len(target_raw)
    # A weak lexical match means ASR paraphrase/mistranscription is too large
    # for sparse exact-word anchors: those anchors can collapse several real
    # words into near-zero duration. In that case preserve the complete audio
    # time axis and map canonical words monotonically across recognized word
    # timings. The script remains the wording authority; ASR remains timing only.
    if sm.ratio() < 0.72:
        if len(target_raw) == 1:
            positions = [0.0]
        else:
            positions = [i * (len(source) - 1) / (len(target_raw) - 1) for i in range(len(target_raw))]
        prev_start = -1.0
        for ti, pos in enumerate(positions):
            lo = int(pos); hi = min(len(source) - 1, lo + 1); frac = pos - lo
            st = float(source[lo]['start']) * (1-frac) + float(source[hi]['start']) * frac
            en = float(source[lo]['end']) * (1-frac) + float(source[hi]['end']) * frac
            st = max(st, prev_start + 0.06)
            aligned[ti] = {'word': target_clean[ti], 'start': st, 'end': max(st + 0.08, en)}
            prev_start = st
        return aligned, sm.ratio(), sm.get_opcodes()
    for tag, a, b, c, d in sm.get_opcodes():
        if tag == 'equal':
            for si, ti in zip(range(a,b), range(c,d)):
                aligned[ti] = {'word': target_clean[ti], 'start': float(source[si]['start']), 'end': float(source[si]['end'])}
        elif c < d:
            if a < b:
                st, en = float(source[a]['start']), float(source[b-1]['end'])
            else:
                st = float(source[a-1]['end']) if a else float(source[0]['start'])
                en = float(source[b]['start']) if b < len(source) else float(source[-1]['end'])
                if en - st < .08:
                    st, en = max(float(source[0]['start']), st-.12), min(float(source[-1]['end']), en+.12)
            en = max(st+.08, en)
            weights = [max(1, len(norm_dst[i])) for i in range(c,d)]
            total = sum(weights); cur = st
            for j, (ti, weight) in enumerate(zip(range(c,d), weights)):
                nxt = en if j == len(weights)-1 else cur + (en-st)*weight/total
                aligned[ti] = {'word': target_clean[ti], 'start': cur, 'end': max(cur+.04, nxt)}
                cur = nxt
    if any(w is None for w in aligned):
        raise ValueError('Some canonical words have no time assignment')
    # Enforce a monotonic sequence and keep every word inside the spoken asset.
    prev = 0.0
    for w in aligned:
        w['start'] = max(prev, min(w['start'], max(0.0, float(source[-1]['end'])-.06)))
        w['end'] = max(w['start']+.04, w['end'])
        prev = w['start']
    return aligned, sm.ratio(), sm.get_opcodes()


def punctuation_boundary(raw):
    return bool(re.search(r'[.!?…:;][\"”»]*$', raw))


def make_cues(raw, clean, lang, base_size):
    font = ImageFont.truetype(FONT, base_size, index=FONT_INDEX)
    bad_end_en = set('a an the my your his her our their its this that these those to of for with at by from in on as and but or nor so because if when while who whom which i me we us he him she they them it not no'.split())
    bad_end_ru = set('я мы ты вы он она оно они меня тебе ему ей их нас вам им его её это этот эта эти не а и но да что если чтобы потому в во на к ко с со о об обо от из у по для за до над под при без между через про ради около вокруг перед пред после вне внутри сквозь'.split())
    bad_start_en = set('a an the to of for with at by from in on as and but or nor so because if when while that who which'.split())
    bad_start_ru = set('в во на к ко с со о об обо от из у по для за до над под при без между через про ради около вокруг перед после а и но что'.split())
    bad_end = bad_end_en if lang == 'en' else bad_end_ru
    bad_start = bad_start_en if lang == 'en' else bad_start_ru
    n=len(raw); boundaries={i+1 for i,r in enumerate(raw) if punctuation_boundary(r)}
    dp=[(float('inf'), None)]*(n+1); dp[0]=(0,None)
    for end in range(1,n+1):
        options=[]
        for size in (1,2,3):
            st=end-size
            if st<0: continue
            tokens=clean[st:end]; line=' '.join(tokens).upper()
            width=sum(font.getlength(tok)+TRACKING*max(0,len(tok)-1) for tok in line.split())+WORD_GAP*max(0,len(line.split())-1)
            peak=width+(ACTIVE_SCALE-1)*max((font.getlength(tok)+TRACKING*max(0,len(tok)-1) for tok in line.split()),default=0)
            cost=dp[st][0] + {1:9.0,2:1.0,3:0}[size] + max(0,peak-980)*.05
            if peak>1020: cost+=1000+peak
            if end<n and clean[end-1].lower() in bad_end: cost+=12.0
            if st>0 and clean[st].lower() in bad_start: cost+=2.0
            # Prefer an ending at punctuation, but let the next sentence
            # complete a short phrase rather than strand a single word.
            if any(st < boundary < end for boundary in boundaries): cost+=3.0
            if end in boundaries: cost-=1.0
            if end==n: cost-=.4
            options.append((cost,st))
        dp[end]=min(options,key=lambda x:x[0])
    cues=[]; end=n
    while end:
        _,st=dp[end]; cues.append((st,end)); end=st
    cues.reverse()
    def group_peak(a,b):
        toks=clean[a:b]; widths=[font.getlength(tok)+TRACKING*max(0,len(tok)-1) for tok in toks]
        return sum(widths)+WORD_GAP*max(0,len(toks)-1)+.05*max(widths,default=0)
    # Rebalance a one-word remainder across an adjacent break instead of
    # leaving an orphan caption. Keep the total at three words and avoid a
    # leading preposition such as FROM when possible.
    for i,(a,b) in enumerate(list(cues)):
        if b-a != 1: continue
        if i+1<len(cues):
            na,nb=cues[i+1]
            if nb-na==3 and clean[na].lower() not in bad_start and group_peak(a,b+1)<=1020 and group_peak(na+1,nb)<=1020:
                cues[i]=(a,b+1); cues[i+1]=(na+1,nb); continue
        if i>0:
            pa,pb=cues[i-1]
            if pb-pa==3 and group_peak(pa,pb-1)<=1020 and group_peak(pb-1,b)<=1020:
                cues[i-1]=(pa,pb-1); cues[i]=(pb-1,b)
    return [' '.join(clean[a:b]).upper() for a,b in cues], cues


def apply_semantic_reflows(cues, clean, lang):
    """Hand-correct sentence-boundary splits that would read ambiguously."""
    plans = {
        'en': [
            ['FOR HIS BIRTHDAY','THINGS WITH HER','FAMILY HAD BEEN','COMPLICATED FOR A','LONG TIME THEY\'D','ONLY JUST STARTED','GETTING BETTER','SHE REALLY WANTED','TO RECONNECT WITH','THEM AND THIS','TRIP MEANT A','LOT TO HER','SO NOW I','HAD TO MAKE','A DECISION'],
            ['CALL HER AND','TELL HER GUS','WAS GONE','I KNEW SHE\'D','BE DEVASTATED','AND IT COULD','RUIN HER','WHOLE TRIP','OR LET HER','SPEND A FEW','DAYS WITH HER','FAMILY THEN TELL','HER FACE TO','FACE I WENT','WITH THE SECOND','OPTION'],
            ['WHEN SHE FLEW','HOME I PICKED','HER UP AT','THE AIRPORT','AND TOLD HER','EVERYTHING','GUS HAD DIED','AND I\'D DELIBERATELY','KEPT IT','FROM HER','WHILE SHE','WAS AWAY','SHE DIDN\'T SAY','A WORD','THE ENTIRE','DRIVE HOME','AT HOME WE','PUT GUS IN','A BOX WE\'D','KEPT FOR THIS','MOMENT AND','BURIED HIM','TOGETHER THEN','SHE FINALLY SAID'],
            ['BEFORE BED I','ASKED IF I','SHOULD SLEEP ON','THE COUCH','SHE SAID I\'D','BE A DEAD','MAN IF I','SLEPT ANYWHERE','OTHER THAN OUR','BED','NO WE DIDN\'T','BREAK UP WE\'RE','STILL TOGETHER','AND WE BOTH','STILL MISS GUS','I DON\'T REGRET','WAITING UNTIL','SHE CAME HOME','BUT I UNDERSTAND','WHY SHE WAS','UPSET WITH ME'],
        ],
        'ru': [
            ['МЫ ПОНИМАЛИ','ЧТО ЕМУ ОСТАЛОСЬ','НЕДОЛГО','НО КОГДА ОН','УМЕР Я','ВСЁ РАВНО','НЕ ВЫДЕРЖАЛ','И РАСПЛАКАЛСЯ'],
            ['С СЕМЬЁЙ','У НЕЁ ДАВНО','БЫЛИ СЛОЖНЫЕ','ОТНОШЕНИЯ','И ТОЛЬКО','НЕДАВНО ОНИ','НАЧАЛИ','НАЛАЖИВАТЬСЯ','ОНА ОЧЕНЬ ХОТЕЛА','СНОВА СТАТЬ БЛИЖЕ','С РОДСТВЕННИКАМИ','И ЭТА ПОЕЗДКА','БЫЛА ДЛЯ НЕЁ','ВАЖНА','И ВОТ ТЕПЕРЬ','МНЕ НУЖНО БЫЛО','РЕШИТЬ ЧТО ДЕЛАТЬ','ПОЗВОНИТЬ И','СКАЗАТЬ ЧТО','ГАС УМЕР'],
            ['ВСЮ ДОРОГУ ДОМОЙ','ОНА МОЛЧАЛА','ДОМА МЫ','ПОЛОЖИЛИ ГАСА','В ЗАРАНЕЕ','ПРИГОТОВЛЕННУЮ','КОРОБКУ','И ВМЕСТЕ','ПОХОРОНИЛИ'],
            ['ПОТОМ ОНА','СКАЗАЛА МНЕ','Я ТЕБЯ','ВСЁ ЕЩЁ ЛЮБЛЮ','НО СЕЙЧАС ТЫ','МНЕ СОВСЕМ НЕ','НРАВИШЬСЯ','Я ПОНИМАЛ','ПОЧЕМУ ОНА ЗЛИТСЯ','И НЕ СТАЛ','СПОРИТЬ','ЧУТЬ ПОЗЖЕ','Я ПРИГОТОВИЛ УЖИН','МЫ СЕЛИ ЗА','СТОЛ И','ОБА РАСПЛАКАЛИСЬ'],
            ['КРОМЕ НАШЕЙ','КРОВАТИ','НЕТ МЫ НЕ','РАССТАЛИСЬ МЫ ДО','СИХ ПОР ВМЕСТЕ','И НАМ ОБОИМ','ВСЁ ЕЩЁ ОЧЕНЬ','НЕ ХВАТАЕТ ГАСА','Я НЕ ЖАЛЕЮ','ЧТО ДОЖДАЛСЯ','ЕЁ ВОЗВРАЩЕНИЯ','НО ПРЕКРАСНО','ПОНИМАЮ ПОЧЕМУ','ОНА ТОГДА НА','МЕНЯ РАЗОЗЛИЛАСЬ'],
        ],
    }
    if lang not in plans: return cues
    for group_strings in plans[lang]:
        groups=[[x.lower() for x in s.split()] for s in group_strings]
        flat=[w for g in groups for w in g]
        normalized=[w.lower() for w in clean]
        start=next((i for i in range(len(clean)-len(flat)+1) if normalized[i:i+len(flat)]==flat),None)
        if start is None:
            raise ValueError(f'Manual caption reflow could not be matched: {group_strings[0]}')
        end=start+len(flat)
        prefix=[(a,min(b,start)) for a,b in cues if a<start and min(b,start)>a]
        suffix=[(max(a,end),b) for a,b in cues if b>end and b>max(a,end)]
        manual=[]; at=start
        for group in groups: manual.append((at,at+len(group))); at+=len(group)
        cues=prefix+manual+suffix
    return cues


def render(lang, frames, asr_override=None, output_override=None):
    script = VOICE / f'003_{lang}_shorts_script.txt'
    audio = VOICE / ('ElevenLabs_2026-10-28T08_06_57_Darth_pvc_sp100_s30_sb90_v4' if lang=='en' else 'ElevenLabs_2026-10-28T08_06_16_Darth_pvc_sp100_s30_sb90_v4')
    asr_root = VOICE / 'Transcripts'
    asr_json = Path(asr_override) if asr_override else asr_root / f'whisper-corrected-{lang}' / (audio.name + '.json')
    if not asr_json.exists(): raise FileNotFoundError(f'Missing corrected-language ASR timing: {asr_json}')
    raw_text=script.read_text(encoding='utf-8').strip()
    token_raw, token_clean=tokenize(raw_text,lang)
    src=read_source_words(asr_json)
    words,ratio,ops=align(token_raw,token_clean,src,lang)
    timestamps=ROOT/f'003_{lang}_word_timestamps_aligned.json'
    timestamps.write_text(json.dumps({'words':words,'sourceWordCount':len(src),'canonicalWordCount':len(words),'alignmentRatio':ratio},ensure_ascii=False,indent=2),encoding='utf-8')
    size=92 if lang=='en' else 105
    plan,cues=make_cues(token_raw,token_clean,lang,size)
    cues=apply_semantic_reflows(cues,token_clean,lang)
    plan=[' '.join(token_clean[a:b]).upper() for a,b in cues]
    plan_path=ROOT/f'003_{lang}_caption_plan.txt'
    plan_path.write_text('\n'.join(plan)+'\n',encoding='utf-8')
    counts=[len(line.split()) for line in plan]
    if max(counts)>3: raise ValueError('Caption exceeds three words')
    # Verify punctuation removal while preserving apostrophes and inner hyphens.
    expected=[w.upper() for w in token_clean]
    actual=[t for line in plan for t in line.split()]
    if actual!=expected: raise ValueError('Cue plan changed or omitted canonical wording')
    starts=[words[a]['start'] for a,b in cues]
    # Keep very fast neighboring cue changes readable. A short cue inherits a
    # small portion of the following interval; no words are reordered.
    for i in range(1,len(starts)):
        starts[i]=max(starts[i],starts[i-1]+0.24)
    ends=[starts[i+1] if i+1<len(starts) else words[b-1]['end'] for i,(a,b) in enumerate(cues)]
    shorts=[(i+1,plan[i],ends[i]-starts[i]) for i in range(len(plan)) if ends[i]-starts[i]<.22]
    if shorts: raise ValueError(f'Short cue(s) below 220 ms: {shorts[:8]}')
    font_cache={}
    def font_at(px):
        if px not in font_cache: font_cache[px]=ImageFont.truetype(FONT,px,index=FONT_INDEX)
        return font_cache[px]
    def width(tok,f): return f.getlength(tok)+TRACKING*max(0,len(tok)-1)
    peaks=[]
    for line in plan:
        f=font_at(size); toks=line.split(); widths=[width(t,f) for t in toks]
        peaks.append(sum(widths)+WORD_GAP*max(0,len(toks)-1)+.05*max(widths,default=0))
    if max(peaks)>1020: raise ValueError(f'Caption too wide at fixed font size: {max(zip(peaks,plan))}')
    (ROOT/f'003_{lang}_caption_sizes.tsv').write_text('cue\twords\tbase_size_px\tpeak_width_px\n'+'\n'.join(f'{i+1}\t{line}\t{size}\t{peaks[i]:.1f}' for i,line in enumerate(plan))+'\n',encoding='utf-8')
    def stamp(s):
        n=round(s*1000); h,n=divmod(n,3600000); m,n=divmod(n,60000); sec,n=divmod(n,1000)
        return f'{h:02d}:{m:02d}:{sec:02d},{n:03d}'
    srt=[]
    for i,line in enumerate(plan): srt.extend([str(i+1),f'{stamp(starts[i])} --> {stamp(ends[i])}',line,''])
    (ROOT/f'003_{lang}_captions.srt').write_text('\n'.join(srt),encoding='utf-8')
    out=Path(output_override) if output_override else ROOT/f'003_{lang}_caption_overlay_v2.mov'
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-f','rawvideo','-pixel_format','rgba','-video_size',f'{W}x{H}','-framerate',str(FPS),'-i','pipe:0','-an','-c:v','qtrle','-pix_fmt','argb','-movflags','+faststart',str(out)]
    proc=subprocess.Popen(cmd,stdin=subprocess.PIPE)
    white=(255,255,255,255); yellow=(255,213,79,255); outline=(0,0,0,210)
    for frame in range(frames):
        t=frame/FPS; ci=bisect.bisect_right(starts,t)-1
        im=Image.new('RGBA',(W,H),(0,0,0,0))
        if ci>=0 and t<ends[ci]:
            a,b=cues[ci]; c=words[a:b]; shown=[w.upper() for w in token_clean[a:b]]
            base=font_at(size); active=next((j for j,w in enumerate(c) if w['start']<=t<w['end']),-1)
            widths=[width(tok,base) for tok in shown]; total=sum(widths)+WORD_GAP*max(0,len(shown)-1); x=(W-total)/2
            draw=ImageDraw.Draw(im)
            for j,w in enumerate(c):
                f=base; color=white
                if j==active:
                    dur=max(.001,w['end']-w['start']); progress=max(0,min(1,(t-w['start'])/dur)); ramp=min(.12,dur*.45)
                    if dur<=2*ramp:
                        q=min(1,progress*2) if progress<=.5 else min(1,(1-progress)*2); eased=q*q*(3-2*q)
                    elif progress<ramp/dur:
                        q=progress*dur/ramp; eased=q*q*(3-2*q)
                    elif progress>1-ramp/dur:
                        q=(1-progress)*dur/ramp; eased=q*q*(3-2*q)
                    else: eased=1.0
                    f=font_at(round(size*(1+.05*eased))); color=yellow
                center=x+widths[j]/2; charx=center-width(shown[j],f)/2
                for ch in shown[j]:
                    cw=f.getlength(ch); draw.text((charx+cw/2,Y),ch,font=f,fill=color,anchor='mm',stroke_width=5,stroke_fill=outline); charx+=cw+TRACKING
                x+=widths[j]+WORD_GAP
        try: proc.stdin.write(im.tobytes())
        except BrokenPipeError: raise RuntimeError('FFmpeg closed the transparent-overlay pipe')
    proc.stdin.close(); rc=proc.wait()
    if rc: raise SystemExit(rc)
    print(f'{lang}: alignment ratio={ratio:.3f}; words={len(words)}; cues={len(plan)}; fixed font={size}px; max words={max(counts)}; max width={max(peaks):.0f}px; frames={frames}; output={out}')
    if ratio<.65: print(f'WARNING: spoken recognition differs substantially from the canonical script; inspect text/audio correspondence before claiming exact transcription.')
    print('\n'.join(plan))

if __name__=='__main__':
    p=argparse.ArgumentParser(); p.add_argument('lang',choices=['en','ru']); p.add_argument('--frames',type=int,required=True); p.add_argument('--asr'); p.add_argument('--output'); a=p.parse_args(); render(a.lang,a.frames,a.asr,a.output)
