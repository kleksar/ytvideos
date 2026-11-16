import importlib.util, io, json, subprocess, sys, tempfile, unittest
from pathlib import Path
from unittest.mock import patch
from PIL import Image, ImageDraw
from export_fixture import passport
from font_fixture import configure, font as fixture_font

configure()

P=Path(__file__).resolve().parents[1]/'montage.py'
spec=importlib.util.spec_from_file_location('montage',P);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
def bind_plan(plan,p):
    plan.setdefault('scenes',[])
    plan.setdefault('audio','audio.m4a')
    audio=p/plan['audio']
    if not audio.exists():audio.write_bytes(b'synthetic audio identity fixture')
    (p/'speed.txt').write_text('Synthetic test fixture: already retimed 1.10x, not production evidence.')
    plan['audio_contract']={'final_audio_sha256':m.delivery.sha256(audio),'applied_speed':1.1,'speed_evidence':'speed.txt'}
    wordpath=p/plan['subtitles']['words'];data=json.loads(wordpath.read_text())
    words=data['words'] if isinstance(data,dict) else data
    text=' '.join(w['text'] for w in words)
    (p/'transcript.txt').write_text(text)
    plan['subtitles']['transcript']='transcript.txt'
    import hashlib
    wordpath.write_text(json.dumps({'words':words,'audio_sha256':m.delivery.sha256(audio),'transcript_sha256':hashlib.sha256(text.encode()).hexdigest()}))
    return plan

def render_captions(plan,p,work,canvas,frames):
    if plan['subtitles'].get('words'):bind_plan(plan,p)
    return m.caption_sequence(plan,p,work,canvas,frames)

# Historical pinned policy, not the current Oddly Drawn production configuration.
LEGACY_TWL_PATH=Path(__file__).parent/'fixtures'/'two_ways_lab_legacy.json'
LEGACY_TWL=json.loads(LEGACY_TWL_PATH.read_text())

