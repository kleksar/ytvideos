"""Read-only checks supplementing the canonical offline QA helper."""
from pathlib import Path
import json, subprocess, hashlib, struct, sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from palmier_client import call
E=Path('/Users/diplomat/ytvideos/channels/paper_detour/videos/032_galveston_1900')
D=E/'Edit/Export/full_v04'
R=json.loads((D/'render_receipt_v04.json').read_text())
C=json.loads((D/'EXPORT_CONTRACT_v04.json').read_text())
P=Path(R['file'])
def digest(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()
assert digest(P)==R['sha256']
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(P)]))
v=next(s for s in probe['streams'] if s['codec_type']=='video')
a=next(s for s in probe['streams'] if s['codec_type']=='audio')
assert v['sample_aspect_ratio']=='1:1' and v['display_aspect_ratio']=='16:9'
assert all(v[k]=='bt709' for k in ['color_space','color_primaries','color_transfer']) and v['color_range']=='tv'
assert v['field_order']=='progressive' and v['r_frame_rate']==v['avg_frame_rate']=='30/1'
assert float(v['start_time'])==0 and float(a['start_time'])==0
frames=json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_frames','-show_entries','frame=best_effort_timestamp_time,interlaced_frame,key_frame,pict_type','-of','json',str(P)]))['frames']
assert len(frames)==17233
errors=[(i,float(f['best_effort_timestamp_time'])-i/30) for i,f in enumerate(frames) if abs(float(f['best_effort_timestamp_time'])-i/30)>0.000002]
assert not errors and all(f.get('interlaced_frame',0)==0 for f in frames)
keys=[i for i,f in enumerate(frames) if f.get('key_frame')==1]
atoms=[]
with P.open('rb') as f:
 size=P.stat().st_size;pos=0
 while pos<size:
  f.seek(pos);hdr=f.read(8);n,t=struct.unpack('>I4s',hdr)
  if n==1:n=struct.unpack('>Q',f.read(8))[0]
  if n==0:n=size-pos
  assert n>=8 and pos+n<=size
  atoms.append({'type':t.decode('latin1'),'offset':pos,'bytes':n});pos+=n
assert next(x['offset'] for x in atoms if x['type']=='moov')<next(x['offset'] for x in atoms if x['type']=='mdat')
before=json.loads((D/'target_read.json').read_text())
after=call('get_timeline',{'projectId':'25533909','timelineId':C['timeline_id']},'full_v04_post_render_fresh')
fields=['fps','width','height','totalFrames','outputColorSpace','tracks']
differences=[k for k in fields if before[k]!=after[k]]
assert not differences, differences
data={'file':str(P),'sha256':R['sha256'],'status':'PASS','cfr':{'decoded_frames':len(frames),'expected_pts':'index / 30','tolerance_seconds':0.000002,'errors':errors},'progressive':True,'sar':v['sample_aspect_ratio'],'dar':v['display_aspect_ratio'],'color':{k:v[k] for k in ['color_space','color_primaries','color_transfer','color_range']},'encoding_engine_managed':{'profile':v.get('profile'),'level':v.get('level'),'has_b_frames':v.get('has_b_frames'),'actual_bit_rate':v.get('bit_rate'),'keyframe_count':len(keys),'gop_min':min(b-a for a,b in zip(keys,keys[1:])) if len(keys)>1 else None,'gop_max':max(b-a for a,b in zip(keys,keys[1:])) if len(keys)>1 else None},'top_level_atoms':atoms,'faststart':True,'edit_list_compatibility':'Both streams start at zero; original accepted AAC delay/padding preserved by stream copy; full decode and frame cadence checked separately. No edit-list removal or re-encoding.','freshness':{'status':'CURRENT','timeline_id':C['timeline_id'],'compared_fields':fields,'changed':differences},'video_elementary_unchanged':R['native_video_unchanged'],'audio_elementary_unchanged':R['accepted_audio_unchanged'],'audio_stream':{k:a.get(k) for k in ['codec_name','sample_rate','channels','channel_layout','bit_rate','duration']}}
(D/'technical_supplement_v04.json').write_text(json.dumps(data,indent=2));print(json.dumps(data,indent=2))
