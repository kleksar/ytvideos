"""The automatic and explicit caption routes must share production constraints."""
from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def load_module(name: str, relative: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


grouping = load_module(
    "semantic_grouping_contract_tests",
    "automation/helpers/paper-subtitles/scripts/semantic_grouping.py",
)


class FixedWidthFont:
    """Predictable metrics; this test font is never a production font override."""

    def getlength(self, text):
        return len(text) * 10


def timed_words(text):
    return [
        {"text": token, "start": index * 0.3, "end": index * 0.3 + 0.2}
        for index, token in enumerate(text.split())
    ]


def phrases_of(groups):
    return [" ".join(word["text"] for word in group) for group in groups]


class SemanticGroupingContractTests(unittest.TestCase):
    def test_short_relative_clause_plan_uses_same_limit_as_automatic_grouping(self):
        words = timed_words("The man who lived.")
        groups = grouping.group_words(words, FixedWidthFont(), 1000, max_words=3)
        phrases = phrases_of(groups)
        self.assertEqual(phrases, ["The man", "who lived."])
        self.assertEqual(
            grouping.plan_phrases(words, phrases, FixedWidthFont(), 1000, max_words=3),
            groups,
        )
        with self.assertRaisesRegex(ValueError, "relative clause"):
            grouping.plan_phrases(words, phrases, FixedWidthFont(), 1000)

    def test_explicit_plan_cannot_exceed_the_word_limit(self):
        with self.assertRaisesRegex(ValueError, "max_words=3"):
            grouping.plan_phrases(
                timed_words("The man who lived."), ["The man who lived."],
                FixedWidthFont(), 1000, max_words=3,
            )

    def test_forced_automatic_breaks_round_trip_without_claiming_semantic_acceptance(self):
        for text, width in [
            ("It has not been properly addressed.", 1000),
            ("Washington's discomfort.", 150),
            ("Five thousand American sailors.", 180),
        ]:
            with self.subTest(text=text):
                words = timed_words(text)
                groups = grouping.group_words(words, FixedWidthFont(), width, max_words=3)
                planned = grouping.plan_phrases(
                    words, phrases_of(groups), FixedWidthFont(), width, max_words=3,
                )
                self.assertEqual(planned, groups)
                self.assertTrue(grouping.boundary_warnings(planned))
                self.assertTrue(all(len(group) <= 3 for group in planned))
                self.assertTrue(all(FixedWidthFont().getlength(phrase) <= width
                                    for phrase in phrases_of(planned)))
                for original, retained in zip(words, [word for group in planned for word in group]):
                    self.assertIs(retained, original)

    def test_word_limit_does_not_license_arbitrary_weak_boundaries(self):
        with self.assertRaisesRegex(ValueError, "syntactic hook"):
            grouping.plan_phrases(
                timed_words("It has not been properly addressed."),
                ["It", "has not been", "properly addressed."],
                FixedWidthFont(), 1000, max_words=3,
            )

    def test_keep_together_is_hard_even_when_width_or_word_count_cannot_fit(self):
        words = timed_words("New York.")
        for width, max_words in [(60, 3), (1000, 1)]:
            with self.subTest(width=width, max_words=max_words):
                with self.assertRaisesRegex(ValueError, "keep_together"):
                    grouping.plan_phrases(
                        words, ["New", "York."], FixedWidthFont(), width,
                        keep_together=["New York"], max_words=max_words,
                    )
                with self.assertRaisesRegex(ValueError, "New York"):
                    grouping.group_words(
                        words, FixedWidthFont(), width,
                        keep_together=["New York"], max_words=max_words,
                    )

    def test_boundary_exception_cannot_override_protected_words(self):
        with self.assertRaisesRegex(ValueError, "keep_together"):
            grouping.plan_phrases(
                timed_words("New York."), ["New", "York."], FixedWidthFont(), 60,
                keep_together=["New York"],
                boundary_exceptions=[{
                    "left": "New", "right": "York.", "reason": "Measured overflow",
                    "user_approved": True, "approval_evidence": "fixture-only.txt",
                    "approval_sha256": "0" * 64,
                }],
            )

    def test_sentence_partition_does_not_silently_break_a_protected_pair(self):
        with self.assertRaisesRegex(ValueError, "keep_together"):
            grouping.group_words(
                timed_words("First. Second."), FixedWidthFont(), 1000,
                keep_together=["First Second"], max_words=3,
            )

    def test_explicit_exception_applies_to_its_own_boundary(self):
        groups = grouping.plan_phrases(
            timed_words("He has another idea."), ["He has", "another idea."],
            FixedWidthFont(), 1000,
            boundary_exceptions=[{
                "left": "He has", "right": "another idea.",
                "reason": "Exact reviewed predicate boundary",
            }],
        )
        self.assertEqual(phrases_of(groups), ["He has", "another idea."])
        self.assertTrue(grouping.boundary_warnings(groups))

    def test_impossible_width_reports_the_sentence_and_actual_constraints(self):
        with self.assertRaisesRegex(ValueError, r"max_text_width=80.*max_words=3.*Unbreakable"):
            grouping.group_words(timed_words("Unbreakable."), FixedWidthFont(), 80, max_words=3)

    def test_no_word_change_omission_or_reordering_is_accepted(self):
        words = timed_words("The man lived.")
        for phrases in [["The man"], ["The men lived."], ["man The lived."]]:
            with self.subTest(phrases=phrases), self.assertRaisesRegex(ValueError, "transcript words"):
                grouping.plan_phrases(words, phrases, FixedWidthFont(), 1000, max_words=3)

    def test_explicit_word_limit_validation_matches_automatic_route(self):
        for value in [0, -1, True, 1.5]:
            with self.subTest(max_words=value), self.assertRaisesRegex(ValueError, "positive integer"):
                grouping.plan_phrases(
                    timed_words("One."), ["One."], FixedWidthFont(), 1000, max_words=value,
                )

    def test_nuviko_overlay_imports_the_canonical_grouping_helper(self):
        overlay = load_module("nuviko_overlay_contract_tests", "automation/subtitles/nuviko_long_subtitles.py")
        self.assertEqual(
            overlay.SEGMENTER_PATH,
            ROOT / "automation/helpers/paper-subtitles/scripts/semantic_grouping.py",
        )
        self.assertEqual(overlay.segmenter.VERSION, grouping.VERSION)


if __name__ == "__main__":
    unittest.main()
