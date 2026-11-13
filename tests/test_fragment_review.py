"""Identity/coverage checks for manual character-edit review, without semantic detection."""
import copy
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
from unittest.mock import patch

from ytvideos.errors import WorkflowError
from ytvideos.media_checks import source_frame_anchors
from ytvideos.production_contract import production_requirements, validate_fragment_review, validate_render_manifest


ROOT = Path(__file__).resolve().parents[1]


class FragmentReviewTests(unittest.TestCase):
    def setUp(self):
        profile = json.loads((ROOT / "channels/scenes_on_repeat/channel.json").read_text())
        self.requirements = production_requirements(profile, "short", variant="character_edit")
        self.plan = {"channel": profile["id"], "format": "short", "production_variant": "character_edit",
            "has_speech": False, "subtitles": {"mode": "none"},
            "music": {"status": "not_used", "reason": "Synthetic policy test without music selection"}, "scenes": []}
        self.sources, rows = [], []
        for index, (first, stop) in enumerate(((0, 14), (11, 24))):
            scene = {"id": "s" + str(index), "clip": "/synthetic/clip-" + str(index) + ".mp4", "clip_sha256": str(index + 1) * 64,
                "source": {"path": "/synthetic/original-" + str(index) + ".mp4", "sha256": str(index + 3) * 64,
                           "start_seconds": 1., "end_seconds": 1. + (stop - first) / 24},
                "start_frame": index * 12, "end_frame": (index + 1) * 12,
                "visible_start_frame": first, "visible_end_frame": stop,
                "crop": {"interpolation": "linear", "keyframes": [
                    {"frame": first, "box": [0, 0, 1080, 1920]}, {"frame": stop - 1, "box": [2, 0, 1082, 1920]}]}}
            self.plan["scenes"].append(scene)
            source = scene["source"]
            points = [1. + frame / 24 for frame in range(stop - first)]
            anchors = [points[0], min(points, key=lambda value: (abs(value - (source["start_seconds"] + source["end_seconds"]) / 2), value)), points[-1]]
            self.sources.append({"id": scene["id"], "clip_sha256": scene["clip_sha256"], "source_sha256": source["sha256"],
                                 "start_seconds": source["start_seconds"], "end_seconds": source["end_seconds"],
                                 "source_anchors_seconds": anchors})
            rows.append({"id": scene["id"], "source": copy.deepcopy(source), "clip_sha256": scene["clip_sha256"],
                "timeline": {key: scene[key] for key in ("start_frame", "end_frame", "visible_start_frame", "visible_end_frame")},
                "crop": copy.deepcopy(scene["crop"]), "method": "Synthetic complete-motion coverage fixture; no human perception asserted.",
                "source_coverage": [{"start_seconds": source["start_seconds"], "end_seconds": source["end_seconds"]}],
                "source_anchors_seconds": anchors,
                "final_anchors_frames": [first, (first + stop - 1) // 2, stop - 1],
                "checked_transition_frames": sorted({first, scene["start_frame"], scene["end_frame"] - 1, stop - 1}),
                "checks": {key: {"status": "PASS", "notes": "Synthetic structured observation for " + key}
                           for key in ("source_motion", "crop", "internal_cuts", "final_motion", "transitions")}})
        self.review = {"schema": "ytv-source-fragment-review-v1", "artifact_sha256": "a" * 64,
                       "reviewer": "independent-fixture", "fragments": rows}

    def validate(self, document=None, plan=None, sources=None):
        return validate_fragment_review(document or self.review, plan=plan or self.plan, requirements=self.requirements,
            media_sha256="a" * 64, reviewer="independent-fixture", sources=sources or self.sources)

    def test_full_source_intervals_crops_and_transition_overlaps_are_bound(self):
        validate_render_manifest(self.plan, self.requirements)
        self.assertEqual(self.validate(), [{key: scene["source"][key] for key in ("path", "sha256")}
                                          for scene in self.plan["scenes"]])

    def test_missing_fragment_data_or_source_failures_cannot_be_passed(self):
        for field in ("source", "clip_sha256", "crop", "visible_start_frame", "visible_end_frame"):
            plan = copy.deepcopy(self.plan)
            del plan["scenes"][0][field]
            with self.subTest(field=field), self.assertRaises(WorkflowError):
                validate_render_manifest(plan, self.requirements)
        for name in self.review["fragments"][0]["checks"]:
            for status in ("FAIL", "UNVERIFIED"):
                review = copy.deepcopy(self.review)
                review["fragments"][0]["checks"][name]["status"] = status
                with self.subTest(name=name, status=status), self.assertRaisesRegex(WorkflowError, "FAIL or UNVERIFIED"):
                    self.validate(review)

    def test_three_stills_partial_interval_and_omitted_transition_do_not_cover_motion(self):
        for field, value in (("source_coverage", []),
                             ("source_coverage", [{"start_seconds": 1., "end_seconds": 1.2}]),
                             ("source_anchors_seconds", [1., 1.1, 1.2]),
                             ("checked_transition_frames", [0, 11]),
                             ("final_anchors_frames", [0, 5, 11])):
            review = copy.deepcopy(self.review)
            review["fragments"][0][field] = value
            with self.subTest(field=field, value=value), self.assertRaises(WorkflowError):
                self.validate(review)

    def test_changed_crop_source_interval_hash_order_or_render_requires_fresh_review(self):
        for mutate in (lambda value: value["scenes"][0]["crop"]["keyframes"][-1].update(box=[3, 0, 1083, 1920]),
                       lambda value: value["scenes"][0]["source"].update(end_seconds=2.),
                       lambda value: value["scenes"][0].update(clip_sha256="f" * 64)):
            plan = copy.deepcopy(self.plan)
            mutate(plan)
            with self.assertRaises(WorkflowError):
                self.validate(plan=plan)
        review = copy.deepcopy(self.review)
        review["fragments"].reverse()
        with self.assertRaises(WorkflowError):
            self.validate(review)
        review = copy.deepcopy(self.review)
        review["artifact_sha256"] = "b" * 64
        with self.assertRaises(WorkflowError):
            self.validate(review)
        sources = copy.deepcopy(self.sources)
        sources[0]["source_sha256"] = "e" * 64
        with self.assertRaisesRegex(WorkflowError, "accepted storyboard"):
            self.validate(sources=sources)


@unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe"), "requires local FFmpeg")
class SourceFrameAnchorTests(unittest.TestCase):
    def test_actual_source_pts_cover_low_fps_vfr_non_frame_aligned_in_and_offset(self):
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            for name, filter_value, duration, expected in (
                    ("low-fps", "null", .5, [0, .25, .416667]),
                    ("reordered-middle", "null", 2, [0, .25, .416667]),
                    ("vfr", "select='eq(n,0)+eq(n,1)+eq(n,4)+eq(n,5)+gte(n,12)'", 2, [0, .333333, .416667]),
                    ("offset", "setpts=PTS+3/TB", 2, [0, .25, .416667])):
                source = directory / (name + ".mp4")
                subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-f", "lavfi", "-i",
                    f"testsrc2=s=90x160:r=12:d={duration}", "-vf", filter_value, "-fps_mode", "vfr",
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", str(source)],
                    check=True, capture_output=True, timeout=30)
                with self.subTest(source=name):
                    self.assertEqual(source_frame_anchors(source, 0, .5), expected)
                    shifted = source_frame_anchors(source, .01, .5)
                    self.assertEqual(shifted, [.083333, expected[1], .416667])
                    # Use the observed original PTS in a 24-fps review contract:
                    # no synthetic arithmetic-midpoint or output-FPS anchors.
                    fixture = FragmentReviewTests()
                    fixture.setUp()
                    scene = fixture.plan["scenes"][0]
                    scene["source"].update(path=str(source), start_seconds=.01, end_seconds=.5)
                    row = fixture.review["fragments"][0]
                    row.update(source=copy.deepcopy(scene["source"]), source_anchors_seconds=shifted,
                               source_coverage=[{"start_seconds": .01, "end_seconds": .5}])
                    fixture.sources[0].update(start_seconds=.01, end_seconds=.5, source_anchors_seconds=shifted)
                    fixture.validate()
                    row["source_anchors_seconds"] = [.01, .255, .458333]
                    with self.assertRaisesRegex(WorkflowError, "source-frame anchors"):
                        fixture.validate()


@unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe"), "requires local FFmpeg")
class FragmentStorageTests(unittest.TestCase):
    def test_shared_original_is_hashed_and_preserved_once_while_every_fragment_is_checked(self):
        import test_edit_script as edit_fixtures
        fixture = edit_fixtures.CharacterEditLifecycle()
        fixture.setUp()
        self.addCleanup(fixture.doCleanups)
        fixture.test_signed_source_audio_to_mp4_has_no_tts_or_fake_srt()
        service = fixture.service
        run = service.store.get(fixture.run_id)
        render = run["tasks"]["render"]
        manifest = next(item for item in render["media_validation"]["evidence_artifacts"] if item["kind"] == "render_manifest")
        plan = json.loads(service.artifacts.resolve(manifest).read_text())
        receipt = json.loads(service.artifacts.resolve(run["artifacts"][run["tasks"]["review"]["receipt"]]).read_text())
        visual = next(item["observed"] for item in receipt["checks"] if item["name"] == "visual_review")
        document = json.loads(Path(visual["evidence"]["path"]).read_text())
        template, row = copy.deepcopy(plan["scenes"][0]), copy.deepcopy(document["fragments"][0])
        source_task = run["tasks"]["image:shot"]
        original_id = source_task["payload"]["source_clip"]["source_artifact_id"]
        # Isolate the storage/coverage boundary with three valid rows sharing
        # one actual source; this snapshot does not claim a second live render.
        plan["scenes"], document["fragments"] = [], []
        render["dependencies"] = [key for key in render["dependencies"] if not key.startswith("image:")]
        for index in range(3):
            start, stop, identity = index * 4, (index + 1) * 4, "part" + str(index)
            scene = copy.deepcopy(template)
            scene.update(id=identity, start_frame=start, end_frame=stop, visible_start_frame=start, visible_end_frame=stop)
            scene["crop"]["keyframes"][0]["frame"], scene["crop"]["keyframes"][-1]["frame"] = start, stop - 1
            plan["scenes"].append(scene)
            observed = copy.deepcopy(row)
            observed.update(id=identity, crop=scene["crop"], final_anchors_frames=[start, (start + stop - 1) // 2, stop - 1],
                            checked_transition_frames=[start, stop - 1], timeline={key: scene[key] for key in row["timeline"]})
            document["fragments"].append(observed)
            task_id = "image:" + identity
            run["tasks"][task_id] = {**copy.deepcopy(source_task), "id": task_id}
            render["dependencies"].append(task_id)
        saved = service.artifacts.put(fixture.write(plan, "shared-source-manifest.json"), "render_manifest")
        render["media_validation"]["evidence_artifacts"] = [saved]
        visual["evidence"] = fixture.record(fixture.write(document, "shared-source-review.json"))
        review = run["tasks"]["review"]
        with patch.object(service.artifacts, "resolve", wraps=service.artifacts.resolve) as resolve, \
                patch.object(service, "_evidence_file", wraps=service._evidence_file) as preserve, \
                patch("ytvideos.media_checks.source_frame_anchors", wraps=source_frame_anchors) as anchors:
            service._validate_output(run, review, run["artifacts"][review["outputs"][0]], receipt=receipt)
        self.assertEqual(sum(call.args[0]["id"] == original_id for call in resolve.call_args_list), 1)
        self.assertEqual(sum(call.args[1] == "fragment_review_source" for call in preserve.call_args_list), 1)
        self.assertEqual(anchors.call_count, 3)
        validation = review["media_validation"]
        self.assertEqual(len(validation["checked_artifact_ids"]), len(set(validation["checked_artifact_ids"])))
        self.assertIn(original_id, validation["checked_artifact_ids"])
        self.assertEqual(sum(item["kind"] == "fragment_review_source" for item in validation["evidence_artifacts"]), 1)


if __name__ == "__main__":
    unittest.main()
