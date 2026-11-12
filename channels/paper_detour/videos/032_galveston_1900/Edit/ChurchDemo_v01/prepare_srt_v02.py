from pathlib import Path
import json,re,textwrap,hashlib
E=Path('/Users/diplomat/ytvideos/channels/paper_detour/videos/032_galveston_1900');D=E/'Edit/Subtitles_v02';D.mkdir(exist_ok=True)
tp=Path('/Users/diplomat/ytvideos/channels/nuviko_history/videos/017_galveston_1900/Source/Scripts/film_en.txt');raw=tp.read_text();tokens=raw.split();W=json.loads((E/'Edit/ChurchDemo_v01/words_source_v02.json').read_text())['words'];assert len(tokens)==len(W)==1514
norm=lambda s:re.sub(r'[^\w’\'-]','',s).lower()
assert all(norm(a)==norm(b['text']) for a,b in zip(tokens,W))
# Existing canonical character alignment supplies every word. Selection below only groups exact narration tokens.
starts=[w['start_seconds']/1.05 for w in W];ends=[w['end_seconds']/1.05 for w in W]
provider_last_end=ends[-1];ends[-1]=574.402608 # explicit, individually reconciled terminal word; ASR recognizes complete "itself." ending573.72, source duration574.402608
bad_end=set('a an the of to in at with from and or but as for than about nearly almost less more'.split())
cues=[];i=0
while i<len(tokens):
    candidates=[]
    for j in range(i+1,min(i+17,len(tokens))+1):
        s=' '.join(tokens[i:j]);n=j-i;duration=ends[j-1]-starts[i];lines=textwrap.wrap(s,width=42,break_long_words=False,break_on_hyphens=False)
        if len(lines)>2 or duration>6.7:break
        if j<len(tokens) and norm(tokens[j-1]) in bad_end:continue
        if n<3 and j<len(tokens) and not re.search(r'[.!?]$',tokens[j-1]):continue
        punct= bool(re.search(r'[.!?:;]$',tokens[j-1]));comma=tokens[j-1].endswith(',')
        score=abs(len(s)-58)*.12+abs(duration-3)*1.5-(5 if punct else 2 if comma else 0)
        if n==1:score+=9
        candidates.append((score,j,lines))
        if punct and n>=3:break
    assert candidates,(i,tokens[i:i+15]);_,j,lines=min(candidates)
    end=ends[j-1]
    # Small pause extension uses only an actual inter-word gap; never bridges removed audio.
    if j<len(tokens):end=min(end+.10,starts[j]-.025)
    cues.append({'start_seconds':round(starts[i],6),'end_seconds':round(end,6),'text':'\n'.join(lines),'first_word':i,'last_word':j-1});i=j
# Editorial segmentation review: restore syntactic groups and complete quantities at cue boundaries.
ends_text={8:'At the turn of the twentieth century,',15:'The highest natural ground on the island',26:'no radar maps on a phone,',32:'Some had experienced earlier storms',36:'and the information reaching the public',40:'By afternoon, people who had expected bad weather',52:'According to accounts of survivors,',55:'At the Weather Bureau,',58:'Darkness made it harder to see',71:'Some estimates are considerably higher,',72:'and the storm remains the deadliest',77:'As the scale of the losses became clear,',96:'And before the ground could rise,',99:'By 1904,',103:'While the seawall was being built,',113:'And every raised house stood among streets',115:'Water pipes, fire hydrants, and streetcar tracks',118:'It was a living city,',129:'Once an area was filled to its new grade,',135:'Imagine stepping out of a front door',138:'Taxpayers helped finance the work,',148:'A heavy masonry church,',153:'Little by little,',157:'Galveston suffered damage,',159:'The seawall and raised ground had become',162:'Hurricanes continued to threaten the island,',164:'No wall can erase the sea',170:'For years, homes stood above muddy streets'}
for num,desired in ends_text.items():
    a=cues[num-1];b=cues[num];joined=tokens[a['first_word']:b['last_word']+1];t=desired.split();assert joined[:len(t)]==t,(num,joined,t)
    boundary=a['first_word']+len(t);a['last_word']=boundary-1;b['first_word']=boundary
    for c in (a,b):
        f,l=c['first_word'],c['last_word'];c['start_seconds']=round(starts[f],6);c['end_seconds']=round(min(ends[l]+.10,starts[l+1]-.025) if l+1<len(tokens) else ends[l],6);c['text']=' '.join(tokens[f:l+1])
