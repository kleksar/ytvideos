#!/usr/bin/env python3
"""Build a review-required source-time, one-line Nuviko subtitle plan from existing words."""
import hashlib, json, re, statistics
from pathlib import Path
from PIL import ImageFont

ROOT = Path(__file__).resolve().parents[2]
TEXT = ROOT / 'Research/TRANSCRIPT_CONTENT_EN_v02.txt'
ALIGN = ROOT / 'Research/WHISPERX_ALIGNMENT_EN_v02.json'
OUT = ROOT / 'Work/subtitles_nuviko_plan_v01/cue_map_source_v01.json'
SRT = ROOT / 'Work/subtitles_nuviko_plan_v01/subtitles_source_draft_v01.srt'
FPS = 30
MAX_WORDS = 8
# S01's 1180px limit is the entire cream panel. Its two 25px pads leave 1130px for ink.
MAX_TEXT_WIDTH = 1130
FONT = ImageFont.truetype('/System/Library/Fonts/Supplemental/Georgia Bold.ttf', 54)
WEAK_END = set('who which that whose because if when while and or but to of in on at for with from by as the a an this these their his her our my your its their they we you he she it me us them not do does was were is are have has had will would could should can might must than more less most very each some any into over under through after before about against between among without within toward towards up down off out back although unless until since so yet'.split())
WEAK_START = set('and or but because which that who when while if'.split())
# Keep historical names and inseparable compounds together even if a boundary scores well.
KEEP_TOGETHER = [('Grand','Saint-Antoine'), ('Jean-Baptiste','Chateau'), ('Jean-Baptiste','Estelle'), ('Chateau','d\'If'), ('we','do'), ('do','not'), ('they','carried')]
LONG_PHRASES = [
    ('while','the','city','continued','its','daily','life'),
    ('a','woman','on','rue','belle','table'),
    ('more','than','two','and','a','half'),
]
ORTHOGRAPHY = {
    'chateau':'Chataud', 'pessonel':'Peyssonnel', 'gerard':'Gairard',
    'beaucer':'Beaucaire', 'ecu':'écus', 'echevin':'échevin',
}


def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def core(s): return re.sub(r"[^\w'-]", '', s.strip('"“”\'’')).lower()
def strip_quotes(s): return s.strip('"“”\'’')
def caption_word(s):
    clean=strip_quotes(s)
    key=core(clean)
    replacement=ORTHOGRAPHY.get(key)
    if replacement:
        # Keep sentence punctuation from the audio token while correcting only name spelling.
        suffix=''
        m=re.search(r'[.,!?;:]+["”\']*$',clean)
        if m: suffix=m.group(0)
        return replacement+suffix
    return clean
def is_sentence_end(s): return bool(re.search(r'[.!?]["”\']*$', s))
def is_clause_end(s): return bool(re.search(r'[,;:]["”\']*$', s))
def token_norm(s):
    s=s.lower().replace('’', "'")
    return re.findall(r"[\w]+(?:'[\w]+)*(?:-[\w]+(?:'[\w]+)*)*", s)

def group_cost(words, i, j):
    group=words[i:j]; n=j-i
    cost={1:30,2:2.0,3:.8,4:0,5:3.0,6:10,7:12,8:14}[n]
    end=core(group[-1]['text']); start=core(group[0]['text'])
    if end in WEAK_END: cost += 20
    if start in WEAK_START: cost += 6
    # Do not end after a possessive determiner: keep it attached to its noun.
    if group[-1]['text'].strip('"“”\'’').lower().endswith("'s") and j<len(words): cost += 30
    if j>0 and j<len(words):
        before=core(words[j-1]['text']); after=core(words[j]['text'])
        if any(before==a.lower() and after==b.lower() for a,b in KEEP_TOGETHER): return float('inf')
    line=' '.join(caption_word(x['text']) for x in group)
    if FONT.getlength(line)>MAX_TEXT_WIDTH: return float('inf')
    if is_clause_end(group[-1]['text']): cost -= 1.25
    if is_sentence_end(group[-1]['text']): cost -= 2.0
    # Prefer not to leave an incomplete clause before a short function-word start.
    if j<len(words) and core(words[j]['text']) in WEAK_START: cost += 2.0
    phrase=tuple(strip_quotes(w['text']).lower() for w in group)
    if n==4 and phrase[-2:] in {('we','do'),('do','not')} : cost += 2
    return cost

def partition(words):
    normalized=[core(w['text']) for w in words]
    spans=[]
    for phrase in LONG_PHRASES:
        size=len(phrase)
        for start in range(len(words)-size+1):
            if tuple(normalized[start:start+size])==phrase:
                if FONT.getlength(' '.join(caption_word(w['text']) for w in words[start:start+size]))>MAX_TEXT_WIDTH:
                    raise ValueError(f'Approved one-line exception exceeds safe width: {phrase}')
                spans.append((start,start+size))
    n=len(words); dp=[float('inf')]*(n+1); prev=[None]*(n+1); dp[0]=0
    for j in range(1,n+1):
        for size in range(1,min(MAX_WORDS,j)+1):
            i=j-size
            # Long but narrow phrases are indivisible exceptions when a normal split
            # would strand a determiner, number fragment, or place name.
            if any(max(i,a)<min(j,b) and not (i==a and j==b) for a,b in spans): continue
            phrase_words=tuple(normalized[i:j])
            if any(i==a and j==b for a,b in spans):
                cost=-8
            else:
                cost=group_cost(words,i,j)
            # Do not split inside a sentence-ending word.
            if any(is_sentence_end(words[k]['text']) for k in range(i,j-1)): continue
            if i>0:
                prev_core=core(words[i-1]['text']); curr_core=core(words[i]['text'])
                if any(prev_core==a.lower() and curr_core==b.lower() for a,b in KEEP_TOGETHER): continue
            score=dp[i]+cost
            if score<dp[j]: dp[j]=score; prev[j]=i
    if prev[n] is None: raise ValueError('Unable to partition a sentence into readable groups')
    result=[]; j=n
    while j:
        i=prev[j]; result.append(words[i:j]); j=i
    return list(reversed(result))

