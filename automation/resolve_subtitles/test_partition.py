"""Synthetic shot cuts, no Resolve/media IO."""
from copy import deepcopy
import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location("resolve_caption_partition_test", Path(__file__).with_name("partition.py"))
partition = importlib.util.module_from_spec(spec)
spec.loader.exec_module(partition)


def fixture():
    def word(index, text, a, b):
        return dict(index=index, text=text, placement_id="voice", start_frame=a, end_frame=b)
    cues = [
        dict(id="C1", text="New York", start_frame=100, end_frame=122,
             spoken_start_frame=101, spoken_end_frame=114,
             words=[word(0, "New", 101, 105), word(1, "York", 107, 114)]),
        dict(id="C2", text="waits", start_frame=125, end_frame=131,
             spoken_start_frame=125, spoken_end_frame=129,
             words=[word(2, "waits", 125, 129)]),
    ]
    shots = [dict(id=f"shot-{i}", carrier_id=f"carrier-{i}", start_frame=a, end_frame=b)
             for i, (a,b) in enumerate(zip([100,103,110,116,125,135], [103,110,116,125,135,140]))]
    return cues, shots


class PartitionTests(unittest.TestCase):
    def test_cut_during_word_preserves_index_and_cut_during_hold_is_neutral(self):
        cues, shots = fixture()
        before = deepcopy((cues, shots))
        result = partition.partition_cues(cues, shots)
        self.assertEqual((cues, shots), before)
        def spans(shot):
            return [(x["start_frame"],x["end_frame"],x["word_index"])
                    for x in result[shot]["sections"][0]["states"]]
        self.assertEqual(spans(0), [(100,101,None), (101,103,0)])
        self.assertEqual(spans(1), [(103,105,0), (105,107,None), (107,110,1)])
        self.assertEqual(spans(2), [(110,114,1), (114,116,None)])
        self.assertEqual(spans(3), [(116,122,None)])
        self.assertEqual(spans(4), [(125,129,2), (129,131,None)])
        self.assertEqual(result[5]["sections"], [])
        self.assertEqual(result[2]["sections"][0]["text"], "New York")
        self.assertEqual(result[2]["sections"][0]["words"], cues[0]["words"])
        self.assertNotIn(124, [s["end_frame"] for shot in result for s in shot["sections"]])

    def test_phrase_start_exactly_on_cut_only_enters_next_shot(self):
        cues, shots = fixture()
        result = partition.partition_cues(cues, shots)
        self.assertEqual([section["cue_id"] for section in result[3]["sections"]], ["C1"])
        self.assertEqual([section["cue_id"] for section in result[4]["sections"]], ["C2"])

    def test_multiple_sections_in_one_shot_keep_the_display_gap(self):
        cues, _ = fixture()
        shot = dict(id="single", carrier_id="same-carrier", start_frame=100, end_frame=140)
        sections = partition.partition_cues(cues, [shot])[0]["sections"]
        self.assertEqual([(row["start_frame"], row["end_frame"]) for row in sections],
                         [(100,122), (125,131)])
        self.assertEqual([row["word_index"] for row in sections[1]["states"]], [2,None])

    def test_bad_shot_gaps_overlap_and_ambiguous_ids_rejected(self):
        for bad, regex in (({"start_frame": 104}, "gap"), ({"start_frame": 102}, "overlap"),
                           ({"id": "shot-0"}, "unique"), ({"carrier_id": ""}, "carrier_id"),
                           ({"start_frame": 103.5}, "bounds")):
            with self.subTest(bad=bad), self.assertRaisesRegex(ValueError, regex):
                cues, shots = fixture()
                shots[1].update(bad)
                partition.partition_cues(cues, shots)

    def test_missing_timeline_coverage_or_inconsistent_words_rejected(self):
        for operation, regex in (
            (lambda cues, shots: shots.pop(0), "outside shot coverage"),
            (lambda cues, shots: cues[0].update(words=[]), "missing"),
            (lambda cues, shots: cues[0]["words"][1].update(index=3), "indices"),
            (lambda cues, shots: cues[0]["words"][1].update(start_frame=104), "overlap"),
            (lambda cues, shots: cues[0]["words"][1].update(end_frame=123), "outside"),
            (lambda cues, shots: cues[0].update(text="Different phrase"), "text disagrees"),
            (lambda cues, shots: cues[0].update(spoken_end_frame=115), "spoken bounds"),
        ):
            with self.subTest(regex=regex), self.assertRaisesRegex(ValueError, regex):
                cues, shots = fixture()
                operation(cues, shots)
                partition.partition_cues(cues, shots)


if __name__ == "__main__":
    unittest.main()
