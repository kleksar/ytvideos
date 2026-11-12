from pathlib import Path
import json,subprocess,hashlib
E=Path('/Users/diplomat/ytvideos/channels/paper_detour/videos/032_galveston_1900');D=E/'Edit/Export/full_v02'
old=json.loads((D/'render_receipt_v02.json').read_text());src=Path(old['file']);dest=src.with_name('032_galveston_en_final_candidate_v03.mp4');assert not dest.exists()
def sha(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()
assert sha(src)==old['sha256']
c=json.loads((D/'EXPORT_CONTRACT_v02.json').read_text());c.update(version=3,status='READY_TO_RENDER')
c['container_repair']={'reason':'Native file omits SAR/DAR signalling; require explicit square pixels16:9 for the unchanged2560x1440 picture.','source_file':str(src),'source_sha256':old['sha256'],'output':str(dest),'method':'ffmpeg stream copy -aspect16:9; container metadata only; compare both encoded stream hashes.','documentation':'https://www.ffmpeg.org/ffmpeg.html#Video-Options','encoding_authorization':'Existing full-film production/export; no pixel or audio encode or sound generation.'}
(D/'EXPORT_CONTRACT_v03.json').write_text(json.dumps(c,indent=2))
args=['ffmpeg','-n','-v','warning','-i',str(src),'-map','0','-c','copy','-aspect:v:0','16:9','-movflags','+faststart',str(dest)];subprocess.run(args,check=True)
p=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(dest)]));v=next(s for s in p['streams'] if s['codec_type']=='video');assert v['sample_aspect_ratio']=='1:1' and v['display_aspect_ratio']=='16:9'
def elementary(kind):return subprocess.check_output(['ffmpeg','-v','error','-i',str(dest),'-map','0:'+kind+':0','-c','copy','-f','hash','-hash','sha256','-']).decode().strip()
vh=elementary('v');ah=elementary('a');assert vh==old['video_elementary_hash'] and ah==old['audio_elementary_hash']
r={**old,'file':str(dest),'sha256':sha(dest),'container_repair_args':args,'video_elementary_hash':vh,'audio_elementary_hash':ah,'status':'RENDERED_PENDING_QA','previous_candidate':old['file'],'previous_sha256':old['sha256']};(D/'render_receipt_v03.json').write_text(json.dumps(r,indent=2));(D/'final_probe_v03.json').write_text(json.dumps(p,indent=2));c.update(status='RENDERED_PENDING_QA',render=r);(D/'EXPORT_CONTRACT_v03.json').write_text(json.dumps(c,indent=2));print(json.dumps(r))
