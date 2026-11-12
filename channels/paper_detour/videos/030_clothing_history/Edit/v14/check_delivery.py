from pathlib import Path
import json,subprocess,hashlib,struct
P=Path('/Users/diplomat/ytvideos/channels/paper_detour/videos/030_clothing_history');E=P/'Edit/v14';F=P/'Work/delivery-v14/previews/PAPER_DETOUR_030_CLOTHING_HISTORY_EN_v14.mp4';N=P/'Work/delivery-v14/scratch/native-v14.mp4';A=P/'Source/Audio/v06/accepted_v05_mix.m4a'
run=lambda args:subprocess.check_output(args)
hashstream=lambda f,s:run(['ffmpeg','-v','error','-i',str(f),'-map',s,'-c','copy','-f','hash','-hash','sha256','-']).decode().strip()
hashes={'final_video':hashstream(F,'0:v:0'),'native_video':hashstream(N,'0:v:0'),'final_audio':hashstream(F,'0:a:0'),'accepted_audio':hashstream(A,'0:a:0')};assert hashes['final_video']==hashes['native_video'];assert hashes['final_audio']==hashes['accepted_audio']
probe=json.loads(run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(F)]));(E/'QA/final_ffprobe.json').write_text(json.dumps(probe,indent=2));v=next(s for s in probe['streams'] if s['codec_type']=='video');a=next(s for s in probe['streams'] if s['codec_type']=='audio')
assert (v['width'],v['height'],v['r_frame_rate'],v['avg_frame_rate'],v['codec_name'],v['pix_fmt'])==(2560,1440,'30/1','30/1','h264','yuv420p');assert all(v[k]=='bt709' for k in ['color_space','color_transfer','color_primaries']);assert v['color_range']=='tv' and v['field_order']=='progressive';assert (a['codec_name'],a['profile'],a['sample_rate'],a['channels'])==('aac','LC','48000',2)
packets=json.loads(run(['ffprobe','-v','error','-select_streams','v:0','-show_packets','-show_entries','packet=pts,duration,flags','-of','json',str(F)]))['packets'];pts=sorted(x['pts'] for x in packets);from fractions import Fraction
step=int(Fraction(1,30)/Fraction(v['time_base']));assert len(pts)==5700 and pts[0]==0 and all(y-x==step for x,y in zip(pts,pts[1:]));keys=sorted(x['pts']//step for x in packets if 'K' in x['flags']);gops=[y-x for x,y in zip(keys,keys[1:])]
def atoms(data,start=0,end=None):
 end=len(data) if end is None else end;pos=start;out=[]
 while pos+8<=end:
  size,kind=struct.unpack('>I4s',data[pos:pos+8]);header=8
  if size==1:size=struct.unpack('>Q',data[pos+8:pos+16])[0];header=16
  if size==0:size=end-pos
  if size<header or pos+size>end:break
  out.append({'type':kind.decode('latin1'),'offset':pos,'size':size,'children':atoms(data,pos+header,pos+size) if kind in [b'moov',b'trak',b'mdia',b'minf',b'stbl',b'edts'] else []});pos+=size
 return out
with F.open('rb') as f:data=f.read()
ats=atoms(data);flat=[]
def walk(xs):
 for x in xs:flat.append(x);walk(x['children'])
walk(ats);moov=next(x for x in ats if x['type']=='moov');mdat=next(x for x in ats if x['type']=='mdat');elsts=[x for x in flat if x['type']=='elst'];report={'file':str(F),'sha256':hashlib.sha256(data).hexdigest(),'stream_identity':hashes,'cadence':{'status':'PASS','count':len(pts),'pts_start':0,'step_ticks':step,'time_base':v['time_base'],'fps':'30/1','unique_pts':len(set(pts))},'container':{'faststart':moov['offset']<mdat['offset'],'edit_lists':len(elsts),'atoms':[{'type':x['type'],'offset':x['offset'],'size':x['size']} for x in ats]},'quality_preferences':{'profile':v['profile'],'level':v['level'],'b_frames':v['has_b_frames'],'gop_min':min(gops),'gop_max':max(gops),'decision':'Native engine managed; GOP differs from preferred15 when shown, retained if texture/text final-frame review passes. Existing edit lists retained for codec priming/Bframe sync; not stripped automatically.'},'required_metadata_status':'PASS','audio_decision':'Existing accepted AAC stream copy, no gain/routing/mix change; new384kbps preference not applied by lossy re-encode.'};(E/'QA/DELIVERY_TECHNICAL.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
