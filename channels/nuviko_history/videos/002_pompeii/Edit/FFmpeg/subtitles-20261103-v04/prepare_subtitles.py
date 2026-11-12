from pathlib import Path
import importlib.util,json
from PIL import ImageFont
ROOT=Path('/Users/diplomat/ytvideos');EP=ROOT/'channels/nuviko_history/videos/002_pompeii';EDIT=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('montage',ROOT/'automation/ffmpeg_montage/montage.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
p=EDIT/'montage_plan_v04.json';plan=json.loads(p.read_text());words=json.loads(Path(plan['subtitles']['words']).read_text())['words'];f=ImageFont.truetype('/System/Library/Fonts/Supplemental/Georgia Bold.ttf',84)
pairs='busy street;clear storytelling;cinematic reconstructions;following morning;famous cities;ancient Rome;trading city;spacious houses;painted walls;very different;major eruption;powerful earthquake;late summer;wide branches;ordinary smoke;little stone;continuous rain;piling up;escape route;important part;dramatic event;Roman fleet;city gates;larger situation;cutting off;fallen material;rather than;volcanic ash;pyroclastic flows;falling stones;tremendous speed;thick layer;ordinary room;loose rock;ground-floor room;volcanic deposits;open door;destructive forces;falling pumice;collapsing buildings;no chance;hours earlier;archaeological evidence;building materials;plaster casts;nineteenth century;hollow spaces;entire population;human lives;final decision;ordinary day;long night;scorching cloud;final day'
pairs=[x.strip() for x in pairs.split(';')]
groups=[];exceptions=[]
for a,b in m.grouping.sentence_ranges(words):
 try:groups.extend(m.grouping.group_words(words[a:b],f,1308,keep_together=pairs))
 except ValueError:
  exceptions.append({'sentence':' '.join(w['text'] for w in words[a:b]),'reason':'Optional phrase bonds cannot fit with adjacent compulsory syntax at shared width; use syntax-safe default partition.'});groups.extend(m.grouping.group_words(words[a:b],f,1308))
phrases=[' '.join(w['text'] for w in g) for g in groups]
m.grouping.plan_phrases(words,phrases,f,1308)
plan['subtitles']['phrases']=phrases;p.write_text(json.dumps(plan,ensure_ascii=False,indent=2)+'\n')
(EDIT/'groups_review_v04.txt').write_text('\n'.join(f'{i+1:03d} {g[0]["start"]:.3f} '+x for i,(g,x) in enumerate(zip(groups,phrases)))+'\n')
(EDIT/'semantic_handoff.json').write_text(json.dumps({'groups':len(groups),'keep_together':pairs,'optional_bonds_not_used':exceptions,'width_px':1308,'exact_tokens_preserved':True,'timing_source':plan['subtitles']['words']},indent=2)+'\n')
print('Reviewed phrase plan:',len(groups),'groups')
