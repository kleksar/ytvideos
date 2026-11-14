"""Real montage preflight sees bound profile bytes; no production QA asserted."""
import hashlib
import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[3]
spec=importlib.util.spec_from_file_location('profile_montage',ROOT/'automation/ffmpeg_montage/montage.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

class PinnedProfileTests(unittest.TestCase):
 def tearDown(self):m.delivery.channel_config.PINNED=None
 def test_preflight_uses_pinned_requirements_and_rejects_tampering(self):
  profile=json.loads((ROOT/'channels/nuviko_history/channel.json').read_text())
  profile['production']['video'].pop('minimum_shot_seconds')
  with tempfile.TemporaryDirectory() as td:
   p=Path(td)/'profile.json';raw=json.dumps(profile,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode();p.write_bytes(raw);sha=hashlib.sha256(raw).hexdigest()
   plan={'channel':'nuviko_history','format':'short','audio':'a.wav','srt':'a.srt','subtitles':{'mode':'words'},'transitions':'direct_cuts',
         'scenes':[{'image':'s.png','start_frame':0,'end_frame':30,'direction':'left_to_right','zoom':'in'}],
         'music':{'status':'present','tracks':[{'path':'m.wav','sha256':'1'*64,'start_frame':0,'end_frame':30}],
                  'mix_evidence':{'path':'mix.json','sha256':'2'*64}}}
   with patch('ytvideos.media_checks.validate_font_face'), patch.object(m.delivery,'load_style',return_value={'font':'synthetic','font_index':0}):
    with self.assertRaisesRegex(ValueError,'at least 2 seconds'):m.production_preflight(plan,Path(td))
    m.delivery.channel_config.configure_pinned_profile(p,sha)
    requirements=m.production_preflight(plan,Path(td))
    self.assertNotIn('minimum_shot_seconds',requirements['video'])
    with self.assertRaisesRegex(ValueError,'identity'):m.delivery.channel_config.channel_profile('paper_detour')
    p.write_text('{"tampered":true}')
    with self.assertRaisesRegex(ValueError,'identity or bytes changed'):m.production_preflight(plan,Path(td))
    with self.assertRaisesRegex(ValueError,'bytes changed'):m.delivery.channel_config.configure_pinned_profile(p,sha)

 def test_actual_montage_subprocess_binds_and_rechecks_profile(self):
  profile=json.loads((ROOT/'channels/nuviko_history/channel.json').read_text())
  profile['production']['video'].pop('minimum_shot_seconds')
  fixture_font=os.environ.get('YTV_TEST_FONT')
  if fixture_font:
   from PIL import ImageFont
   family,style=ImageFont.truetype(fixture_font,16,index=0).getname()
   profile['production']['captions']['font']={'family':family,'style':style}
  with tempfile.TemporaryDirectory() as td:
   root=Path(td);p=root/'profile.json';raw=json.dumps(profile,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode();p.write_bytes(raw);sha=hashlib.sha256(raw).hexdigest()
   (root/'a.wav').write_bytes(b'synthetic fixture');(root/'s.png').write_bytes(b'synthetic fixture')
   plan={'channel':'nuviko_history','format':'short','audio':'a.wav','srt':'a.srt','subtitles':{'mode':'words'},'transitions':'direct_cuts',
         'scenes':[{'image':'s.png','start_frame':0,'end_frame':120,'direction':'left_to_right','zoom':'in'}],
         'music':{'status':'present','tracks':[{'path':'m.wav','sha256':'1'*64,'start_frame':0,'end_frame':120}],
                  'mix_evidence':{'path':'mix.json','sha256':'2'*64}}}
   if fixture_font:
    plan['font_override']={'path':fixture_font,'index':0}
   manifest=root/'manifest.json';manifest.write_text(json.dumps(plan))
   argv=[sys.executable,str(ROOT/'automation/ffmpeg_montage/montage.py'),str(manifest),'--output',str(root/'unused.mp4'),
         '--work-dir',str(root/'work'),'--plan-only','--pinned-profile',str(p),'--pinned-profile-sha256',sha]
   if fixture_font:
    wrong=json.loads(json.dumps(profile));wrong['production']['captions']['font']={'family':'not-the-fixture-font','style':'Bold'}
    wrong_raw=json.dumps(wrong,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode();wrong_path=root/'wrong-profile.json';wrong_path.write_bytes(wrong_raw)
    wrong_argv=argv.copy();wrong_argv[wrong_argv.index('--pinned-profile')+1]=str(wrong_path);wrong_argv[wrong_argv.index('--pinned-profile-sha256')+1]=hashlib.sha256(wrong_raw).hexdigest()
    wrong_result=subprocess.run(wrong_argv,capture_output=True,text=True,timeout=30)
    self.assertNotEqual(wrong_result.returncode,0);self.assertIn('font family/style differs',wrong_result.stderr)
    self.assertFalse((root/'work').exists())
   result=subprocess.run(argv,capture_output=True,text=True,timeout=30)
   self.assertEqual(result.returncode,0,result.stderr)
   self.assertTrue((root/'work'/'plan.json').is_file())
   p.write_text('{"tampered":true}');argv[argv.index('--work-dir')+1]=str(root/'second-work')
   bad=subprocess.run(argv,capture_output=True,text=True,timeout=30)
   self.assertNotEqual(bad.returncode,0);self.assertIn('profile bytes changed',bad.stderr)
   self.assertFalse((root/'second-work').exists())

if __name__=='__main__':unittest.main()
