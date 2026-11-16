import contextlib
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import tts


class GenericChannelTests(unittest.TestCase):
    def test_paid_flag_cannot_hide_behind_argparse_abbreviation(self):
        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            tts.arguments(['--channel', 'paper_detour', '--output-dir', '/tmp/example', '--gen'])

    def test_scenes_and_paper_use_their_selected_voices(self):
        self.assertEqual(tts.channel_voice('scenes_on_repeat'), 'K60rGfHNsqGiO3nscQV3')
        self.assertEqual(tts.channel_voice('paper_detour'), 'ktkP7Nsj67dw2zcplQYt')
        parsed = tts.arguments(['--channel', 'scenes_on_repeat', '--output-dir', '/tmp/example'])
        self.assertEqual(parsed.channel, 'scenes_on_repeat')

    def test_arbitrary_configured_channel_is_discovered(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for index in range(10):
                folder = root / 'channels' / f'channel_{index}'
                folder.mkdir(parents=True)
                (folder / 'channel.json').write_text(json.dumps({'schema_version': 1, 'id': f'channel_{index}',
                    'voice': {'provider': 'elevenlabs', 'id': 'sharedvoice'}}))
            with patch.object(tts.channel_config, 'ROOT', root):
                self.assertEqual(len(tts.channel_config.configured_channels()), 10)
                self.assertEqual(tts.channel_voice('channel_9'), 'sharedvoice')
                self.assertEqual(tts.channel_voice('channel_0'), tts.channel_voice('channel_9'))
                self.assertEqual(tts.arguments(['--channel', 'channel_9', '--output-dir', str(root/'out')]).channel, 'channel_9')

    def test_unconfigured_or_invalid_voice_stops_before_network(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            channel = root/'channels'/'custom'
            channel.mkdir(parents=True)
            for voice in ({}, {'provider': 'other', 'id': 'voice'}, {'provider': 'elevenlabs', 'id': '../bad'}):
                (channel/'channel.json').write_text(json.dumps({'schema_version': 1, 'id': 'custom', 'voice': voice}))
                with patch.object(tts.channel_config, 'ROOT', root), patch('tts.urllib.request.urlopen') as send:
                    with self.assertRaises(tts.TTSError):
                        tts.channel_voice('custom')
                    send.assert_not_called()


if __name__ == '__main__':
    unittest.main()
