#!/usr/bin/env python3
"""Rebuild a reviewable Nuviko one-line word-highlight cue map from video captions.
No media is rendered and no Palmier/YouTube state is changed.
"""
import difflib, html, json, re, hashlib
from pathlib import Path
from PIL import ImageFont

EP=Path(__file__).resolve().parents[2]
REC=EP/'Source/Recovered'
AUTO=REC/'youtube_source.en.vtt'
CREATOR=REC/'youtube_source.en-eEY6OEpapPo.vtt'
OLD=REC/'old_caption_track_v06.json'
OUT=EP/'Edit/Subtitles/karaoke_v01'
OUT.mkdir(parents=True,exist_ok=True)

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def seconds(s):
    h,m,v=s.split(':'); return int(h)*3600+int(m)*60+float(v)

def parse_auto(path):
    words=[]
    for block in path.read_text(encoding='utf-8').split('\n\n'):
        lines=block.splitlines()
        if not lines or '-->' not in lines[0]: continue
        left,right=lines[0].split('-->'); start=seconds(left.strip()); end=seconds(right.strip().split()[0])
        active=[line for line in lines[1:] if re.search(r'<\d{2}:\d{2}:\d{2}\.\d{3}>',line)]
        if not active: continue
        line=active[-1]; parts=re.split(r'(<\d{2}:\d{2}:\d{2}\.\d{3}>)',line)
        cur=start; buf=''
        for part in parts:
            m=re.fullmatch(r'<(\d{2}:\d{2}:\d{2}\.\d{3})>',part)
            if not m: buf+=part; continue
            t=seconds(m.group(1)); txt=html.unescape(re.sub(r'</?c[^>]*>','',buf)).strip()
            toks=re.findall(r"\S+",txt)
            if toks:
                span=max(0,t-cur)
                for i,tok in enumerate(toks): words.append({'text':tok,'start':cur+span*i/len(toks),'end':cur+span*(i+1)/len(toks),'timing_source':'youtube_auto_caption_word_marker'})
            cur=t;buf=''
        txt=html.unescape(re.sub(r'</?c[^>]*>','',buf)).strip(); toks=re.findall(r"\S+",txt)
        if toks:
            span=max(0,end-cur)
            for i,tok in enumerate(toks): words.append({'text':tok,'start':cur+span*i/len(toks),'end':cur+span*(i+1)/len(toks),'timing_source':'youtube_auto_caption_word_marker'})
    return words

def parse_creator(path):
    cues=[]
    for block in path.read_text(encoding='utf-8').split('\n\n'):
        lines=block.splitlines()
        if not lines or '-->' not in lines[0]: continue
        l,r=lines[0].split('-->'); a=seconds(l.strip()); b=seconds(r.strip().split()[0])
        text=' '.join(x.strip() for x in lines[1:] if x.strip())
        text=html.unescape(re.sub(r'<[^>]+>','',text)).strip()
        if text: cues.append({'start':a,'end':b,'text':text})
    return cues

def norm(s): return re.sub(r"[^\w']",'',s.lower())

