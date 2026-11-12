from pathlib import Path
import json,re,hashlib,textwrap
P=Path('/Users/diplomat/ytvideos/channels/paper_detour/videos/030_clothing_history');E=P/'Edit/v14';w=json.loads((P/'Source/Voice/v05/words.json').read_text());segments=(E/'srt_segments.txt').read_text().splitlines();cues=[];mapping=[];i=0
for no,line in enumerate(segments,1):
 tokens=line.split();actual=[x['text'] for x in w[i:i+len(tokens)]]
 assert tokens==actual,(no,tokens,actual)
 first=w[i];last=w[i+len(tokens)-1];start=first['start'];end=last['end'];wrapped=[line] if len(line)<=42 else min(([line[:k],line[k+1:]] for k in range(len(line)) if line[k]==' ' and k<=42 and len(line)-k-1<=42),key=lambda pair:abs(len(pair[0])-len(pair[1])));assert len(wrapped)<=2
 cues.append({'start_seconds':start,'end_seconds':end,'text':'\n'.join(wrapped)})
 mapping.append({'cue':no,'words':[i,i+len(tokens)],'source_start':start,'source_end':end,'final_start':start,'final_end':end,'text':line,'duration':round(end-start,3),'cps':round(len(line)/(end-start),2)})
 i+=len(tokens)
assert i==len(w),(i,len(w));assert ' '.join(segments)==' '.join((P/'Source/Script/NARRATION_EN_v05_20261102.txt').read_text().split())
(E/'SRT_CUES_v14.json').write_text(json.dumps({'cues':cues},indent=2));(E/'SRT_CONFORM_v14.json').write_text(json.dumps({'mapping':'final=source; source_in=0,final_start=0,speed=1; accepted AAC untouched; +5ms codec residual under1frame confirmed by seven landmarks','voice_sha256':'353e12d00c37a25d6724aae5bdff9a1ca5a32e240b1a53de1af3612d2519f3ff','original_word_count':len(w),'rows':mapping,'last_cue_note':'Existing word end187.6 retained. Raw trailing punctuation ends187.76; spoken us letters end187.44; no new clamp.'},indent=2))
print('cues',len(cues),'words',i);print('short/fast',[(x['cue'],x['text'],x['duration'],x['cps']) for x in mapping if x['duration']<.7 or x['cps']>25])
