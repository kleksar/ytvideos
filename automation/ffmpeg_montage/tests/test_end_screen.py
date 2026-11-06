import importlib.util, tempfile, unittest
from pathlib import Path

P = Path(__file__).resolve().parents[1] / "montage.py"
spec = importlib.util.spec_from_file_location("montage_end_screen", P)
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)

class EndScreenTest(unittest.TestCase):
 def test_scope_and_duration(self):
  with tempfile.TemporaryDirectory() as td:
   b=Path(td); (b/"audio").touch(); (b/"image").touch()
   def plan(channel, form, duration=300, role="end_screen", final=True):
    scenes=[{"image":"image","start_frame":0,"end_frame":150,"direction":"left_to_right","zoom":"none"}, {"image":"image","start_frame":150,"end_frame":150+duration,"direction":"none","zoom":"none","role":role}]
    if not final: scenes.append({"image":"image","start_frame":150+duration,"end_frame":300+duration,"direction":"right_to_left","zoom":"none"})
    return {"channel":channel,"format":form,"audio":"audio","scenes":scenes,"subtitles":{"mode":"none"}}
   for channel in ("paper", "nuviko"):
    self.assertEqual(m.validate(plan(channel,"long"),b)["frames"],450)
    for kwargs in ({"form":"short"},{"form":"long","duration":299},{"form":"long","role":"scene"},{"form":"long","final":False}):
     with self.subTest(channel=channel, **kwargs), self.assertRaises(ValueError): m.validate(plan(channel,**kwargs),b)

if __name__ == "__main__": unittest.main()