auto=parse_auto(AUTO); creator=parse_creator(CREATOR)
manual_text=' '.join(c['text'] for c in creator)
manual_words=re.findall(r"\S+",manual_text)
auto_norm=[norm(w['text']) for w in auto]; manual_norm=[norm(w) for w in manual_words]
matcher=difflib.SequenceMatcher(a=manual_norm,b=auto_norm,autojunk=False)
aligned=[None]*len(manual_words); mappings=[]
for tag,i1,i2,j1,j2 in matcher.get_opcodes():
    if tag=='equal':
        for mi,ai in zip(range(i1,i2),range(j1,j2)): aligned[mi]={**auto[ai],'source_index':ai,'mapping':'exact_token'}
    elif tag=='replace':
        mcount,acount=i2-i1,j2-j1
        if mcount==0 or acount==0: raise ValueError(f'Unmapped transcript span: {manual_words[i1:i2]} / {auto[j1:j2]}')
        if mcount==1 and acount==1:
            src=auto[j1]
            aligned[i1]={'text':manual_words[i1],'start':src['start'],'end':src['end'],'timing_source':src['timing_source'],'source_index':j1,'mapping':'one_caption_token_text_reconciliation'}
        elif acount==1:
            src=auto[j1]; span=src['end']-src['start']; weights=[max(1,len(re.sub(r'[^A-Za-z0-9]','',w))) for w in manual_words[i1:i2]]; total=sum(weights); cursor=src['start']
            for k,(mi,w,wt) in enumerate(zip(range(i1,i2),manual_words[i1:i2],weights)):
                nxt=src['end'] if k==mcount-1 else cursor+span*wt/total
                aligned[mi]={'text':w,'start':cursor,'end':nxt,'timing_source':src['timing_source'],'source_index':j1,'mapping':'one_caption_token_split_across_spoken_words'};cursor=nxt
        elif mcount==1:
            aligned[i1]={'text':manual_words[i1],'start':auto[j1]['start'],'end':auto[j2-1]['end'],'timing_source':auto[j1]['timing_source'],'source_index':[j1,j2-1],'mapping':'caption_words_joined_to_one_spoken_word'}
        elif mcount==acount:
            for mi,ai in zip(range(i1,i2),range(j1,j2)): aligned[mi]={'text':manual_words[mi], 'start':auto[ai]['start'],'end':auto[ai]['end'],'timing_source':auto[ai]['timing_source'],'source_index':ai,'mapping':'text_variant'}
        else:
            # Proportionally partition the matched time span; preserve every source word.
            start,end=auto[j1]['start'],auto[j2-1]['end']; weights=[max(1,len(re.sub(r'[^A-Za-z0-9]','',w))) for w in manual_words[i1:i2]];total=sum(weights);cursor=start
            for k,(mi,w,wt) in enumerate(zip(range(i1,i2),manual_words[i1:i2],weights)):
                nxt=end if k==mcount-1 else cursor+(end-start)*wt/total
                aligned[mi]={'text':w,'start':cursor,'end':nxt,'timing_source':auto[j1]['timing_source'],'source_index':[j1,j2-1],'mapping':'proportional_span_reconciliation'};cursor=nxt
        mappings.append({'manual_word_range':[i1,i2],'auto_word_range':[j1,j2],'manual':manual_words[i1:i2],'auto':[w['text'] for w in auto[j1:j2]],'mapping':aligned[i1]['mapping']})
    else: raise ValueError(f'Unmapped tokens: {tag} {manual_words[i1:i2]} / {auto[j1:j2]}')
if any(w is None for w in aligned): raise ValueError('Incomplete word timing map')
if any(w['end']<=w['start'] for w in aligned): raise ValueError('Nonpositive word timing')
if any(aligned[i]['start']<aligned[i-1]['start'] for i in range(1,len(aligned))): raise ValueError('Word times are not monotone')

font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Georgia Bold.ttf',62); max_width=1600
weak_end=set('a an the of in on at to for from with by as into and or but that which who whose because if when is are was were be been being had has have do does did will can could would should it its their this these those not no so'.split())
weak_start=set('and or but of in on at to for from with as into that which who whose because if when is are was were be been being had has have do does did will can could would should'.split())
def terminal(t): return t.rstrip('"”\')]}').endswith(('.', '?','!'))

def segment(items):
    n=len(items); dp=[(float('inf'),None)]*(n+1);dp[n]=(0,None)
    for i in range(n-1,-1,-1):
        for j in range(i+1,min(n,i+5)+1):
            g=items[i:j]; line=' '.join(x['text'] for x in g)
            if font.getlength(line)+8>max_width: break
            if any(terminal(x['text']) for x in g[:-1]): break
            if j<n and norm(g[-1]['text'])=='not': continue
            left=norm(g[-1]['text']); right=norm(items[j]['text']) if j<n else ''
            cost=abs(len(g)-3)*1.1 + (8 if len(g)>4 else 0)
            if len(g)==1 and j<n and not terminal(g[-1]['text']): cost+=28
            if j<n and left in weak_end and not terminal(g[-1]['text']): cost+=100
            if j<n and right in weak_start and not terminal(g[-1]['text']): cost+=2.5
            if j<n and terminal(g[-1]['text']): cost-=4
            elif j<n and g[-1]['text'].endswith((',', ';', ':')): cost-=1
            if i>0 and norm(g[0]['text']) in ('who','which','that','because','if','when'): cost-=1
            value=cost+dp[j][0]
            if value<dp[i][0]: dp[i]=(value,j)
    if dp[0][1] is None: raise ValueError('Could not segment a line-safe cue')
    result=[];i=0
    while i<n: j=dp[i][1];result.append(items[i:j]);i=j
    return result

