"""Probe and fully decode exact exports, retaining representative frame and audio evidence."""
import json, subprocess as sp, math, sys
from PIL import Image, ImageDraw
from build_review_edit import setup, read, ref, dump

mode,name=sys.argv[1:3]
ep,ch,fmt,filename,d,w,canvas,word,wm,transcript,frames,speech,media,speed,out,manifest=setup(name)
q=w/'qa-v01'
receipt_path=out.with_suffix('.mp4.delivery.json')
receipt=read(receipt_path)
assert ref(out)==receipt['media']
if mode=='sample':
 q.mkdir()
 ff=['ffmpeg','-nostdin','-hide_banner']
 probe=json.loads(sp.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',out]))
 v,a=probe['streams']; assert [v['width'],v['height']]==canvas and v['codec_name']=='h264' and v['pix_fmt']=='yuv420p'
 assert v['r_frame_rate']==v['avg_frame_rate']=='30/1' and v['sample_aspect_ratio']=='1:1'
 assert int(v['nb_frames'])==frames and v['field_order']=='progressive'
 assert all(v[x]=='bt709' for x in ['color_space','color_transfer','color_primaries']) and v['color_range']=='tv'
 assert a['codec_name']=='aac' and a['profile']=='LC' and a['channels']==2 and a['sample_rate']=='48000'
 assert abs(float(a['duration'])-frames/30)<.04 and abs(float(v['duration'])-frames/30)<.00001
 dump(q/'probe.json',probe)
 scenes=read(manifest)['scenes']
 sample=[0,frames-1]
 for s in scenes:
  i,j=s['start_frame'],s['end_frame']
  sample.extend([i,(i+j)//2,j-1] if fmt=='short' else [(i+j)//2])
 if fmt=='long':
  for j in (1,len(scenes)//4,len(scenes)//2,(3*len(scenes))//4,len(scenes)-1):
   f=scenes[j]['start_frame']; sample.extend((f-1,f))
 sample=sorted(set(sample))
 select='select='+ '+'.join(f'eq(n\\,{i})' for i in sample)
 maxsize=(216,384) if fmt=='short' else (320,180)
 decoded=sp.run(ff+['-nostats','-v','error','-xerror','-progress','pipe:1','-i',out,
   '-map','0:v:0','-map','0:a:0','-fps_mode','passthrough','-f','null','-',
   '-map','0:v:0','-vf',select+f',scale={maxsize[0]}:{maxsize[1]}:flags=lanczos','-fps_mode','vfr','-q:v','3',q/'frame-%04d.jpg'],
   check=True,capture_output=True,text=True).stdout
 count=int([line.split('=',1)[1] for line in decoded.splitlines() if line.startswith('frame=')][-1])
 assert count==frames and decoded.rstrip().endswith('progress=end'),(count,frames)
 (q/'decode-progress.log').write_text(decoded)
 with (q/'audio-preservation.log').open('x') as log:
  sp.run(ff+['-nostats','-i',out,'-i',media,'-filter_complex','[0:a][1:a]apsnr','-vn','-f','null','-'],check=True,stderr=log)
 with (q/'audio-levels.log').open('x') as log:
  sp.run(ff+['-nostats','-i',out,'-af','ebur128=peak=true','-vn','-f','null','-'],check=True,stderr=log)
 files=sorted(q.glob('frame-*.jpg')); assert len(files)==len(sample)
 for first in range(0,len(sample),9 if fmt=='short' else 20):
  part=sample[first:first+(9 if fmt=='short' else 20)]
  cols=3 if fmt=='short' else 4
  tw,th=maxsize; cw,chh=tw+10,th+24
  sheet=Image.new('RGB',(cols*cw,math.ceil(len(part)/cols)*chh),(19,24,31));draw=ImageDraw.Draw(sheet)
  for i,f in enumerate(part):
   x,y=(i%cols)*cw,(i//cols)*chh
   sheet.paste(Image.open(files[first+i]),(x+5,y+4))
   label=next(j for j,s in enumerate(scenes,1) if s['start_frame']<=f<s['end_frame'])
   draw.text((x+5,y+th+7),f'S{label:03d}  f{f}  {f/30:.2f}s',fill='white')
  sheet.save(q/f'export-{first//(9 if fmt=="short" else 20)+1:02d}.jpg',quality=93)
 dump(q/'technical.json',dict(media=ref(out),manifest=ref(manifest),frame_count=frames,duration=frames/30,
       full_decode='PASS',decoded_sample_frames=sample,audio_preservation=ref(q/'audio-preservation.log'),
       audio_levels=ref(q/'audio-levels.log'),probe=ref(q/'probe.json'),subjective_listening='UNVERIFIED'))
 print(name,len(sample),'sample frames; full two-stream decode PASS')
elif mode=='bind':
 ev=q/'REPORT.md'; assert ev.is_file()
 assert read(q/'technical.json')['media']==receipt['media']
 receipt['technical_review']=dict(status='PASS',full_decode='PASS',media_sha256=receipt['media']['sha256'],evidence=ref(ev))
 sidecar=out.with_suffix('.srt')
 mapping=w/'srt-mapping-v01.json'
 if sidecar.is_file() and mapping.is_file():
  rec=read(mapping); assert rec['status']=='PASS' and rec['srt']==ref(sidecar) and rec['audio']==ref(media)
  receipt['srt_review']=dict(media_sha256=receipt['media']['sha256'],language='en',srt=ref(sidecar),evidence=ref(mapping),
    structure='PASS',text_coverage='PASS',timing_mapping='PASS',playback='UNVERIFIED')
 receipt_path.write_text(json.dumps(receipt,indent=2,ensure_ascii=False)+'\n')
 print(name,receipt['media']['sha256'])
