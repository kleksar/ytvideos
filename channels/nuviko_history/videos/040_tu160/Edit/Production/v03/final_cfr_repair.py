from pathlib import Path
import importlib.util,json,subprocess,datetime
r=Path(__file__).resolve().parents[3];old=r/'Work/production-text-v03/render';work=r/'Work/production-text-v03/cfr-repair-v04';work.mkdir(exist_ok=False)
engine=r/'Work/production-text-v03/frozen/automation/ffmpeg_montage/montage.py';spec=importlib.util.spec_from_file_location('montage_cfr',engine);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);d=m.delivery
manifest=r/'Edit/Production/v03/plan.json';plan=json.loads(manifest.read_text());prep=json.loads((old/'plan.json').read_text());sub=json.loads((old/'subtitle_contract.json').read_text());review=json.loads((old/'subtitle_review.json').read_text());out=r/'Deliverables/NUVIKO_040_TU160_EN_REVIEW_v04.mp4';assert not out.exists()
passport=json.loads((r/'Edit/Export/EXPORT_CONTRACT_v03.json').read_text());passport['purpose']='Review export; CFR correction to visual revision v03 after technical QA detected two missing frames.';passport['preflight']['output_path']=str(out);passport['preflight']['time']=datetime.datetime.now().astimezone().isoformat();passport['preflight']['fresh_settings_evidence']=str(work/'settings_check.json');passport['settings_check_receipt']=str(work/'settings_check.json');passport['encoding']['requested_arguments']['encoder']='h264_videotoolbox';passport['encoding']['engine']='Frozen shared FFmpeg renderer with h264_videotoolbox; final command includes explicit 30 fps CFR and frame limit';passport['encoding']['engine_managed_fields'].append('Explicit CFR repair -r 30 -fps_mode cfr -frames:v 21773; other render inputs unchanged')
passpath=r/'Edit/Export/EXPORT_CONTRACT_v04.json';passpath.write_text(json.dumps(passport,indent=2,ensure_ascii=False)+'\n')
for record in passport['edit']['dependencies']+sub['profiles']+sub['engine']:d.check_record(record)
cmd=json.loads((old/'render_command.json').read_text());cmd[cmd.index('-c:v')+1]='h264_videotoolbox';cmd=cmd[:-1]+['-r','30','-fps_mode','cfr','-frames:v',str(prep['frames']),str(out)]
audio_info=json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','a:0','-show_entries','stream=codec_name,profile,channels,sample_rate,bit_rate,duration:format=duration','-of','json',prep['audio']]))['streams'][0]
settings=d.check_export_settings(passport,cmd,prep,audio_info,manifest,out);d.write_json(work/'settings_check.json',{'status':'PASS','settings':settings});d.write_json(work/'render_command.json',cmd)
prov=d.freeze_render(work,passpath,work/'render_command.json',sub['engine'],prep,audio_info,manifest,out)
prov['recovery']=d.file_record(r/'Work/production-text-v03/recovery/recovery.json');prov['cfr_fix']={'reason':'QA v03 identified 2 missing frames and variable average cadence','flags':['-r','30','-fps_mode','cfr','-frames:v',str(prep['frames'])],'picture_input':d.file_record(old/'picture.mp4')}
d.write_json(work/'render_provenance.json',prov)
print('SETTINGS_PASS; starting corrected final encode',flush=True);m.run(cmd)
inputs=d.render_inputs(manifest,plan,manifest.parent)
for record in inputs+sub['profiles']+sub['engine']:d.check_record(record)
d.write_receipt(out,plan['channel'],sub,inputs,review,prov)
print('RENDERED',out,flush=True)
