import importlib.util
import tempfile
import unittest
from pathlib import Path

path=Path(__file__).resolve().parents[1]/'scripts/animate_paper_captions.py'
spec=importlib.util.spec_from_file_location('animate_paper',path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

class AccentMotionTests(unittest.TestCase):
 def test_reading_hold_cannot_be_shortened_by_fades(self):
  self.assertEqual(m.keyframes(12,78,4,30),[12,16,73,77])
  with self.assertRaises(ValueError):m.keyframes(12,30,4,30)
 def test_moving_alpha_bounds_and_asset_identity_are_enforced(self):
  with tempfile.TemporaryDirectory() as tmp:
   root=Path(tmp);png=root/'cue.png';png.write_bytes(b'asset')
   cue={'id':'C1','png':'cue.png','png_sha256':m.digest(png),'lines':['TEXT'],'metrics':{'size_px':[200,100],'alpha_bbox':[0,0,200,100]}}
   pair={'cue':'C1','anchor':'primary','comparisons':[{'anchor':'primary','checks':{'technical':'PASS'},'layer_top_left_px':[400,300]}]}
   prepared={'canvas':[1080,1920],'cues':[cue],'pairs':[pair]};video={'avg_frame_rate':'30/1','r_frame_rate':'30/1','nb_frames':'120','width':540,'height':960};config={'motion':{'rise_canvas_fraction':.02,'transition_frames':4},'intervals':[{'cue':'C1','start_frame':12,'end_frame':78}]}
   plan=m.build_plan(config,prepared,video,root);self.assertEqual(plan['cues'][0]['y'],150)
   pair['comparisons'][0]['layer_top_left_px']=[400,0]
   with self.assertRaises(ValueError):m.build_plan(config,prepared,video,root)
   pair['comparisons'][0]['layer_top_left_px']=[400,300];png.write_bytes(b'changed')
   with self.assertRaises(ValueError):m.build_plan(config,prepared,video,root)
 def test_interval_beyond_media_is_rejected(self):
  with self.assertRaises(ValueError):m.build_plan({'motion':{'rise_canvas_fraction':.02,'transition_frames':4},'intervals':[{'cue':'C1','start_frame':12,'end_frame':121}]},{'canvas':[1080,1920],'cues':[],'pairs':[]},{'avg_frame_rate':'30/1','r_frame_rate':'30/1','nb_frames':'120','width':540,'height':960},Path('.'))

if __name__=='__main__':unittest.main()