# Balanced, clause-aware two-line wraps; avoid splitting units, names and determiners from their objects.
protected=['one hundred miles an hour','three point three miles','American Society of Civil Engineers','Galveston and Texas History Center','Saint Patrick\'s Church','kept in place','low barrier island','seven hundred jacks','wooden supports','thirty-eight thousand','two thousand','three thousand','seven hundred','five feet','nine feet','sixteen feet','seventeen feet','six thousand','United States','Gulf Coast','Saint Patrick\'s','Isaac Cline','Galveston and Texas','Civil Engineers','three point three','Weather Bureau','Hurricane Ike','screw jacks','mean low water','narrow wooden path','American South']
expanded=[]
for c in cues:
    f,l=c['first_word'],c['last_word'];ts=' '.join(tokens[f:l+1])
    can_wrap=len(ts)<=42 or any(max(len(' '.join(tokens[f:k])),len(' '.join(tokens[k:l+1])))<=42 and not any(p in ts and p not in ' '.join(tokens[f:k]) and p not in ' '.join(tokens[k:l+1]) for p in protected) for k in range(f+1,l+1))
    if not can_wrap or ends[l]-starts[f]>7:
        choices=[]
        for mid in range(f+2,l):
            a=' '.join(tokens[f:mid]);b=' '.join(tokens[mid:l+1])
            if min(len(a),len(b))<12 or max(len(a),len(b))>82:continue
            if norm(tokens[mid-1]) in bad_end:continue
            if any(p in ts and p not in a and p not in b for p in protected):continue
            choices.append((abs(len(a)-len(b))-(15 if a.endswith(',') else 0),mid))
        assert choices,ts;mid=min(choices)[1]
        intervals=[(f,mid-1),(mid,l)]
    else:intervals=[(f,l)]
    for a,b in intervals:expanded.append({'first_word':a,'last_word':b,'text':' '.join(tokens[a:b+1]),'start_seconds':round(starts[a],6),'end_seconds':round(min(ends[b]+.10,starts[b+1]-.025) if b+1<len(tokens) else ends[b],6)})
cues=expanded
for c in cues:
    ts=' '.join(c['text'].split());parts=ts.split()
    if len(ts)<=42:c['text']=ts;continue
    opts=[]
    for k in range(1,len(parts)):
        l=' '.join(parts[:k]);r=' '.join(parts[k:]);
        if max(len(l),len(r))>42:continue
        if any(p in ts and p not in l and p not in r for p in protected):continue
        score=abs(len(l)-len(r))+(24 if norm(parts[k-1]) in bad_end else 0)-(8 if l.endswith((',',':',';')) else 0)
        opts.append((score,l+'\n'+r))
    assert opts,ts;c['text']=min(opts)[1]
for c in cues:
    if c['text'].replace('\n',' ')=='According to the Galveston and Texas History Center,':c['text']='According to the\nGalveston and Texas History Center,'
out={'language':'en','timebase':'final','cues':[{k:c[k] for k in ('start_seconds','end_seconds','text')} for c in cues]}
(D/'cues_v02.json').write_text(json.dumps(out,indent=2,ensure_ascii=False));(D/'segmentation_review_v02.txt').write_text('\n'.join(f"{i+1:03} {c['start_seconds']:.3f}-{c['end_seconds']:.3f} {c['text'].replace(chr(10),' / ')}" for i,c in enumerate(cues)))
(D/'conform_v02.json').write_text(json.dumps({'audio':'channels/nuviko_history/videos/017_galveston_1900/Source/Voice/odom_5vsg/film/voice_en_105.wav','audio_sha256':'ddfe274d2a67c1250053192a0ef3b28f41cdd49e3120404a0fa9f8700ce5cd52','alignment':'voice_en.alignment.json','alignment_speed_divisor':1.05,'editor_audio_speed':1,'final_start':0,'retained_source':[0,574.402608],'narration_words':1514,'terminal_provider_word_end':provider_last_end,'terminal_corrected_end':574.402608,'terminal_resolution':'Only final itself word overrun reconciled individually: inspect_media ASR recognizes itself.573.24-573.72; punctuation/whitespace excluded; exact original WAV duration574.402608 used as terminal hold end. No global shift/compression/clamp.','timing_mapping':'VERIFIED_STILL_BASELINE9A5FE055; bind resulting unchanged track and final MP4 after export','subjective_listening':'UNVERIFIED','final_media':'PENDING'},indent=2))
print('cues',len(cues))
