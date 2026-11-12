import importlib.util,json,pathlib
from PIL import ImageFont
p=pathlib.Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('grp','/Users/diplomat/ytvideos/.agents/skills/ytv-paper-subtitles/scripts/semantic_grouping.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
words=json.loads((p/'word_times_provisional.json').read_text())['words']; font=ImageFont.truetype('/System/Library/Fonts/Supplemental/ChalkboardSE.ttc',50,index=2)
groups=g.group_words(words,font,1298,combine_sentences=True); phrases=[' '.join(x['text'] for x in z) for z in groups]
changes={
('But the model assumes only two hundred and fifty','paid days in a year.'):('But the model assumes','only two hundred and fifty paid days','in a year.'),
('about one hundred and seventy-six',"days' pay for the annual basket."):("about one hundred and seventy-six days' pay",'for the annual basket.'),
('That is about a hundred fewer','wage-days than in the early sixteen hundreds.'):('That is about a hundred fewer wage-days','than in the early sixteen hundreds.'),
('Between the early fifteen hundreds and the early','sixteen hundreds, the wage-day cost went up.'):('Between the early fifteen hundreds','and the early sixteen hundreds,','the wage-day cost went up.')}
for old,new in changes.items():
 idx=next(i for i in range(len(phrases)-1) if tuple(phrases[i:i+2])==old); phrases[idx:idx+2]=new
try:g.plan_phrases(words,phrases,font,1298,combine_sentences=True)
except ValueError as e:print('invalid phrase plan:',e); raise
plan=json.loads((p/'plan_draft.json').read_text());plan['subtitles']['phrases']=phrases;(p/'plan_phrases_draft.json').write_text(json.dumps(plan,indent=2)+'\n');print('phrase plan',len(phrases),'groups; semantic and visual checks still needed')
