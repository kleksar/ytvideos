#!/usr/bin/env python3
"""Build a frame-exact, transcript-informed still montage map for 002_en_long."""
import csv, json, math
from pathlib import Path

ROOT = Path('/Users/diplomat/Desktop/pompei_story')
TRANSCRIPT = ROOT / '_montazh' / 'ElevenLabs_At_first,_lightweight_white_stones_began_.json'
OUT = Path(__file__).with_name('pompeii_montage_map.csv')
FPS = 30
TOTAL_FRAMES = 27185
TOTAL_SECONDS = TOTAL_FRAMES / FPS
# Each range is a narrative block; image numbers are curated from visual review and the montage plan.
BLOCKS = [
 (0,23.04,[27,2,13,25],'Opening: pumice, shelter, roof danger'),
 (23.04,49.44,[30,7,25],'79 AD and residents’ choices'),
 (49.44,73.12,[30,18,28,20],'Evidence: objects, letters, deposits, archaeology'),
 (73.12,115.36,[3,23,30,24,23,30],'Ordinary Pompeii, trades, homes, social differences'),
 (115.36,141.04,[6,3,1],'Vesuvius, its slopes, familiar landscape'),
 (141.04,167.28,[4,20,22],'Earthquake damage, repairs, traces'),
 (167.28,190.32,[3,6,1],'Late summer/fall and date uncertainty'),
 (190.32,212.32,[14,5,18],'Eruption column; Pliny observes from Misenum'),
 (212.32,237.28,[1,6,5],'Eruption mechanics and wind toward Pompeii'),
 (237.28,276.40,[6,2,27,13,2,27,13],'Pumice begins, close detail, streets and roofs'),
 (276.40,303.60,[25,13,10,4],'Sheltering and roof collapse risk'),
 (303.60,328.00,[7,13,19],'Some leave; survivors and later returns'),
 (328.00,395.92,[5,8,26,29,8],'Pliny the Elder, fleet, route to Stabiae; not Pompeii gates'),
 (395.92,417.92,[9,13,27],'Evening darkness and buried streets'),
 (417.92,471.04,[10,4,20,25,10],'Night shaking, weakened buildings, difficult choice'),
 (471.04,491.92,[11,5],'Pliny the Younger and his mother across the bay'),
 (491.92,542.48,[9,12,12,12,12,12],'Herculaneum: distinct overnight pyroclastic sequence'),
 (542.48,584.88,[13,25,27,2,13],'Pompeii next morning, pumice accumulation'),
 (584.88,594.88,[14],'Eruption column collapses'),
 (594.88,642.24,[15,16,15,16],'Pyroclastic flow reaches Pompeii; no glowing lava river'),
 (642.24,668.24,[15,16,25],'Duration, heat, uncertainty about individual deaths'),
 (668.24,688.00,[17,22],'Burial of the city'),
 (688.00,715.76,[29,18,20],'Pliny dies at Stabiae; letters compared with archaeology'),
 (715.76,747.92,[19,20,17],'Survivors, return attempts, ruins gradually covered'),
 (747.92,761.04,[20,30],'18th-century excavations'),
 (761.04,819.04,[21,28,21,28,21,28],'Respectful explanation of voids and plaster casts'),
 (819.04,846.08,[22,23,24,30,23,24],'Daily life: streets, bakery, homes, objects'),
 (846.08,873.44,[3,1,5,7,25],'Pompeii as home; practical question of survival'),
 (873.44,887.04,[7,25,15],'Different outcomes: escape, roofs, later flow'),
 (887.04,TOTAL_SECONDS,[17,30],'Ash preserves traces; close on ordinary life'),
]

doc=json.loads(TRANSCRIPT.read_text())
ends=sorted({float(s['end']) for s in doc['segments']})
starts=sorted({float(s['start']) for s in doc['segments']})
bounds=sorted(set(ends+starts))
rows=[]
frame=0
for bstart,bend,pool,note in BLOCKS:
    t=bstart
    shot_index=0
    while bend-t > 1e-6:
        remaining=bend-t
        if remaining <= 15.0:
            cut=bend
        else:
            lo=t+6.0; hi=min(t+15.0,bend)
            candidates=[x for x in bounds if lo-1e-6 <= x <= hi+1e-6]
            if candidates:
                cut=min(candidates,key=lambda x:(abs(x-(t+10.5)),x))
            else:
                cut=min(t+12.0,bend)
        if cut <= t+1e-6:
            raise RuntimeError(f'Non-progressing cut in {note}: {t} -> {cut}')
        img=pool[shot_index % len(pool)]
        start_frame=frame
        end_frame=min(TOTAL_FRAMES,round(cut*FPS))
        if end_frame <= start_frame:
            raise RuntimeError('Frame rounding produced an empty shot')
        seg_text=' '.join(s['text'].strip() for s in doc['segments'] if s['start'] < cut and s['end'] > t)
        rows.append({
            'shot':len(rows)+1,'start_frame':start_frame,'end_frame':end_frame,
            'start_seconds':f'{start_frame/FPS:.3f}','end_seconds':f'{end_frame/FPS:.3f}',
            'duration_seconds':f'{(end_frame-start_frame)/FPS:.3f}',
            'image_number':f'{img:02d}','narration_reference':seg_text,
            'story_block':note,
        })
        frame=end_frame
        t=cut
        shot_index+=1
if frame != TOTAL_FRAMES:
    # Carry frame rounding drift into the final shot so the picture ends exactly with the existing timeline.
    rows[-1]['end_frame']=TOTAL_FRAMES
    rows[-1]['end_seconds']=f'{TOTAL_SECONDS:.3f}'
    rows[-1]['duration_seconds']=f'{(TOTAL_FRAMES-int(rows[-1]["start_frame"]))/FPS:.3f}'
    frame=TOTAL_FRAMES
with OUT.open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0]))
    w.writeheader(); w.writerows(rows)
used=sorted({int(r['image_number']) for r in rows})
print(json.dumps({'rows':len(rows),'total_frames':frame,'total_seconds':TOTAL_SECONDS,'max_shot_seconds':max(int(r['end_frame'])-int(r['start_frame']) for r in rows)/FPS,'min_shot_seconds':min(int(r['end_frame'])-int(r['start_frame']) for r in rows)/FPS,'images_used':used,'missing_images':sorted(set(range(1,31))-set(used)),'map':str(OUT)},ensure_ascii=False))
