#!/usr/bin/env python3
"""Create an ASR-timed review frame map while preserving accepted caption text/style."""
import hashlib, importlib.util, json, math, re, os
from pathlib import Path

ROOT=Path('/Users/diplomat/ytvideos')
BASE=ROOT/'channels/paper_detour/videos/001_radio_game/Shorts/02_decoder/Edit/renewal_20261102'
OLD=BASE/'subtitle_preview_20261102'
OUT=BASE/'subtitle_asr_retime_20261102'
TEXT=BASE/'subtitle_build_20261102/narration_exact.txt'
ALIGN=BASE/'subtitle_build_20261102/voice_alignment_conformed_1p05.json'
ASR=BASE/'whisper_recheck_20261102/PAPER_DETOUR_001_SHORT02_RENEWAL_EN_20261102.json'
VIDEO=ROOT/'channels/paper_detour/videos/001_radio_game/Shorts/02_decoder/Deliverables/PAPER_DETOUR_001_SHORT02_RENEWAL_EN_20261102.mp4'
frames=OUT/'frames'
if frames.exists(): raise SystemExit(f'Frames output exists: {frames}')
text=TEXT.read_text(encoding='utf-8').strip()
data=json.loads(ALIGN.read_text())
spec=importlib.util.spec_from_file_location('word_timings',ROOT/'automation/captions/word_timings.py')
module=importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
old_words=module.convert(text,data,'en')['words']
old_cues=json.loads((OLD/'cue_map.json').read_text())
whisper=json.loads(ASR.read_text())
asr_words=[w for seg in whisper['segments'] for w in seg['words']]

def norm(s): return re.sub(r"[^a-z0-9']",'',s.lower())
new_words=[]; methods=[]; i=j=0
while i<len(old_words) and j<len(asr_words):
    src=old_words[i]; token=norm(src['text'])
    if token=='spedup' and j+1<len(asr_words) and norm(asr_words[j]['word'])=='sped' and norm(asr_words[j+1]['word'])=='up':
        a,b=asr_words[j:j+2]
        new_words.append({'text':src['text'],'start_seconds':a['start'],'end_seconds':b['end']})
        methods.append({'method':'ASR merge of hyphenated word','source_word_indices':[i],'asr_word_indices':[j,j+1]})
        i+=1; j+=2; continue
    if [norm(w['text']) for w in old_words[i:i+4]]==['one','hundred','and','two'] and norm(asr_words[j]['word'])=='102':
        span=asr_words[j]['end']-asr_words[j]['start']
        old_span=old_words[i+3]['end_seconds']-old_words[i]['start_seconds']
        if old_span<=0 or span<=0: raise ValueError('Invalid numeric phrase span')
        for k,srcnum in enumerate(old_words[i:i+4]):
            start=asr_words[j]['start']+(srcnum['start_seconds']-old_words[i]['start_seconds'])/old_span*span
            end=asr_words[j]['start']+(srcnum['end_seconds']-old_words[i]['start_seconds'])/old_span*span
            new_words.append({'text':srcnum['text'],'start_seconds':start,'end_seconds':end})
            methods.append({'method':'ASR number phrase; internal words proportionally mapped from existing character alignment','source_word_indices':[i+k],'asr_word_indices':[j]})
        i+=4; j+=1; continue
    if token!=norm(asr_words[j]['word']):
        raise ValueError(f'Word mismatch at source {i}/ASR {j}: {src["text"]!r} vs {asr_words[j]["word"]!r}')
    new_words.append({'text':src['text'],'start_seconds':asr_words[j]['start'],'end_seconds':asr_words[j]['end']})
    methods.append({'method':'ASR word timestamp','source_word_indices':[i],'asr_word_indices':[j]})
    i+=1; j+=1
if i!=len(old_words) or j!=len(asr_words): raise ValueError(f'Incomplete map: source {i}/{len(old_words)}, ASR {j}/{len(asr_words)}')

cues=old_cues['groups']
if sum(c['words'] for c in cues)!=len(new_words): raise ValueError('Cue word counts do not match word map')
new_cues=[]; flat=0; frame_states=[None]*1098
for gi,cue in enumerate(cues):
    group=new_words[flat:flat+cue['words']]
    if [norm(w['text']) for w in group]!=[norm(w) for w in cue['text'].split()]: raise ValueError(f'Text mismatch in group {gi}: {cue["text"]}')
    start=group[0]['start_seconds']; end=group[-1]['end_seconds']
    if gi+1<len(cues):
        nxt=new_words[flat+cue['words']]['start_seconds']
        if 0<=nxt-end<=0.25: end=nxt
    if start<0 or end<start or end>1098/30+0.001: raise ValueError(f'Invalid cue {gi}: {start}–{end}')
    new_cues.append({**cue,'start':start,'end':end,'timing_basis':'local Whisper word timestamps; ASR estimate'})
    for wi,w in enumerate(group):
        begin=max(0,math.ceil(w['start_seconds']*30-1e-7))
        stop=min(1098,math.ceil((group[wi+1]['start_seconds'] if wi+1<len(group) else end)*30-1e-7))
        for frame in range(begin,stop): frame_states[frame]=flat+wi
    flat+=cue['words']

frames.mkdir(parents=True)
assets=OLD/'overlays'
blank=assets/'blank.png'
for n,asset_index in enumerate(frame_states):
    src=assets/f'{asset_index:04}.png' if asset_index is not None else blank
    os.link(src,frames/f'{n:06}.png')
meta={k:v for k,v in old_cues.items() if k!='groups'}
meta.update({'status':'REVIEW_REQUIRED','alignment':str(ASR.resolve()),'groups':new_cues,
             'timing':'local Whisper word timestamps mapped to exact delivered video; audible synchronization unverified',
             'note':'Existing exact wording, group boundaries, geometry and per-word PNG styles preserved. ASR word timings replace provider character timing. Number 102 was internally apportioned using the existing word alignment; this approximation requires listening review.'})
(OUT/'cue_map.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n')
word_map={'version':1,'status':'ASR_ESTIMATE_REVIEW_REQUIRED','video_sha256':hashlib.sha256(VIDEO.read_bytes()).hexdigest(),'transcript_sha256':hashlib.sha256(TEXT.read_bytes()).hexdigest(),'source_alignment_sha256':hashlib.sha256(ALIGN.read_bytes()).hexdigest(),'asr_result_sha256':hashlib.sha256(ASR.read_bytes()).hexdigest(),'asr_source_video_sha256':old_cues['video'] and hashlib.sha256(VIDEO.read_bytes()).hexdigest(),'word_timing_method':'Exact normalized Whisper word matches; merge Sped + -up; proportionally map the four spoken number words across Whisper token 102 using existing character-alignment intervals.','audible_sync':'UNVERIFIED','words':[{'index':n,**w,**methods[n]} for n,w in enumerate(new_words)]}
(OUT/'asr_word_timing_map.json').write_text(json.dumps(word_map,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'groups':len(new_cues),'words':len(new_words),'frames':len(frame_states),'video_sha256':word_map['video_sha256'],'number_approximation_words':[new_words[n] for n in range(29,33)],'timing':'ASR estimate, listening unverified'},ensure_ascii=False))
