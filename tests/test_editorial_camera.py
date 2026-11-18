import importlib.util
import shutil
import subprocess
import tempfile
import unittest
from unittest.mock import patch
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]

def load(name, path):
    spec = importlib.util.spec_from_file_location(name, ROOT / path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

clock = load('camera_clock_test', 'automation/helpers/camera_motion.py')
montage = load('camera_montage_test', 'automation/ffmpeg_montage/montage.py')

class EditorialCameraTests(unittest.TestCase):
    def test_linear_full_interval_without_edge_holds(self):
        for n in (2, 5, 120, 301):
            p = [clock.progress(i, n) for i in range(n)]
            self.assertEqual((p[0], p[-1]), (0, 1))
            for a, b in zip(p, p[1:]):
                self.assertAlmostEqual(b-a, 1/(n-1), places=12)
        for n in (0, 1, True):
            with self.assertRaises(ValueError):
                clock.expression(n)

    def test_scene_cache_identity_changes_with_shared_clock(self):
        with patch.object(montage.subprocess, 'check_output', return_value='ffmpeg test'):
            with patch.object(montage.delivery, 'sha256', side_effect=lambda p: 'clock-v1' if p.name=='camera_motion.py' else 'same'):
                a=montage.scene_engine_identity()
            with patch.object(montage.delivery, 'sha256', side_effect=lambda p: 'clock-v2' if p.name=='camera_motion.py' else 'same'):
                b=montage.scene_engine_identity()
        self.assertNotEqual(a,b)
        self.assertEqual(a['montage'],b['montage'])

    @unittest.skipUnless(shutil.which('ffmpeg'), 'FFmpeg required for pixel sampling regression')
    def test_perspective_all_frames_equal_independent_static_linear_reference(self):
        # Frame-exact FFmpeg sampling, not merely a string containing "linear".
        # Fails old on/(N-1), easing, or shortened edge-hold timelines.
        with tempfile.TemporaryDirectory() as td:
            image = Path(td)/'grid.png'
            im = Image.new('RGB', (160, 90), '#253850'); d = ImageDraw.Draw(im)
            for x in range(8, 153, 13):
                d.line((x, 0, x, 89), fill='#f4db91', width=2)
            for y in range(7, 85, 11):
                d.line((0, y, 159, y), fill='#e96032', width=2)
            im.save(image)
            def render(vf, count):
                return subprocess.check_output(['ffmpeg','-v','error','-threads','1','-filter_threads','1',
                    '-loop','1','-framerate','30','-i',str(image),'-vf',vf,'-frames:v',str(count),
                    '-f','rawvideo','-pix_fmt','yuv420p','pipe:1'])
            size = 160*90*3//2
            for a,b in (({'scale':1.0,'center':[.5,.5]}, {'scale':1.08,'center':[.5,.5]}),
                        ({'scale':1.08,'center':[.5,.5]}, {'scale':1.0,'center':[.5,.5]}),
                        ({'scale':1.10,'center':[.48,.5]}, {'scale':1.10,'center':[.52,.5]}),
                        ({'scale':1.05,'center':[.49,.5]}, {'scale':1.15,'center':[.52,.51]})):
                n=5; result=render(montage.camera_filter(160,90,n,{'start':a,'end':b}),n)
                self.assertEqual(len(result), n*size)
                for i in range(n):
                    u=i/(n-1)
                    k={'scale':a['scale']+(b['scale']-a['scale'])*u,
                       'center':[(x*a['scale']+(y*b['scale']-x*a['scale'])*u)/(a['scale']+(b['scale']-a['scale'])*u) for x,y in zip(a['center'],b['center'])]}
                    expected=render(montage.camera_filter(160,90,2,{'start':k,'end':k}),1)
                    self.assertEqual(result[i*size:(i+1)*size],expected,(a,b,i))
                self.assertNotEqual(result[:size], result[size:2*size])
                self.assertNotEqual(result[-size:], result[-2*size:-size])

            # Legacy source-perspective endpoints must become linear visible
            # affine motion, not reciprocal zoom between endpoints.
            for direction, zoom in (('none','in'),('none','out'),('left_to_right','in')):
                w,h,n=160,90,5; sw,sh=176,100
                result=render(montage.motion_filter(w,h,n,direction,zoom),n)
                es=(26*w/1920,2*w/1920) if zoom=='in' else (2*w/1920,26*w/1920)
                ex=21.708*w/1920; xs=(ex,-ex) if direction=='left_to_right' else (0,0)
                zs=[sw/(sw+2*e) for e in es]
                ls=[(e-x)*z for e,x,z in zip(es,xs,zs)]
                ts=[e*sh/sw*z for e,z in zip(es,zs)]
                for i in range(n):
                    u=i/(n-1); z=zs[0]+(zs[1]-zs[0])*u
                    left=ls[0]+(ls[1]-ls[0])*u; top=ts[0]+(ts[1]-ts[0])*u
                    vf=(f'scale={sw}:{sh}:force_original_aspect_ratio=increase:flags=lanczos,crop={sw}:{sh},'
                        f"perspective=sense=destination:x0='{left}':y0='{top}':x1='{left}+W*{z}':y1='{top}':"
                        f"x2='{left}':y2='{top}+H*{z}':x3='{left}+W*{z}':y3='{top}+H*{z}':"
                        f'interpolation=cubic:eval=frame,crop={w}:{h}:8:5,setsar=1,format=yuv420p')
                    expected=render(vf,1)
                    self.assertEqual(result[i*size:(i+1)*size],expected,(direction,zoom,i))

if __name__ == '__main__':
    unittest.main()
