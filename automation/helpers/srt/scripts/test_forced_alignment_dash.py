import hashlib
import importlib.util
import unittest
import json
import sys
import tempfile
from types import SimpleNamespace
from unittest.mock import patch
from pathlib import Path

spec = importlib.util.spec_from_file_location('dash_alignment', Path(__file__).with_name('forced_alignment.py'))
m = importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

class ForcedDashAlignmentTests(unittest.TestCase):
    def test_split_words_keep_exact_transcript_and_audio_binding(self):
        text='the waves—but escaped.'
        seg=[{'word':x,'start':i,'end':i+0.5} for i,x in enumerate(['the','waves','but','escaped'])]
        result=m.build_map(text,'a'*64,{'word_segments':seg})
        self.assertEqual([w['text'] for w in result['words']],['the','waves—','but','escaped.'])
        self.assertEqual([w.get('join_previous',False) for w in result['words']],[False,False,True,False])
        self.assertEqual(result['transcript_sha256'],hashlib.sha256(text.encode()).hexdigest())
        self.assertEqual(result['audio_sha256'],'a'*64)
        self.assertEqual(result['status'],'REVIEW_REQUIRED')

    def test_legacy_single_token_and_mixed_split(self):
        text='one—two three–four'
        seg=[{'word':x,'start':i,'end':i+0.5} for i,x in enumerate(['one—two','three','four'])]
        words=m.build_map(text,'a'*64,{'word_segments':seg})['words']
        self.assertEqual([w['text'] for w in words],['one—two','three–','four'])
        self.assertTrue(words[2]['join_previous'])

    def test_cli_sends_space_to_aligner_but_keeps_exact_transcript(self):
        text='U.S. 1920 waves—but stopped.'
        with tempfile.TemporaryDirectory() as td:
            p=Path(td);(p/'speech.txt').write_text(text);(p/'audio').write_bytes(b'fixture audio')
            observed=[]
            def align(segments, model, metadata, audio, device, return_char_alignments):
                observed.append(segments[0]['text'])
                # Simulate WhisperX splitting the actual received text on spaces.
                return {'word_segments':[{'word':x,'start':i,'end':i+0.5}
                                         for i,x in enumerate(segments[0]['text'].split(' '))]}
            fake=SimpleNamespace(load_audio=lambda path:[0]*16000,
                                 load_align_model=lambda **kw:(object(),{}),align=align)
            argv=['forced_alignment.py','--audio',str(p/'audio'),'--text',str(p/'speech.txt'),
                  '--language','en','--output',str(p/'map.json'),'--raw-output',str(p/'raw.json')]
            with patch.dict(sys.modules, {'whisperx':fake}), patch.object(sys,'argv',argv):
                m.main()
            result=json.loads((p/'map.json').read_text())
            self.assertEqual(observed,['U.S. 1920 waves— but stopped.'])
            self.assertEqual(result['transcript_sha256'],hashlib.sha256(text.encode()).hexdigest())
            self.assertEqual(result['audio_sha256'],hashlib.sha256(b'fixture audio').hexdigest())
            self.assertEqual([w['text'] for w in result['words']],['U.S.','1920','waves—','but','stopped.'])
            self.assertTrue(result['words'][3]['join_previous'])
            self.assertEqual(result['status'],'REVIEW_REQUIRED')

    def test_missing_wrong_or_unordered_tokens_fail(self):
        text='waves—but'
        for seg in ([{'word':'waves','start':0,'end':0.1}],
                    [{'word':'waves','start':0,'end':0.1},{'word':'boat','start':0.2,'end':0.3}],
                    [{'word':'waves','start':0,'end':0.3},{'word':'but','start':0.2,'end':0.4}]):
            with self.assertRaises(ValueError):m.build_map(text,'a'*64,{'word_segments':seg})

if __name__=='__main__':unittest.main()
