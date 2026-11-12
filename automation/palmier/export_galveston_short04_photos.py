#!/usr/bin/env python3
"""Export revised Galveston 04 once, after explicit frame-by-frame QA evidence.

Dry run performs local checks only. visual_qa.json must cite the exact revision
SHA-256 and verified saved frame images. No automatic confirmation or retry.
"""
import argparse,json,os,shutil
from pathlib import Path
from assemble_history_long import sha
from revise_galveston_short04_photos import PHOTOS,TIMELINE,connect,create,replace

FRAMES={850,851,884,916,917,955,993,994}
STEPS=['import_media']*2+['add_clips']*2+['apply_layout','apply_effect','apply_color']*2+['apply_layout']*2+['manage_tracks']

def prepare(series):
    root=Path(series).resolve();d=root/'Edit/Shorts';j=d/'04_photo_revision';mp=d/'04_manifest_assembly_placeholders.json';rp=d/'04_manifest_assembly_placeholders_palmier_receipt.json';revpath=j/'revision_result.json';qapath=j/'visual_qa.json';baseline=json.loads((j/'00_baseline.json').read_text());rev=json.loads(revpath.read_text());qa=json.loads(qapath.read_text());m=json.loads(mp.read_text());r=json.loads(rp.read_text())
    if rev.get('status')!='revised_needs_visual_qa' or rev.get('steps')!=len(STEPS) or rev.get('timelineId')!=TIMELINE or r.get('status')!='assembled' or r.get('timelineId')!=TIMELINE:raise ValueError('Revision or assembly incomplete')
    if rev.get('manifestSha256')!=sha(mp) or rev.get('originalReceiptSha256')!=sha(rp) or r.get('manifestSha256')!=sha(mp) or baseline.get('manifestSha256')!=sha(mp) or baseline.get('receiptSha256')!=sha(rp) or baseline.get('tracks')!=r.get('tracks'):raise ValueError('Baseline evidence mismatch')
    if rev.get('timeline')!=r.get('timeline') or rev.get('project')!=r.get('project') or m.get('frames')!=1100: raise ValueError('Timeline mismatch')
    old=baseline['tracks']
    for i,name in enumerate(STEPS,1):
        step=json.loads((j/f'{i:02d}_{name}.json').read_text())
        if step.get('state')!='confirmed' or step.get('tool')!=name or step.get('beforeTracks')!=old or not isinstance(step.get('afterTracks'),list): raise ValueError('Incomplete or broken mutation history')
        old=step['afterTracks']
    if old!=rev.get('tracks'):raise ValueError('Final snapshot differs from mutation history')
    for i,(name,digest,start,end) in enumerate(PHOTOS):
        p=root/'Source/Archive/Gresham_Highsmith_2012'/name
        if sha(p)!=digest or rev['photos'][i]!={'path':str(p),'sha256':digest,'frames':[start,end]}:raise ValueError('Photo mismatch')
    for asset in [m['voice'],m['captions'],m['srt'],*m['scenes']]:
        if sha(Path(asset['path']))!=asset['sha256']:raise ValueError('Original asset changed')
    if qa.get('revisionSha256')!=sha(revpath) or qa.get('status')!='passed' or qa.get('checked')!={'full_buildings_uncropped':True,'blurred_background_visible':True,'titles_readable_and_above_photos':True,'placeholders_hidden':True,'transitions_correct':True} or not isinstance(qa.get('reviewer'),str) or not qa['reviewer'].strip():raise ValueError('Explicit visual QA is missing or mismatched')
    evidence=qa.get('frames');
    if not isinstance(evidence,list) or {x.get('frame') for x in evidence}!=FRAMES or len(evidence)!=len(FRAMES):raise ValueError('Missing visual QA frames')
    for x in evidence:
        path=Path(x.get('path','')).resolve()
        if not path.is_relative_to(j) or not path.is_file() or path.suffix.lower() not in ('.png','.jpg','.jpeg') or sha(path)!=x.get('sha256'):raise ValueError('Frame evidence changed')
    out=root/'Deliverables'/f"{m['timeline']}_photos_v2_palmier.mp4"; journal=j/'export_photos_v2.json'
    if journal.exists() or out.exists():raise ValueError('Output or export journal exists; reconcile manually')
    return dict(root=root,j=j,mp=mp,rp=rp,revpath=revpath,qapath=qapath,rev=rev,r=r,m=m,out=out,journal=journal,hashes={str(p):sha(p) for p in [mp,rp,revpath,qapath,*[j/f'{i:02d}_{name}.json' for i,name in enumerate(STEPS,1)],*[Path(x['path']).resolve() for x in evidence]]})

def execute(p,call):
    def guard():
        if any(sha(Path(k))!=v for k,v in p['hashes'].items()):raise RuntimeError('Evidence changed')
        for asset in [p['m']['voice'],p['m']['captions'],p['m']['srt'],*p['m']['scenes']]:
            if sha(Path(asset['path']))!=asset['sha256']:raise RuntimeError('Original asset changed')
        for photo in p['rev']['photos']:
            if sha(Path(photo['path']))!=photo['sha256']:raise RuntimeError('Photo changed')
        if shutil.disk_usage(p['root']).free<5*1024**3:raise RuntimeError('Less than 5 GiB free')
        if p['out'].exists():raise RuntimeError('Output exists')
        project=Path(p['r']['project']).resolve();pr=call('manage_project',{'action':'list'});tl=call('get_timeline',{});ex=call('manage_exports',{'action':'list'}).get('exports')
        if any(not isinstance(pr.get(k),dict) or not pr[k].get('path') or Path(pr[k]['path']).resolve()!=project for k in ('active','visible')):raise RuntimeError('Project differs')
        if (tl.get('id'),tl.get('name'),tl.get('fps'),tl.get('width'),tl.get('height'),tl.get('totalFrames'))!=(TIMELINE,p['m']['timeline'],30,1080,1920,1100) or tl!=p['rev'].get('timelineSnapshot') or tl.get('tracks')!=p['rev']['tracks']:raise RuntimeError('Timeline differs from verified snapshot')
        if not isinstance(ex,list) or any(not isinstance(x,dict) or x.get('status') not in ('completed','failed','cancelled','canceled') for x in ex):raise RuntimeError('Export active or unknown')
    guard();p['out'].parent.mkdir(parents=True,exist_ok=True)
    args={'mode':'video','codec':'H.264','resolution':'Match Timeline','timelineId':TIMELINE,'outputPath':str(p['out']),'overwrite':False}
    record={'state':'pending_outcome_unknown','args':args,'revisionSha256':sha(p['revpath']),'visualQaSha256':sha(p['qapath'])}
    create(p['journal'],record);guard();result=call('export_project',args)
    if result.get('status') not in ('started','queued') or not result.get('jobId'):raise RuntimeError('Ambiguous export result; reconcile manually')
    record.update(state='queued',result=result);replace(p['journal'],record);return record

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--series',type=Path,required=True);p.add_argument('--execute',action='store_true');a=p.parse_args(); plan=prepare(a.series)
    if not a.execute:print(json.dumps({'mode':'offline_only','output':str(plan['out'])}));return
    print(json.dumps(execute(plan,connect()),ensure_ascii=False))
if __name__=='__main__':main()
