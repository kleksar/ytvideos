#!/usr/bin/env python3
"""Queue a revised long-film export once after all read-only checks; dry-run by default."""
import argparse
import json
import os
import shutil
from pathlib import Path
from assemble_history_long import sha
from inspect_connection import PalmierConnection
from revise_history_long import snapshot


def prepare(series):
    root=Path(series).resolve(); directory=root/'Edit/Long'; manifest=directory/'manifest.json'
    original=directory/'palmier_receipt.json'; revision=directory/'revision_030_031/revision_result.json'
    m=json.loads(manifest.read_text()); r=json.loads(original.read_text()); rev=json.loads(revision.read_text())
    if m.get('status')!='ready' or r.get('status')!='assembled' or rev.get('status')!='revised': raise ValueError('Required receipts are incomplete')
    if sha(manifest)!=r.get('manifestSha256') or sha(manifest)!=rev.get('manifestSha256') or sha(original)!=rev.get('originalReceiptSha256'):
        raise ValueError('Manifest or original receipt changed')
    if rev.get('timelineId')!=r.get('timelineId') or rev.get('project')!=r.get('project'): raise ValueError('Revision mismatch')
    for i, scene in enumerate(m['scenes']):
        if i not in (29,30) and sha(Path(scene['path']))!=scene['sha256']: raise ValueError('Original media changed')
    if sha(Path(m['voice']))!=m['sha256']['voice'] or sha(Path(m['srt']))!=m['sha256']['srt']: raise ValueError('Voice or SRT changed')
    for num in (30,31):
        j=json.loads((directory/f'revision_030_031/{num:03d}_import.json').read_text())
        if j.get('state')!='confirmed' or sha(Path(j['result']['path']))!=j['result']['sha256']: raise ValueError('Corrected image changed or import unconfirmed')
        for action in ('replace','keyframes'):
            if json.loads((directory/f'revision_030_031/{num:03d}_{action}.json').read_text()).get('state')!='confirmed': raise ValueError('Revision not fully confirmed')
    output=root/'Deliverables'/f"{m['timeline']}_palmier_v2.mp4"
    journal=directory/'revision_030_031/export_v2.json'
    if output.exists() or journal.exists(): raise ValueError('V2 output or export journal exists; reconcile manually')
    if shutil.disk_usage(root).free<10*1024**3: raise ValueError('Less than 10 GiB free')
    return {'root':root,'manifest':manifest,'original':original,'revision':revision,'revisionHash':sha(revision),'m':m,'r':r,'rev':rev,'out':output,'journal':journal}


def execute(info, call):
    def guard():
        if sha(info['manifest'])!=info['rev']['manifestSha256'] or sha(info['original'])!=info['rev']['originalReceiptSha256'] or sha(info['revision'])!=info['revisionHash']:
            raise RuntimeError('Revision evidence changed')
        if shutil.disk_usage(info['root']).free<10*1024**3: raise RuntimeError('Less than 10 GiB free')
        project=Path(info['r']['project']).resolve(); pr=call('manage_project',{'action':'list'});tl=call('get_timeline',{}); exports=call('manage_exports',{'action':'list'}).get('exports')
        if any(not isinstance(pr.get(k),dict) or not pr[k].get('path') or Path(pr[k]['path']).resolve()!=project for k in ('active','visible')): raise RuntimeError('Active project changed')
        if (tl.get('id'),tl.get('name'),tl.get('fps'),tl.get('width'),tl.get('height'),tl.get('totalFrames'))!=(info['r']['timelineId'],info['m']['timeline'],30,1920,1080,info['m']['frames']): raise RuntimeError('Active timeline differs')
        if snapshot(tl['tracks'])!=snapshot(info['rev']['tracks']): raise RuntimeError('Revised timeline changed')
        if not isinstance(exports,list) or any(not isinstance(x,dict) or x.get('status') not in ('completed','failed','cancelled','canceled') for x in exports): raise RuntimeError('Export running or state unknown')
        if info['out'].exists(): raise RuntimeError('V2 output already exists')
        return tl
    tl=guard(); info['out'].parent.mkdir(parents=True,exist_ok=True)
    args={'mode':'video','codec':'H.264','resolution':'Match Timeline','timelineId':tl['id'],'outputPath':str(info['out']),'overwrite':False}
    j={'state':'outcome_unknown','action':'export_v2','args':args,'revisionSha256':info['revisionHash']}
    with info['journal'].open('x') as f:
        json.dump(j,f,indent=2);f.flush();os.fsync(f.fileno())
    fd=os.open(str(info['journal'].parent),os.O_RDONLY)
    try: os.fsync(fd)
    finally: os.close(fd)
    guard()
    result=call('export_project',args)
    if result.get('status') not in ('started','queued') or not result.get('jobId'): raise RuntimeError('Export response ambiguous; reconcile manually')
    j.update(state='queued',result=result)
    tmp=info['journal'].with_suffix('.tmp')
    with tmp.open('x') as f:
        json.dump(j,f,indent=2);f.flush();os.fsync(f.fileno())
    tmp.replace(info['journal'])
    fd=os.open(str(info['journal'].parent),os.O_RDONLY)
    try: os.fsync(fd)
    finally: os.close(fd)
    return j


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--series',type=Path,required=True);p.add_argument('--execute',action='store_true');a=p.parse_args();info=prepare(a.series)
    if not a.execute:
        print(json.dumps({'mode':'offline-dry-run','output':str(info['out'])},indent=2));return
    c=PalmierConnection();c.connect()
    def call(name,args):
        result=c.request('tools/call',{'name':name,'arguments':args})
        if result.get('isError'):raise RuntimeError(f'{name}: {result}')
        return json.loads(next(x['text'] for x in result['content'] if x['type']=='text'))
    print(json.dumps(execute(info,call),indent=2))
if __name__=='__main__':main()
