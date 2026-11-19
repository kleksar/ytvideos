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
            geometry=dict(reference_width=1440,reference_height=2560,font_size_px=104,max_visible_width_px=1024,
                          center_x_ratio=0.4722222222222222,center_y_ratio=0.762),
            style=dict(font=str(path),font_index=2,text='#F4E8C8',highlight='#FFD166',outline='#18243A',
                       background=None,outline_width=3,pad_x=20,pad_y=12)))
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

    def history(self,path):
        plan,shots=self.data(path)
        plan['target']['raster']=[2560,1440]
        plan['style']=dict(channel='nuviko_history',format='long',font_face={'family':'Georgia','style':'Bold'},
                           geometry=dict(reference_width=2560,reference_height=1440,font_size_px=84,max_visible_width_px=1344,
                                         center_x_ratio=0.5,baseline_y_ratio=0.8944444444444445,bottom_y_ratio=0.925),
                           style=dict(font=str(path),font_index=0,text='#F3E9D5',
                               highlight='#FFD166',outline='#20252B',background='#20252BCC',pad_x=29,pad_y=17,outline_width=0))
        return plan,shots

    def test_history_preserves_case_and_panel_geometry_across_cuts(self):
        class Georgia(Font):
            def getname(self): return ('Georgia','Bold')
        with tempfile.TemporaryDirectory() as temp:
            path=Path(temp)/'font';path.write_bytes(b'synthetic')
            plan,shots=self.history(path)
            result=native_layout(plan,shots,'nuviko-history-long-native-v1',font_loader=lambda *a,**k:Georgia())
            first,next_shot=result['shots'][:2]
            self.assertEqual([node['text'] for node in first['nodes']],['New','York'])
            self.assertEqual([node['x'] for node in first['nodes']],[node['x'] for node in next_shot['nodes']])
            panel,second=first['panels'][0],next_shot['panels'][0]
            self.assertEqual(panel['x'],.5)
            self.assertEqual(panel['y'],1-(1193+135/2)/1440)
            self.assertEqual(panel['width'],(8*20+2*29)/2560)
            self.assertEqual(panel['height'],135/1440)
            self.assertEqual({k:v for k,v in panel.items() if k not in ('first','last')},
                             {k:v for k,v in second.items() if k not in ('first','last')})
            self.assertEqual((panel['first'],panel['last']),(0,3))
            self.assertEqual((second['first'],second['last']),(0,7))

    def test_history_rejects_panel_mismatch_and_overwide_phrase(self):
        class WideGeorgia(Font):
            def getname(self): return ('Georgia','Bold')
            def getlength(self,text): return len(text)*162
        with tempfile.TemporaryDirectory() as temp:
            path=Path(temp)/'font';path.write_bytes(b'synthetic')
            for key,value in (('background','#20252BFF'),('pad_x',20),('pad_y',5),('outline_width',1)):
                with self.subTest(key=key):
                    plan,shots=self.history(path)
                    plan['style']['style'][key]=value
                    with self.assertRaisesRegex(ValueError,'Active panel'):
                        native_layout(plan,shots,'nuviko-history-long-native-v1')
            plan,shots=self.history(path)
            with self.assertRaisesRegex(ValueError,'safe width'):
                native_layout(plan,shots,'nuviko-history-long-native-v1',font_loader=lambda *a,**k:WideGeorgia())

    def test_active_profile_geometry_and_style_drift_rejected_for_both_recipes(self):
        with tempfile.TemporaryDirectory() as temp:
            path=Path(temp)/'font';path.write_bytes(b'synthetic')
            for factory,recipe,fields in (
                (self.data,'paper-short-v09',('reference_width','center_x_ratio','center_y_ratio','max_visible_width_px')),
                (self.history,'nuviko-history-long-native-v1',('reference_height','center_x_ratio','baseline_y_ratio','bottom_y_ratio','max_visible_width_px')),
            ):
                for field in fields:
                    with self.subTest(recipe=recipe,field=field):
                        plan,shots=factory(path)
                        plan['style']['geometry'][field] += .01
                        with self.assertRaisesRegex(ValueError,'profile geometry differs'):
                            native_layout(plan,shots,recipe)
                for field in ('background','outline_width','pad_x','pad_y','font_index'):
                    with self.subTest(recipe=recipe,field=field):
                        plan,shots=factory(path)
                        del plan['style']['style'][field]
                        with self.assertRaisesRegex(ValueError,'Active panel'):
                            native_layout(plan,shots,recipe)

if __name__=='__main__':unittest.main()
