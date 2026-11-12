from pathlib import Path
import importlib.util,json,subprocess,hashlib,concurrent.futures,datetime
root=Path(__file__).resolve().parents[3];work=root/'Work/production-text-v03/render';recovery=root/'Work/production-text-v03/recovery';recovery.mkdir(exist_ok=False)
engine=root/'Work/production-text-v03/frozen/automation/ffmpeg_montage/montage.py';sp=importlib.util.spec_from_file_location('montage_recovery',engine);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);d=m.delivery
manifest=root/'Edit/Production/v03/plan.json';plan=json.loads(manifest.read_text());prep=json.loads((work/'plan.json').read_text());contract=json.loads((work/'subtitle_contract.json').read_text());review=json.loads((work/'subtitle_review.json').read_text());prov=json.loads((work/'render_provenance.json').read_text());passport=json.loads((root/'Edit/Export/EXPORT_CONTRACT_v03.json').read_text())
for record in passport['edit']['dependencies']+contract['profiles']+contract['engine']:d.check_record(record)
if json.loads((work/'input_manifest.json').read_text())!=plan:raise RuntimeError('input manifest differs')
if review['subtitle_contract_sha256']!=d.fingerprint(contract):raise RuntimeError('subtitle review mismatch')
inputs=d.render_inputs(manifest,plan,manifest.parent);d.validate_render_binding(prov,contract,str(manifest),str(root/'Deliverables/NUVIKO_040_TU160_EN_REVIEW_v03.mp4'))
clips=[];redo=[];report=[]
for i,s in enumerate(prep['scenes']):
 p=work/f'scene_{i:05d}.mp4';c=work/f'scene_{i:05d}.command.json';n=s['end_frame']-s['start_frame'];valid=False;reason='missing'
 if p.exists() and c.exists():
  old=json.loads(c.read_text());vf=m.camera_filter(*prep['canvas'],n,s['camera']) if s.get('camera') else m.motion_filter(*prep['canvas'],n,s['direction'],s['zoom']);expected=['ffmpeg','-hide_banner','-loglevel','error','-n','-loop','1','-framerate','30','-i',s['image'],'-vf',vf,'-frames:v',str(n),'-an','-c:v','libx264','-b:v','20M','-pix_fmt','yuv420p',str(p)]
  q=subprocess.run(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=nb_frames,width,height,codec_name','-of','json',str(p)],capture_output=True,text=True)
  try:
   st=json.loads(q.stdout)['streams'][0];valid=q.returncode==0 and old==expected and int(st['nb_frames'])==n and st['width']==2560 and st['height']==1440 and st['codec_name']=='h264';reason='verified saved command and container frame count' if valid else 'command or frame count mismatch'
  except Exception:reason='incomplete/unreadable segment'
 if valid: clips.append(p)
 else:clips.append(recovery/f'scene_{i:05d}.mp4');redo.append((i,s))
 report.append({'scene':i,'path':str(p),'expected_frames':n,'reuse':valid,'reason':reason})
print('Complete segments:',len(clips)-len(redo),'regenerating:',[i for i,_ in redo],flush=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
 for f in [pool.submit(m.scene_render,i,s,recovery,prep['canvas'],'libx264','20M') for i,s in redo]:f.result()
listing=recovery/'scenes.ffconcat';listing.write_text('ffconcat version 1.0\n'+''.join('file '+m.quote(x)+'\n' for x in clips))
video=work/'picture.mp4';m.run(['ffmpeg','-hide_banner','-loglevel','error','-n','-f','concat','-safe','0','-i',str(listing),'-c','copy',str(video)])
cmd=json.loads((work/'render_command.json').read_text());out=Path(cmd[-1]);m.run(cmd)
for record in inputs+contract['profiles']+contract['engine']:d.check_record(record)
rec={'schema':'reboot-recovery-v1','time':datetime.datetime.now().astimezone().isoformat(),'reason':'Host reboot interrupted run; complete segments retained; incomplete segments regenerated using frozen renderer','segment_records':report,'regenerated_indices':[i for i,_ in redo],'listing':str(listing),'original_work':str(work),'engine':d.file_record(engine)}
recpath=recovery/'recovery.json';d.write_json(recpath,rec);prov['recovery']=d.file_record(recpath)
d.write_receipt(out,plan['channel'],contract,inputs,review,prov)
print('RENDERED',out,flush=True)
