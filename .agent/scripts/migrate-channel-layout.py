#!/usr/bin/env python3
"""One-time channel-layout migration with recovery snapshots; no network or publication actions."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil

ROOT = Path(__file__).resolve().parents[2]
RUN = ROOT / 'Work/channel_layout_20261104'
SKIP = {'.git', '.venv', 'venv', 'node_modules', '__pycache__', 'site-packages', '.cache'}
TEXT = {'.md', '.py', '.json', '.toml', '.yaml', '.yml', '.sh', '.txt', '.csv', '.ffconcat', '.srt', '.ini', '.cfg'}
MEDIA = {'.png','.jpg','.jpeg','.webp','.gif','.mp3','.wav','.m4a','.mp4','.mov','.aac','.flac','.mkv','.ogg'}

def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda:f.read(1024*1024), b''): h.update(block)
    return h.hexdigest()

def mapping():
    pairs = {'new_channel':'channels/paper_detour', 'stories':'archive/legacy_stories',
             'borisenko':'projects/borisenko', 'stories/automation':'automation',
             'stories/brand/nuviko':'channels/nuviko_history/brand',
             'stories/docs/story-shorts-v1':'channels/nuviko_stories/docs/story-shorts-v1',
             'stories/docs/NUVIKO_HISTORY_STORYTELLING_STANDARD.md':'channels/nuviko_history/docs/STORYTELLING_STANDARD.md',
             'stories/docs/HISTORY_STORY_PIPELINE.md':'channels/nuviko_history/docs/HISTORY_STORY_PIPELINE.md',
             'stories/footages':'channels/nuviko_stories/footages',
             'stories/assets':'channels/nuviko_stories/assets'}
    for name in ('pipeline.py','voice_run.py','test_pipeline.py','test_voice_run.py','runs','settings.example.json','RUNBOOK.md'):
        pairs['stories/automation/'+name] = 'channels/nuviko_stories/automation/'+name
    registry=json.loads((ROOT/'.agent/episode-registry.json').read_text())
    for e in registry['entries']:
        old=e['path']
        if not old.startswith('stories/videos/'):continue
        slug=old.rsplit('/',1)[1]
        channel=e['channel']
        dest={'Stories':'channels/nuviko_stories/videos', 'Nuviko History':'channels/nuviko_history/videos',
              'Paper Detour':'channels/paper_detour/legacy', 'UNVERIFIED':'archive/unclassified_episodes'}[channel]
        pairs[old]=dest+'/'+slug
    # Existing historical aliases retain their targets without deciding a channel from a slug.
    for old,target in [('stories/videos/1','stories/videos/001_brother_ex_best_friend'),
                       ('stories/videos/2','stories/videos/002_pompeii'),('stories/videos/003','stories/videos/003_gus')]:
        dest=pairs[target].rsplit('/',1)[0]
        pairs[old]=dest+'/'+old.rsplit('/',1)[1]
    return pairs

def mapper(pairs):
    keys=sorted(pairs,key=len,reverse=True)
    def apply(path):
        path=str(path)
        for k in keys:
            if path==k or path.startswith(k+'/'):return pairs[k]+path[len(k):]
        return path
    return apply

def files():
    for dp,ds,fs in os.walk(ROOT, followlinks=False):
        rel=Path(dp).relative_to(ROOT)
        ds[:]=[d for d in ds if d not in SKIP and not (Path(dp)/d).is_symlink()
               and str(rel/d) not in ('Work/channel_layout_20261104','Shared/Image_Motion/Tools/sam2-local')]
        for n in fs:
            p=Path(dp)/n
            if not p.is_symlink():yield p

def eligible(path):
    if path == Path(__file__).resolve():return False
    rel=path.relative_to(ROOT)
    if any(part in ('Work','Archive','archive','audits','history','experiments','checks','chat','sam2-local','consultations','research','Research') for part in rel.parts):return False
    if '.palmier' in str(rel):return False
    if path.suffix.lower() not in TEXT and path.name not in ('.gitignore',):return False
    n=path.name.lower()
    return not (n.startswith('.env') or n in ('credentials.json','client.json') or
                path.suffix=='.json' and any(s in n for s in ('token','oauth','client_secret')))

def transform(text, old, new, apply, pairs):
    # Resolve Markdown links against their original parent BEFORE moving a document.
    protected=[]
    def link(m):
        target=m.group(1)
        if re.match(r'[a-zA-Z][\w+.-]*:',target) or target.startswith('#'):return m.group(0)
        raw=target.strip('<>'); tail=''
        if '#' in raw:raw,tail=raw.split('#',1);tail='#'+tail
        if not raw:return m.group(0)
        if raw.startswith(str(ROOT)+'/'):dest=ROOT/apply(raw[len(str(ROOT))+1:])
        elif raw.startswith('/'):return m.group(0)
        else:
            original=Path(os.path.normpath(str(ROOT/old.parent/raw)))
            try:dest=ROOT/apply(original.relative_to(ROOT))
            except ValueError:return m.group(0)
        result=str(dest) if raw.startswith('/') else os.path.relpath(dest,ROOT/new.parent)
        if ' ' in result:result='<'+result+tail+'>';tail=''
        protected.append(']('+result+tail+')')
        return '\x01LINK'+str(len(protected)-1)+'\x02'
    text=re.sub(r'\]\((<[^>]+>|[^\s)]+)\)',link,text)
    keys=sorted(pairs,key=len,reverse=True)
    pattern=re.compile(r'(?<![\w.-])('+'|'.join(re.escape(k) for k in keys)+r')(?=/|$|[\x01\s\x22\x27`)\]\},:;])')
    text=pattern.sub(lambda m: m.group(1) if m.group(1) in {'stories','new_channel','borisenko'} and text[m.end():m.end()+1] != '/' and text[max(0,m.start()-1):m.start()] not in {'/','`'} else pairs[m.group(1)],text)
    for i,p in enumerate(protected):text=text.replace('\x01LINK'+str(i)+'\x02',p)
    return text

def plan():
    if (RUN/'plan.json').exists():raise SystemExit('Existing migration plan; inspect it before rerunning.')
    RUN.mkdir(parents=True,exist_ok=True)
    pairs=mapping();apply=mapper(pairs)
    moves=[];media=[];symlinks=[]
    for dp,ds,fs in os.walk(ROOT,followlinks=False):
        rel=Path(dp).relative_to(ROOT)
        ds[:]=[d for d in ds if d not in SKIP and str(rel/d) not in ('Work/channel_layout_20261104','Shared/Image_Motion/Tools/sam2-local')]
        for n in ds+fs:
            p=Path(dp)/n
            if p.is_symlink():
                target=Path(os.path.normpath(str(p.parent/os.readlink(p))))
                try:target=ROOT/apply(target.relative_to(ROOT))
                except ValueError:pass
                symlinks.append({'old':str(p.relative_to(ROOT)),'new':apply(p.relative_to(ROOT)),'target':str(target),'was_valid':p.exists()})
        ds[:]=[d for d in ds if not (Path(dp)/d).is_symlink()]
    for p in files():
        old=p.relative_to(ROOT);new=apply(old)
        if str(old)!=new:moves.append({'old':str(old),'new':new,'bytes':p.stat().st_size})
        if p.suffix.lower() in MEDIA:media.append({'old':str(old),'new':new,'sha256':digest(p),'bytes':p.stat().st_size})
    data={'root':str(ROOT),'mapping':pairs,'files':moves,'symlinks':symlinks,'media':media,'status':'PLANNED'}
    (RUN/'plan.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'moving_files':len(moves),'media_pins':len(media),'links':len(symlinks)}))

def execute():
    data=json.loads((RUN/'plan.json').read_text());assert data['status']=='PLANNED'
    pairs=data['mapping'];apply=mapper(pairs)
    edits=[]
    # Compute and back up every edit before any move. A per-file backup provides rollback.
    for p in list(files()):
        if not eligible(p):continue
        try:original=p.read_text()
        except (UnicodeError,OSError):continue
        old=p.relative_to(ROOT);new=Path(apply(old))
        updated=transform(original,old,new,apply,pairs)
        if updated==original:continue
        backup=RUN/'backup'/old;backup.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,backup)
        edits.append({'old':str(old),'new':str(new),'before':digest(p),'after':hashlib.sha256(updated.encode()).hexdigest()})
        target=RUN/'updated'/old;target.parent.mkdir(parents=True,exist_ok=True);target.write_text(updated)
    data['edits']=edits;(RUN/'plan.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
    for item in edits:
        p=ROOT/item['old'];assert digest(p)==item['before'],f'Concurrent modification: {p}'
        shutil.copyfile(RUN/'updated'/item['old'],p)
    data['status']='TEXT_REWRITTEN';(RUN/'plan.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
    finish_moves(data)

def finish_moves(data):
    pairs=data['mapping']
    # Extract specific children first, then move the remaining parent trees.
    def move_tree(src,dst):
        if dst.is_dir() and not dst.is_symlink() and src.is_dir() and not src.is_symlink():
            for child in list(src.iterdir()):move_tree(child,dst/child.name)
            src.rmdir()
        else:
            assert not dst.exists() and not dst.is_symlink(),f'Collision: {dst}'
            dst.parent.mkdir(parents=True,exist_ok=True);shutil.move(str(src),str(dst))
    for old in sorted(pairs,key=lambda x:(-len(Path(x).parts),x)):
        src=ROOT/old;dst=ROOT/pairs[old]
        if not src.exists() and not src.is_symlink():continue
        move_tree(src,dst)
    for item in data['symlinks']:
        p=ROOT/item['new']
        if p.is_symlink():p.unlink()
        p.parent.mkdir(parents=True,exist_ok=True)
        p.symlink_to(os.path.relpath(item['target'],p.parent),target_is_directory=True)
    # Thin compatibility routes preserve old absolute paths, open sessions and archived receipts.
    aliases={'new_channel':'channels/paper_detour','stories':'archive/legacy_stories','borisenko':'projects/borisenko'}
    for old,new in aliases.items():(ROOT/old).symlink_to(os.path.relpath(ROOT/new,(ROOT/old).parent),target_is_directory=True)
    for old,new in pairs.items():
        if not old.startswith('stories/'):continue
        route=ROOT/'archive/legacy_stories'/old[len('stories/'):]
        if route.exists() or route.is_symlink():continue
        route.parent.mkdir(parents=True,exist_ok=True)
        route.symlink_to(os.path.relpath(ROOT/new,route.parent),target_is_directory=True)
    data['status']='MOVED';(RUN/'plan.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'moved_files':len(data['files']),'rewritten_texts':len(data['edits'])}))

def verify():
    data=json.loads((RUN/'plan.json').read_text());errors=[]
    for x in data['files']:
        p=ROOT/x['new']
        if not p.is_file():errors.append('Missing moved file: '+x['new'])
    for x in data['media']:
        p=ROOT/x['new']
        if not p.is_file() or digest(p)!=x['sha256']:errors.append('Media mismatch: '+x['new'])
    for x in data['symlinks']:
        p=ROOT/x['new']
        if x['was_valid'] and not p.exists():errors.append('New broken symlink: '+x['new'])
    report={'moved_files':len(data['files']),'media_hashes_checked':len(data['media']),'errors':errors}
    (RUN/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(report,ensure_ascii=False));return bool(errors)

if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('mode',choices=['plan','apply','resume','verify']);args=a.parse_args()
    if args.mode=='plan':plan()
    elif args.mode=='apply':execute()
    elif args.mode=='resume':finish_moves(json.loads((RUN/'plan.json').read_text()))
    else:raise SystemExit(verify())