# Force the exact user-approved opening and two reflows that preserve complete phrases.
forced_phrases=[
'At a plague','cemetery in London,','archaeologists found','one hundred and eighty-one coins.','They lay','in the grave','of a woman','who died','during the epidemic.','We do not know','why the money','remained with her.'
]
forced=[];cursor=0
for phrase in forced_phrases:
    toks=phrase.split(); chunk=aligned[cursor:cursor+len(toks)]
    if [norm(x['text']) for x in chunk] != [norm(x) for x in toks]: raise ValueError(f'Opening phrase does not match source text: {phrase}')
    if font.getlength(' '.join(x['text'] for x in chunk))+8>max_width: raise ValueError(f'Opening phrase too wide: {phrase}')
    forced.append(chunk);cursor+=len(toks)
groups=forced+segment(aligned[cursor:])

def force_phrase(phrase, splits):
    global groups
    toks=phrase.split(); flat=[x for g in groups for x in g]; at=None
    for i in range(len(flat)-len(toks)+1):
        if [norm(x['text']) for x in flat[i:i+len(toks)]]==[norm(x) for x in toks]: at=i;break
    if at is None: raise ValueError(f'Forced phrase absent: {phrase}')
    # Preserve all established group boundaries outside this exact source range.
    stop=at+len(toks); target=flat[at:stop]; before=[];after=[];pos=0
    for g in groups:
        end=pos+len(g)
        if end<=at: before.append(g)
        elif pos<at: before.append(g[:at-pos])
        if pos>=stop: after.append(g)
        elif end>stop: after.append(g[stop-pos:])
        pos=end
    out=before
    p=0
    for count in splits:
        out.append(target[p:p+count]); p+=count
    if p!=len(target): raise ValueError('Forced split count mismatch')
    out+=after
    groups=out
force_phrase('for those who could no longer help themselves.',[8])
force_phrase('of mutual help as it would be to see nothing but cruelty.',[3,9])
force_phrase('and tried to live moderately.',[5])
force_phrase('people were not always buried hastily and without order.',[5,4])
force_phrase('did not all amount to the same response.',[8])
force_phrase('Visits to people in isolation were restricted, too.',[8])
force_phrase('The delivery of necessities had to be arranged separately.',[4,5])
force_phrase('It was not a final victory.',[6])
force_phrase('In what is now Kyrgyzstan.',[5])
force_phrase('associated with the Black Death.',[5])
force_phrase('traces of the disease itself.',[5])

# Verify exact coverage, width, and the user's sample boundaries.
flat=[x for g in groups for x in g]
if len(flat)!=len(aligned) or any(a is not b for a,b in zip(flat,aligned)): raise ValueError('Groups changed word order or coverage')
for g in groups:
    line=' '.join(x['text'] for x in g)
    if font.getlength(line)+8>max_width: raise ValueError('One-line cue exceeds the safe width: '+line)
issues=[]
for i,g in enumerate(groups[:-1]):
    last=norm(g[-1]['text'])
    if last in weak_end and not terminal(g[-1]['text']): issues.append({'group':i,'left':' '.join(x['text'] for x in g),'right':' '.join(x['text'] for x in groups[i+1])})
if len(groups[0:12])!=12 or [' '.join(x['text'] for x in g) for g in groups[:12]]!=forced_phrases: raise ValueError('Opening examples failed')

cues=[];wordbase=0
for i,g in enumerate(groups):
    start=g[0]['start']; spoken_end=g[-1]['end']; display_end=groups[i+1][0]['start'] if i+1<len(groups) else 707.465578
    cues.append({'cue_id':f'C{i+1:04d}','word_range':[wordbase,wordbase+len(g)],'text':' '.join(x['text'] for x in g),'start':start,'spoken_end':spoken_end,'display_start':start,'display_end':display_end,'words':g,'display_rule':'hold until next group; no blank gaps; active-word highlight only during provisional spoken interval; neutral panel during pauses'})
    wordbase+=len(g)

