"""Guard the accepted reference's separate-block and truthful-route contracts."""
import json
import unittest
from pathlib import Path


class ApprovedEndscreenReferenceTests(unittest.TestCase):
    def setUp(self):
        root = Path(__file__).resolve().parents[1]
        self.pack = root / 'docs/reference-packs/ybw-approved-endscreen'
        self.data = json.loads((self.pack / 'manifest.json').read_text())

    def test_approved_asset_has_fixed_identity(self):
        self.assertEqual(self.data['status'], 'owner_approved')
        self.assertEqual(len(self.data['asset']['sha256']), 64)
        self.assertEqual(self.data['asset']['dimensions'], [1672, 941])
        self.assertIn('ImageGen', self.data['asset']['method'])
        self.assertTrue((self.pack / 'generation_prompt.txt').read_text().strip())

    def test_riddle_and_previous_card_are_distinct(self):
        block = self.data['last_block']
        self.assertEqual(block['seconds'] * block['fps'], block['frames'])
        self.assertEqual(block['frames'], 300)
        self.assertTrue(block['separate_from_future_riddle'])
        self.assertFalse(self.data['real_card_baked'])
        self.assertEqual(self.data['future_riddle_template_status'], 'not_approved_by_this_acceptance')

    def test_route_does_not_invent_previous_mind_episode(self):
        self.assertEqual(self.data['previous_story_mapping'], {
            'mind': None, 'everyone': 'mind', 'teleportation': 'everyone',
            'three_wishes': 'teleportation', 'rewind': 'three_wishes',
        })

    def test_card_safe_rectangle_is_inside_canvas_and_widescreen(self):
        x, y, width, height = self.data['card_safe_rect_source_xywh']
        self.assertGreaterEqual(min(x, y), 0)
        self.assertLessEqual(x + width, 1672)
        self.assertLessEqual(y + height, 941)
        self.assertAlmostEqual(width / height, 16 / 9)
