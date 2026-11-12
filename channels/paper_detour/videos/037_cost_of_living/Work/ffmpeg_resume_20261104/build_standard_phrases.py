import importlib.util,json,pathlib
from PIL import ImageFont
w=pathlib.Path(__file__).resolve().parent; path=w/'renderer_root/.agents/skills/ytv-paper-subtitles/scripts/semantic_grouping.py';s=importlib.util.spec_from_file_location('g',path);g=importlib.util.module_from_spec(s);s.loader.exec_module(g); words=json.loads((w/'forced_alignment.json').read_text())['words'];font=ImageFont.truetype('/System/Library/Fonts/Supplemental/ChalkboardSE.ttc',84,index=2)
manual={
'That gap is the meaning of the three hundred and thirty-three wage-days.':['That gap is the meaning of the','three hundred and thirty-three','wage-days.'],
"For the first half of the fifteen hundreds, the London building-labourer figures give us a more precise comparison: about one hundred and seventy-six days' pay for the annual basket.":['For the first half','of the fifteen hundreds,','the London building-labourer','figures give us','a more precise','comparison: about','one hundred and seventy-six',"days' pay",'for the annual basket.'],
"On the model's two-hundred-and-fifty-day year, that leaves a margin above this particular bill.":["On the model's",'two-hundred-and-fifty-day','year, that leaves a margin','above this particular bill.']}
original=g._partition_sentence
def partition(ws,*args,**kwargs):
 try:return original(ws,*args,**kwargs)
 except ValueError:
  sentence=' '.join(x['text'] for x in ws)
  if sentence not in manual:raise
  ans=[];i=0
  for text in manual[sentence]:
   n=len(text.split()); x=ws[i:i+n]; assert ' '.join(q['text'] for q in x)==text;ans.append(x);i+=n
  assert i==len(ws);return ans
g._partition_sentence=partition
groups=g.group_words(words,font,1298,combine_sentences=True);phrases=[' '.join(x['text'] for x in group) for group in groups]
repairs=[
 (["For sixteen","hundred to sixteen forty-nine,"],["For sixteen hundred","to sixteen forty-nine,"]),
 (["rises from three point two","grams to seven point one."],["rises","from three point two grams","to seven point one."]),
 (["It sets wage","limits and provides","penalties for disobedience."],["It sets wage limits","and provides penalties","for disobedience."]),
 (["Between the early fifteen","hundreds and the early","sixteen hundreds,"],["Between the early","fifteen hundreds and the early","sixteen hundreds,"])]
for old,new in repairs:
 i=next(i for i in range(len(phrases)-len(old)+1) if phrases[i:i+len(old)]==old);phrases[i:i+len(old)]=new
exceptions=[{'left':'That gap is the meaning of the','right':'three hundred and thirty-three','reason':'User requested standard size and separating number from unit; this article remains with the preceding phrase because the full following number exceeds the width.'},{'left':'comparison: about','right':'one hundred and seventy-six','reason':'User requested standard size and separating number from unit; the complete number fits alone, but not with its modifier.'}]
g.plan_phrases(words,phrases,font,1298,combine_sentences=True,boundary_exceptions=exceptions)
plan=json.loads((w/'plan_forced_draft.json').read_text());plan['subtitles']['phrases']=phrases;plan['subtitles']['boundary_exceptions']=exceptions;(w/'plan_standard_draft.json').write_text(json.dumps(plan,indent=2)+'\n');print('standard-size groups:',len(phrases),'exceptions:',len(exceptions))
