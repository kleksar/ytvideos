from copy import deepcopy
from pathlib import Path
import tempfile
import unittest
from layout import native_layout
from test_partition import fixture

class Font:
    def getname(self):return ('Chalkboard SE','Bold')
    def getlength(self,text):return len(text)*20

class LayoutTests(unittest.TestCase):
    def data(self,path):
        cues,shots=fixture()
        plan=dict(target={'raster':[1440,2560]},conform_sha256='a'*64,cues=cues,style=dict(
            channel='paper_detour',format='short',font_face={'family':'Chalkboard SE','style':'Bold'},
            geometry={'font_size_px':104},style={'font':str(path),'font_index':2,'text':'#F4E8C8','highlight':'#FFD166','outline':'#18243A'}))
        return plan,shots
    def test_phrase_carries_geometry_but_only_speech_is_highlighted(self):
        with tempfile.TemporaryDirectory() as temp:
            path=Path(temp)/'font';path.write_bytes(b'synthetic font fixture')
            plan,shots=self.data(path);prior=deepcopy(plan)
            result=native_layout(plan,shots,'paper-short-v09',font_loader=lambda *a,**k:Font())
            self.assertEqual(plan,prior)
            first=result['shots'][0]['nodes'];nextshot=result['shots'][1]['nodes']
            self.assertEqual(first[0]['text'],'NEW')
            self.assertEqual(first[0]['x'],nextshot[0]['x'])
            self.assertEqual((first[0]['active_first'],first[0]['active_last']),(1,3))
            hold=result['shots'][3]['nodes']
            self.assertTrue(all(n['active_first'] is None for n in hold))
            self.assertEqual(result['visual'],'UNVERIFIED')
    def test_no_font_or_channel_fallback(self):
        with tempfile.TemporaryDirectory() as temp:
            path=Path(temp)/'font';path.write_bytes(b'synthetic')
            plan,shots=self.data(path)
            with self.assertRaisesRegex(ValueError,'No calibrated'):
                native_layout(plan,shots,'nuviko-guessed')
            plan['style']['channel']='nuviko_history'
            with self.assertRaisesRegex(ValueError,'differs'):
                native_layout(plan,shots,'paper-short-v09')
            plan['style']['channel']='paper_detour';path.unlink()
            with self.assertRaisesRegex(ValueError,'font file'):
                native_layout(plan,shots,'paper-short-v09')
    def test_long_phrase_is_rejected_not_squeezed(self):
        with tempfile.TemporaryDirectory() as temp:
            path=Path(temp)/'font';path.write_bytes(b'synthetic')
            plan,shots=self.data(path)
            class Wide(Font):
                def getlength(self,text):return len(text)*400
            with self.assertRaisesRegex(ValueError,'safe width'):
                native_layout(plan,shots,'paper-short-v09',font_loader=lambda *a,**k:Wide())

if __name__=='__main__':unittest.main()
