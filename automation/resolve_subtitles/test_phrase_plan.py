import copy
import sys
from pathlib import Path
import tempfile
import unittest
sys.path.insert(0, str(Path(__file__).parent))
from phrase_plan import RECIPE, STYLE, phrase_layout, write_comps


def fixture():
    panel = dict(center=[0.5, 0.19212962962962965], width=0.5, height=69/1080,
                 color=[32/255,37/255,43/255,0.8])
    return dict(target=dict(origin_frame=0,end_frame=38,raster=[608,1080]),
                native_titles=dict(recipe_id=RECIPE,style=copy.deepcopy(STYLE),
                display_evidence=dict(kind='approved_display_intervals',source='synthetic fixture'),
                display_clips=[dict(start_frame=0,end_frame=38,text='One phrase',panel=panel,width_review='native_verified')]))


class PhrasePlanTests(unittest.TestCase):
    def test_whole_phrase_not_word_split_and_sanitized_comp(self):
        request=fixture()
        rows=phrase_layout(request)
        self.assertEqual(len(rows),1)
        self.assertEqual(rows[0]['text'],'One phrase')
        with tempfile.TemporaryDirectory() as folder:
            path=write_comps(rows,folder)[0]
            value=Path(path).read_text()
            self.assertIn('GlobalEnd = 37',value)
            self.assertIn('Value = "One phrase"',value)
            self.assertNotIn('/Users/',value)
            self.assertNotIn('__TEXT__',value)

    def test_no_global_font_size_or_color_override(self):
        for key,value in [('size',STYLE['size']*.85),('color',[1,0,0,1]),('font','Arial')]:
            request=fixture()
            request['native_titles']['style'][key]=value
            with self.subTest(key=key), self.assertRaisesRegex(ValueError,'style'):
                phrase_layout(request)

    def test_unsupported_profile_and_unverified_width_fail(self):
        request=fixture()
        request['target']['raster']=[1920,1080]
        with self.assertRaisesRegex(ValueError,'calibrated'):
            phrase_layout(request)
        request=fixture()
        request['native_titles']['display_clips'][0]['width_review']='guessed'
        with self.assertRaisesRegex(ValueError,'width'):
            phrase_layout(request)

    def test_no_gap_or_fractional_timing_or_panel_drift(self):
        for a,b in [(1,38),(0,37),(0,38.0),(0,0)]:
            request=fixture()
            row=request['native_titles']['display_clips'][0]
            row.update(start_frame=a,end_frame=b)
            with self.subTest(a=a,b=b), self.assertRaises(ValueError):
                phrase_layout(request)
        request=fixture()
        request['native_titles']['display_clips'][0]['panel']['height']=.5
        with self.assertRaisesRegex(ValueError,'Panel'):
            phrase_layout(request)

if __name__=='__main__':
    unittest.main()