text=TEXT.read_text().strip()
alignment=json.loads(ALIGN.read_text())
words=alignment['words']
# Check literal spoken word sequence, permitting orthographic hyphen compounds to map as one word.
transcript_tokens=token_norm(text)
aligned_tokens=[]
for w in words: aligned_tokens.extend(token_norm(w['text']))
if transcript_tokens != aligned_tokens:
    raise ValueError(f'transcript/alignment token mismatch: {len(transcript_tokens)} transcript vs {len(aligned_tokens)} aligned')

# Partition separately at sentence-ending punctuation so sentence starts never append to prior line.
sentences=[]; current=[]
for w in words:
    current.append(w)
    if is_sentence_end(w['text']): sentences.append(current); current=[]
if current: sentences.append(current)
groups=[]
for sentence in sentences: groups.extend(partition(sentence))

cues=[]
for index,g in enumerate(groups):
    start=float(g[0]['start'])
    next_start=float(groups[index+1][0]['start']) if index+1<len(groups) else None
    display=[caption_word(x['text']) for x in g]
    cue_text=' '.join(display).replace('Belle Table','Belle-Table')
    cue_text=cue_text.replace('Chataud d\'If','Château d\'If')
    if FONT.getlength(cue_text)>MAX_TEXT_WIDTH:
        raise ValueError(f"Corrected one-line cue exceeds S01 panel: {cue_text}")
    cues.append({'cue':index+1,'text':cue_text,'text_width_px':round(FONT.getlength(cue_text),1),'word_indices':[words.index(x) for x in g],
      'source_start_seconds':start,'source_end_seconds':next_start,
      'group_words':[{'text':strip_quotes(x['text']),'caption_text':caption_word(x['text']),'source_start_seconds':float(x['start']),
        'source_end_seconds':float(x['end']),'alignment_score':float(x.get('score',0))} for x in g],
      'display_rule':'cue holds until next cue start; current highlight holds through pauses; new word highlight begins at its aligned start'})

# Source-time SRT draft uses whole groups; in-video word highlighting remains separate.
def stamp(t):
    ms=max(0,round(t*1000)); h,ms=divmod(ms,3600000); m,ms=divmod(ms,60000); s,ms=divmod(ms,1000)
    return f'{h:02}:{m:02}:{s:02},{ms:03}'
srt=[]
for c in cues:
    a=c['source_start_seconds']; b=c['source_end_seconds']
    if b is None: b=537.5
    if b<=a: raise ValueError(f'non-positive cue {c["cue"]}')
    srt.extend([str(c['cue']),f'{stamp(a)} --> {stamp(b)}',c['text'],''])
SRT.write_text('\n'.join(srt))
report={'version':'v01','status':'SOURCE_TIME_DRAFT_REVIEW_REQUIRED','episode':'016_marseille_1720','language':'en','fps':FPS,
 'source_audio_sha256':alignment['audio_sha256'],'alignment_transcript_sha256':alignment['transcript_sha256'],
 'alignment_file_sha256':sha(ALIGN),'alignment_method':'WhisperX forced alignment; estimate, not audible acceptance',
 'transcript_file_sha256':sha(TEXT),'subtitle_orthography_corrections':'See Research/FACT_CHECK_NOTES_v01.md; correct historical names and French place/currency spellings in captions only; audio unchanged.',
 'target_canvas':[1672,941],'style_profile':'Nuviko fieldnotes S01: Georgia Bold 54px, cream panel, center x=836, panel bottom y=871; one line; max width 1180px; spoken word warm yellow.',
 'group_max_words':MAX_WORDS,'max_text_width_px':MAX_TEXT_WIDTH,'font':'Georgia Bold 54 px','group_count':len(cues),'word_count':len(words),'sentence_count':len(sentences),
 'width_check':{'status':'PASS','max_measured_px':max(c['text_width_px'] for c in cues),'over_limit':sum(c['text_width_px']>MAX_TEXT_WIDTH for c in cues)},
 'cue_hold':'first cue starts at first aligned spoken word; each previous cue remains visible until next cue starts; final cue held through 537.5s',
 'word_highlight':'word starts at its aligned source start; previous word stays highlighted during pauses until the next word begins; no future-word highlight',
 'timing_status':'REVIEW_REQUIRED; no audible verification yet; source-time only, not conformed to final edit',
 'files':{'cue_map':OUT.name,'srt_source_draft':SRT.name},'cues':cues}
OUT.write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({'status':report['status'],'groups':len(cues),'words':len(words),'sentences':len(sentences),'single_word_groups':sum(len(c['group_words'])==1 for c in cues),'weak_endings':[c['text'] for c in cues if core(c['group_words'][-1]['text']) in WEAK_END]},indent=2,ensure_ascii=False))
