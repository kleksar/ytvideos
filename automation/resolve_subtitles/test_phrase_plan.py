import copy
import sys
from pathlib import Path
import tempfile
import unittest
sys.path.insert(0, str(Path(__file__).parent))
from phrase_plan import RECIPE, STYLE, phrase_layout, write_comps


def bind_words(request):
    rows=request["native_titles"]["display_clips"]
    words=[]
    groups=[]
    for row in rows:
        indexes=[]
        for token in row["text"].split():
            indexes.append(len(words))
            words.append(dict(text=token,placement_id="vo"))
        groups.append(indexes)
    request["words"]=words
    request["native_titles"]["groups"]=groups
    return request


def fixture():
    panel = dict(center=[0.5, 0.19212962962962965], width=0.5, height=69/1080,
                 color=[32/255,37/255,43/255,0.8])
    return bind_words(dict(target=dict(origin_frame=0,end_frame=38,raster=[608,1080]),
                native_titles=dict(locale='en',recipe_id=RECIPE,style=copy.deepcopy(STYLE),
                display_evidence=dict(kind='approved_display_intervals',source='synthetic fixture'),
                display_clips=[dict(start_frame=0,end_frame=38,text='One phrase',panel=panel,width_review='native_verified')])))


class PhrasePlanTests(unittest.TestCase):
    def test_russian_preposition_preflight_does_not_rewrite_cc(self):
        request=fixture()
        request['native_titles']['locale']='ru-RU'
        row=request['native_titles']['display_clips'][0]
        row.update(text='шли мимо с',end_frame=20)
        request['native_titles']['display_clips'].append(dict(row,start_frame=20,end_frame=38,text='Дмитрием'))
        bind_words(request)
        before=copy.deepcopy(request)
        with self.assertRaisesRegex(ValueError,'preposition'):
            phrase_layout(request)
        self.assertEqual(request,before)
        row['text']='шли мимо'
        request['native_titles']['display_clips'][1]['text']='с Дмитрием'
        bind_words(request)
        self.assertEqual(len(phrase_layout(request)),2)
        for text in ('буква «с».', 'с!', 'мимо'):
            row['text']=text
            bind_words(request)
            self.assertEqual(len(phrase_layout(request)),2)
        row['text']='шли мимо с,'
        with self.assertRaisesRegex(ValueError,'preposition'):
            phrase_layout(request)
        request['native_titles']['locale']='en'
        bind_words(request)
        self.assertEqual(len(phrase_layout(request)),2)

    def test_display_groups_preserve_protected_tokens_and_exact_text(self):
        request=fixture()
        request['keep_together']=[[0,1]]
        row=request['native_titles']['display_clips'][0]
        row.update(text='One',end_frame=20)
        request['native_titles']['display_clips'].append(dict(row,start_frame=20,end_frame=38,text='phrase'))
        request['native_titles']['groups']=[[0],[1]]
        with self.assertRaisesRegex(ValueError,'protected'):
            phrase_layout(request)
        request['keep_together']=[]
        self.assertEqual(len(phrase_layout(request)),2)
        row['text']='Invented'
        with self.assertRaisesRegex(ValueError,'exactly match'):
            phrase_layout(request)
        request=fixture()
        request['native_titles'].pop('groups')
        with self.assertRaisesRegex(ValueError,'grouping'):
            phrase_layout(request)

    def test_reviewed_imperative_vocative_pairs_not_name_heuristic(self):
        request=fixture()
        row=request['native_titles']['display_clips'][0]
        row.update(text='Пойдём, Татьяна',end_frame=20)
        request['native_titles']['display_clips'].append(dict(row,start_frame=20,end_frame=38,text='Пойдём, Дмитрий'))
        request['native_titles']['locale']='ru'
        bind_words(request)
        request['keep_together']=[[0,1],[2,3]]
        self.assertEqual(len(phrase_layout(request)),2)
        request['native_titles']['groups']=[[0],[1],[2],[3]]
        with self.assertRaisesRegex(ValueError,'protected'):
            phrase_layout(request)

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
