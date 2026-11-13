"""Narrow work must use complete selected rules without creating production state."""
from contextlib import redirect_stderr, redirect_stdout
import io
import json
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch

from ytvideos.cli import main
from ytvideos.context import STAGE_REFERENCES, TASK_EXECUTION_REFERENCE, instruction_packet, snapshot_references
from ytvideos.errors import WorkflowError
from ytvideos.util import file_digest


ROOT = Path(__file__).resolve().parents[1]


class InstructionPacketTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        shutil.copytree(ROOT / '.agent', self.root / '.agent')
        shutil.copytree(ROOT / '.agents', self.root / '.agents')
        for path in {TASK_EXECUTION_REFERENCE, *(p for values in STAGE_REFERENCES.values() for p in values)}:
            target = self.root / path
            target.parent.mkdir(parents=True, exist_ok=True)
            if not target.exists():
                target.write_text('Synthetic instructions for ' + path)
        profile = self.root / 'channels/manual_channel/PROFILE.md'
        profile.parent.mkdir(parents=True)
        profile.write_text('Synthetic manual identity; not permission to publish.')

    def packet(self, **changes):
        return instruction_packet(self.root, **{'channel': 'manual_channel', 'stage': 'packaging',
                                                'format': 'long', **changes})

    def test_manual_channel_gets_skill_full_standards_and_profile_without_enabling_production(self):
        packet = self.packet()
        self.assertEqual(packet['scope'], 'instructions_only')
        self.assertEqual(packet['channel_status'], 'manual')
        self.assertIsNone(packet['channel_configuration'])
        self.assertEqual(packet['skill']['name'], 'ytv-release-video')
        for path in ('docs/standards/thumbnails.md', 'docs/standards/visual.md',
                     'docs/standards/release.md', 'docs/operations/thumbnail-contract.md', TASK_EXECUTION_REFERENCE, 'channels/manual_channel/PROFILE.md'):
            self.assertIn(path, packet['read_next'])
            document = next(item for item in packet['reference_documents'] if item['path'] == path)
            self.assertEqual(document['text'], (self.root / path).read_text())
            self.assertEqual(document['sha256'], file_digest(self.root / path))
        self.assertNotIn('run_id', packet)
        self.assertFalse((self.root / 'channels/manual_channel/channel.json').exists())

    def test_narrow_clip_review_receives_shared_procedure_without_creating_run(self):
        path = '.agents/skills/ytv-produce-video/references/video-clips.md'
        packet = self.packet(stage='review', format='short')
        self.assertIn(path, packet['references'])
        self.assertNotIn('run_id', packet)
        (self.root / path).unlink()
        with self.assertRaisesRegex(WorkflowError, 'missing.*video-clips'):
            self.packet(stage='review', format='short')

    def test_registered_channel_uses_the_same_selector_as_a_new_run(self):
        profile_path = self.root / 'channels/manual_channel/channel.json'
        profile = {'schema_version': 1, 'id': 'manual_channel', 'status': 'frozen',
                   'name': 'Synthetic identity', 'language': 'en',
                   'context_references': [{'path': 'recipe.md', 'stages': ['packaging']}]}
        profile_path.write_text(json.dumps(profile))
        (self.root / 'recipe.md').write_text('Exact selected recipe.')
        packet = self.packet()
        snapshot = snapshot_references(self.root, profile, 'long')
        self.assertEqual(packet['references'], snapshot['routes']['packaging'])
        self.assertEqual(packet['channel_configuration'], profile)
        self.assertEqual(packet['channel_status'], 'frozen')  # Reading rules is not production admission.

    def test_thumbnail_gets_its_own_stage_skill_and_no_experiment_operations(self):
        packet = self.packet(stage='thumbnail', format='short')
        self.assertEqual(packet['skill']['name'], 'ytv-produce-video')
        self.assertIn('docs/standards/thumbnails.md', packet['references'])
        self.assertIn('docs/operations/thumbnail-contract.md', packet['references'])
        self.assertNotIn('docs/operations/thumbnail-experiments.md', packet['references'])

    def test_retention_gets_complete_read_only_instructions_without_a_production_stage(self):
        packet = self.packet(stage='retention', format='short')
        self.assertEqual(packet['skill']['name'], 'ytv-operate')
        required = (TASK_EXECUTION_REFERENCE, 'docs/standards/editorial.md',
                    '.agents/skills/ytv-operate/references/shorts-retention.md',
                    'channels/manual_channel/PROFILE.md')
        for path in required:
            self.assertIn(path, packet['read_next'])
            document = next(item for item in packet['reference_documents'] if item['path'] == path)
            self.assertEqual(document['text'], (self.root / path).read_text())
            self.assertEqual(document['sha256'], file_digest(self.root / path))
        snapshot = snapshot_references(self.root, {'id': 'manual_channel'}, 'short')
        self.assertNotIn('retention', STAGE_REFERENCES)
        self.assertNotIn('retention', snapshot['routes'])
        self.assertNotIn(required[2], snapshot['documents'])

    def test_retention_rejects_long_format(self):
        with self.assertRaisesRegex(WorkflowError, 'retention.*short'):
            self.packet(stage='retention', format='long')

    def test_retention_requires_its_reference_and_one_operate_skill(self):
        path = self.root / '.agents/skills/ytv-operate/references/shorts-retention.md'
        original = path.read_text()
        path.unlink()
        with self.assertRaisesRegex(WorkflowError, 'missing.*shorts-retention'):
            self.packet(stage='retention', format='short')
        path.write_text(original)
        catalog_path = self.root / '.agent/skill-catalog.json'
        catalog = json.loads(catalog_path.read_text())
        catalog['skills'].append(next(item for item in catalog['skills'] if item['name'] == 'ytv-operate'))
        catalog_path.write_text(json.dumps(catalog))
        with self.assertRaisesRegex(WorkflowError, 'exactly one skill'):
            self.packet(stage='retention', format='short')

    def test_missing_blank_or_escaping_rules_never_return_an_incomplete_packet(self):
        path = self.root / 'docs/standards/thumbnails.md'
        original = path.read_text()
        for content in ('', '   \n', None):
            if content is None:
                path.unlink()
            else:
                path.write_text(content)
            with self.subTest(content=content), self.assertRaises(WorkflowError):
                self.packet()
            path.write_text(original)
        outside = self.root.parent / (self.root.name + '-outside.md')
        outside.write_text('Not inside the project')
        self.addCleanup(outside.unlink)
        path.unlink()
        path.symlink_to(outside)
        with self.assertRaisesRegex(WorkflowError, 'outside-repository'):
            self.packet()

    def test_missing_profile_skill_or_ambiguous_catalog_blocks_before_any_work(self):
        skill_path = self.root / '.agents/skills/ytv-release-video/SKILL.md'
        original = skill_path.read_text()
        skill_path.write_text('  ')
        with self.assertRaisesRegex(WorkflowError, 'empty task reference'):
            self.packet()
        skill_path.write_text(original)
        catalog_path = self.root / '.agent/skill-catalog.json'
        catalog = json.loads(catalog_path.read_text())
        entry = next(item for item in catalog['skills'] if item['name'] == 'ytv-release-video')
        catalog['skills'].append(entry)
        catalog_path.write_text(json.dumps(catalog))
        with self.assertRaisesRegex(WorkflowError, 'exactly one skill'):
            self.packet()
        with self.assertRaises(WorkflowError):
            self.packet(channel='unknown_channel')
        with self.assertRaises(WorkflowError):
            self.packet(channel='../manual_channel')

    def test_invalid_catalog_never_returns_an_incomplete_packet(self):
        path = self.root / '.agent/skill-catalog.json'
        for catalog in ([], {}, {'skills': 'wrong'}, {'skills': [None]},
                        {'skills': [{'name': 'test', 'path': 'test.md', 'stages': 'packaging'}]}):
            path.write_text(json.dumps(catalog))
            with self.subTest(catalog=catalog), self.assertRaisesRegex(WorkflowError, 'invalid skill catalog'):
                self.packet()

    def test_cli_does_not_open_a_store_or_create_workspace(self):
        for stage, format in (('packaging', 'long'), ('retention', 'short')):
            output, errors = io.StringIO(), io.StringIO()
            with self.subTest(stage=stage), \
                    patch('ytvideos.cli.Store', side_effect=AssertionError('Must not open a store')), \
                    redirect_stdout(output), redirect_stderr(errors):
                code = main(['--project-root', str(self.root), '--db', str(self.root / 'state.sqlite'),
                             '--workspace', str(self.root / 'workspace'), 'instructions',
                             '--channel', 'manual_channel', '--format', format, '--stage', stage])
                self.assertEqual(code, 0, errors.getvalue())
                self.assertEqual(json.loads(output.getvalue())['scope'], 'instructions_only')
                self.assertFalse((self.root / 'workspace').exists())
                self.assertFalse((self.root / 'state.sqlite').exists())