transcript_path=REC/'narration_en_from_youtube_creator_captions.txt'
transcript_path.write_text(manual_text+'\n',encoding='utf-8')
word_path=REC/'word_alignment_from_youtube_captions_v01.json'
word_path.write_text(json.dumps({'status':'PROVISIONAL_REQUIRES_AUDIBLE_ALIGNMENT_REVIEW','source_audio_sha256':sha(REC/'black_death_original_audio.m4a'),'source_vtt_sha256':sha(AUTO),'creator_caption_sha256':sha(CREATOR),'word_count':len(aligned),'alignment_source':'YouTube automatic VTT word timestamps, reconciled by ordered transcript sequence to the creator English caption track','mappings':mappings,'words':aligned,'limitations':['YouTube auto word-boundary timing has not been checked by listening.','11 creator-caption tokens are split or joined against automatic caption tokens; the replacements and spans are recorded.','The source transcript is the creator English caption track; wording is not separately verified against the audio.']},ensure_ascii=False,indent=2)+'\n')
result={'version':'nuviko-black-death-s01-karaoke-v01','status':'DRAFT_REQUIRES_AUDIBLE_SYNC_AND_VISUAL_REVIEW','language':'en','source_transcript':str(transcript_path.relative_to(EP)),'transcript_sha256':sha(transcript_path),'source_audio':'Source/Recovered/black_death_original_audio.m4a','source_audio_sha256':sha(REC/'black_death_original_audio.m4a'),'alignment_map':str(word_path.relative_to(EP)),'alignment_sha256':sha(word_path),'canvas':[1920,1080],'fps':30,'style':{'reference':'channels/nuviko_history/brand/fieldnotes_kit_v01/rendered/proofs/S01.png','font':'Georgia Bold','font_size_px':62,'center_x':960,'bottom_y':999,'one_line_max_width_px':max_width,'panel_fill':'#F3E9D5','neutral_text':'#302D27','active_text':'warm ochre #C28A2C with dark outline','fixed_word_positions_within_group':True},'continuity':'Replace each phrase at the next group start with no blank interval. During pauses hold the current phrase and neutralize word highlight; highlight one aligned spoken word at a time.','word_count':len(aligned),'cue_count':len(cues),'grouping':{'max_words_aim':4,'max_words_general':5,'explicit_exceptions':['Opening 181 phrase is creator transcript as spoken words; width-fit longer phrases retained when needed for syntax.','for those who could no longer help themselves.','of mutual help / as it would be to see nothing but cruelty.'],'weak_end_issues':issues,'single_word_groups':sum(len(c['words'])==1 for c in cues),'opening_examples':[c['text'] for c in cues[:12]]},'cues':cues,'rendered_overlay':None,'qa':{'transcript_word_coverage':'PASS_SEQUENCE_COUNT_ONLY','subtitle_semantic_readthrough':'DRAFT_AUTOMATED_WITH_TARGETED_REFLOWS','audible_timing':'UNVERIFIED','screen_composite':'NOT_RENDERED','palmier':'NOT_MODIFIED'}}
(OUT/'cue_map_candidate_v01.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
validation={'status':'STRUCTURAL_DRAFT_ONLY','transcript_words':len(aligned),'auto_timing_words':len(auto),'group_count':len(groups),'single_word_group_count':result['grouping']['single_word_groups'],'width_violations':0,'opening_rules':{'ends_with_who':False,'we_do_not_know_together':True},'weak_ending_candidates':issues,'text_to_audio':'UNVERIFIED','vtt_token_mappings':mappings}
(OUT/'validation_candidate_v01.json').write_text(json.dumps(validation,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'words':len(aligned),'auto_words':len(auto),'manual_caption_words':len(manual_words),'cues':len(groups),'single_word_groups':result['grouping']['single_word_groups'],'weak_end_issues':issues,'width_violations':0,'opening':[c['text'] for c in cues[:12]],'mapping_diffs':mappings},ensure_ascii=False,indent=2))
