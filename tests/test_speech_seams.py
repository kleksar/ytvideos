import unittest
from automation.helpers.speech_seams import audit

class SpeechSeamsTest(unittest.TestCase):
    def check_gap(self, size):
        return audit([.5]*100+[0]*size+[.5]*100,1000,[dict(left_word_end=.1,right_word_start=(100+size)/1000,cut=(100+size/2)/1000)])[0]
    def test_exact_50ms(self):
        self.assertEqual(self.check_gap(50)['status'],'MEASURED_CANDIDATE')
    def test_short_gap(self):
        self.assertEqual(self.check_gap(49)['status'],'REVIEW')
    def test_long_gap(self):
        self.assertEqual(self.check_gap(200)['natural_quiet_ms'],200)
    def test_word_boundary_required(self):
        self.assertEqual(audit([0]*1000,1000,[{'cut':.5}])[0]['status'],'REVIEW')
    def test_quiet_inside_word_cannot_pass(self):
        self.assertEqual(audit([0]*1000,1000,[dict(left_word_end=.7,right_word_start=.8,cut=.5)])[0]['status'],'REVIEW')
    def test_noise_requires_review(self):
        self.assertEqual(audit([.01]*1000,1000,[dict(left_word_end=.1,right_word_start=.9,cut=.5)])[0]['status'],'REVIEW')
    def test_invalid_bounds(self):
        self.assertEqual(audit([0]*1000,1000,[dict(left_word_end=0,right_word_start=2,cut=.5)])[0]['status'],'REVIEW')
    def test_no_mutation(self):
        x=[.5]*100+[0]*100+[.5]*100;old=x.copy()
        audit(x,1000,[dict(left_word_end=.1,right_word_start=.2,cut=.15)])
        self.assertEqual(x,old)
    def test_nonfinite(self):
        with self.assertRaises(ValueError):audit([float('nan')],1000,[])
    def test_stereo_does_not_cancel(self):
        import tempfile,wave,struct
        from pathlib import Path
        from automation.helpers.speech_seams import read_pcm
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'a.wav'
            with wave.open(str(p),'wb') as f:
                f.setparams((2,2,1000,0,'NONE','not compressed'))
                f.writeframes(struct.pack('<hh',16384,-16384)*100)
            samples,rate=read_pcm(p)
            self.assertEqual(rate,1000)
            self.assertEqual(samples,[.5]*100)
