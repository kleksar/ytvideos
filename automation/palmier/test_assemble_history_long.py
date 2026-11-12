#!/usr/bin/env python3
"""Offline manifest and mocked-bridge tests. Never contacts Palmier."""
import json
import subprocess
import struct
import tempfile
import wave
import zlib
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import assemble_history_long as mod


class HistoryLongTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        source = self.root / 'Source/Long'
        source.mkdir(parents=True)
        edit = self.root / 'Edit/Long'
        edit.mkdir(parents=True)
        self.project = self.root / 'project.palmier'
        self.project.mkdir()
        self.voice = source / 'voice_105.wav'
        self.srt = source / 'voice.srt'
        self.voice.write_bytes(b'voice')
        self.srt.write_text('1\n00:00:00,000 --> 00:00:01,500\nHello there\n')
        self.images = [source / 'image1.png', source / 'image2.png']
        for i, path in enumerate(self.images):
            path.write_bytes(bytes([i + 1]))
        self.manifest = {
            'status': 'ready', 'timeline': '016_en_marseille_long', 'fps': 30,
            'frames': 301, 'voice_speed_applied': 1.05, 'voice': str(self.voice),
            'srt': str(self.srt), 'sha256': {'voice': mod.sha(self.voice), 'srt': mod.sha(self.srt)},
            'scenes': [
                {'start': 0, 'end': 150, 'cue': 'first', 'path': str(self.images[0]), 'sha256': mod.sha(self.images[0])},
                {'start': 150, 'end': 301, 'cue': 'second', 'path': str(self.images[1]), 'sha256': mod.sha(self.images[1])},
            ],
        }
        self.path = edit / 'manifest.json'
        self.duration = '10.01'

    def inspect(self, path):
        if path.suffix == '.wav':
            return {'streams': [{'codec_type': 'audio', 'codec_name': 'pcm_s16le', 'duration': self.duration}]}
        return {'streams': [{'codec_type': 'video', 'width': 1920, 'height': 1080}]}

    def validate(self):
        self.path.write_text(json.dumps(self.manifest))
        return mod.validate(self.path, self.root, inspect=self.inspect, free_space=mod.MIN_FREE)

    def test_valid_and_dynamic_duration(self):
        self.assertEqual(self.validate()['frames'], 301)
        self.duration = '20.5'
        self.manifest['frames'] = 615
        self.manifest['scenes'][1]['end'] = 615
        self.assertEqual(self.validate()['duration'], 20.5)

    def test_cli_dry_run_with_actual_media(self):
        def png(path, red):
            def chunk(kind, data):
                return struct.pack('>I', len(data)) + kind + data + struct.pack('>I', zlib.crc32(kind + data) & 0xffffffff)
            pixels = b''.join(b'\0' + bytes([red, 0, 0]) * 16 for _ in range(9))
            path.write_bytes(b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', struct.pack('>IIBBBBB', 16, 9, 8, 2, 0, 0, 0)) + chunk(b'IDAT', zlib.compress(pixels)) + chunk(b'IEND', b''))
        with wave.open(str(self.voice), 'wb') as out:
            out.setnchannels(1); out.setsampwidth(2); out.setframerate(48000); out.writeframes(b'\0\0' * 48000)
        png(self.images[0], 1); png(self.images[1], 2)
        self.srt.write_text('1\n00:00:00,000 --> 00:00:00,900\nHello\n')
        self.manifest['sha256'] = {'voice': mod.sha(self.voice), 'srt': mod.sha(self.srt)}
        self.manifest['frames'] = 30
        self.manifest['scenes'][0].update(end=15, sha256=mod.sha(self.images[0]))
        self.manifest['scenes'][1].update(start=15, end=30, sha256=mod.sha(self.images[1]))
        self.path.write_text(json.dumps(self.manifest))
        result = subprocess.run(['python3', str(Path(mod.__file__).resolve()), str(self.path), '--series', str(self.root)],
                                capture_output=True, text=True, check=True)
        summary = json.loads(result.stdout)
        self.assertEqual(summary['mode'], 'offline-dry-run')
        self.assertEqual(summary['frames'], 30)
        self.assertFalse((self.path.parent / 'palmier_receipt.json').exists())

    def test_frame_count_must_match_audio(self):
        self.manifest['frames'] += 1
        with self.assertRaisesRegex(ValueError, 'WAV duration'):
            self.validate()

    def test_gap_or_duplicate_image_rejected(self):
        self.manifest['scenes'][1]['start'] += 1
        with self.assertRaisesRegex(ValueError, 'without gaps'):
            self.validate()
        self.manifest['scenes'][1]['start'] -= 1
        self.images[1].write_bytes(self.images[0].read_bytes())
        self.manifest['scenes'][1]['sha256'] = mod.sha(self.images[1])
        with self.assertRaisesRegex(ValueError, 'Duplicate image content'):
            self.validate()

    def test_invalid_voice_speed_timeline_and_hash(self):
        self.manifest['voice_speed_applied'] = 1.0
        with self.assertRaisesRegex(ValueError, 'voice speed'):
            self.validate()
        self.manifest['voice_speed_applied'] = 1.05
        self.manifest['timeline'] = '../other'
        with self.assertRaisesRegex(ValueError, 'timeline name'):
            self.validate()
        self.manifest['timeline'] = '016_en_marseille_long'
        self.voice.write_bytes(b'changed')
        with self.assertRaisesRegex(ValueError, 'hash mismatch'):
            self.validate()

    def test_srt_out_of_bounds_and_overlaps(self):
        self.srt.write_text('1\n00:00:00,000 --> 00:00:11,000\nToo long\n')
        self.manifest['sha256']['srt'] = mod.sha(self.srt)
        with self.assertRaisesRegex(ValueError, 'outside audio'):
            self.validate()
        self.srt.write_text('1\n00:00:00,000 --> 00:00:02,000\nFirst\n\n2\n00:00:01,000 --> 00:00:03,000\nSecond\n')
        self.manifest['sha256']['srt'] = mod.sha(self.srt)
        with self.assertRaisesRegex(ValueError, 'overlap'):
            self.validate()

    def test_external_asset_and_prior_receipt_rejected(self):
        outsider = self.root / 'outside.png'
        outsider.write_bytes(b'abc')
        self.manifest['scenes'][0]['path'] = str(outsider)
        with self.assertRaisesRegex(ValueError, 'external'):
            self.validate()
        self.manifest['scenes'][0]['path'] = str(self.images[0])
        (self.path.parent / 'palmier_receipt.json').write_text('{}')
        with self.assertRaisesRegex(ValueError, 'Receipt exists'):
            self.validate()

    def test_active_export_prevents_any_mutation(self):
        info = self.validate()
        calls = []
        project = self.project
        class Fake:
            def connect(self): pass
            def request(self, method, params):
                name = params['name']; calls.append(name)
                if name == 'manage_project': data = {'active': {'path': str(project)}, 'visible': {'path': str(project)}}
                elif name == 'get_timeline': data = {'width': 1920, 'height': 1080, 'fps': 30, 'timelines': []}
                elif name == 'manage_exports': data = {'exports': [{'status': 'rendering'}]}
                else: raise AssertionError('Unexpected mutation or read: ' + name)
                return {'content': [{'type': 'text', 'text': json.dumps(data)}]}
        with patch.dict('sys.modules', {'inspect_connection': SimpleNamespace(PalmierConnection=Fake)}):
            with self.assertRaisesRegex(RuntimeError, 'export in progress'):
                mod.execute(info, project)
        self.assertFalse(info['receipt'].exists())
        self.assertNotIn('organize_media', calls)

    def test_successful_mock_assembly_journals_all_mutations(self):
        info = self.validate()
        project = self.project
        manifest = self.manifest
        calls = []
        class Fake:
            def __init__(self):
                self.folder = False
                self.assets = []
                self.clips = []
                self.active = False
            def connect(self): pass
            def request(self, method, params):
                name, args = params['name'], params['arguments']
                calls.append(name)
                actions = {'organize_media': 'create_media_folder', 'create_timeline': 'create_timeline',
                           'import_media': 'import_media', 'set_keyframes': 'set_keyframes'}
                if name in actions:
                    receipt = json.loads(info['receipt'].read_text())
                    assert receipt['pending']['action'] == actions[name]
                if name == 'add_clips':
                    receipt = json.loads(info['receipt'].read_text())
                    assert receipt['pending']['action'] in ('add_clips', 'add_voice')
                if name == 'manage_project': data = {'active': {'path': str(project)}, 'visible': {'path': str(project)}}
                elif name == 'manage_exports': data = {'exports': []}
                elif name == 'get_timeline':
                    data = {'width': 1920, 'height': 1080, 'fps': 30,
                            'name': info['timeline'] if self.active else 'previous',
                            'id': 'timeline-id' if self.active else 'old',
                            'timelines': [{'name': info['timeline']}] if self.active else [],
                            'tracks': [{'clips': self.clips}] if self.clips else [],
                            'totalFrames': max([x['frames'][1] for x in self.clips], default=0),
                            'durationSeconds': 301 / 30}
                elif name == 'get_media':
                    if 'ids' in args: data = {'assets': [x for x in self.assets if x['id'] in args['ids']]}
                    elif 'folder' in args: data = {'assets': self.assets}
                    else: data = {'folders': [info['timeline']] if self.folder else [], 'assets': self.assets}
                elif name == 'organize_media':
                    self.folder = True; data = {'createdFolders': [info['timeline']]}
                elif name == 'create_timeline':
                    self.active = True; data = {'timelineId': 'timeline-id'}
                elif name == 'import_media':
                    ref = 'media-' + str(len(self.assets))
                    self.assets.append({'id': ref, 'name': Path(args['source']['path']).stem, 'folder': info['timeline']})
                    data = {'mediaRef': ref}
                elif name == 'add_clips':
                    added = []
                    for e in args['entries']:
                        clip = {'id': 'clip-' + str(len(self.clips)), 'frames': [e['startFrame'], e.get('endFrame', 301)], 'mediaRef': e['mediaRef']}
                        self.clips.append(clip); added.append({'id': clip['id']})
                    data = {'clips': added}
                elif name == 'set_keyframes':
                    next(x for x in self.clips if x['id'] == args['clipId'])['keyframes'] = {'scale': args['keyframes']}
                    data = {}
                else: raise AssertionError(name)
                return {'content': [{'type': 'text', 'text': json.dumps(data)}]}
        with patch.dict('sys.modules', {'inspect_connection': SimpleNamespace(PalmierConnection=Fake)}), \
             patch.object(mod.shutil, 'disk_usage', return_value=SimpleNamespace(free=mod.MIN_FREE)):
            result = mod.execute(info, project)
        self.assertEqual(result['timelineId'], 'timeline-id')
        receipt = json.loads(info['receipt'].read_text())
        self.assertEqual(receipt['status'], 'assembled')
        self.assertNotIn('pending', receipt)
        self.assertEqual([x['action'] for x in receipt['steps']],
                         ['create_media_folder', 'create_timeline', 'import_media', 'import_media', 'import_media',
                          'add_clips', 'set_keyframes', 'set_keyframes', 'add_voice'])
        self.assertNotIn('export_project', calls)

    def test_uncertain_mutation_leaves_pending_journal(self):
        info = self.validate()
        project = self.project
        class Fake:
            def connect(self): pass
            def request(self, method, params):
                name = params['name']
                if name == 'manage_project': data = {'active': {'path': str(project)}, 'visible': {'path': str(project)}}
                elif name == 'get_timeline': data = {'width': 1920, 'height': 1080, 'fps': 30, 'timelines': []}
                elif name == 'manage_exports': data = {'exports': []}
                elif name == 'get_media': data = {'folders': [], 'assets': []}
                elif name == 'organize_media':
                    receipt = json.loads(info['receipt'].read_text())
                    assert receipt['pending'] == {'action': 'create_media_folder', 'folder': info['timeline']}
                    raise TimeoutError('unknown result')
                else: raise AssertionError(name)
                return {'content': [{'type': 'text', 'text': json.dumps(data)}]}
        with patch.dict('sys.modules', {'inspect_connection': SimpleNamespace(PalmierConnection=Fake)}), \
             patch.object(mod.shutil, 'disk_usage', return_value=SimpleNamespace(free=mod.MIN_FREE)):
            with self.assertRaises(TimeoutError):
                mod.execute(info, project)
        self.assertEqual(json.loads(info['receipt'].read_text())['pending']['action'], 'create_media_folder')
        with self.assertRaisesRegex(ValueError, 'Receipt exists'):
            self.validate()


if __name__ == '__main__':
    unittest.main()
