import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from test_montage import m


class PortableProfileTests(unittest.TestCase):
    def test_new_registered_channel_can_reuse_an_explicit_visual_profile(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            config = root/'channels'/'custom'
            config.mkdir(parents=True)
            (config/'channel.json').write_text(json.dumps({'schema_version': 1, 'id': 'custom',
                'visual_profile': 'paper', 'voice': {'speed': 1.15}, 'release_policy': {'end_screen': True}}))
            (root/'audio.m4a').write_bytes(b'fixture identity')
            (root/'scene.png').write_bytes(b'fixture identity')
            plan = {'channel': 'custom', 'format': 'short', 'audio': 'audio.m4a',
                    'subtitles': {'mode': 'none'}, 'scenes': [{'image': 'scene.png',
                    'start_frame': 0, 'end_frame': 120, 'direction': 'left_to_right', 'zoom': 'in'}]}
            with patch.object(m.delivery.channel_config, 'ROOT', root):
                self.assertEqual(m.validate(plan, root)['channel'], 'custom')
                self.assertEqual(m.delivery.profile_paths('custom', 'short')[0].name, 'paper.json')

    def test_canonical_channel_id_uses_registered_visual_profile(self):
        self.assertEqual(m.delivery.profile_paths('paper_detour', 'short'), m.delivery.profile_paths('paper', 'short'))
        self.assertEqual(m.delivery.protected_channel('UCMVfdfaNxV3ZkI3_J3Eejzw'), 'paper_detour')
        self.assertTrue(m.delivery.same_channel('paper', 'paper_detour'))

    def test_new_channel_requires_configured_profile_without_silent_fallback(self):
        with self.assertRaisesRegex(ValueError, 'No montage visual profile configured'):
            m.delivery.profile_paths('scenes_on_repeat', 'short')
        with self.assertRaises((ValueError, FileNotFoundError)):
            m.delivery.profile_paths('unregistered', 'short')

    def test_explicit_override_is_recorded_and_missing_override_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            plan = {'channel': 'paper_detour', 'format': 'short',
                    'font_override': {'path': '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 'index': 0}}
            if not Path(plan['font_override']['path']).exists():
                self.skipTest('Explicit Linux fixture unavailable')
            profile = m.delivery.load_style(plan, Path(directory))
            self.assertEqual(profile['font'], plan['font_override']['path'])
            self.assertEqual(profile['font_index'], 0)
            plan['font_override']['index'] = True
            with self.assertRaises(ValueError):
                m.delivery.load_style(plan, Path(directory))
            plan['font_override'] = {'path': 'missing.ttf', 'index': 0}
            with self.assertRaisesRegex(ValueError, 'existing'):
                m.delivery.load_style(plan, Path(directory))

    def test_approved_font_is_not_silently_replaced_on_other_host(self):
        with patch.dict(os.environ, {}, clear=True):
            if Path('/System/Library/Fonts/Supplemental/ChalkboardSE.ttc').exists():
                self.skipTest('Host has the actual approved font')
            with self.assertRaisesRegex(ValueError, 'Approved profile font is unavailable'):
                m.delivery.load_style({'channel': 'paper', 'format': 'short'}, Path('.'))


if __name__ == '__main__':
    unittest.main()
