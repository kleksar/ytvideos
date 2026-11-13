"""Real media decoding regressions; fake providers are never used for these checks."""
import json
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
from unittest.mock import patch
import wave

from PIL import Image

import test_workflow as workflow_fixture
from ytvideos import media_checks
from ytvideos.errors import WorkflowError
from ytvideos.service import Production
from ytvideos.store import Store
from ytvideos.util import file_digest


ROOT = Path(__file__).resolve().parents[1]


@unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe"), "media checks require FFmpeg tools")
class MediaChecksTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        temporary = tempfile.TemporaryDirectory()
        cls.addClassCleanup(temporary.cleanup)
        cls.directory = Path(temporary.name)
        cls.audio = cls.directory / "tone.wav"
        with wave.open(str(cls.audio), "wb") as output:
            output.setparams((1, 2, 8000, 0, "NONE", "not compressed"))
            output.writeframes(b"\x00\x00" * 8000)
        cls.video = cls.directory / "sample.mp4"
        subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-f", "lavfi", "-i", "color=c=orange:s=64x36:r=5:d=1",
                        "-i", str(cls.audio), "-c:v", "libx264", "-preset", "ultrafast", "-c:a", "aac",
                        "-shortest", "-movflags", "+faststart", str(cls.video)], check=True, capture_output=True, timeout=30)
        cls.silent = cls.directory / "silent.mp4"
        subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-i", str(cls.video), "-an", "-c:v", "copy", str(cls.silent)],
                       check=True, capture_output=True, timeout=30)
        cls.image = cls.directory / "image.png"
        Image.new("RGB", (16, 9), "orange").save(cls.image)

    def write(self, value, name="input.txt"):
        path = self.directory / name
        path.write_text(value if isinstance(value, str) else json.dumps(value))
        return path

    def test_actual_mp4_streams_and_complete_decode_pass(self):
        result = media_checks.validate_video(self.video)
        self.assertGreater(result["duration_seconds"], 0)
        self.assertEqual(result["video"][0]["tag"], "avc1")
        self.assertEqual(result["audio"][0]["codec"], "aac")

    def test_renaming_text_to_mp4_does_not_pass(self):
        with self.assertRaises(WorkflowError):
            media_checks.validate_video(self.write("this is not video", "false.mp4"))

    def test_audio_stream_is_required_when_speech_is_expected(self):
        with self.assertRaisesRegex(WorkflowError, "expected audio"):
            media_checks.validate_video(self.silent)
        self.assertTrue(media_checks.validate_video(self.silent, require_audio=False)["video"])

    def test_audio_output_must_really_decode_as_audio(self):
        self.assertEqual(media_checks.validate_audio(self.audio)["audio"][0]["channels"], 1)
        with self.assertRaisesRegex(WorkflowError, "without video"):
            media_checks.validate_audio(self.video)
        with self.assertRaises(WorkflowError):
            media_checks.validate_audio(self.write("not audio", "false.wav"))

    def test_truncated_video_does_not_pass_header_only_validation(self):
        corrupt = self.directory / "truncated.mp4"
        data = self.video.read_bytes()
        corrupt.write_bytes(data[:int(len(data) * .75)])
        with self.assertRaises(WorkflowError):
            media_checks.validate_video(corrupt)

    def test_real_image_mime_dimensions_and_pixels_are_checked(self):
        result = media_checks.validate_image(self.image)
        self.assertEqual((result["mime"], result["width"], result["height"]), ("image/png", 16, 9))
        with self.assertRaises(WorkflowError):
            media_checks.validate_image(self.write("not pixels", "false.png"))
        truncated = self.directory / "truncated.png"
        truncated.write_bytes(self.image.read_bytes()[:40])
        with self.assertRaises(WorkflowError):
            media_checks.validate_image(truncated)

    def test_srt_uses_canonical_parser_and_actual_media_bounds(self):
        valid = self.write("1\n00:00:00,000 --> 00:00:00,800\nA fixture.\n", "valid.srt")
        self.assertEqual(media_checks.validate_srt(valid, duration=1, project_root=ROOT)["cues"], 1)
        invalid = ["1\n00:00:00,000 --> 00:00:02,000\nToo long.\n",
                   "1\n00:00:00,900 --> 00:00:00,800\nReversed.\n",
                   "1\n00:00:00,000 --> 00:00:00,800\nOne.\n\n2\n00:00:00,700 --> 00:00:00,900\nOverlap.\n",
                   "1\n00:00:00.000 --> 00:00:00.800\nWrong delimiter.\n"]
        for text in invalid:
            with self.subTest(text=text), self.assertRaises(WorkflowError):
                media_checks.validate_srt(self.write(text), duration=1, project_root=ROOT)

    def test_review_must_contain_observed_probe_of_exact_render(self):
        review = {"reviewed_sha256": file_digest(self.video), "probe": media_checks.probe_media(self.video)}
        media_checks.validate_review(self.write(review), render_path=self.video, render_sha256=file_digest(self.video))
        for wrong in ({**review, "reviewed_sha256": "f" * 64},
                      {**review, "probe": {**review["probe"], "duration_seconds": 100}}):
            with self.subTest(wrong=wrong), self.assertRaises(WorkflowError):
                media_checks.validate_review(self.write(wrong), render_path=self.video, render_sha256=file_digest(self.video))

    def test_core_completion_validation_rejects_plain_text_render(self):
        service = Production(Store(self.directory / "core.db"), self.directory / "artifacts", ROOT)
        artifact = service.artifacts.put(self.write("A plausible receipt cannot make this an MP4"), "mp4")
        with self.assertRaises(WorkflowError):
            service._validate_output({"tasks": {"packaging": {"status": "pending"}}}, {"stage": "render"}, artifact)

    def test_decoder_does_not_hold_a_database_write_transaction(self):
        fixture = workflow_fixture.WorkflowContract()
        fixture.setUp()
        self.addCleanup(fixture.doCleanups)
        self.addCleanup(fixture.tearDown)
        fixture.production_ready()
        claim = fixture.service.claim(fixture.run_id, "audio", "audio-worker")
        receipt = fixture.receipt("audio", claim, self.audio)
        validate = media_checks.validate_audio

        def while_decoding(path):
            pool = ThreadPoolExecutor(max_workers=1)
            try:
                other = pool.submit(fixture.service.claim, fixture.run_id, "packaging", "parallel-packager")
                # A validator running inside BEGIN IMMEDIATE would block this
                # independent task until it timed out and this test failed.
                other.result(timeout=2)
            finally:
                pool.shutdown(wait=False)
            return validate(path)

        with patch.object(media_checks, "validate_audio", side_effect=while_decoding):
            fixture.service.complete(fixture.run_id, "audio", claim["token"], self.audio, receipt, actual_units=0)
        self.assertEqual(fixture.store.get(fixture.run_id)["tasks"]["packaging"]["status"], "running")

    def test_licensed_recipe_accepts_actual_clip_with_bound_source_and_rights(self):
        service = Production(Store(self.directory / "clips.db"), self.directory / "clip-artifacts", ROOT)
        clip = service.artifacts.put(self.video, "clip")
        source = service.artifacts.put(self.video, "source_video")
        rights = service.artifacts.put(self.write("Synthetic software fixture created by this test."), "rights_evidence")
        run = {"profile": {"recipe": "licensed_clips"}, "tasks": {"packaging": {"status": "pending"}},
               "artifacts": {item["id"]: item for item in (clip, source, rights)}}
        task = {"stage": "scene_image", "payload": {"source_clip": {
            "source_artifact_id": source["id"], "rights_artifact_id": rights["id"], "start_seconds": 0,
            "end_seconds": media_checks.probe_media(self.video)["duration_seconds"], "authority": "Synthetic test fixture author"}}}
        service._validate_output(run, task, clip)
        self.assertTrue(task["media_validation"]["observed"]["video"])
        del run["artifacts"][rights["id"]]
        with self.assertRaisesRegex(WorkflowError, "rights evidence is missing"):
            service._validate_output(run, task, clip)

    def test_licensed_channel_thumbnail_is_still_an_image(self):
        service = Production(Store(self.directory / "thumbnail.db"), self.directory / "thumb-artifacts", ROOT)
        image = service.artifacts.put(self.image, "thumbnail")
        run = {"profile": {"recipe": "licensed_clips", "name": "Synthetic channel"}, "format": "short",
               "tasks": {"packaging": {"status": "pending"}}, "artifacts": {}}
        task = {"stage": "scene_image", "payload": {"purpose": "thumbnail", "title": "Synthetic title",
                                                     "reference_na_reason": "This test isolates image/clip routing."}}
        # Full evidence validation has its own real-preview integration suite.
        with patch("ytvideos.image_review.validate_files", return_value=[]):
            service._validate_output(run, task, image,
                                     receipt={"checks": [{"name": "thumbnail_review", "observed": {}}]})
        self.assertEqual(task["media_validation"]["observed"]["mime"], "image/png")


if __name__ == "__main__":
    unittest.main()
