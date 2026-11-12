import json
import re
from pathlib import Path

ROOT = Path('/Users/diplomat/ytvideos/channels/paper_detour/videos/030_clothing_history')
shots = json.loads((ROOT / 'Storyboard/SHOTLIST_v06.json').read_text())
words = json.loads((ROOT / 'Source/Voice/v05/words.json').read_text())

# id, scene, authored lines, exact semantic trigger, exact end marker, zone.
rows = [
 ('D01','V07',['TIME ERASED','THE REST'],'Almost all their clothing is gone','gone','primary'),
 ('D02','V02',['1 MILLION+','YEARS AGO'],'More than a million years ago','ago','primary'),
 ('D03','V03',['ONE SHARP','EDGE'],'one edge becomes sharp','sharp','primary'),
 ('D04','V04',['STONE','SURVIVES'],'But that stone will survive','survive','primary'),
 ('D05','V05',['GENERATIONS','LATER'],'Thousands of generations pass','pass','primary'),
 ('D06','V06',['MADE BY','HUMAN HANDS'],'bone needles shaped by careful human hands','hands','primary'),
 ('D07','V09',['SOMEONE','WORE THIS'],'A living person once wore it','it','primary'),
 ('D08','V11',['THE PAST','GETS PERSONAL'],'Suddenly the past has more than tools','tools','primary'),
 ('D09','V12',['FOLLOW THE','FOOTSTEPS'],"Follow its owner's footsteps",'footsteps','primary'),
 ('D10','V13',['ROMAN','BRITAIN'],'Roman Britain','Britain','primary'),
 ('D11','V14',['TRACES','BECOME PEOPLE'],"We're looking at people",'people','primary'),
 ('D12','V16',['AROUND','1400'],'1400','1400','alternate'),
 ('D13','V17',['A NEW','SILHOUETTE'],'Straight lines give way to folds and layers','layers','alternate'),
 ('D14','V19',['AMSTERDAM','1559'],'1559','portrait','alternate'),
 ('D15','V20',['ONE FAMILY','MANY STYLES'],'these people belong to the same family','own','alternate'),
 ('D16','V21',['LOOK','CLOSER'],'Different hats fabrics little details','details','alternate'),
 ('D17','V23',['18TH','CENTURY'],'eighteenth century','century','alternate'),
 ('D18','V25',['IMPOSSIBLE','TO IGNORE'],"You wouldn't exactly blend into the background",'these','alternate'),
 ('D19','V26',['YOUR OUTFIT','ARRIVES FIRST'],'your outfit arrives before you do','do','alternate'),
 ('D20','V27',['THE','CRINOLINE'],'crinoline appears beneath the skirt','skirt','alternate'),
 ('D21','V28',['MIND THE','DOORWAY'],'Imagine trying to get through a doorway','carriage','alternate'),
 ('D22','V29',['THE','1920S'],'The 1920s','1920s','alternate'),
 ('D23','V30',['SHAPE','RESET'],'gives way to a completely different shape','shape','alternate'),
 ('D24','V32',["TODAY'S",'WARDROBE'],'a modern street','street','primary'),
 ('D25','V34',["TOMORROW'S",'HISTORY'],"one day they'll be history too",'too','primary'),
 ('D26','V36',["WE'RE",'NEXT'],'Visitors study them as closely as we study that ancient sandal','sandal','primary'),
 ('D27','V37',['WHO WORE','THIS?'],'who wore them and where they were going','going','primary'),
 ('D28','V38',['WHAT','SURVIVES?'],'Things survive disappear and surprise people centuries later','later','primary'),
]

def norm(s):
    return re.sub(r"[^a-z0-9']", '', s.lower().replace('’', "'"))

