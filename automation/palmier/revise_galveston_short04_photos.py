#!/usr/bin/env python3
"""Journalled revision of Galveston Short 04; dry-run by default. No export.

Unknown outcomes are never retried: reconcile the journal manually. Read the
four-up image verification instructions before exporting the revised timeline.
"""
import argparse, json, os, shutil
from pathlib import Path
from assemble_history_long import sha
from inspect_connection import PalmierConnection

TIMELINE='25A67072'
PHOTOS=(('LC-DIG-highsm-18754-working.jpg','c53aa258324dc8383e081254b1fe4d7824919f2039d6f0dd152600feb11e32e9',851,917),('LC-DIG-highsm-18756-working.jpg','60448ef57377fadb07cf42d0e810496da4221799b18316a2104214267990b1e9',917,994))

def syncdir(path):
    fd=os.open(str(path),os.O_RDONLY)
    try: os.fsync(fd)
    finally: os.close(fd)

def create(path,obj):
    with path.open('x') as f:
        json.dump(obj,f,ensure_ascii=False,indent=2); f.write('\n');f.flush();os.fsync(f.fileno())
    syncdir(path.parent)

def replace(path,obj):
    tmp=path.with_suffix(path.suffix+'.tmp')
    create(tmp,obj); os.replace(tmp,path);syncdir(path.parent)

def load(series):
    root=Path(series).resolve(); edit=root/'Edit/Shorts'; manifest=edit/'04_manifest_assembly_placeholders.json'; receipt=edit/'04_manifest_assembly_placeholders_palmier_receipt.json'; journal=edit/'04_photo_revision'
    m=json.loads(manifest.read_text());r=json.loads(receipt.read_text())
    if r.get('status')!='assembled' or r.get('manifestSha256')!=sha(manifest) or r.get('timelineId')!=TIMELINE or r.get('timeline')!=m.get('timeline') or m.get('frames')!=1100 or m.get('fps')!=30: raise ValueError('Wrong manifest or assembly receipt')
    if journal.exists(): raise ValueError('Revision directory exists; reconcile before retry')
    photos=[]
    for name,digest,start,end in PHOTOS:
        p=root/'Source/Archive/Gresham_Highsmith_2012'/name
        if not p.is_file() or sha(p)!=digest: raise ValueError('Photo is missing or changed')
        photos.append({'path':str(p),'sha256':digest,'frames':[start,end]})
    for k in ('voice','captions','srt'):
        a=m[k]; p=Path(a['path']);
        if not p.is_file() or sha(p)!=a['sha256']: raise ValueError('Voice, captions or SRT changed')
    for s in m['scenes']:
        if sha(Path(s['path']))!=s['sha256']: raise ValueError('Original scene changed')
    tracks=r['tracks']; caption_ref=r['media'][m['captions']['path']]
    captions=[t for t in tracks if any(c.get('mediaRef')==caption_ref and c.get('frames')==[0,1100] for c in t.get('clips',[]))]
    if len(captions)!=1 or captions[0]['index']!=0: raise ValueError('Caption track missing or not above all tracks')
    return dict(root=root,manifest=manifest,receipt=receipt,journal=journal,m=m,r=r,photos=photos,manifest_hash=sha(manifest),receipt_hash=sha(receipt),caption_track=captions[0]['trackId'])

def stable_track(t):
    # Labels and current index are derived from ordering; other properties and
    # every original clip remain exactly equal, including effects and grades.
    return {k:v for k,v in t.items() if k not in ('index','label','gaps')}

def by_id(tracks):
    result={t['trackId']:stable_track(t) for t in tracks}
    if len(result)!=len(tracks): raise ValueError('Duplicate trackId')
    return result

def connect():
    c=PalmierConnection();c.connect()
    def call(name,args):
        result=c.request('tools/call',{'name':name,'arguments':args})
        if result.get('isError'): raise RuntimeError(f'{name}: {result}')
        return json.loads(next(x['text'] for x in result['content'] if x['type']=='text'))
    return call

