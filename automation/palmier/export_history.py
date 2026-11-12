#!/usr/bin/env python3
"""Queue a confirmed assembled history timeline once; never blind-retry."""
import argparse, json, os, shutil
from pathlib import Path
from assemble_history_long import sha
from inspect_connection import PalmierConnection

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--series',type=Path,required=True);p.add_argument('--manifest',type=Path,required=True);p.add_argument('--receipt',type=Path,required=True);p.add_argument('--project',type=Path,required=True);a=p.parse_args()
 root=a.series.resolve();manifest=a.manifest.resolve();rp=a.receipt.resolve();project=a.project.resolve()
 if not manifest.is_relative_to(root/'Edit') or not rp.is_relative_to(root/'Edit'):raise ValueError('Manifest and receipt must belong to episode')
 m=json.loads(manifest.read_text());r=json.loads(rp.read_text())
 if m.get('status')!='ready' or r.get('status')!='assembled' or r.get('timeline')!=m.get('timeline') or r.get('manifestSha256')!=sha(manifest) or Path(r.get('project','')).resolve()!=project:raise ValueError('Assembly receipt does not match manifest/project')
 if shutil.disk_usage(root).free<10*1024**3:raise ValueError('Less than 10 GiB free before export')
 out=root/'Deliverables'/f"{m['timeline']}_palmier.mp4";out.parent.mkdir(parents=True,exist_ok=True)
 journal=rp.with_name(rp.stem+'_export.json')
 if out.exists() or journal.exists():raise FileExistsError('Export output or journal exists; inspect before retry')
 c=PalmierConnection();c.connect()
 def call(name,args):
  result=c.request('tools/call',{'name':name,'arguments':args})
  if result.get('isError'):raise RuntimeError(f'{name}: {result}')
  return json.loads(next(x['text'] for x in result['content'] if x['type']=='text'))
 pr=call('manage_project',{'action':'list'});tl=call('get_timeline',{});ex=call('manage_exports',{'action':'list'}).get('exports')
 if any(Path(pr[k]['path']).resolve()!=project for k in ('active','visible')) or tl['id']!=r['timelineId'] or tl['name']!=m['timeline'] or tl['totalFrames']!=m['frames']:raise RuntimeError('Active project/timeline differs from assembled receipt')
 if not isinstance(ex,list) or any(not isinstance(x,dict) or x.get('status') not in ('completed','failed','cancelled','canceled') for x in ex):raise RuntimeError('Another export is active or state unknown')
 def clips(tracks):return sorted((c['id'],c.get('mediaRef'),c['frames'],c.get('keyframes',{}).get('scale')) for tr in tracks for c in tr.get('clips',[]))
 if clips(tl['tracks'])!=clips(r['tracks']):raise RuntimeError('Timeline content changed since assembly')
 request={'status':'requesting','manifestSha256':sha(manifest),'timelineId':tl['id'],'path':str(out)}
 with journal.open('x') as f:json.dump(request,f,indent=2);f.flush();os.fsync(f.fileno())
 result=call('export_project',{'mode':'video','codec':'H.264','resolution':'Match Timeline','timelineId':tl['id'],'outputPath':str(out),'overwrite':False})
 request.update(status='queued',result=result)
 with journal.open('w') as f:json.dump(request,f,ensure_ascii=False,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
 print(json.dumps(request,ensure_ascii=False))
if __name__=='__main__':main()
