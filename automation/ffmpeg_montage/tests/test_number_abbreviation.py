import importlib.util
import unittest
from pathlib import Path

from PIL import ImageFont


ROOT = Path(__file__).resolve().parents[3]
SPEC = importlib.util.spec_from_file_location(
    "subtitle_grouping_number_test",
    ROOT / ".agents/skills/ytv-paper-subtitles/scripts/semantic_grouping.py",
)
grouping = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(grouping)


class NumberAbbreviationTest(unittest.TestCase):
    def test_number_abbreviation_and_standalone_no(self):
        tokens = "The vessel No. 1 arrived. No. It sank.".split()
        words = [{"text": token, "start": i, "end": i + 0.5}
                 for i, token in enumerate(tokens)]
        sentences = [" ".join(w["text"] for w in words[a:b])
                     for a, b in grouping.sentence_ranges(words)]
        self.assertEqual(sentences, ["The vessel No. 1 arrived.", "No.", "It sank."])

        font_path = Path("/System/Library/Fonts/Supplemental/Georgia Bold.ttf")
        if not font_path.exists():
            self.skipTest("Nuviko font is not available on this host")
        font = ImageFont.truetype(str(font_path), 84)
        phrases = ["The vessel No. 1 arrived.", "No.", "It sank."]
        groups = grouping.plan_phrases(words, phrases, font, 1286, combine_sentences=True)
        self.assertEqual([" ".join(w["text"] for w in group) for group in groups], phrases)


if __name__ == "__main__":
    unittest.main()