def run(plan,call):
    r=plan['r'];j=plan['journal']; project=Path(r['project']).resolve(); expected=r['tracks']; seq=0
    if not project.is_dir() or project.suffix!='.palmier': raise ValueError('Project not found')
    def guard():
        if sha(plan['manifest'])!=plan['manifest_hash'] or sha(plan['receipt'])!=plan['receipt_hash']: raise RuntimeError('Evidence changed')
        for p in plan['photos']:
            if sha(Path(p['path']))!=p['sha256']: raise RuntimeError('Photo changed')
        if shutil.disk_usage(plan['root']).free<5*1024**3: raise RuntimeError('Less than 5 GiB free')
        pr=call('manage_project',{'action':'list'});tl=call('get_timeline',{}); ex=call('manage_exports',{'action':'list'}).get('exports')
        if any(not isinstance(pr.get(k),dict) or not pr[k].get('path') or Path(pr[k]['path']).resolve()!=project for k in ('active','visible')): raise RuntimeError('Active or visible project differs')
        if (tl.get('id'),tl.get('name'),tl.get('fps'),tl.get('width'),tl.get('height'),tl.get('totalFrames'))!=(TIMELINE,r['timeline'],30,1080,1920,1100): raise RuntimeError('Wrong timeline')
        if not isinstance(ex,list) or any(not isinstance(x,dict) or x.get('status') not in ('completed','failed','cancelled','canceled') for x in ex): raise RuntimeError('Export active or unknown')
        return tl
    tl=guard()
    if tl['tracks']!=expected: raise RuntimeError('Full tracks differ from assembly receipt')
    # No repeated run of any partial journal, even if no request was sent.
    j.mkdir();syncdir(j.parent)
    create(j/'00_baseline.json',{'manifestSha256':plan['manifest_hash'],'receiptSha256':plan['receipt_hash'],'timelineId':TIMELINE,'project':str(project),'tracks':expected,'timelineSnapshot':tl,'photos':plan['photos']})
    def mutation(name,args,validate):
        nonlocal seq,expected
        before=guard()
        if before['tracks']!=expected: raise RuntimeError('Timeline changed since previous step')
        seq+=1;path=j/f'{seq:02d}_{name}.json'
        record={'state':'pending_outcome_unknown','tool':name,'arguments':args,'beforeTracks':expected}
        create(path,record)
        # Re-guard *after* durable pending, to catch a change before request.
        if guard()['tracks']!=expected: raise RuntimeError('Timeline changed before mutation')
        result=call(name,args);after=guard(); validate(expected,after['tracks'],result)
        expected=after['tracks'];record.update(state='confirmed',result=result,afterTracks=expected);replace(path,record)
        return result
    def unchanged(before,after,result):
        if before!=after: raise RuntimeError('Import changed timeline')
    refs=[]
    for p in plan['photos']:
        inventory=call('get_media',{'folder':r['timeline']}).get('assets')
        if not isinstance(inventory,list) or any(x.get('name')==Path(p['path']).stem for x in inventory): raise RuntimeError('Photo already in media inventory or inventory invalid')
        def imported(before,after,result):
            unchanged(before,after,result);ref=result.get('mediaRef'); assets=call('get_media',{'ids':[ref]}).get('assets') if ref else None
            if not isinstance(assets,list) or len(assets)!=1 or assets[0].get('generationStatus') or assets[0].get('type')!='image': raise RuntimeError('Photo import not confirmed')
        result=mutation('import_media',{'source':{'path':p['path']},'folder':r['timeline']},imported); refs.append(result['mediaRef'])
    new_tracks=[];new_clips=[]
    for layer in ('background','foreground'):
        def added(before,after,result):
            old=by_id(before); now=by_id(after); ids=set(now)-set(old)
            if len(ids)!=1 or any(now.get(k)!=v for k,v in old.items()): raise RuntimeError('Original tracks changed or new track ambiguous')
            tid=next(iter(ids)); order=[t['trackId'] for t in after]
            if order!=[tid]+[t['trackId'] for t in before]: raise RuntimeError('Unexpected layer order')
            tr=now[tid]; clips=tr.get('clips',[])
            if tr.get('type')!='video' or len(clips)!=2 or sorted((c.get('mediaRef'),tuple(c.get('frames',[]))) for c in clips)!=sorted((refs[i],tuple(plan['photos'][i]['frames'])) for i in range(2)): raise RuntimeError('Wrong new photo clips')
            if len({c.get('id') for c in clips})!=2 or any(not c.get('id') for c in clips): raise RuntimeError('Clip IDs invalid')
            response=result.get('clips');
            if not isinstance(response,list) or {c.get('id') for c in response}!={c['id'] for c in clips}: raise RuntimeError('Clip response ambiguous')
        entries=[{'mediaRef':refs[i],'startFrame':p['frames'][0],'endFrame':p['frames'][1]} for i,p in enumerate(plan['photos'])]
        mutation('add_clips',{'entries':entries},added)
        track=expected[0];new_tracks.append(track['trackId']);new_clips.append([next(c['id'] for c in track['clips'] if c['mediaRef']==ref) for ref in refs])
    def target_only(cid,check,allowed):
        def validate(before,after,result):
            b=by_id(before);a=by_id(after)
            if [t['trackId'] for t in before]!=[t['trackId'] for t in after] or set(a)!=set(b): raise RuntimeError('Track order changed')
            found=0
            for tid in b:
                bt,at=b[tid],a[tid]
                if {k:v for k,v in bt.items() if k!='clips'}!={k:v for k,v in at.items() if k!='clips'}: raise RuntimeError('Track properties changed')
                bc={c['id']:c for c in bt.get('clips',[])};ac={c['id']:c for c in at.get('clips',[])}
                if set(bc)!=set(ac): raise RuntimeError('Clip set changed')
                for k in bc:
                    if k!=cid and bc[k]!=ac[k]: raise RuntimeError('Unrelated clip changed')
                    if k==cid:
                        found+=1
                        if {x:v for x,v in bc[k].items() if x not in allowed}!={x:v for x,v in ac[k].items() if x not in allowed} or not check(ac[k]): raise RuntimeError('Unexpected target clip change')
            if found!=1: raise RuntimeError('Target clip not unique')
        return validate
    for cid in new_clips[0]:
        mutation('apply_layout',{'layout':'full','fit':'fill','slots':[{'slot':'main','clipIds':[cid]}]},target_only(cid,lambda c: True, {'transform','crop'}))
        mutation('apply_effect',{'clipIds':[cid],'effects':[{'type':'blur.gaussian','params':{'radius':30}}]},target_only(cid,lambda c:any(x.get('type')=='blur.gaussian' and x.get('params',{}).get('radius')==30 and x.get('enabled',True) for x in c.get('effects',[])), {'effects'}))
        mutation('apply_color',{'clipIds':[cid],'exposure':-1},target_only(cid,lambda c:c.get('color',{}).get('exposure')==-1, {'color'}))
    for cid in new_clips[1]:
        mutation('apply_layout',{'layout':'full','fit':'fit','slots':[{'slot':'main','clipIds':[cid]}]},target_only(cid,lambda c: True, {'transform','crop'}))
    def reorder(before,after,result):
        if by_id(before)!=by_id(after): raise RuntimeError('Track or clip content changed during reorder')
        prior=[t['trackId'] for t in before]; want=[plan['caption_track']]+[x for x in prior if x!=plan['caption_track']]
        if [t['trackId'] for t in after]!=want: raise RuntimeError('Incorrect track order')
    mutation('manage_tracks',{'reorder':[{'trackId':plan['caption_track'],'to':0}]},reorder)
    final_timeline=guard()
    if final_timeline['tracks']!=expected: raise RuntimeError('Final timeline changed')
    final={'status':'revised_needs_visual_qa','timelineId':TIMELINE,'timeline':r['timeline'],'project':str(project),'manifestSha256':plan['manifest_hash'],'originalReceiptSha256':plan['receipt_hash'],'photos':plan['photos'],'photoRefs':refs,'photoTracks':new_tracks,'photoClips':new_clips,'captionTrack':plan['caption_track'],'steps':seq,'tracks':expected,'timelineSnapshot':final_timeline}
    create(j/'revision_result.json',final)
    return final

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--series',type=Path,required=True);p.add_argument('--execute',action='store_true');a=p.parse_args();plan=load(a.series)
    if not a.execute: print(json.dumps({'mode':'offline_only','timelineId':TIMELINE,'photos':plan['photos']}));return
    print(json.dumps(run(plan,connect()),ensure_ascii=False))
if __name__=='__main__':main()
