import importlib.util
import shutil
import subprocess
import tempfile
import unittest
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
                        ({'scale':1.10,'center':[.48,.5]}, {'scale':1.10,'center':[.52,.5]})):
                n=5; result=render(montage.camera_filter(160,90,n,{'start':a,'end':b}),n)
                self.assertEqual(len(result), n*size)
                for i in range(n):
                    u=i/(n-1)
                    k={'scale':a['scale']+(b['scale']-a['scale'])*u,
                       'center':[x+(y-x)*u for x,y in zip(a['center'],b['center'])]}
                    expected=render(montage.camera_filter(160,90,2,{'start':k,'end':k}),1)
                    self.assertEqual(result[i*size:(i+1)*size],expected,(a,b,i))
                self.assertNotEqual(result[:size], result[size:2*size])
                self.assertNotEqual(result[-size:], result[-2*size:-size])

if __name__ == '__main__':
    unittest.main()