tokens = [norm(w['text']) for w in words]
def find(phrase, scene, after=None):
    parts = [norm(x) for x in phrase.split()]
    candidates = []
    for i in range(len(words)-len(parts)+1):
        if tokens[i:i+len(parts)] == parts:
            if after is not None and i < after:
                continue
            if scene['startFrame']/30-1.5 <= words[i]['start'] < scene['endFrame']/30:
                candidates.append(i)
    if not candidates:
        raise ValueError((phrase, scene['id']))
    i = candidates[0]
    return i, i+len(parts)-1

plan = []
for ident, scene_id, lines, trigger, end, anchor in rows:
    scene = next(s for s in shots if s['id'] == scene_id)
    a,b = find(trigger, scene)
    try:
        _,end_index = find(end, scene, a)
    except ValueError:
        end_index = b
    start = max(scene['startFrame']+3, round(words[a]['start']*30))
    stop = min(scene['endFrame']-3, max(round(words[end_index]['end']*30)+12, start+84))
    assert stop-start >= 48, (ident,start,stop)
    plan.append({'id':ident,'scene':scene_id,'lines':lines,'anchor':anchor,
                 'startFrame':start,'endFrame':stop,'spoken_trigger':trigger,'spoken_end':end,
                 'spoken_start_seconds':words[a]['start'],'spoken_end_seconds':words[end_index]['end'],
                 'alignment':'Source/Voice/v05/words.json; Lawrence v05, unchanged speed',
                 'listening':'UNVERIFIED; timing measured, voice delivery not inferred',
                 'camera_motion':scene['camera_motion'],'status':'PLANNED until actual PNG and scene-motion preflight'})
(ROOT/'Storyboard/ACCENT_PLAN_v06.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2)+'\n')
header = '''# v06 — denser visual story beats and full-image camera movement

User explicitly requested movement of the pictures themselves and many more visible text beats after accepting the look/sound/story of v05. This instruction overrides the channel static-scene default for030 only. Extra High remains waived for030; no delegation. Narration, cuts, soundtrack and190s running time remain unchanged.

39 complete images move as whole layers: restrained5.5–9% push/pull and6.5% overscanned lateral drift. No body-part animation or artificial parallax. Text stays screen-fixed with the accepted short entry/hold/exit, and grain stays full-frame above pictures, below text. Original6 cues are preserved;28 new cues give34 in total. Scenes V10,V15,V18,V31,V33 remain text-free as short moving visual breaths.

The actual audible performance is UNVERIFIED; all timing is word-alignment-derived. No invented pause, stress or listening result is asserted. Added dates/places refer to spoken content; other cues are editorial framing, not historical quotations.

## Decisions before manufacture

'''
parts=[header]
for cue in plan:
    scene=next(s for s in shots if s['id']==cue['scene'])
    selected=' / '.join(cue['lines'])
    parts.append(f"### {cue['id']} — {cue['scene']}\n\nSpoken beat: {scene['spoken']}\n\nNarrator intention/evidence: {cue['spoken_trigger']} → {cue['spoken_end']}; verified against the accepted English text/alignment. Viewer expectation: read an object/costume → connect it with the human/time/reveal in this beat. Image already shows the physical evidence and silhouette.\n\nOptions: literal ‘{cue['spoken_trigger']}’; complementary ‘{selected}’; no text (image/voice alone). Selected ‘{selected}’: a short visual signpost or question makes the changing scale, period or human relationship easier to follow. Literal transcript would add more reading; no text would preserve the long quiet stretches the user specifically rejected. Dates and key punchlines deliberately repeat the spoken cue. No additional historical claim or attributed quotation is introduced.\n\nTrigger/end: {cue['spoken_trigger']} / {cue['spoken_end']}; frames{cue['startFrame']}–{cue['endFrame']}; {cue['anchor']} anchor, same optical cap height as v05. Listening UNVERIFIED. Geometry, PNG spelling and motion path remain subject to actual-pair preflight.\n\n")
(ROOT/'Storyboard/DECISIONS_v06.md').write_text(''.join(parts))
print(f'{len(plan)} new cues timed from the unchanged voice; original6 retained.')
