import pathlib,json,re,hashlib,difflib
root=pathlib.Path.cwd();w=root/'Work'; original=json.load(open(w/'word_map_mix_draft_v01.json')); forced=json.load(open(w/'asr_check_v01/hybrid_alignment_prefer_b_draft_v02.json'))['words'];target=original['words']; norm=lambda s:re.sub(r'[^a-z0-9]','',s.lower());a=[norm(x['text']) for x in target];b=[norm(x['text']) for x in forced];sm=difflib.SequenceMatcher(None,a,b,autojunk=False);out=[None]*len(target); corrections=[]
for op,i,j,k,l in sm.get_opcodes():
 if op=='equal':
  for ii,kk in zip(range(i,j),range(k,l)):
   x=forced[kk];out[ii]={'text':target[ii]['text'],'start':x['start'],'end':x['end']}
 elif op=='replace' and (i,j,k,l)==(436,437,436,438):
  # Full spoken number is a single transcript token; two aligner number tokens undercount its duration.
  out[i]={'text':target[i]['text'],'start':forced[k]['start'],'end':forced[l]['start']-.001};corrections.append({'token_index':i,'reason':'merged 1 + 300 as one transcript token; end extends to just before next word estimated onset, needs listening'})
 elif op=='delete' and j==i+1 and target[i]['text']=='—':
  corrections.append({'token_index':i,'reason':'unspoken punctuation; display event put in available neighboring gap'})
 else: raise ValueError((op,i,j,k,l))
for i,x in enumerate(out):
 if x is None:
  left=out[i-1]['end'];right=out[i+1]['start'];
  if right-left<.004:raise ValueError(('no punctuation gap',i,left,right))
  start=round(left+(right-left)/3,3);end=round(left+2*(right-left)/3,3);out[i]={'text':target[i]['text'],'start':start,'end':end}
for i,x in enumerate(out):
 if not 0 <= x['start'] < x['end'] <=559.84: raise ValueError(('bounds',i,x))
 if i and x['start']<out[i-1]['end']:raise ValueError(('overlap',i,x,out[i-1]))
r={'status':'DRAFT_NOT_FINAL','audio_sha256':original['audio_sha256'],'transcript_sha256':original['transcript_sha256'],'words':out,'source':'Original WhisperX B preferred by user on three excerpts; shifted chunk estimates used for 105 word boundaries by heuristic. See hybrid_alignment_prefer_b_draft_v02.json and user receipt.','limitations':'Most word onsets and all local corrections have not been heard; do not use as accepted final map or full render input. Punctuation-only tokens use available silence, not claimed speech.','corrections':corrections}
path=w/'word_map_mix_prefer_b_draft_v01.json';path.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n');print('tokens',len(out),'map',path,'last',out[-1])
