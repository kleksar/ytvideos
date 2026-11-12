"""Build this batch's reviewed shot inventory and track cadence profiles."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

edit = Path(__file__).resolve().parent
batch = edit.parent
repo = batch.parents[1]
stock = repo/'Work/nuviko-videos-short-batch-20261110'
pilot = repo/'Work/satisfying-runaway-pilot/Source'
local = batch/'Source/Footage'
clips = {p.stem: p for d in [stock/'new-footage',stock,pilot,local]
         for ext in ('*.mp4','*.webm') for p in d.glob(ext)}
metadata = {
    '10411103': ('wide','architecture','calm'), '13830672': ('wide','waterfall','active'),
    '15367486': ('medium','castle','calm'), '20568097': ('wide','castle','calm'),
    '26346980': ('wide','dune','calm'), '28891505': ('wide','peaks','active'),
    '29393034': ('wide','haze','calm'), '29645507': ('wide','night skyline','active'),
    '32120722': ('wide','coast','calm'), '33871227': ('wide','waterfall','active'),
    '34707370': ('medium','windows','calm'), '35065432': ('medium','valley village','calm'),
    '35091927': ('medium','night towers','active'), '35970539': ('wide','night skyline','calm'),
    '36029898': ('medium','red canyon','active'), '36410669': ('wide','bridge','active'),
    '37898716': ('medium','street lights','active'), '5061380': ('medium','forest river','active'),
    '5619693': ('medium','shore foam','active'), '6216792': ('wide','dusk','calm'),
    '7076544': ('medium','high rises','active'), '7366444': ('close','falling water','active'),
    'pexels-30320376': ('medium','mountain mist','calm'), 'pexels-35179742': ('medium','autumn falls','active'),
    'pexels-35188969': ('medium','waterfall','active'), 'pexels-36086839': ('wide','snow forest','calm'),
    'pexels-37362542': ('close','forest stream','active'),
    '10001446': ('close','wave texture','active'), '11142097': ('close','flame','active'),
    '13037145': ('medium','gull','active'), '32509235': ('wide','mountain lake','calm'),
    '33353416': ('close','flower','calm'), '33771384': ('close','water ripples','active'),
    '34535413': ('medium','dune footprints','calm'), '35867202': ('wide','turquoise lake','active'),
    '36221445': ('medium','bird','active'), '36974946': ('wide','foggy valley','calm'),
    '6316369': ('close','surf','active'), '8859850': ('medium','rock waterfall','active'),
    'amnesia-ibiza': ('close','dance floor','active'), 'nps-mowich-rainstorm': ('wide','lake mist','calm'),
    'okanagan-mule-deer': ('medium','deer','active'), 'san-francisco-timelapse': ('medium','traffic','active'),
    'usda-bumblebee': ('close','bee','active'),
}
# Left and right entries anchor the edit. Middle entries are curated alternatives for the planner.
directions = {
 'paparazzi': ('32509235 33771384 pexels-30320376 34535413 nps-mowich-rainstorm 35065432 26346980 32120722 pexels-36086839 36974946 29393034 pexels-35179742 15367486 20568097 35867202 28891505',
               [.52, .093], [.97, 1.56, 1.05, 1.55, 1.05, .95], .48, 1.67, 1.40),
 'mthu': ('usda-bumblebee 33353416 5061380 okanagan-mule-deer pexels-37362542 pexels-35188969 33871227 36221445 32120722 33771384 13830672 8859850 28891505 26346980 13037145',
          [.5085, .286], [.80, 1.28, 1.03, 1.02, 2.03, 1.03, 1.0, 2.03], .48, 2.11, .94),
 'super-funk': ('11142097 7366444 6316369 5619693 13037145 10001446 29393034 13830672 36029898 33871227 28891505 36221445 7076544 37898716 15367486 33771384 26346980 8859850 5061380',
                [.4615, .106], [.68, .92, .7, .93, .5, .9, .93], .39, 1.15, 1.05),
 'bloodstream': ('35867202 33771384 36221445 8859850 32120722 pexels-35188969 33871227 26346980 5061380 pexels-36086839 36974946 28891505 6316369 35065432 32509235',
                 None, [.82, 1.45, .92, 1.35, 1.0, 1.44], .49, 1.61, 1.08),
 'bow-bow-bow': ('amnesia-ibiza@4.5 10411103 37898716 34707370 29645507 35091927 35970539 36410669 7076544 san-francisco-timelapse 6216792 37898716@5.5 35091927@8 29645507@9 7076544@7.5 35970539@9 amnesia-ibiza@8 amnesia-ibiza@12 amnesia-ibiza@16 amnesia-ibiza@20 amnesia-ibiza@24 amnesia-ibiza@27.4',
                 [.4615, .246], [.46, .92, .46, .93, .92, .46, .92], .40, 1.10, .95),
}
old_anchors = json.loads((edit/'beat-motion-accents.json').read_text())
current = json.loads((edit/'review-index.json').read_text())
order = ('mthu','super-funk','bloodstream','bow-bow-bow','paparazzi')
if len(sys.argv)>1:
    order = (sys.argv[1],)
for name in order:
    ids,pulse,holds,lower,upper,opening = directions[name]
    ids=ids.split()
    version = old_anchors[name]['new_revision']
    previous = json.loads((edit/f'{name}-review-{version}-contract.json').read_text())
    current_row=next(r for r in current if Path(r["file"]).name==Path(previous["output"]).name)
    originals = {Path(c['path']).stem:c for c in previous['clips']}
    shots=[]
    for pos,tag in enumerate(ids):
        stem,_,source_in=tag.partition('@')
        original=originals.get(stem,{})
        path=clips[stem]
        start=float(source_in) if source_in else original.get('source_in',2.5)
        scale,subject,motion=metadata[stem]
        duration=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',str(path)]))
        if name=='bow-bow-bow' and stem=='amnesia-ibiza':
            scale='close' if float(source_in)%8==4 else 'medium'
            subject='stage lights' if float(source_in)%8==0 else 'dance floor'
        shots.append({'id':tag,'path':str(path),'source_in':start,'max_seconds':round(duration-start-.15,3),
                      'pre_crop':original.get('pre_crop',''), 'scale':scale,'subject':subject,'motion':motion,
                      'priority':.24 if pos<7 else .10})
    approved = old_anchors[name]['accents'] if name=='mthu' else []
    if name=='paparazzi':
        approved = [{'frame':41,'attack_seconds':1.376871,'strength':3.132,'role':'opening pickup'}]
    profile={'holds':holds,'min':lower,'max':upper,'opening_max':opening}
    if name=='mthu':
        profile['required']=[a['frame'] for a in approved]
    write={'media':current_row['file'],'media_sha256':current_row['sha256'],'fps':30,'frames':previous['frames'],
           'profile':profile,'pulse':pulse,'approved_accents':approved,'first':ids[0],'last':ids[-1],
           'shots':shots, 'old_revision':version,'new_revision':f'v{int(version[1:])+1:02}'}
    if name=='bow-bow-bow':
        write['motif']={'subjects':['dance floor','stage lights'],'positions':[5,9,13,16]}
    (edit/f'{name}-dynamic-input.json').write_text(json.dumps(write,indent=2)+'\n')
