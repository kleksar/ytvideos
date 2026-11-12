"""Allocate distinct video sources across the five current review timelines."""
import json
from pathlib import Path
import subprocess
import sys

edit = Path(__file__).resolve().parent
root = edit.parent
repo = root.parents[1]
stock = json.loads((root/'Source/Footage/stock-20261111-manifest.json').read_text())
available = {str(x['id']):x for x in stock if 'file' in x}
old = {}
for path in edit.glob('*-dynamic-input.json'):
    for shot in json.loads(path.read_text())['shots']:
        old.setdefault(shot['id'],shot)
index = {Path(x['file']).name:x for x in json.loads((edit/'review-index.json').read_text())}
tags = {
 '1792746':('close','damselfly','calm'), '4800092':('close','ladybird','active'),
 '8225196':('close','snail','calm'), '36683560':('medium','butterfly','active'),
 '8031854':('close','wing on stem','calm'), '31150724':('medium','squirrel in tree','active'),
 '37065730':('medium','squirrel foraging','active'), '33909106':('medium','jellyfish','calm'),
 '38680136':('wide','turtle reef','active'),
 '32106032':('wide','stone ridge','active'), '4288052':('wide','golden fog','calm'),
 '7964548':('medium','red ridge','calm'), '8366004':('wide','coastal mountains','active'),
 '29674793':('medium','mountain path','active'),
 '29204046':('wide','cloud forest','active'), '8357584':('medium','cliff rock','active'),
 '4208318':('medium','stone escarpment','active'), '36310592':('close','cascade aerial','active'),
 '11924928':('wide','green valley','active'), '32646884':('wide','alpine ravine','calm'),
 '9669145':('close','red clouds underwater','active'), '7145060':('medium','green and red ink','active'),
 '7565621':('close','paint diffusion','active'), '6378175':('close','spark tracing','active'),
 '34387937':('close','flare','active'), '4194080':('medium','spark shower','active'),
 '28985119':('medium','skateboard','active'), '18450934':('wide','river flight','active'),
 '19829354':('wide','fireworks reflection','active'), '31619152':('close','blue diffusion','active'),
 '7722388':('medium','dance floor','active'), '37301839':('close','dance floor','active'),
 '35234123':('wide','dance floor','active'), '9003388':('medium','dance floor','active'),
 '12893900':('close','stage lights','active'), '31569926':('close','dance floor','active'),
 '7269160':('close','DJ deck','active'), '7271358':('medium','dance floor','active'),
 '9956024':('wide','crosswalk','active'), '32779195':('medium','street lights','active'),
 '30432352':('medium','night traffic','active'), '34290117':('wide','pedestrians','active'),
 '27937641':('wide','old city at night','calm')
}
inventory = {
 'mthu': '36683560 usda-bumblebee 8225196 1792746 4800092 37065730 31150724 33909106 38680136 okanagan-mule-deer 33353416 pexels-37362542 5061380 8031854',
 'paparazzi': '32509235 32106032 4288052 7964548 8366004 29674793 26346980 34535413 nps-mowich-rainstorm 35065432 pexels-36086839 36974946 29393034 15367486 20568097 pexels-30320376 28891505',
 'bloodstream': '35867202 33771384 36221445 32120722 pexels-35188969 33871227 29204046 8357584 4208318 36310592 11924928 32646884 pexels-35179742 8859850',
 'super-funk': '11142097 7366444 6316369 5619693 13037145 10001446 13830672 36029898 9669145 7145060 7565621 6378175 34387937 4194080 28985119 18450934 31619152 19829354',
 'bow-bow-bow': '7722388 37301839 35234123 9003388 12893900 31569926 7269160 7271358 9956024 32779195 30432352 34290117 27937641 10411103 37898716 34707370 29645507 35091927 35970539 7076544 36410669 6216792'
}
keys = [k for group in inventory.values() for k in group.split()]
assert len(keys)==len(set(keys))

def make_shot(ident):
    if ident in old:
        return dict(old[ident])
    if ident not in available:
        raise ValueError(f'Missing candidate {ident}')
    src=available[ident]
    scale,subject,motion=tags[ident]
    source_in=.75
    if ident in {'36683560','6378175','19829354'}:
        source_in=1.1
    return {'id':ident,'path':src['file'],'source_in':source_in,'max_seconds':src['duration']-source_in-.2,
            'pre_crop':'','scale':scale,'subject':subject,'motion':motion,'priority':.35,
            'sha256':src['sha256'],'source_page':src['page']}

for name in (sys.argv[1:] or inventory):
    prior=json.loads((edit/f'{name}-dynamic-input.json').read_text())
    version=prior['new_revision']
    version_next=f'v{int(version[1:])+1:02}'
    original=json.loads((edit/f'{name}-review-{version}-contract.json').read_text())
    row=index[Path(original['output']).name]
    ids=inventory[name].split()
    prior.update(media=row['file'],media_sha256=row['sha256'],old_revision=version,new_revision=version_next,
                 shots=[make_shot(i) for i in ids],first=ids[0],last=ids[-1])
    if name=='bow-bow-bow':
        prior['last']='31569926'
        prior['motif']={'subjects':['dance floor','stage lights','DJ deck'],'positions':[5,9,13,16]}
    if name=='mthu':
        # Keep the seven primary accents and a consistent one-second secondary cadence.
        prior['last']='33909106'
    if name=='super-funk':
        prior['profile']['required']=[363,377,391,404]
        prior['profile']['holds']=[.93,.93,.92,.92,.70,.92]
        prior['profile']['max']=1.4
    (edit/f'{name}-unique-input.json').write_text(json.dumps(prior,indent=2)+'\n')
