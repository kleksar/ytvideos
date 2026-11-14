import hashlib
import importlib.util
import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path
from PIL import Image, ImageDraw
from unittest.mock import patch


HELPER = Path(__file__).resolve().parents[1] / "montage_trial.py"
spec = importlib.util.spec_from_file_location("montage_trial", HELPER)
trial = importlib.util.module_from_spec(spec)
spec.loader.exec_module(trial)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class MontageTrialTests(unittest.TestCase):
    def setUp(self):
        if not shutil.which("ffmpeg") or not shutil.which("ffprobe"):
            self.skipTest("ffmpeg and ffprobe are required for local fixture tests")
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.image = self.root / "still.png"
        subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-f", "lavfi", "-i",
                        "color=c=navy:s=96x96", "-frames:v", "1", str(self.image)],
                       check=True, stdin=subprocess.DEVNULL, capture_output=True)
        self.video = self.root / "clip.mp4"
        subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-f", "lavfi", "-i",
                        "testsrc2=s=96x96:r=10", "-t", "1.2", "-an", "-c:v", "libx264",
                        "-pix_fmt", "yuv420p", "-bsf:v",
                        "h264_metadata=colour_primaries=1:transfer_characteristics=13:matrix_coefficients=6:video_full_range_flag=0",
                        str(self.video)], check=True,
                       stdin=subprocess.DEVNULL, capture_output=True)
        self.video_bt709 = self.root / "clip-bt709.mp4"
        subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-f", "lavfi", "-i",
                        "testsrc2=s=96x96:r=10", "-t", "1.2", "-an", "-c:v", "libx264",
                        "-pix_fmt", "yuv420p", "-bsf:v",
                        "h264_metadata=colour_primaries=1:transfer_characteristics=1:matrix_coefficients=1:video_full_range_flag=0",
                        str(self.video_bt709)], check=True,
                       stdin=subprocess.DEVNULL, capture_output=True)
        self.script = self.root / "script.txt"
        self.script.write_text("Fixture script", encoding="utf-8")
        self.storyboard = self.root / "storyboard.json"
        self.storyboard.write_text("{}", encoding="utf-8")
        self.video_audio_tail = self.root / "short-video-long-audio.mp4"
        subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-f", "lavfi", "-i",
                        "testsrc2=s=96x96:r=10", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo",
                        "-filter:v", "trim=duration=1.2", "-map", "0:v", "-map", "1:a", "-t", "3.0",
                        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-bsf:v",
                        "h264_metadata=colour_primaries=1:transfer_characteristics=13:matrix_coefficients=1:video_full_range_flag=0",
                        "-c:a", "aac", str(self.video_audio_tail)], check=True,
                       stdin=subprocess.DEVNULL, capture_output=True)

    def tearDown(self):
        self.temp.cleanup()

    def _camera(self, start, end):
        return {"start": {"center": [0.5, 0.5], "scale": start},
                "end": {"center": [0.5, 0.5], "scale": end},
                "focus": [0.5, 0.5], "subject": "synthetic test subject",
                "reason": "exercise canonical camera filter"}

    def _manifest(self):
        return {"schema": trial.SCHEMA, "purpose": trial.PURPOSE,
                "provenance": {"run_id": "synthetic-fixture",
                               "script": {"path": self.script.name, "sha256": digest(self.script)},
                               "storyboard": {"path": self.storyboard.name, "sha256": digest(self.storyboard)}},
                "timing_basis": "Synthetic test fixture uses explicit eight-frame provisional windows.",
                "canvas": [64, 64], "fps": 10, "audio_policy": "mute",
                "scenes": [
                    {"id": "T001", "type": "image", "source": self.image.name, "source_sha256": digest(self.image),
                     "start_frame": 0, "end_frame": 8, "direction": "none", "zoom": "in",
                     "camera": self._camera(1.0, 1.035)},
                    {"id": "T002", "type": "video", "source": self.video.name, "source_sha256": digest(self.video),
                     "source_in_seconds": 0.2, "used_duration_frames": 8,
                     "direction": "none", "zoom": "none",
                     "start_frame": 8, "end_frame": 16},
                    {"id": "T003", "type": "image", "source": self.image.name, "source_sha256": digest(self.image),
                     "start_frame": 16, "end_frame": 24, "direction": "none", "zoom": "out",
                     "camera": self._camera(1.035, 1.0)},
                ]}

    def _write_manifest(self, manifest):
        path = self.root / "manifest.json"
        path.write_text(json.dumps(manifest), encoding="utf-8")
        return path

    def test_mixed_trial_renders_exact_frames_silently_and_records_receipt(self):
        manifest = self._write_manifest(self._manifest())
        before = {str(path): digest(path) for path in (self.image, self.video)}
        output = self.root / "trial.mp4"
        receipt = trial.render(manifest, output)

        self.assertTrue(output.is_file())
        self.assertEqual(receipt["purpose"], "montage_trial")
        self.assertFalse(receipt["production_acceptance"])
        self.assertEqual(receipt["review"], "UNVERIFIED")
        self.assertTrue(receipt["source_unchanged"])
        self.assertEqual(receipt["timeline"]["frames"], 24)
        self.assertEqual(receipt["timeline"]["duration_seconds"], 2.4)
        self.assertEqual(receipt["output"]["sha256"], digest(output))
        self.assertEqual(before, {str(path): digest(path) for path in (self.image, self.video)})
        probe = trial.ffprobe(output)
        stream = trial._video_stream(probe, output)
        self.assertEqual(int(stream["nb_read_frames"]), 24)
        self.assertEqual(stream["color_primaries"], "bt709")
        self.assertEqual(stream["color_transfer"], "bt709")
        self.assertEqual(stream["color_space"], "bt709")
        self.assertEqual(stream["color_range"], "tv")
        self.assertFalse(any(s.get("codec_type") == "audio" for s in probe["streams"]))
        receipt_path = Path(str(output) + ".montage_trial.json")
        self.assertTrue(receipt_path.is_file())
        saved = json.loads(receipt_path.read_text(encoding="utf-8"))
        self.assertEqual(saved["output"]["sha256"], digest(output))

    def test_invalid_source_hash_fails_before_output(self):
        manifest = self._manifest()
        manifest["scenes"][0]["source_sha256"] = "0" * 64
        with self.assertRaisesRegex(trial.TrialError, "hash mismatch"):
            trial.validate(manifest, self.root / "manifest.json")

    def test_short_clip_window_is_rejected(self):
        manifest = self._manifest()
        manifest["scenes"][1]["source_in_seconds"] = 0.9
        path = self._write_manifest(manifest)
        with self.assertRaisesRegex(trial.TrialError, "actual video stream"):
            trial.render(path, self.root / "short.mp4")
        self.assertFalse((self.root / "short.mp4").exists())

    def test_long_audio_tail_does_not_extend_short_video_stream(self):
        manifest = self._manifest()
        row = manifest["scenes"][1]
        row["source"] = self.video_audio_tail.name
        row["source_sha256"] = digest(self.video_audio_tail)
        row["source_in_seconds"] = 0.9
        path = self._write_manifest(manifest)
        probe = trial.ffprobe(self.video_audio_tail)
        self.assertGreater(float(probe["format"]["duration"]), 2.9)
        with self.assertRaisesRegex(trial.TrialError, "actual video stream"):
            trial.render(path, self.root / "audio-tail.mp4")
        self.assertFalse((self.root / "audio-tail.mp4").exists())

    def test_standard_bt709_video_tags_are_supported(self):
        scene = {"id": "BT709", "type": "video", "source": self.video_bt709.name,
                 "source_sha256": digest(self.video_bt709), "source_in_seconds": 0,
                 "used_duration_frames": 8, "direction": "none", "zoom": "none",
                 "start_frame": 0, "end_frame": 8}
        plan = trial.validate({**self._manifest(), "scenes": [scene]}, self.root / "manifest.json")
        self.assertEqual(plan["frames"], 8)
        receipt_info = trial._check_video_window(plan["scenes"][0], plan["fps"])
        self.assertEqual(receipt_info["color_transfer"], "bt709")
        self.assertEqual(receipt_info["color_space"], "bt709")

    def test_rgb_swatches_are_actually_converted_to_bt709(self):
        image = self.root / "swatches.png"
        colors = [(0, 0, 0), (128, 128, 128), (255, 0, 0), (255, 255, 255)]
        source = Image.new("RGB", (128, 64))
        draw = ImageDraw.Draw(source)
        for index, color in enumerate(colors):
            draw.rectangle((index * 32, 0, index * 32 + 31, 63), fill=color)
        source.save(image)
        manifest = self._manifest()
        manifest["canvas"] = [128, 64]
        manifest["scenes"] = [{"id": "swatches", "type": "image", "source": image.name,
                               "source_sha256": digest(image), "start_frame": 0, "end_frame": 10,
                               "direction": "none", "zoom": "none",
                               "camera": self._camera(1.0, 1.0)}]
        path = self._write_manifest(manifest)
        output = self.root / "swatches.mp4"
        trial.render(path, output)
        decoded = subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-protocol_whitelist",
                                  "file,pipe", "-format_whitelist", "mov", "-i", str(output),
                                  "-frames:v", "1", "-f", "rawvideo", "-pix_fmt", "rgb24", "pipe:1"],
                                 check=True, stdin=subprocess.DEVNULL, capture_output=True).stdout
        expected_gray = round(255 * (1.099 * (((128 / 255 + 0.055) / 1.055) ** 2.4) ** 0.45 - 0.099))
        expected = [(0, 0, 0), (expected_gray,) * 3, (255, 0, 0), (255, 255, 255)]
        for index, rgb in enumerate(expected):
            offset = (32 * 32 + index * 32 + 16) * 3
            observed = tuple(decoded[offset:offset + 3])
            self.assertLessEqual(max(abs(a - b) for a, b in zip(observed, rgb)), 8,
                                 f"swatch {index}: expected {rgb}, observed {observed}")

    def test_unsupported_video_camera_fields_are_rejected(self):
        manifest = self._manifest()
        manifest["scenes"][1]["direction"] = "none"
        manifest["scenes"][1]["zoom"] = "none"
        manifest["scenes"][1]["camera"] = self._camera(1.0, 1.0)
        with self.assertRaisesRegex(trial.TrialError, "unsupported keys"):
            trial.validate(manifest, self.root / "manifest.json")

    def test_odd_sized_rgb_images_render_without_padding_or_color_shift(self):
        for size in ((95, 96), (96, 95), (95, 97)):
            with self.subTest(size=size):
                Image.new("RGB", size, (0, 255, 255)).save(self.image)
                manifest = self._manifest()
                manifest["scenes"] = [manifest["scenes"][0]]
                manifest["scenes"][0].update(zoom="none", camera=self._camera(1.0, 1.0))
                output = self.root / f"odd-{size[0]}-{size[1]}.mp4"
                receipt = trial.render(self._write_manifest(manifest), output)
                self.assertEqual(receipt["timeline"]["frames"], 8)
                decoded = subprocess.run([
                    "ffmpeg", "-v", "error", "-i", str(output), "-frames:v", "1",
                    "-f", "rawvideo", "-pix_fmt", "rgb24", "pipe:1",
                ], check=True, capture_output=True).stdout
                for x, y in ((0, 0), (63, 0), (0, 63), (63, 63), (32, 32)):
                    offset = (y * 64 + x) * 3
                    observed = tuple(decoded[offset:offset + 3])
                    self.assertLessEqual(max(abs(a - b) for a, b in zip(observed, (0, 255, 255))), 8)

    def test_unknown_image_parameter_is_rejected(self):
        manifest = self._manifest()
        manifest["scenes"][0]["motion_filter"] = "user supplied expression"
        with self.assertRaisesRegex(trial.TrialError, "unsupported keys"):
            trial.validate(manifest, self.root / "manifest.json")

    def test_provenance_hash_is_checked(self):
        manifest = self._manifest()
        manifest["provenance"]["script"]["sha256"] = "0" * 64
        with self.assertRaisesRegex(trial.TrialError, "hash mismatch"):
            trial.validate(manifest, self.root / "manifest.json")

    def test_unknown_video_color_metadata_is_rejected(self):
        manifest = self._manifest()
        manifest["scenes"][1]["source"] = self.image.name
        manifest["scenes"][1]["source_sha256"] = digest(self.image)
        path = self._write_manifest(manifest)
        with self.assertRaisesRegex(trial.TrialError, "unsupported or unknown SDR video color metadata"):
            trial.render(path, self.root / "unknown-color.mp4")
        self.assertFalse((self.root / "unknown-color.mp4").exists())

    def test_no_overwrite(self):
        manifest = self._write_manifest(self._manifest())
        output = self.root / "existing.mp4"
        output.write_bytes(b"keep")
        with self.assertRaisesRegex(trial.TrialError, "never overwrites"):
            trial.render(manifest, output)
        self.assertEqual(output.read_bytes(), b"keep")

    def test_atomic_publish_refuses_concurrent_output_and_receipt(self):
        temp_output = self.root / "temporary.mp4"
        temp_receipt = self.root / "temporary.json"
        temp_output.write_bytes(b"new video")
        temp_receipt.write_bytes(b"new receipt")
        output = self.root / "raced.mp4"
        receipt = Path(str(output) + ".montage_trial.json")
        output.write_bytes(b"concurrent output")
        with self.assertRaisesRegex(trial.TrialError, "appeared during render"):
            trial._publish_no_clobber(temp_output, temp_receipt, output, receipt)
        self.assertEqual(output.read_bytes(), b"concurrent output")
        output.unlink()
        receipt.write_bytes(b"concurrent receipt")
        with self.assertRaisesRegex(trial.TrialError, "appeared during render"):
            trial._publish_no_clobber(temp_output, temp_receipt, output, receipt)
        self.assertFalse(output.exists())
        self.assertEqual(receipt.read_bytes(), b"concurrent receipt")

    def test_manifest_mutation_during_preflight_fails(self):
        manifest = self._write_manifest(self._manifest())
        validate = trial.validate

        def mutate_after_parse(value, path):
            result = validate(value, path)
            path.write_text(path.read_text() + " ", encoding="utf-8")
            return result

        with patch.object(trial, "validate", side_effect=mutate_after_parse):
            with self.assertRaisesRegex(trial.TrialError, "manifest hash mismatch|manifest changed during preflight"):
                trial.render(manifest, self.root / "manifest-race.mp4")
        self.assertFalse((self.root / "manifest-race.mp4").exists())


if __name__ == "__main__":
    unittest.main()
