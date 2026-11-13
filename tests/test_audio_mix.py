"""Real offline audio checks for complete source intervals and an explicit terminal fade."""
import copy
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
from unittest.mock import patch
import wave

import numpy as np

from ytvideos.music_contract import file_record, helper


ROOT = Path(__file__).resolve().parents[1]


@unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe"), "requires local FFmpeg")
class SourceAudioTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.directory = Path(temporary.name)
        self.mixer = helper(ROOT, "automation/audio_mix.py", "test_source_audio_mix")
        self.source = self.directory / "source.wav"
        self.ffmpeg("-f", "lavfi", "-i", "sine=frequency=440:sample_rate=48000:duration=1", self.source)
        self.plan = {"schema": "ytv-source-audio-v1", "segments": [
            {"id": "first", **file_record(self.source), "start_seconds": .1, "end_seconds": .5, "gain": 1},
            {"id": "second", **file_record(self.source), "start_seconds": .5, "end_seconds": .9, "gain": 1}]}

    def ffmpeg(self, *args):
        subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-n", *map(str, args)],
                       check=True, capture_output=True, timeout=30)

    def render(self, plan, name):
        manifest, output = self.directory / (name + ".json"), self.directory / (name + ".wav")
        manifest.write_text(json.dumps(plan))
        self.mixer.render(manifest, output)
        with wave.open(str(output)) as stream:
            return np.frombuffer(stream.readframes(stream.getnframes()), "<i2").reshape(-1, stream.getnchannels())

    def test_selected_terminal_fade_preserves_phase_prefix_and_duration(self):
        plain = self.render(self.plan, "plain")
        unchanged = self.render({**self.plan, "fade_out_seconds": 0}, "natural-tail")
        faded = self.render({**self.plan, "fade_out_seconds": .2}, "selected-fade")
        self.assertTrue(np.array_equal(plain, unchanged))
        self.assertEqual(plain.shape, faded.shape)
        self.assertEqual(len(faded), 38400)
        self.assertTrue(np.array_equal(plain[:28800], faded[:28800]))
        self.assertLess(np.sqrt(np.mean(faded[-2400:].astype(float) ** 2)),
                        .2 * np.sqrt(np.mean(plain[-2400:].astype(float) ** 2)))
        self.assertLessEqual(int(np.max(abs(faded[-1]))), 1)

    def test_fade_rejects_nonfinite_bool_negative_or_longer_than_mix(self):
        for value in (True, -1, .801, float("nan"), float("inf"), "0.2", None):
            with self.subTest(value=value), self.assertRaisesRegex(ValueError, "terminal fade"):
                self.mixer.validate_plan({**self.plan, "fade_out_seconds": value}, self.directory)

    def test_video_container_duration_cannot_extend_its_shorter_audio(self):
        source = self.directory / "short-audio-long-video.mp4"
        self.ffmpeg("-f", "lavfi", "-i", "color=black:s=16x16:r=30:d=1.5", "-f", "lavfi", "-i",
                    "sine=frequency=440:sample_rate=48000:duration=0.5", "-c:v", "libx264", "-c:a", "aac", source)
        plan = copy.deepcopy(self.plan)
        for segment in plan["segments"]:
            segment.update(file_record(source))
        with self.assertRaisesRegex(ValueError, "actual audio stream"):
            self.render(plan, "invalid-source")
        self.assertFalse((self.directory / "invalid-source.wav").exists())

    def test_missing_stream_duration_still_checks_the_actual_mixed_samples(self):
        # A demuxer without stream.duration must not fall back to a longer
        # container. Keep real FFmpeg extraction and the final WAV measurement.
        plan = copy.deepcopy(self.plan)
        plan["segments"][-1]["end_seconds"] = 1.4
        original_run = subprocess.run
        def no_source_duration(command, **kwargs):
            result = original_run(command, **kwargs)
            if command[0] == "ffprobe" and Path(command[-1]).resolve() == self.source.resolve():
                value = json.loads(result.stdout)
                value["streams"][0].pop("duration", None)
                result.stdout = json.dumps(value)
            return result
        with patch.object(self.mixer.subprocess, "run", side_effect=no_source_duration):
            with self.assertRaisesRegex(ValueError, "complete requested intervals"):
                self.render(plan, "missing-duration")


if __name__ == "__main__":
    unittest.main()
