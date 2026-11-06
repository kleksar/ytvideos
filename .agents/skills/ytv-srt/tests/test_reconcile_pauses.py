import importlib.util
import unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/'scripts/reconcile_pauses.py'
s=importlib.util.spec_from_file_location('reconcile_pauses',p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)

class TestPauseReconciliation(unittest.TestCase):
 def test_spanning_pause_is_flagged_and_provider_is_not_shifted(self):
  provider=[{'text':'Portuguese','start_seconds':38.32,'end_seconds':38.96},{'text':'or','start_seconds':39.28,'end_seconds':39.36},{'text':'read','start_seconds':39.44,'end_seconds':39.76}]
  observed=[{'word':'Portuguese','start':38.26,'end':38.6},{'word':'or','start':38.6,'end':39.32},{'word':'read','start':39.32,'end':39.72}]
  words,flags=m.reconcile(provider,observed,[[38.99,39.24]])
  self.assertEqual(words[1]['start'],39.28)
  self.assertTrue(any(x['word']=='or' and x['reason']=='asr_word_spans_silence' for x in flags))
 def test_unmatched_words_are_retained_and_flagged(self):
  words,flags=m.reconcile([{'text':'nineteen','start_seconds':1,'end_seconds':1.2}], [{'word':'1988','start':1,'end':1.4}], [])
  self.assertEqual(words[0]['text'],'nineteen');self.assertEqual(flags[0]['reason'],'unmatched_asr_tokenization')
if __name__=='__main__':unittest.main()
