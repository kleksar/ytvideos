import hashlib
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[3]
spec = importlib.util.spec_from_file_location('emdash_montage', ROOT/'automation/ffmpeg_montage/montage.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

class FixedFont:
    def getlength(self, value): return len(value) * 10

class TestEmDashWordHighlight(unittest.TestCase):
    def validate(self, tokens, transcript='waves—but'):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td)
            (p/'transcript').write_text(transcript)
            (p/'words').write_text(json.dumps({'audio_sha256':'a'*64,'transcript_sha256':hashlib.sha256(transcript.encode()).hexdigest(),'words':tokens}))
            with patch.object(m.delivery, 'audio_binding', return_value={'audio':{'sha256':'a'*64}}):
                return m.delivery.validate_words({'subtitles':{'transcript':'transcript','words':'words'}},p,90)

    def test_separate_timing_preserves_contiguous_dash(self):
        words=[{'text':'waves—','start':0.1,'end':0.4},{'text':'but','start':0.5,'end':0.7,'join_previous':True}]
        self.assertEqual(self.validate(words)[0], words)
        self.assertEqual(m.grouping._phrase(words), 'waves—but')
        self.assertEqual(m.grouping._phrase(words[1:]), 'but')
        self.assertTrue(m.grouping._fits(words, FixedFont(), 90, None))
        with patch.object(m.ImageDraw, 'Draw') as draw_factory:
            drawer=draw_factory.return_value
            m.draw_caption_state(['waves—','but'],1,size=(300,100),center_x=150,baseline=50,font=FixedFont(),profile={'background':None,'highlight':'yellow','text':'white','outline':None},pad_x=0,stroke=0,join_previous=[False,True])
            calls=drawer.text.call_args_list
            self.assertEqual(calls[0].args[0][0],105)
            self.assertEqual(calls[1].args[0][0],165)
            self.assertEqual(calls[0].kwargs['fill'],'white')
            self.assertEqual(calls[1].kwargs['fill'],'yellow')

    def test_rejects_changed_text_or_false_join(self):
        def word(t,s,e,**kw):return {'text':t,'start':s,'end':e,**kw}
        with self.assertRaisesRegex(ValueError,'transcript'):
            self.validate([word('waves—',0.1,0.4),word('but',0.5,0.7)])
        with self.assertRaisesRegex(ValueError,'transcript'):
            self.validate([word('wave—',0.1,0.4),word('but',0.5,0.7,join_previous=True)])
        with self.assertRaisesRegex(ValueError,'transcript'):
            self.validate([word('wa',0.1,0.4),word('ves—but',0.5,0.7,join_previous=True)])

    def test_joined_words_are_atomic_at_automatic_and_manual_cue_boundaries(self):
        words=[{'text':'waves—','start':0.1,'end':0.4},
               {'text':'but','start':0.5,'end':0.7,'join_previous':True},
               {'text':'stopped.','start':0.8,'end':1.0}]
        # Prior behavior split into "waves—" / "but stopped.", producing SRT
        # text coverage FAIL. Do not break the bond even when width forces it.
        with self.assertRaisesRegex(ValueError, 'no valid one-line partition'):
            m.grouping.group_words(words, FixedFont(), 120)
        with self.assertRaisesRegex(ValueError, 'splits keep_together'):
            m.grouping.plan_phrases(words,['waves—','but stopped.'],FixedFont(),120)
        groups=m.grouping.group_words(words,FixedFont(),180)
        self.assertEqual([m.grouping._phrase(g) for g in groups],['waves—but stopped.'])
        ss=importlib.util.spec_from_file_location('emdash_srt', ROOT/'automation/helpers/srt/scripts/srt_tool.py')
        srt=importlib.util.module_from_spec(ss);ss.loader.exec_module(srt)
        cues=[{'text':m.grouping._phrase(g),'start_seconds':g[0]['start'],
               'end_seconds':g[-1]['end']} for g in groups]
        self.assertEqual(srt.check(cues,'waves—but stopped.',2)[1]['text_coverage'],'PASS')

    def test_forced_alignment_map_survives_renderer_contract(self):
        a=importlib.util.spec_from_file_location('emdash_aligner',ROOT/'automation/helpers/srt/scripts/forced_alignment.py')
        aligner=importlib.util.module_from_spec(a);a.loader.exec_module(aligner)
        aligned={'word_segments':[{'word':'waves','start':0.1,'end':0.4},
                                  {'word':'but','start':0.5,'end':0.7}]}
        result=aligner.build_map('waves—but','a'*64,aligned)
        self.assertEqual(self.validate(result['words'])[0],result['words'])

    def test_mixed_legacy_and_separate_dash_words(self):
        words=[{'text':'one—two','start':0.1,'end':0.2},
               {'text':'three–','start':0.3,'end':0.4},
               {'text':'four','start':0.5,'end':0.6,'join_previous':True}]
        self.validate(words, 'one—two three–four')
        self.assertEqual(m.grouping._phrase(words), 'one—two three–four')

    def test_legacy_whitespace_map_remains_accepted(self):
        self.validate([{'text':'waves—but','start':0.1,'end':0.7}])
        self.validate([{'text':'waves—','start':0.1,'end':0.4},{'text':'but','start':0.5,'end':0.7}], 'waves— but')

if __name__ == '__main__': unittest.main()
