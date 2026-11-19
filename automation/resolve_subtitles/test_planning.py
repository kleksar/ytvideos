"""Synthetic, offline coverage of the native Resolve subtitle planning contract."""
import copy
import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location("resolve_subtitles_planning_test", Path(__file__).with_name("planning.py"))
planning = importlib.util.module_from_spec(spec)
spec.loader.exec_module(planning)


def fixture():
    sha = "a" * 64
    sha2 = "b" * 64
    placements = [
        dict(id="vo-first", source_sha256=sha, source_in="1", source_out="3",
             timeline_start=86412, timeline_end=86442, speed="2"),
        dict(id="vo-second", source_sha256=sha2, source_in="3", source_out="4",
             timeline_start=86451, timeline_end=86481, speed="1"),
    ]
    def word(pid, source, start, end, text):
        return dict(placement_id=pid, source_sha256=source, start=start, end=end, text=text, confidence="0.97")
    words = [
        word("vo-first", sha, "1.2", "1.4", "New"),
        word("vo-first", sha, "1.4", "1.6", "York"),
        word("vo-first", sha, "2.2", "2.4", "waits."),
        word("vo-second", sha2, "3.1", "3.2", "20"),
        word("vo-second", sha2, "3.2", "3.4", "million"),
        word("vo-second", sha2, "3.6", "3.8", "people."),
    ]
    anchors = [dict(placement_id=w["placement_id"], word_index=i, timeline_frame=frame)
               for i, (w, frame) in enumerate(zip(words, [86415, 86418, 86430, 86454, 86457, 86469]))]
    return dict(target=dict(project_id="proj-abc", timeline_id="timeline-a", fps="30/1",
                            raster=[2560, 1440], origin_frame=86400, end_frame=86490),
                channel="nuviko_history", format="long",
                placements=placements, words=words, groups=[[0, 1], [2], [3, 4], [5]],
                keep_together=[[0, 1], [3, 4]], transcript="New York waits. 20 million people.",
                evidence=dict(kind="timeline_observed", source="synthetic timing observations", anchors=anchors))


class PlannerTests(unittest.TestCase):
    def test_speed_offset_midpoints_and_real_srt_trims(self):
        request = fixture()
        before = copy.deepcopy(request)
        result = planning.plan_subtitles(request)
        self.assertEqual(request, before)
        self.assertEqual(result["style"]["font_face"], {"family": "Georgia", "style": "Bold"})
        self.assertEqual(result["style"]["style"]["highlight"], "#FFD166")
        self.assertEqual(result["target"]["origin_frame"], 86400)
        self.assertEqual(result["alignment"]["result"], "WITHIN_ONE_FRAME")
        self.assertEqual(result["playback"], "UNVERIFIED")
        cues = result["cues"]
        self.assertEqual([(cue["start_frame"], cue["end_frame"]) for cue in cues],
                         [(86400, 86430), (86430, 86454), (86454, 86469), (86469, 86490)])
        self.assertEqual(cues[0]["spoken_start_frame"], 86415)
        self.assertEqual(cues[0]["spoken_end_frame"], 86421)
        self.assertEqual(cues[-1]["spoken_end_frame"], 86475)
        self.assertEqual(cues[0]["words"][0]["start_frame"], 86415)
        self.assertIn("00:00:00,500 --> 00:00:00,700\nNew York", result["srt"])
        self.assertIn("00:00:01,800 --> 00:00:02,100\n20 million", result["srt"])

    def test_paper_resolves_own_style_and_does_not_hold_by_default(self):
        request = fixture()
        request["channel"] = "paper_detour"
        request["format"] = "short"
        request["target"]["raster"] = [1440, 2560]
        result = planning.plan_subtitles(request)
        self.assertEqual(result["style"]["font_face"], {"family": "Chalkboard SE", "style": "Bold"})
        self.assertEqual(result["style"]["geometry"]["font_size_px"], 104)
        self.assertEqual(result["cues"][0]["end_frame"], result["cues"][0]["spoken_end_frame"])

    def test_reject_identity_and_ambiguous_timebase(self):
        for key, value in (("project_id", "current"), ("timeline_id", ""), ("fps", 29.97),
                           ("origin_frame", 86400.5), ("raster", [1920, 1080])):
            with self.subTest(key=key), self.assertRaises(ValueError):
                request = fixture()
                request["target"][key] = value
                planning.plan_subtitles(request)

    def test_reject_vo_overlap_non_linear_bad_duration_and_word_trim(self):
        for mutation, error in (
            (lambda r: r["placements"][1].update(timeline_start=86441), "overlap"),
            (lambda r: r["placements"][0].update(retime="speed_ramp"), "constant-speed"),
            (lambda r: r["placements"][0].update(speed="1.9"), "length disagrees"),
            (lambda r: r["words"][0].update(start="0.9"), "trim"),
            (lambda r: r["words"][0].update(source_sha256="c"*64), "audio hash"),
            (lambda r: r["words"][0].update(confidence="0.7"), "confidence below"),
        ):
            with self.subTest(error=error), self.assertRaisesRegex(ValueError, error):
                request = fixture()
                mutation(request)
                planning.plan_subtitles(request)

    def test_local_drift_and_global_offset_fail_closed(self):
        for shifts, result in (((0, 2, 5, 0, 1, 5), "NON_UNIFORM"), ((2, 2, 2, 2, 2, 2), "OFFSET_CANDIDATE")):
            with self.subTest(result=result), self.assertRaisesRegex(ValueError, result):
                request = fixture()
                for anchor, drift in zip(request["evidence"]["anchors"], shifts):
                    anchor["timeline_frame"] += drift
                planning.plan_subtitles(request)

    def test_missing_anchors_or_hash_does_not_count_as_confirmation(self):
        request = fixture()
        request["evidence"]["anchors"].pop(4)
        with self.assertRaisesRegex(ValueError, "first/middle/last"):
            planning.plan_subtitles(request)
        request = fixture()
        request["evidence"]["conform_sha256"] = "b" * 64
        with self.assertRaisesRegex(ValueError, "stale"):
            planning.plan_subtitles(request)

    def test_entities_and_exact_transcript_are_preserved(self):
        request = fixture()
        request["groups"] = [[0], [1], [2], [3, 4], [5]]
        with self.assertRaisesRegex(ValueError, "protected"):
            planning.plan_subtitles(request)
        request = fixture()
        request["transcript"] = "20 billion people."
        with self.assertRaisesRegex(ValueError, "transcript coverage"):
            planning.plan_subtitles(request)

    def test_group_cannot_cross_cut_or_duplicate_word(self):
        for groups, error in (([[0, 1], [2, 3], [4, 5]], "speech cut"),
                              ([[0, 1], [2], [3, 4], [4, 5]], "exactly once")):
            with self.subTest(error=error), self.assertRaisesRegex(ValueError, error):
                request = fixture()
                request["groups"] = groups
                planning.plan_subtitles(request)


if __name__ == "__main__":
    unittest.main()