class TestMontage(unittest.TestCase):
 @patch.object(m.delivery.channel_config, 'channel_profile', return_value=(LEGACY_TWL, LEGACY_TWL_PATH))
 def test_optional_minimum_scene_frames_prevents_unintended_flash(self, _profile):
  with tempfile.TemporaryDirectory() as td:
   p=Path(td);(p/'audio.wav').write_bytes(b'audio');Image.new('RGB',(20,20)).save(p/'image.png')
   def scene(start,end):
    return {'image':'image.png','start_frame':start,'end_frame':end,'direction':'none','zoom':'none'}
   plan={'channel':'two_ways_lab','format':'short','canvas':[1080,1920],'audio':'audio.wav',
         'minimum_scene_frames':45,'scenes':[scene(0,50),scene(50,70),scene(70,120)],'subtitles':{'mode':'none'}}
   with self.assertRaisesRegex(ValueError,'scene 2: 20 frames.*minimum 45'):m.validate(plan,p)
   plan['scenes']=[scene(0,50),scene(50,100),scene(100,150)]
   self.assertEqual(m.validate(plan,p)['frames'],150)
   plan['minimum_scene_frames']=True
   with self.assertRaisesRegex(ValueError,'must be an integer'):m.validate(plan,p)
 @patch.object(m.delivery.channel_config, 'channel_profile', return_value=(LEGACY_TWL, LEGACY_TWL_PATH))
 def test_channel_policy_still_rejects_single_frame_when_duration_enforcement_is_disabled(self, _profile):
  with tempfile.TemporaryDirectory() as td:
   p=Path(td);(p/'audio.wav').write_bytes(b'audio');Image.new('RGB',(20,20)).save(p/'image.png')
   plan={'channel':'two_ways_lab','format':'short','audio':'audio.wav','enforce_scene_duration':False,
         'scenes':[{'image':'image.png','start_frame':0,'end_frame':1,'direction':'none','zoom':'none'}],
         'subtitles':{'mode':'none'}}
   with self.assertRaisesRegex(ValueError,'minimum of 2 frames'):m.validate(plan,p)
   plan['scenes'][0]['end_frame']=2
   self.assertEqual(m.validate(plan,p)['frames'],2)
   plan['scenes'][0]['direction']='top_to_bottom'
   with self.assertRaisesRegex(ValueError,'direction not allowed'):m.validate(plan,p)
 def test_nuviko_background_transparency_in_both_formats(self):
  for form,canvas in [('short',[1440,2560]),('long',[2560,1440])]:
   with self.subTest(form=form),tempfile.TemporaryDirectory() as td:
    p=Path(td); work=p/'work'; work.mkdir()
    (p/'words.json').write_text(json.dumps([{'text':'Hello','start':.1,'end':.5}]))
    render_captions({'channel':'nuviko','format':form,'subtitles':{'mode':'words','words':'words.json'}},p,work,canvas,30)
    image=Image.open(work/'caption_states'/'00000_neutral.png').convert('RGBA')
    bounds=image.getbbox(); self.assertIsNotNone(bounds)
    background=image.getpixel((bounds[0],0))
    self.assertEqual(background,(32,37,43,204))
    composite=Image.alpha_composite(Image.new('RGBA',image.size,(255,255,255,255)),image)
    self.assertEqual(composite.getpixel((bounds[0],0)),(77,81,85,255))
 def test_correlative_complement_keeps_final_day_together(self):
  font=fixture_font('nuviko',84)
  tokens="And today, whenever archaeologists uncover another street or room, we learn not only about Pompeii's final day.".split()
  words=[{'text':t,'start':i*.3,'end':i*.3+.2} for i,t in enumerate(tokens)]
  groups=m.grouping.group_words(words,font,1308)
  phrases=[' '.join(w['text'] for w in g) for g in groups]
  self.assertEqual([w['text'] for g in groups for w in g],tokens)
  self.assertTrue(any("Pompeii's final day." in phrase for phrase in phrases))
  self.assertFalse(any(phrase == 'day.' for phrase in phrases))
  self.assertEqual(m.grouping.plan_phrases(words,phrases,font,1308),groups)
 def test_reviewed_phrase_keeps_clause_punctuation(self):
  font=fixture_font('paper',84)
  words=[{'text':t,'start':i*.3,'end':i*.3+.2} for i,t in enumerate('To understand that, go back two days.'.split())]
  groups=m.grouping.plan_phrases(words,['To understand that,','go back two days.'],font,1298)
  self.assertEqual(' '.join(w['text'] for g in groups for w in g),'To understand that, go back two days.')
  words[2]['text']='that'
  with self.assertRaisesRegex(ValueError,'syntactic hook'):
   m.grouping.plan_phrases(words,['To understand that','go back two days.'],font,1298)
 def test_subtitle_profiles_and_scaling(self):
  for channel,form,canvas,expected in [('paper','long',[2560,1440],84),('paper','short',[1440,2560],104),('nuviko','long',[2560,1440],84),('nuviko','short',[1440,2560],68),('paper','short',[720,1280],52),('nuviko','long',[1280,720],42)]:
   with self.subTest(channel=channel,form=form,canvas=canvas),tempfile.TemporaryDirectory() as td:
    p=Path(td);(p/'words.json').write_text(json.dumps([{'text':'Hello','start':0.1,'end':0.5}]))
    work=p/'work';work.mkdir()
    plan={'channel':channel,'format':form,'subtitles':{'mode':'words','words':'words.json'}}
    render_captions(plan,p,work,canvas,30)
    result=json.loads((work/'caption_groups.json').read_text())
    self.assertEqual((result['channel'],result['format'],result['resolved_font_size_px']),(channel,form,expected))
    self.assertEqual(result['profile']['name'],channel)
 def test_canvas_orientation_matches_format(self):
  for form,canvas in [('short',[2560,1440]),('long',[1440,2560])]:
   with self.subTest(form=form),tempfile.TemporaryDirectory() as td:
    with self.assertRaisesRegex(ValueError,'orientation must match format'):
     m.validate({'channel':'paper','format':form,'canvas':canvas},Path(td))
 def test_short_font_override_cannot_break_profile(self):
  for channel in ('paper','nuviko'):
   with self.subTest(channel=channel),tempfile.TemporaryDirectory() as td:
    plan={'channel':channel,'format':'short','subtitles':{'style':{'font_size_portrait':72}}}
    with self.assertRaisesRegex(ValueError,'shared format profile'):
     render_captions(plan,Path(td),Path(td),[1440,2560],30)
 def test_short_visible_width_and_position_are_shared(self):
  for channel in ('paper','nuviko'):
   with self.subTest(channel=channel),tempfile.TemporaryDirectory() as td:
    p=Path(td);work=p/'work';work.mkdir()
    (p/'words.json').write_text(json.dumps([{'text':x,'start':i*.2,'end':i*.2+.15} for i,x in enumerate('Sailors arrived safely.'.split())]))
    render_captions({'channel':channel,'format':'short','subtitles':{'mode':'words','words':'words.json'}},p,work,[1440,2560],30)
    data=json.loads((work/'caption_groups.json').read_text())
    self.assertEqual(data['max_visible_width_px'],1024)
    self.assertAlmostEqual(data['center_x_px'],680)
    self.assertEqual(data['shared_short_geometry']['center_y_ratio'],.762)
    for image_path in (work/'caption_states').glob('*.png'):
     bounds=Image.open(image_path).getbbox()
     self.assertTrue(bounds and bounds[0]>=168 and bounds[2]<=1192, (channel,bounds))
 def test_long_visible_geometry_is_shared(self):
  for channel in ('paper','nuviko'):
   with self.subTest(channel=channel),tempfile.TemporaryDirectory() as td:
    p=Path(td);work=p/'work';work.mkdir()
    (p/'words.json').write_text(json.dumps([{'text':x,'start':i*.2,'end':i*.2+.15} for i,x in enumerate('The sailors returned safely.'.split())]))
    _,top=render_captions({'channel':channel,'format':'long','subtitles':{'mode':'words','words':'words.json'}},p,work,[2560,1440],30)
    data=json.loads((work/'caption_groups.json').read_text())
    self.assertEqual((data['resolved_font_size_px'],data['max_visible_width_px'],data['center_x_px'],data['baseline']),(84,1344,1280,1288))
    for image_path in (work/'caption_states').glob('*.png'):
     bounds=Image.open(image_path).getbbox()
     self.assertTrue(bounds and bounds[0]>=608 and bounds[2]<=1952 and top+bounds[3]<=1332,(channel,bounds,top))
 def test_long_geometry_override_rejected(self):
  for channel in ('paper','nuviko'):
   with self.subTest(channel=channel),tempfile.TemporaryDirectory() as td:
    plan={'channel':channel,'format':'long','subtitles':{'style':{'safe_width_ratio':.9}}}
    with self.assertRaisesRegex(ValueError,'shared format profile'):
     render_captions(plan,Path(td),Path(td),[2560,1440],30)
 def test_american_sailors_fits_in_both_styles(self):
  for channel in ('paper','nuviko'):
   with self.subTest(channel=channel),tempfile.TemporaryDirectory() as td:
    p=Path(td);work=p/'work';work.mkdir()
    (p/'words.json').write_text(json.dumps([{'text':'American','start':.1,'end':.4},{'text':'sailors.','start':.5,'end':.8}]))
    plan={'channel':channel,'format':'short','subtitles':{'mode':'words','words':'words.json','phrases':['American sailors.']}}
    render_captions(plan,p,work,[1440,2560],30)
    self.assertEqual(len(json.loads((work/'caption_groups.json').read_text())['groups']),1)
 def test_paper_short_automatically_groups_at_most_three_words(self):
  with tempfile.TemporaryDirectory() as td:
   p=Path(td);work=p/'work';work.mkdir()
   tokens='The ship reached Thailand. Five sailors arrived.'.split()
   (p/'words.json').write_text(json.dumps([{'text':word,'start':i*.2,'end':i*.2+.15} for i,word in enumerate(tokens)]))
   render_captions({'channel':'paper','format':'short','subtitles':{'mode':'words','words':'words.json'}},p,work,[1440,2560],60)
   groups=json.loads((work/'caption_groups.json').read_text())['groups']
   self.assertTrue(all(len(group)<=3 for group in groups))
   self.assertEqual([w['text'] for group in groups for w in group],tokens)
 def test_short_number_boundary_when_width_requires_it(self):
  font=fixture_font('paper',128)
  words=[{'text':w} for w in 'Five thousand American sailors.'.split()]
  # Width is measured from the explicit test font, not a macOS font's metrics.
  width=max(font.getlength('Five thousand'),font.getlength('American sailors.'))+1
  groups=m.grouping.group_words(words,font,width,max_words=3)
  self.assertEqual([w['text'] for group in groups for w in group],[w['text'] for w in words])
  self.assertGreater(len(groups),1)
  self.assertTrue(all(len(group)<=3 and font.getlength(' '.join(w['text'] for w in group))<=width for group in groups))
 def test_direction_rule(self):
  with tempfile.TemporaryDirectory() as td:
   p=Path(td);(p/'audio').touch();(p/'im').touch()
   s=lambda a,b,d,z:{'image':'im','start_frame':a,'end_frame':b,'direction':d,'zoom':z}
   plan={'channel':'nuviko','format':'long','audio':'audio','scenes':[s(0,120,'left_to_right','in'),s(120,240,'left_to_right','out')],'subtitles':{'mode':'none'}}
   with self.assertRaisesRegex(ValueError,'repeat direction'):m.validate(plan,p)
   plan['scenes'][1]['direction']='right_to_left';self.assertEqual(m.validate(plan,p)['frames'],240)
 def test_zoom_rule_checks_components_independently(self):
  with tempfile.TemporaryDirectory() as td:
   p=Path(td);(p/'audio').touch();(p/'im').touch()
   def scene(start,direction,zoom):return {'image':'im','start_frame':start,'end_frame':start+120,'direction':direction,'zoom':zoom}
   plan={'channel':'nuviko','format':'long','audio':'audio','subtitles':{'mode':'none'},'scenes':[scene(0,'left_to_right','in'),scene(120,'right_to_left','in')]}
   with self.assertRaisesRegex(ValueError,'repeat zoom in'):m.validate(plan,p)
   plan['scenes'][1]['zoom']='out';self.assertEqual(m.validate(plan,p)['frames'],240)
   plan['scenes'][1]=scene(120,'right_to_left','none');plan['scenes'].append(scene(240,'none','in'));self.assertEqual(m.validate(plan,p)['frames'],360)
   plan['scenes'][1]=scene(120,'right_to_left','out');plan['scenes'][2]=scene(240,'none','out')
   with self.assertRaisesRegex(ValueError,'repeat zoom out'):m.validate(plan,p)
 def test_all_motion_modes_construct(self):
  for direction in m.DIRECTIONS:
   for zoom in m.ZOOMS:
    s=m.motion_filter(320,180,120,direction,zoom);self.assertIn('perspective=',s);self.assertIn('crop=320:180',s)
 def test_slow_pan_preserves_subpixel_progress_on_every_encoded_frame(self):
  # A seven-pixel pan over four seconds is below one pixel per frame. Integer
  # crop/zoompan rounding produces long holds followed by a full-pixel jump.
  with tempfile.TemporaryDirectory() as td:
   p=Path(td);source=p/'source.png';out=p/'motion.mp4'
   image=Image.new('RGB',(320,180),'black');ImageDraw.Draw(image).rectangle((115,65,205,115),fill='white');image.save(source)
   subprocess.run(['ffmpeg','-v','error','-loop','1','-framerate','30','-i',str(source),
                   '-vf',m.motion_filter(320,180,120,'left_to_right','none'),'-frames:v','120',
                   '-c:v','libx264','-crf','0','-pix_fmt','yuv420p',str(out)],check=True,capture_output=True)
   raw=subprocess.check_output(['ffmpeg','-v','error','-i',str(out),'-f','rawvideo','-pix_fmt','gray','-'])
   self.assertEqual(len(raw),120*320*180)
   centers=[]
   for index in range(120):
    frame=raw[index*320*180:(index+1)*320*180]
    columns=[sum(frame[x::320]) for x in range(320)]
    centers.append(sum(x*weight for x,weight in enumerate(columns))/sum(columns))
   steps=[after-before for before,after in zip(centers,centers[1:])]
   mean_step=(centers[-1]-centers[0])/119
   self.assertGreater(mean_step,0)
   self.assertLess(mean_step,.1)
   self.assertGreater(min(steps),0,'A held/backward frame interrupts the slow pan')
   self.assertLess(max(steps),2*mean_step,'A quantized jump is much larger than subpixel progress')
 def test_visible_motion_directions_and_zoom(self):
  with tempfile.TemporaryDirectory() as td:
   p=Path(td);image=Image.new('RGB',(320,180),'black');ImageDraw.Draw(image).rectangle((70,35,250,145),fill='red');image.save(p/'source.png')
   def measure(direction,zoom):
    out=p/(direction+'_'+zoom+'.mp4');vf=m.motion_filter(320,180,120,direction,zoom)
    subprocess.run(['ffmpeg','-loglevel','error','-loop','1','-framerate','30','-i',str(p/'source.png'),'-vf',vf,'-frames:v','120','-c:v','libx264','-pix_fmt','yuv420p',str(out)],check=True)
    result=[]
    for frame in (0,119):
     raw=subprocess.check_output(['ffmpeg','-loglevel','error','-i',str(out),'-vf',f'select=eq(n\\,{frame})','-frames:v','1','-f','image2pipe','-vcodec','png','-'])
     im=Image.open(io.BytesIO(raw)).convert('RGB');px=im.load();points=[(x,y) for y in range(180) for x in range(320) if px[x,y][0]>100 and px[x,y][1]<70]
     result.append((sum(x for x,y in points)/len(points),sum(y for x,y in points)/len(points),len(points)))
    return result
   for direction,axis,sign in [('left_to_right',0,1),('right_to_left',0,-1),('top_to_bottom',1,1),('bottom_to_top',1,-1)]:
    a,b=measure(direction,'none');self.assertGreater((b[axis]-a[axis])*sign,1,direction)
   a,b=measure('none','in');self.assertGreater(b[2],a[2]);a,b=measure('none','out');self.assertLess(b[2],a[2])
 def test_focus_camera_render_and_bounds(self):
  fx,fy=.72,.45;zs,ze=1.075,1.10
  cam={'subject':'red target','reason':'emphasize target','focus':[fx,fy],'start':{'center':[.5,.5],'scale':zs},'end':{'center':[fx-(fx-.5)*zs/ze,fy-(fy-.5)*zs/ze],'scale':ze}}
  # Keeping an off-centre subject fixed while zooming requires compensating
  # translation; these endpoints move the image centre right-to-left.
  m.validate_camera(cam,'right_to_left','in')
  with tempfile.TemporaryDirectory() as td:
   p=Path(td);im=Image.new('RGB',(640,360),(0,150,0));ImageDraw.Draw(im).rectangle((440,144,480,180),fill='red');im.save(p/'source.png');out=p/'camera.mp4'
   subprocess.run(['ffmpeg','-loglevel','error','-loop','1','-framerate','30','-i',str(p/'source.png'),'-vf',m.camera_filter(640,360,120,cam),'-frames:v','120','-c:v','libx264',str(out)],check=True)
   coords=[]
   for frame in (0,119):
    raw=subprocess.check_output(['ffmpeg','-loglevel','error','-i',str(out),'-vf',f'select=eq(n\\,{frame})','-frames:v','1','-f','image2pipe','-vcodec','png','-']);img=Image.open(io.BytesIO(raw)).convert('RGB');px=img.load()
    pts=[(x,y) for y in range(360) for x in range(640) if px[x,y][0]>150 and px[x,y][1]<60];coords.append((sum(x for x,y in pts)/len(pts),sum(y for x,y in pts)/len(pts),len(pts)))
    self.assertTrue(all(px[x,y][1]>80 for x,y in [(0,0),(639,0),(0,359),(639,359)]))
   self.assertLess(abs(coords[0][0]-coords[1][0]),1);self.assertLess(abs(coords[0][1]-coords[1][1]),1);self.assertGreater(coords[1][2],coords[0][2])
  bad=dict(cam,end={'scale':1.10,'center':[.9,.5]})
  with self.assertRaisesRegex(ValueError,'exposes an image edge'):m.validate_camera(bad,'right_to_left','in')
 def test_end_to_end_profiles(self):
  for channel,form,canvas in [('paper','long',[320,180]),('nuviko','long',[320,180]),('paper','short',[180,320]),('nuviko','short',[180,320])]:
   with self.subTest(channel=channel,form=form),tempfile.TemporaryDirectory() as td:
    p=Path(td);Image.new('RGB',(400,225),'#6c8ea0').save(p/'image.png')
    subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-f','lavfi','-i','sine=frequency=440:duration=8','-c:a','aac',str(p/'audio.m4a')],check=True)
    words=[{'text':'The','start':0.2,'end':0.4},{'text':'ship','start':0.5,'end':0.8},{'text':'arrived.','start':0.9,'end':1.3},{'text':'The','start':4.2,'end':4.4},{'text':'city','start':4.5,'end':4.8},{'text':'waited.','start':4.9,'end':5.2}];(p/'words.json').write_text(json.dumps(words))
    plan={'channel':channel,'format':form,'canvas':canvas,'audio':'audio.m4a','scenes':[{'image':'image.png','start_frame':0,'end_frame':120,'direction':'left_to_right','zoom':'in'},{'image':'image.png','start_frame':120,'end_frame':240,'direction':'top_to_bottom','zoom':'out'}],'subtitles':{'mode':'words','words':'words.json'}}
    Image.new('RGBA',(24,24),(255,0,0,180)).save(p/'accent.png');plan['overlays']=[{'path':'accent.png','start_frame':30,'end_frame':60,'x':10,'y':10}]
    if channel=='nuviko':
     with self.assertRaisesRegex(ValueError,'only the subtitle layer'):
      m.validate(plan,p)
     del plan['overlays']
    if form=='short':plan['subtitles']['phrases']=['The ship','arrived.','The city','waited.']
    bind_plan(plan,p);(p/'plan.json').write_text(json.dumps(plan));out=p/'result.mp4';work=p/'work'
    audio={'codec_name':'aac','profile':'LC','channels':1,'sample_rate':'44100'}
    contract=p/'export.json';contract.write_text(json.dumps(passport(m,p/'plan.json',m.validate(plan,p),audio,out)))
    subprocess.run(['python3',str(P),str(p/'plan.json'),'--technical-probe','--output',str(out),'--work-dir',str(work),'--encoder','libx264','--bitrate','800k','--export-contract',str(contract)],check=True,capture_output=True,text=True)
    data=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','stream=codec_type,width,height,nb_frames','-of','json',str(out)]));video=next(x for x in data['streams'] if x['codec_type']=='video');self.assertEqual((video['width'],video['height'],video['nb_frames']),(canvas[0],canvas[1],'240'));self.assertTrue(any(x['codec_type']=='audio' for x in data['streams']))
    self.assertEqual(json.loads((work/'caption_groups.json').read_text())['profile']['name'],channel)
    receipt=json.loads(Path(str(out)+'.delivery.json').read_text())
    self.assertEqual(receipt['media'],m.delivery.file_record(out))
    self.assertFalse(receipt['acceptance']['accepted'])
    self.assertTrue(all(check['status']=='UNVERIFIED' for check in receipt['review']['checks'].values()))

 def test_pcm_stereo_settings_check_and_actual_encoding(self):
  with tempfile.TemporaryDirectory() as td:
   p=Path(td);Image.new('RGB',(400,225),'#6c8ea0').save(p/'image.png')
   subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-f','lavfi','-i','anoisesrc=d=4:r=44100:seed=1',
                   '-ac','2','-c:a','pcm_s16le',str(p/'audio.wav')],check=True)
   (p/'words.json').write_text(json.dumps([{'text':'Fixture.','start':.2,'end':1.0}]))
   plan=bind_plan({'channel':'nuviko','format':'long','canvas':[320,180],'audio':'audio.wav',
                  'source_transfer':'srgb',
                  'scenes':[{'image':'image.png','start_frame':0,'end_frame':120,'direction':'left_to_right','zoom':'in'}],
                  'subtitles':{'mode':'words','words':'words.json'}},p)
   manifest=p/'plan.json';manifest.write_text(json.dumps(plan));out=p/'result.mp4'
   audio={'codec_name':'pcm_s16le','channels':2,'sample_rate':'44100'}
   contract=p/'export.json';contract.write_text(json.dumps(passport(m,manifest,m.validate(plan,p),audio,out)))
   argv=[sys.executable,str(P),str(manifest),'--technical-probe','--output',str(out),'--export-contract',str(contract),'--encoder','libx264','--bitrate','800k']
   subprocess.run(argv+['--work-dir',str(p/'check'),'--check-settings'],check=True,capture_output=True,text=True)
   self.assertFalse(out.exists());self.assertFalse(list((p/'check').glob('scene_*.mp4')))
   bad=argv.copy();bad[bad.index('--bitrate')+1]='20M'
   result=subprocess.run(bad+['--work-dir',str(p/'bad')],capture_output=True,text=True)
   self.assertEqual(result.returncode,2);self.assertIn('video_bitrate',result.stderr)
   self.assertFalse(out.exists());self.assertFalse(list((p/'bad').glob('scene_*.mp4')))
   subprocess.run(argv+['--work-dir',str(p/'render')],check=True,capture_output=True,text=True)
   receipt=json.loads(Path(str(out)+'.delivery.json').read_text())
   self.assertEqual(receipt['schema'],'ytv-delivery-v2')
   self.assertEqual(receipt['render']['settings']['audio']['target_bit_rate'],256000)
   actual=json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','a:0',
      '-show_entries','stream=codec_name,channels,sample_rate,bit_rate','-of','json',str(out)]))['streams'][0]
   self.assertEqual((actual['codec_name'],actual['channels'],actual['sample_rate']),('aac',2,'44100'))
   # VBR mean is measured evidence, not the requested encoder target.
   command=json.loads((p/'render'/'render_command.json').read_text())
   self.assertEqual(command[command.index('-b:a')+1],'256k')
   subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-i',str(out),'-f','null','-'],check=True,capture_output=True)

if __name__=='__main__':unittest.main()
