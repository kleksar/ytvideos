#!/usr/bin/env python3
"""Revise scenes 030 and 031 of an assembled long timeline; dry-run by default.

Requires a matching original manifest and assembled receipt. Every Palmier
mutation receives its own exclusive, fsynced journal; unknown outcomes must be
reconciled manually. Never invoke while an export is running. No export here.
"""
import argparse
import json
import os
import shutil
from pathlib import Path
from assemble_history_long import sha, probe
from inspect_connection import PalmierConnection


def load_plan(series):
    root = Path(series).resolve()
    manifest = root/'Edit/Long/manifest.json'
    original = root/'Edit/Long/palmier_receipt.json'
    journal_dir = root/'Edit/Long/revision_030_031'
    m = json.loads(manifest.read_text()); r = json.loads(original.read_text())
    if m.get('status') != 'ready' or r.get('status') != 'assembled' or r.get('manifestSha256') != sha(manifest) or r.get('timeline') != m.get('timeline'):
        raise ValueError('Original assembled receipt does not match manifest')
    if m.get('fps') != 30 or len(m.get('scenes', [])) < 31 or len(r.get('imageClipIds', [])) != len(m['scenes']):
        raise ValueError('Invalid original scene index')
    if journal_dir.exists() and any(journal_dir.iterdir()):
        raise ValueError('Revision journal exists; reconcile manually')
    clips = {c['id']: (track, c) for track in r['tracks'] for c in track.get('clips', [])}
    entries = []
    for index in (29, 30):
        scene = m['scenes'][index]; cid = r['imageClipIds'][index]
        if cid not in clips: raise ValueError('Original clip missing from receipt')
        track, clip = clips[cid]
        if clip.get('frames') != [scene['start'], scene['end']] or clip.get('mediaRef') != r['media'].get(scene['path']) or clip.get('mediaType') != 'image' or track.get('type') != 'video':
            raise ValueError('Scene, clip and original media disagree')
        if set(clip) - {'id','frames','mediaRef','mediaType','keyframes','trimEndFrame'} or set(clip.get('keyframes', {})) != {'scale'}:
            raise ValueError('Unexpected clip settings: preserve manually')
        path = root/f'Source/Long/Images/{index+1:03d}_corrected.png'
        if not path.is_file(): raise ValueError(f'Missing corrected image: {path}')
        image = next((x for x in probe(path)['streams'] if x.get('codec_type') == 'video'), {})
        if not image.get('height') or abs(image.get('width', 0)/image['height'] - 16/9) > .006:
            raise ValueError('Corrected image must be 16:9')
        entries.append({'number': index+1, 'path': str(path), 'sha256': sha(path), 'clipId': cid,
                        'trackId': track['trackId'], 'trackIndex': track['index'], 'old': clip,
                        'keyframes': clip['keyframes']['scale'], 'frames': clip['frames']})
    return {'root': root, 'manifest': manifest, 'manifestHash': sha(manifest), 'original': original,
            'receiptHash': sha(original), 'receipt': r, 'entries': entries, 'journalDir': journal_dir}


def snapshot(tracks):
    return {c['id']: {'trackId': t['trackId'], 'trackIndex': t['index'], 'clip': c}
            for t in tracks for c in t.get('clips', [])}


