from copy import deepcopy
import unittest
from srt_plan import plan_srt

SRT = '1\n00:00:00,500 --> 00:00:00,700\nA phrase\n\n2\n00:00:01,000 --> 00:00:01,300\nNext phrase\n'

class SrtPlanTests(unittest.TestCase):
    def target(self, fps='30'):
        return dict(fps=fps, origin_frame=100, end_frame=300)

    def test_gap_adjacent_first_last_and_source_immutable(self):
        target=self.target(); before=deepcopy(target)
        for text in (SRT, SRT.replace('00:00:00,700', '00:00:01,000')):
            plan=plan_srt(text,target); a,b=plan['cues']
            self.assertEqual((a['start_frame'], a['end_frame']), (115,130))
            self.assertEqual((b['start_frame'], b['end_frame']), (130,139))
            self.assertEqual(a['spoken_end_frame'], 130 if text != SRT else 121)
            self.assertEqual(a['text'], 'A phrase')
        self.assertEqual(target,before)
        self.assertIn('00:00:00,700',SRT)

    def test_fractional_fps(self):
        cues=plan_srt(SRT,self.target('30000/1001'))['cues']
        self.assertEqual([(c['start_frame'],c['end_frame']) for c in cues],[(115,130),(130,139)])

    def test_invalid(self):
        for text in ('', 'bad', SRT.replace('00:00:01,000','00:00:00,600'),
                     SRT.replace('A phrase','  '), SRT.replace('00:00:00,700','00:00:00,500')):
            with self.subTest(text=text), self.assertRaises(ValueError):
                plan_srt(text,self.target())
        with self.assertRaises(ValueError):
            plan_srt(SRT,dict(fps='30',origin_frame=100,end_frame=110))
