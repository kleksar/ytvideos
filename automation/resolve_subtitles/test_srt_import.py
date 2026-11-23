"""Synthetic transport tests: these do not establish live Resolve behavior."""
from copy import deepcopy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import layout
import srt_import
from test_srt_plan import SRT

class Font:
    def __init__(self, family): self.family=family
    def getname(self): return (self.family,'Bold')
    def getlength(self,text): return len(text)*20

class Client:
    def __init__(self,timeout): pass
    def close(self): pass

class DirectImportTests(unittest.TestCase):
    def run_profile(self, name, expected_orientation):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); src=root/'speech.srt'; src.write_text(SRT)
            template=json.loads((Path(__file__).parent/'templates'/f'{name}.json').read_text())
            font=root/'font';font.write_bytes(b'synthetic font')
            template['style']['style']['font']=str(font)
            file=root/'template.json';file.write_text(json.dumps(template))
            width,height=template['recipe']['raster']
            observed=dict(project_id='project-exact',timeline_id='timeline-exact',fps_observed='30',
                width_observed=str(width),height_observed=str(height),origin_frame=100,end_frame=300)
            snap=dict(video_track_state={'1':True},picture=[[['clip',100,300,0,0,True,{},'media']]],
                      timecode='00:00:00:00',page='edit')
            calls=[]
            def call(_client, expression, branded=False):
                if expression.startswith('discover_current'): return observed
                if expression.startswith('snapshot'): return deepcopy(snap)
                calls.append(expression)
                return dict(status='CREATED' if len(calls)==1 else 'UNCHANGED',native_cues=0)
            def render(plan,shots,recipe_id,**kwargs):
                return layout.native_layout(plan,shots,recipe_id,font_loader=lambda *a,**kw:Font(template['recipe']['font']['family']),**kwargs)
            with patch.object(srt_import,'ResolveMCP',Client), patch.object(srt_import,'script_call',side_effect=call), patch.object(srt_import,'native_layout',side_effect=render):
                a=srt_import.install_srt(src,file,root/'out')
                b=srt_import.install_srt(src,file,root/'out')
            self.assertEqual((a['status'],b['status']),('CREATED','UNCHANGED'))
            self.assertEqual(a['orientation'],expected_orientation)
            self.assertEqual(calls[0],calls[1])
            self.assertEqual(src.read_text(),SRT)
            result=json.loads((root/'out'/'native-layout.json').read_text())
            self.assertTrue(all(node['active_first'] is None for shot in result['shots'] for node in shot['nodes']))
            self.assertNotIn('ImportMedia',calls[0])

    def test_portrait_and_landscape_templates_share_timing(self):
        self.run_profile('paper-short-v09','portrait')
        self.run_profile('nuviko-history-long-native-v1','landscape')

    def test_missing_carrier_fails_before_native_install(self):
        from srt_plan import choose_carriers,plan_srt
        cues=plan_srt(SRT,dict(fps='30',origin_frame=100,end_frame=300))['cues']
        for picture in ([], [[['x',100,125,0,0,True,{},'m']]], [[['x',100,300,0,0,False,{},'m']]]):
            with self.assertRaisesRegex(ValueError,'covers'):
                choose_carriers(dict(picture=picture,video_track_state={'1':True}),cues)

if __name__ == '__main__': unittest.main()