def run(plan, call):
    r = plan['receipt']; project = Path(r['project']).resolve(); expected = snapshot(r['tracks'])
    if len(expected) != sum(len(t.get('clips', [])) for t in r['tracks']): raise ValueError('Duplicate clip ID in receipt')
    if not project.is_dir() or project.suffix != '.palmier': raise ValueError('Project missing')
    if shutil.disk_usage(plan['root']).free < 8*1024**3: raise ValueError('Insufficient disk space')
    def guard(compare=True):
        if sha(plan['manifest']) != plan['manifestHash'] or sha(plan['original']) != plan['receiptHash']:
            raise RuntimeError('Original manifest or receipt changed')
        for e in plan['entries']:
            if sha(Path(e['path'])) != e['sha256']: raise RuntimeError('Corrected image changed')
        pr = call('manage_project', {'action':'list'}); tl = call('get_timeline', {})
        if any(not isinstance(pr.get(k), dict) or not pr[k].get('path') or Path(pr[k]['path']).resolve() != project for k in ('active','visible')):
            raise RuntimeError('Active or visible project changed')
        if (tl.get('id'), tl.get('name'), tl.get('fps'), tl.get('width'), tl.get('height'), tl.get('totalFrames')) != (r['timelineId'], r['timeline'], 30, 1920, 1080, json.loads(plan['manifest'].read_text())['frames']):
            raise RuntimeError('Active timeline changed')
        exports = call('manage_exports', {'action':'list'}).get('exports')
        if not isinstance(exports, list) or any(not isinstance(x, dict) or x.get('status') not in ('completed','failed','cancelled','canceled') for x in exports):
            raise RuntimeError('Export running or state unknown')
        actual = snapshot(tl['tracks'])
        if compare and actual != expected: raise RuntimeError('Timeline differs from expected revision state')
        return tl, actual
    guard()
    plan['journalDir'].mkdir(parents=True, exist_ok=True)
    def sync_dir():
        fd = os.open(str(plan['journalDir']), os.O_RDONLY)
        try: os.fsync(fd)
        finally: os.close(fd)
    def begin(number, action, payload):
        path = plan['journalDir']/f'{number:03d}_{action}.json'
        with path.open('x') as f:
            json.dump({'state':'outcome_unknown','action':action,'input':payload}, f, indent=2)
            f.flush(); os.fsync(f.fileno())
        sync_dir(); return path
    def done(path, payload):
        prior = json.loads(path.read_text())
        if prior.get('state') != 'outcome_unknown': raise RuntimeError('Mutation journal changed')
        prior.update(state='confirmed', result=payload)
        temp = path.with_suffix('.tmp')
        with temp.open('x') as f:
            json.dump(prior, f, indent=2)
            f.flush(); os.fsync(f.fileno())
        temp.replace(path); sync_dir()
    for e in plan['entries']:
        guard(); name = Path(e['path']).stem
        inventory = call('get_media', {'folder':r['timeline']}).get('assets')
        if not isinstance(inventory,list) or any(a.get('name') == name for a in inventory): raise RuntimeError('Media name already exists or inventory malformed')
        args = {'source':{'path':e['path']}, 'folder':r['timeline']}
        journal = begin(e['number'], 'import', args); result = call('import_media', args); ref = result['mediaRef']
        guard(); ready = call('get_media', {'ids':[ref]}).get('assets')
        if not isinstance(ready,list) or len(ready)!=1 or ready[0].get('generationStatus'): raise RuntimeError('Import not confirmed')
        done(journal, {'mediaRef':ref, 'path':e['path'], 'sha256':e['sha256']})
        guard(); args = {'entries':[{'mediaRef':ref,'startFrame':e['frames'][0],'endFrame':e['frames'][1],'trackIndex':e['trackIndex']}]}
        journal = begin(e['number'], 'replace', args); result = call('add_clips', args)
        added = result.get('clips', [])
        if len(added)!=1 or not added[0].get('id'): raise RuntimeError('Replacement response ambiguous')
        cid = added[0]['id']; tl, actual = guard(compare=False)
        before_without = {k:v for k,v in expected.items() if k != e['clipId']}
        actual_without = {k:v for k,v in actual.items() if k != cid}
        replacement = actual.get(cid)
        if actual_without != before_without or not replacement or replacement['trackId'] != e['trackId'] or replacement['clip'].get('frames') != e['frames'] or replacement['clip'].get('mediaRef') != ref:
            raise RuntimeError('Replacement changed unrelated timeline content or has wrong span')
        expected = actual; done(journal, {'oldClipId':e['clipId'],'clipId':cid,'trackId':e['trackId'],'frames':e['frames'],'mediaRef':ref})
        guard(); args = {'clipId':cid,'property':'scale','keyframes':e['keyframes']}
        journal = begin(e['number'], 'keyframes', args); call('set_keyframes', args); tl, actual = guard(compare=False)
        changed = {k:v for k,v in actual.items() if k != cid}
        now = actual.get(cid)
        before_clip = {k:v for k,v in expected[cid]['clip'].items() if k != 'keyframes'}
        after_clip = {k:v for k,v in now['clip'].items() if k != 'keyframes'} if now else None
        if changed != {k:v for k,v in expected.items() if k != cid} or not now or now['trackId'] != e['trackId'] or after_clip != before_clip or now['clip'].get('keyframes') != {'scale':e['keyframes']}:
            raise RuntimeError('Keyframes or timeline content differ after replacement')
        expected = actual; done(journal, {'clipId':cid,'keyframes':e['keyframes']})
    tl, _ = guard()
    final = plan['journalDir']/'revision_result.json'
    with final.open('x') as f:
        json.dump({'status':'revised','timelineId':tl['id'],'project':str(project),'manifestSha256':plan['manifestHash'],'originalReceiptSha256':plan['receiptHash'],'tracks':tl['tracks']},f,indent=2)
        f.flush(); os.fsync(f.fileno())
    sync_dir(); return {'status':'revised','result':str(final)}


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--series',type=Path,required=True);p.add_argument('--execute',action='store_true');a=p.parse_args()
    plan=load_plan(a.series)
    if not a.execute:
        print(json.dumps({'mode':'offline-dry-run','entries':plan['entries']},ensure_ascii=False,indent=2));return
    c=PalmierConnection();c.connect()
    def call(name,args):
        result=c.request('tools/call',{'name':name,'arguments':args})
        if result.get('isError'): raise RuntimeError(f'{name}: {result}')
        return json.loads(next(x['text'] for x in result['content'] if x['type']=='text'))
    print(json.dumps(run(plan,call),ensure_ascii=False,indent=2))
if __name__=='__main__': main()
