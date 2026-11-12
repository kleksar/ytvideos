import json, tempfile, unittest
from pathlib import Path
from unittest.mock import patch
import assemble_history_short as mod

class ShortManifestTests(unittest.TestCase):
 def setUp(self):
  self.temp=tempfile.TemporaryDirectory();self.root=Path(self.temp.name);(self.root/'Edit/Shorts').mkdir(parents=True)
  def asset(name,data):
   p=self.root/name;p.write_bytes(data);return {'path':str(p),'sha256':mod.sha(p)}
  self.voice=asset('voice.wav',b'voice');self.captions=asset('captions.mov',b'mov')
  self.srt=asset('captions.srt',b'1\n00:00:00,000 --> 00:00:00,900\nHello\n')
  one=asset('one.png',b'one');two=asset('two.png',b'two')
  self.m={'status':'ready','timeline':'test_short','frames':30,'fps':30,'voice_speed_applied':1.05,
          'voice':self.voice,'captions':self.captions,'srt':self.srt,
          'scenes':[{**one,'start':0,'end':15,'cue':'One'},{**two,'start':15,'end':30,'cue':'Two'}]}
  self.path=self.root/'Edit/Shorts/01_manifest.json'
  self.patcher=patch.object(mod,'probe',side_effect=self.probe);self.patcher.start()
 def tearDown(self):self.patcher.stop();self.temp.cleanup()
 def probe(self,p):
  if p.suffix=='.wav':return {'streams':[{'codec_type':'audio','codec_name':'pcm_s16le','duration':'1'}]}
  if p.suffix=='.mov':return {'streams':[{'codec_type':'video','width':1080,'height':1920,'nb_frames':'30','pix_fmt':'yuva444p12le'}]}
  return {'streams':[{'codec_type':'video','width':900,'height':1600}]}
 def save(self):self.path.write_text(json.dumps(self.m))
 def test_valid_draft(self):
  self.save();m,receipt=mod.validate(self.path,self.root);self.assertEqual(m['frames'],30);self.assertFalse(receipt.exists())
 def test_rejects_gap(self):
  self.m['scenes'][1]['start']=16;self.save()
  with self.assertRaises(ValueError):mod.validate(self.path,self.root)
 def test_rejects_changed_asset(self):
  self.save();Path(self.voice['path']).write_bytes(b'tampered')
  with self.assertRaises(ValueError):mod.validate(self.path,self.root)
 def test_rejects_duplicate_scene_content(self):
  self.m['scenes'][1].update(self.m['scenes'][0]);self.m['scenes'][1].update(start=15,end=30);self.save()
  with self.assertRaises(ValueError):mod.validate(self.path,self.root)
 def test_rejects_prior_receipt(self):
  self.save();self.path.with_name(self.path.stem+'_palmier_receipt.json').write_text('{}')
  with self.assertRaises(ValueError):mod.validate(self.path,self.root)
 def test_rejects_caption_outside_audio(self):
  Path(self.srt['path']).write_text('1\n00:00:00,000 --> 00:00:01,500\nHello\n');self.srt['sha256']=mod.sha(Path(self.srt['path']));self.save()
  with self.assertRaises(ValueError):mod.validate(self.path,self.root)
if __name__=='__main__':unittest.main()
