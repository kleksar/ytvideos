import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from PIL import Image

SCRIPT = Path(__file__).parents[1] / 'scripts' / 'thumbnail_previews.py'


class ThumbnailPreviewCardTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.main = self.root / 'main.jpg'
        self.neighbor = self.root / 'neighbor.jpg'
        Image.new('RGB', (320, 180), 'red').save(self.main)
        Image.new('RGB', (200, 200), 'blue').save(self.neighbor)

    def tearDown(self):
        self.tmp.cleanup()

    def run_cli(self, *args):
        return subprocess.run([sys.executable, str(SCRIPT), str(self.main), *map(str, args)],
                              capture_output=True, text=True)

    def test_legacy_crop_and_manifest_remain_available(self):
        out = self.root / 'legacy'
        result = self.run_cli('--out', out, '--widths', '100', '--crops', '2:3')
        self.assertEqual(result.returncode, 0, result.stderr)
        manifest = json.loads((out / 'manifest.json').read_text())
        self.assertEqual(len(manifest['previews']), 2)
        self.assertTrue((out / 'qa_full_100x56.jpg').is_file())

    def test_exact_escaped_fields_relative_neighbor_and_provenance(self):
        spec = self.root / 'card.json'
        spec.write_text(json.dumps({
            'title': 'Primary <exact> & title', 'channel': 'Ch <one>', 'duration': '12:34',
            'metadata': {'views': '1,234 views'},
            'neighbors': [{'image': 'neighbor.jpg', 'title': 'Neighbor "two"',
                           'channel': 'Other', 'duration': '1:02'}]}, ensure_ascii=False))
        out = self.root / 'mock'
        result = self.run_cli('--out', out, '--widths', '100', '--crops', '2:3', '--card-json', spec)
        self.assertEqual(result.returncode, 0, result.stderr)
        page = (out / 'qa_cards.html').read_text()
        self.assertIn('Primary &lt;exact&gt; &amp; title', page)
        self.assertIn('Ch &lt;one&gt;', page)
        self.assertIn('1,234 views', page)
        self.assertIn('neighbor.jpg', page)
        self.assertIn(hashlib.sha256(self.neighbor.read_bytes()).hexdigest(), page)
        self.assertIn('Dark theme · LOCAL MOCK', page)
        self.assertNotIn('http://', page)
        self.assertIn('section class="theme-light" style="background:#fff;color:#0f0f0f;', page)
        self.assertIn('section class="theme-dark" style="background:#181818;color:#f1f1f1;', page)
        self.assertEqual(page.count('<body>'), 1)
        manifest = json.loads((out / 'manifest.json').read_text())
        self.assertEqual(manifest['card_mock']['json_sha256'], hashlib.sha256(spec.read_bytes()).hexdigest())
        self.assertEqual(len(manifest['card_mock']['assets']), 2)

    def test_invalid_duration_fails_without_changing_source(self):
        before = self.main.read_bytes()
        spec = self.root / 'bad.json'
        spec.write_text(json.dumps({'title': 'x', 'channel': 'y', 'duration': '3:99'}))
        result = self.run_cli('--out', self.root / 'bad-out', '--card-json', spec)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.main.read_bytes(), before)
        self.assertFalse((self.root / 'bad-out' / 'qa_cards.html').exists())

    def test_invalid_metadata_schema_fails_before_any_output(self):
        for invalid in ({'metadata': {'views': 123}}, {'metadata': {'viewz': '123'}},
                        {'neighbors': {}}, {'neighbors': None}, {'duration': None}):
            with self.subTest(invalid=invalid):
                spec = self.root / 'bad-meta.json'
                spec.write_text(json.dumps({'title': 'x', 'channel': 'y', **invalid}))
                out = self.root / 'bad-meta-out'
                result = self.run_cli('--out', out, '--card-json', spec)
                self.assertNotEqual(result.returncode, 0)
                self.assertNotIn('Traceback', result.stderr)
                self.assertFalse(out.exists())

    def test_invalid_regions_fail_before_writing_card(self):
        spec = self.root / 'card.json'
        spec.write_text(json.dumps({'title': 'x', 'channel': 'y'}))
        for region in ({'box': [0, 0, 1, 1]}, {'label': 'subject', 'box': ['0', 0, 1, 1]}):
            with self.subTest(region=region):
                regions = self.root / 'regions.json'
                regions.write_text(json.dumps({'regions': [region]}))
                out = self.root / 'bad-regions-out'
                result = self.run_cli('--out', out, '--card-json', spec, '--regions', regions)
                self.assertNotEqual(result.returncode, 0)
                self.assertNotIn('Traceback', result.stderr)
                self.assertFalse(out.exists())

    def test_neighbor_asset_output_collision_is_rejected_before_writes(self):
        out = self.root / 'collision'
        out.mkdir()
        conflicting_asset = out / 'qa_full_100x56.jpg'
        Image.new('RGB', (320, 180), 'green').save(conflicting_asset)
        original = conflicting_asset.read_bytes()
        spec = self.root / 'collision.json'
        spec.write_text(json.dumps({'title': 'x', 'channel': 'y', 'neighbors': [
            {'image': 'collision/qa_full_100x56.jpg', 'title': 'n', 'channel': 'c'}]}))
        result = self.run_cli('--out', out, '--widths', '100', '--crops', '2:3', '--card-json', spec)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(conflicting_asset.read_bytes(), original)
        self.assertFalse((out / 'qa_cards.html').exists())
        self.assertFalse((out / 'manifest.json').exists())


if __name__ == '__main__':
    unittest.main()
