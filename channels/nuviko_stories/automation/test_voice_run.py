import json
from pathlib import Path
import tempfile
import unittest
from unittest import mock

import pipeline
import voice_run


class VoiceRunTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.runs = self.root / 'automation' / 'runs'
        self.runs.mkdir(parents=True)
        self.run = pipeline.create(self.root, self.runs, '')
        self.path = self.runs / (self.run['episode'] + '.json')
        for language in ('ru', 'en'):
            story = self.root / f'{language}.txt'
            story.write_text(f'test {language}', encoding='utf-8')
            pipeline.transition(self.run, language, 'story', 'start')
            pipeline.transition(self.run, language, 'story', 'complete', path=str(story))
        pipeline.save(self.path, self.run)

    def tearDown(self):
        self.temp.cleanup()

    def state(self):
        return json.loads(self.path.read_text())

    def test_dry_run_has_no_network_or_state_change(self):
        before = self.path.read_bytes()
        with mock.patch.object(voice_run.tts, 'synthesize') as synth, mock.patch.object(voice_run.tts, 'get_api_key') as key:
            voice_run.run(self.root, self.run['episode'], ['ru', 'en'], channel='paper_detour')
        synth.assert_not_called()
        key.assert_not_called()
        self.assertEqual(before, self.path.read_bytes())

    def test_success_persists_intent_before_request_and_resumes_without_duplicate(self):
        def synthesize(content, destination, **kwargs):
            language = destination.stem[-2:]
            state = self.state()['languages'][language]['voice']
            self.assertEqual(state['status'], 'in_progress')
            self.assertEqual(state['request']['destination'], str(destination))
            destination.write_bytes(b'ID3mock')
            destination.with_suffix('.alignment.json').write_text('{"alignment": null}')
        with mock.patch.object(voice_run.tts, 'verify_backup_voice'), mock.patch.object(voice_run.tts, 'get_api_key', return_value='secret'), mock.patch.object(voice_run.tts, 'synthesize', side_effect=synthesize) as synth:
            voice_run.run(self.root, self.run['episode'], ['ru', 'en'], True, channel='paper_detour')
            voice_run.run(self.root, self.run['episode'], ['ru', 'en'], True, channel='paper_detour')
        self.assertEqual(synth.call_count, 2)
        self.assertEqual(self.state()['languages']['ru']['voice']['status'], 'completed')
        self.assertIn('alignment', self.state()['languages']['en']['voice'])
        self.assertNotIn('secret', self.path.read_text())

    def test_uncertain_request_blocks_retry_even_with_partial_file(self):
        def synthesize(content, destination, **kwargs):
            destination.write_bytes(b'ID3partial')
            raise voice_run.tts.TTSError('uncertain')
        with mock.patch.object(voice_run.tts, 'verify_backup_voice'), mock.patch.object(voice_run.tts, 'get_api_key', return_value='secret'), mock.patch.object(voice_run.tts, 'synthesize', side_effect=synthesize) as synth:
            with self.assertRaises(voice_run.tts.TTSError):
                voice_run.run(self.root, self.run['episode'], ['ru', 'en'], True, channel='paper_detour')
            with self.assertRaisesRegex(ValueError, 'уже запускался'):
                voice_run.run(self.root, self.run['episode'], ['ru', 'en'], True, channel='paper_detour')
        self.assertEqual(synth.call_count, 1)
        self.assertEqual(self.state()['languages']['ru']['voice']['status'], 'in_progress')
        self.assertEqual(self.state()['languages']['en']['voice']['status'], 'pending')

    def test_second_language_failure_preserves_first_and_blocks_retry(self):
        def synthesize(content, destination, **kwargs):
            if destination.stem.endswith('en'):
                raise voice_run.tts.TTSError('timeout; outcome unknown')
            destination.write_bytes(b'ID3mock')
            destination.with_suffix('.alignment.json').write_text('{"alignment": null}')
        with mock.patch.object(voice_run.tts, 'verify_backup_voice'), mock.patch.object(voice_run.tts, 'get_api_key', return_value='secret'), mock.patch.object(voice_run.tts, 'synthesize', side_effect=synthesize) as synth:
            with self.assertRaises(voice_run.tts.TTSError):
                voice_run.run(self.root, self.run['episode'], ['ru', 'en'], True, channel='paper_detour')
            with self.assertRaises(ValueError):
                voice_run.run(self.root, self.run['episode'], ['ru', 'en'], True, channel='paper_detour')
            voice_run.run(self.root, self.run['episode'], ['ru'], True, channel='paper_detour')
        self.assertEqual(synth.call_count, 2)
        state = self.state()['languages']
        self.assertEqual(state['ru']['voice']['status'], 'completed')
        self.assertEqual(state['en']['voice']['status'], 'in_progress')

    def test_modified_story_blocks_all_requests_and_existing_output_blocks(self):
        (self.root / 'en.txt').write_text('changed')
        with mock.patch.object(voice_run.tts, 'synthesize') as synth:
            with self.assertRaisesRegex(ValueError, 'изменён'):
                voice_run.run(self.root, self.run['episode'], ['ru', 'en'], True, channel='paper_detour')
            synth.assert_not_called()
        self.assertEqual(self.state()['languages']['ru']['voice']['status'], 'pending')
        (self.root / 'en.txt').write_text('test en')
        output = pipeline.episode_directory(self.root, self.run['episode']) / 'Source' / 'Voice' / 'voice_ru.mp3'
        output.write_bytes(b'existing')
        with self.assertRaises(voice_run.tts.TTSError):
            voice_run.run(self.root, self.run['episode'], ['ru', 'en'], True, channel='paper_detour')

    def test_voice_uses_renamed_directory_and_legacy_alias(self):
        old = self.root / 'videos' / self.run['directory']
        source = old / 'Source' / 'Voice' / 'script_ru.txt'
        source.write_text('script', encoding='utf-8')
        record = pipeline.artifact(source)
        new = old.with_name(self.run['episode'] + '_renamed')
        old.rename(new)
        old.symlink_to(new.name, target_is_directory=True)
        (self.root / 'videos' / self.run['episode']).symlink_to(new.name, target_is_directory=True)
        self.assertEqual(voice_run.checked_artifact(record, 'script'), (new / 'Source' / 'Voice' / 'script_ru.txt').resolve())
        jobs = voice_run.plan(self.root, self.run, ['ru'], voice_run.tts.channel_voice('paper_detour'))
        self.assertEqual(jobs[0][2], (new / 'Source' / 'Voice' / 'voice_ru.mp3').resolve())
        (new / 'Source' / 'Voice' / 'script_ru.txt').write_text('changed', encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'изменён'):
            voice_run.checked_artifact(record, 'script')


if __name__ == '__main__':
    unittest.main()
