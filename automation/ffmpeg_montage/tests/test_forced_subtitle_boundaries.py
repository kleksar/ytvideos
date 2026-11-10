"""Regression coverage for width-forced, explicitly documented subtitle breaks."""
import importlib.util
import unittest
from pathlib import Path

MODULE = Path(__file__).resolve().parents[3] / '.agents/skills/ytv-paper-subtitles/scripts/semantic_grouping.py'
spec = importlib.util.spec_from_file_location('semantic_grouping_forced_tests', MODULE)
grouping = importlib.util.module_from_spec(spec)
spec.loader.exec_module(grouping)


class FixedWidthFont:
    def getlength(self, value):
        return len(value) * 30


class ForcedBoundaryTests(unittest.TestCase):
    def test_short_overflow_possessive_is_exposed_as_warning(self):
        words = [{'text': x, 'start': i, 'end': i + 0.5}
                 for i, x in enumerate(["Washington's", 'discomfort.'])]
        groups = grouping.group_words(words, FixedWidthFont(), 450, max_words=3)
        self.assertEqual(["Washington's", 'discomfort.'],
                         [' '.join(w['text'] for w in group) for group in groups])
        self.assertTrue(grouping.boundary_warnings(groups))
        groups = grouping.group_words(words, FixedWidthFont(), 1200, max_words=3)
        self.assertEqual(len(groups), 1)

    def test_recorded_boundaries_are_allowed_only_when_needed(self):
        for left, right in [('and around', 'one hundred and fifty'),
                            ('had not been', 'properly addressed.')]:
            with self.subTest(left=left):
                words = [{'text': x, 'start': i, 'end': i + 0.5}
                         for i, x in enumerate((left + ' ' + right).split())]
                exceptions = [{'left': left, 'right': right, 'reason': 'measured overflow'}]
                groups = grouping.plan_phrases(words, [left, right], FixedWidthFont(), 700,
                                               boundary_exceptions=exceptions)
                self.assertEqual(len(groups), 2)
                with self.assertRaises(ValueError):
                    grouping.plan_phrases(words, [left, right], FixedWidthFont(), 2000,
                                          boundary_exceptions=exceptions)


if __name__ == '__main__':
    unittest.main()
