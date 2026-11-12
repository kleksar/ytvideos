from pathlib import Path
import json,subprocess,hashlib
E=Path('/Users/diplomat/ytvideos/channels/paper_detour/videos/032_galveston_1900');D=E/'Edit/Export/full_v04';c=json.loads((D/'EXPORT_CONTRACT_v04.json').read_text());native=Path(c['submitted_args']['outputPath']);audio=Path(c['audio']['final_component']['file']);dest=E/'Work/church-demo-v01/previews/032_galveston_en_final_candidate_v04.mp4'
def sha(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()
def probe(p):return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(p)]))
def elementary(p,kind):return subprocess.check_output(['ffmpeg','-v','error','-i',str(p),'-map','0:'+kind+':0','-c','copy','-f','hash','-hash','sha256','-']).decode().strip()
r=probe(native);v=next(s for s in r['streams'] if s['codec_type']=='video');assert v['width']==2560 and v['height']==1440 and v['r_frame_rate']=='30/1' and int(v['nb_frames'])==17233
assert v['codec_name']=='h264' and v['pix_fmt']=='yuv420p' and all(v[x]=='bt709' for x in ('color_space','color_transfer','color_primaries')) and v['color_range']=='tv'
assert sha(audio)==c['audio']['final_component']['sha256'];assert not dest.exists()
args=['ffmpeg','-n','-v','error','-i',str(native),'-i',str(audio),'-map','0:v:0','-map','1:a:0','-c','copy','-map_metadata','-1','-aspect:v:0','16:9','-movflags','+faststart',str(dest)]
subprocess.run(args,check=True)
a0=elementary(audio,'a');a1=elementary(dest,'a');v0=elementary(native,'v');v1=elementary(dest,'v');assert a0==a1 and v0==v1
final=probe(dest);fv=next(x for x in final['streams'] if x['codec_type']=='video');assert fv['sample_aspect_ratio']=='1:1' and fv['display_aspect_ratio']=='16:9';(D/'native_probe.json').write_text(json.dumps(r,indent=2));(D/'final_probe.json').write_text(json.dumps(final,indent=2))
receipt={'file':str(dest),'sha256':sha(dest),'native_file':str(native),'native_sha256':sha(native),'video_elementary_hash':v1,'audio_elementary_hash':a1,'native_video_unchanged':v0==v1,'accepted_audio_unchanged':a0==a1,'mux_args':args,'status':'RENDERED_PENDING_QA','timeline_id':c['timeline_id'],'frame_count':17233,'fps':'30/1'};(D/'render_receipt_v04.json').write_text(json.dumps(receipt,indent=2));c.update(status='RENDERED_PENDING_QA',render=receipt);(D/'EXPORT_CONTRACT_v04.json').write_text(json.dumps(c,indent=2));print(json.dumps(receipt))
