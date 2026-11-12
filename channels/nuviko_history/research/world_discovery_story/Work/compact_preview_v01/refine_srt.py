import json,re,textwrap
from pathlib import Path
root=Path(__file__).resolve().parents[2]
src=root/'Edit/Subtitles/world_discovery_en_preview_v01_DRAFT.srt';dest=root/'Edit/Subtitles/world_discovery_en_preview_v02_DRAFT.srt'
w=json.loads((root/'Work/montage_trial_v01/words_EXPERIMENT.json').read_text())['words']; blocks=src.read_text().strip().split('\n\n'); groups=[];i=0
for b in blocks:
 lines=b.splitlines();tokens=' '.join(lines[2:]).split(); n=len(tokens)
 if tokens != [v['text'] for v in w[i:i+n]]:raise ValueError(f'tokens mismatch {lines[0]}')
 groups.append({'number':int(lines[0]),'timing':lines[1], 'words':w[i:i+n], 'text':tokens});i+=n
assert i==len(w)
fix={1,14,29,61,125,133,143,164,170,174}
def stamp(s):
 ms=round(s*1000);return f'{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02},{ms%1000:03}'
for n in sorted(fix):
 a,b=groups[n-1],groups[n];b['text'].insert(0,a['text'].pop());b['words'].insert(0,a['words'].pop()); a['timing']=a['timing'].split(' --> ')[0]+' --> '+stamp(a['words'][-1]['end']);b['timing']=stamp(b['words'][0]['start'])+' --> '+b['timing'].split(' --> ')[1]
for g in groups:
 t=textwrap.wrap(' '.join(g['text']),width=42,break_long_words=False,break_on_hyphens=False)
 if len(t)>2:raise ValueError(f'too many lines in cue {g["number"]}: {t}')
 g['output']=str(g['number'])+'\n'+g['timing']+'\n'+'\n'.join(t)
dest.write_text('\n\n'.join(x['output'] for x in groups)+'\n');print('corrected cues',sorted(fix),'plus following groups')
