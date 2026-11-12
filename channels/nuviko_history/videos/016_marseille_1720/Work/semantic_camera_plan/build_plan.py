from pathlib import Path
import json
EP=Path(__file__).resolve().parents[2]
# Scene-specific focus decisions from inspected originals and accepted narration.
rows='''
ship|.72,.52|I
health official refusing entry|.66,.45|L+
covered body on deck|.51,.64|U+
worried captain|.67,.43|L+
health papers between captain and officials|.40,.64|R+
mainland quarantine gate and porters|.70,.46|L+
captain behind prison bars|.23,.43|R+
deserted street leading into the city|.67,.56|L-
cordon and inspection|.48,.53|O
warning ignored by seated officials|.49,.56|I
harbour cargo beside ship|.53,.57|L-
departing three-masted ship|.66,.52|L+
captain and navigator over chart|.43,.63|R+
captain at trading-port window|.36,.46|O
busy trading waterfront|.51,.51|I
hands examining valuable cloth|.57,.59|U+
merchant ship alongside dock|.56,.47|L-
porters raising cargo bales|.47,.57|I
hands touching silk|.59,.51|R+
valuable goods filling the hold|.64,.56|L-
market buyers|.46,.54|I
merchant waiting beside an hourglass|.31,.48|R+
sealed commercial papers on textiles|.46,.58|I
senior merchant in his office|.45,.44|O
two men discussing the cargo|.45,.51|I
sailor handling rigging|.78,.51|L+
sick passenger in bunk|.65,.63|I
man attending the sick crew|.53,.49|O
abandoned cup in empty infirmary|.21,.56|R+
helpless sick man|.37,.57|I
surgeon's bag and folded bandages|.55,.63|U+
anxious captain clutching book|.62,.46|L+
captain writing his account|.45,.53|I
captain isolated above crew|.76,.30|L-
ship kept far from shore|.50,.54|I
captain pointing towards shore|.39,.40|R+
authority refusing the approaching boat|.50,.56|O
sealed health papers|.48,.68|I
ship off rocky Marseille coast|.89,.50|L+
captain looking towards Marseille|.31,.48|R-
arrival at trading port|.65,.47|L+
health officer questioning a sailor|.53,.45|I
quarantine record in front of official|.51,.61|U+
captain presenting documents|.51,.55|I
ship waiting at a distance|.73,.52|L-
remote quarantine island|.59,.44|I
isolated island seen from ship|.58,.45|O
bills of health and seals|.57,.66|U+
captain's declaration on table|.50,.59|I
closed ledger and health bill|.52,.55|O
official weighing two documents|.47,.51|I
people and belongings entering quarantine|.56,.51|L+
quarantine doors opening toward city|.51,.53|I
cargo behind mainland barrier|.60,.58|L-
merchants making a decision over papers|.50,.59|I
everyday market life continuing|.52,.52|O
porter struggling beside infirmary|.35,.58|R+
covered body under watch|.52,.58|I
exhausted porters beside bales|.63,.53|L+
people leaving quarantine along path|.43,.54|R-
passengers walking out through gate|.62,.53|L-
quarantine wall with city beyond|.47,.52|O
textiles handled near the city|.48,.60|I
woman falling ill at street corner|.27,.52|R+
sick woman and carer|.31,.52|I
physician examining the woman|.59,.48|L+
tailor weakening at his worktable|.57,.51|I
bereaved household around covered body|.50,.56|O
physician inspecting swollen gland|.53,.48|I
sick man overlooked at busy market|.90,.62|L+
cargo workers next to city officials|.60,.47|I
crowded city seen across rooftops|.48,.56|O
quiet street awaiting outbreak|.62,.59|L+
Marseille street layout on map|.64,.51|I
sick porter at closed doorway|.23,.57|R+
hourglass beside physician's report|.26,.57|I
patients filling the infirmary|.50,.54|O
woman looking out at departing families|.65,.51|L-
families carrying belongings out of city|.50,.53|O
closed gate stopping passage|.52,.45|I
quarantine store with goods left idle|.44,.55|R-
empty market square|.52,.53|O
bearers carrying body through crowded street|.53,.53|I
covered bodies left in narrow street|.40,.64|R-
overwhelmed city council|.43,.52|I
funeral bearers below crowded rooftops|.62,.63|L+
organizer directing burial workers|.45,.47|I
workers carrying bodies along fortification|.57,.57|O
workers digging mass burial trench|.52,.58|U+
clergyman accompanying body bearers|.72,.48|L-
resident offering food to elderly woman|.55,.53|I
exhausted man in isolated room|.74,.54|L+
physician caring for a dying patient|.37,.49|R+
city officials confronting report|.51,.58|I
silent Marseille waterfront|.50,.55|O
neighbour bringing help to doorway|.62,.53|L+
official stamping order|.37,.59|I
people leaving ship for shore|.51,.64|U-
ship isolated off island|.65,.48|L+
burning ship and flames|.45,.44|I
wreck remains spread along coast|.48,.62|O
empty infirmary|.46,.55|R-
cargo on silent waterfront|.64,.62|L-
people forcing quarantine doors|.54,.51|I
ledger and hourglass marking consequences|.57,.57|O
Provence on map|.53,.48|I
record book opened at table|.55,.59|U+
prisoner led under guard|.53,.45|I
island fortress enclosing captain|.50,.46|O
captain behind barred window|.62,.46|L+
judge applying seal to decision|.47,.62|I
captain standing outside prison gate|.35,.48|R-
quiet port after release|.50,.54|O
ordinary street life returning|.51,.56|I
Jarre island across open water|.50,.45|O
divers approaching wreck|.41,.51|R+
diver beside exposed ship timbers|.55,.57|I
preserved hull planking|.57,.48|L+
diver's light revealing wreck remains|.55,.62|U+
archivist comparing map and wreck photograph|.52,.62|I
official thinking beside health record|.34,.47|R+
ledger and sealed papers representing decisions|.53,.60|I
Marseille and distant quarantine island|.51,.49|O
wreck remains beside documentary record|.53,.54|I
captain and city official separated by gate|.49,.52|O
hand beside rich textiles and closed ledger|.57,.53|I
Marseille harbour after the catastrophe|.52,.55|O
'''.strip().splitlines()
assert len(rows)==127,len(rows)
sources=json.loads((EP/'Edit/ImageMotion/sources.json').read_text());ranges=json.loads((EP/'Work/layered_motion_v01/scene_ranges.json').read_text());spoken=json.loads((EP/'Storyboard/SHOT_MAP_v01.json').read_text())['scenes']
plan=json.loads((EP/'Edit/FFmpeg/montage_v04.json').read_text());items=[];previous=None;previous_zoom=None
for i,(row,source,r,story) in enumerate(zip(rows,sources,ranges,spoken)):
 subject,xy,mode=row.split('|');fx,fy=map(float,xy.split(','));direction={'L':'right_to_left','R':'left_to_right','U':'bottom_to_top','D':'top_to_bottom'}.get(mode[0],'none');zoom='out' if mode=='O' or mode.endswith('-') else 'in'
 if direction==previous:direction='none'
 if zoom==previous_zoom:zoom='out' if zoom=='in' else 'in'
 previous=direction;previous_zoom=zoom
 zs,ze=(1.075,1.100) if zoom=='in' else (1.100,1.075)
 start=[.5,.5];end=[fx-(fx-.5)*zs/ze,fy-(fy-.5)*zs/ze]
 if direction=='right_to_left':end[0]+=.016
 if direction=='left_to_right':end[0]-=.016
 if direction=='bottom_to_top':end[1]+=.016
 if direction=='top_to_bottom':end[1]-=.016
 camera={'focus':[fx,fy],'subject':subject,'reason':('Concentrate on ' if zoom=='in' else 'Reveal the surroundings of ')+subject+'. Preserve the focus while gently guiding the eye; direction respects the adjacent scene.', 'spoken_context':story.get('spoken_text_asr_draft',''),'start':{'center':start,'scale':zs},'end':{'center':end,'scale':ze}}
 items.append({'image':source['image'],'start_frame':r['start'],'end_frame':r['end'],'direction':direction,'zoom':zoom,'camera':camera})
plan['scenes']=items;(EP/'Edit/FFmpeg/montage_v06.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2)+'\n')
print('Wrote',len(items),'scene-specific camera plans')
