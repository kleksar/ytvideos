import json,importlib.util
from PIL import ImageFont
from pathlib import Path
p=Path('/Users/diplomat/ytvideos/.agents/skills/ytv-paper-subtitles/scripts/semantic_grouping.py')
s=importlib.util.spec_from_file_location('sg',p);sg=importlib.util.module_from_spec(s);s.loader.exec_module(sg)
w=json.load(open('Work/montage_trial_v01/words_EXPERIMENT.json'))['words'];f=ImageFont.truetype('/System/Library/Fonts/Supplemental/Georgia Bold.ttf',84)
base=['East Polynesia','South America','North America','thirteenth century','fifteenth century','mountainous coast']
candidates=['centuries before','living there','long before','forty-five thousand','twenty-one thousand','fourteen thousand','hundred years','years ago','Māori communities','hundred years','many different','Ocean routes','South Pacific']
for pair in candidates:
 try:
  groups=sg.group_words(w,f,1286,keep_together=base+[pair],combine_sentences=True)
  print(pair, 'OK',len(groups))
 except ValueError:print(pair,'UNSATISFIABLE')
