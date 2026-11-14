"""Real synthetic media verifies the music-first software path, never live creative QA."""
import copy
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

from PIL import ImageFont

from ytvideos.adapters.media import LocalMediaAdapter
from ytvideos.errors import WorkflowError
from ytvideos.media_checks import probe_media
from ytvideos.media_script import bind_requirements, read_script
from ytvideos.music_contract import (ENGINE, MANIFEST_SCHEMA, MIX_SCHEMA, file_record,
                                    helper, validate_plan)
from ytvideos.production_contract import production_requirements
from ytvideos.util import file_digest


ROOT = Path(__file__).resolve().parents[1]
FONT = Path("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf")


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value if isinstance(value, str) else json.dumps(value))
    return path


def ffmpeg(*args):
    return subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-n", *map(str, args)],
                          check=True, capture_output=True, timeout=90)


class MusicFixture:
    """A visibly named fixture profile; production never accepts the fixture font/canvas."""
    def __init__(self, directory, *, vocal=False, fade_out_seconds=None):
        directory = Path(directory).resolve()
        self.directory, self.project = directory, directory / "project"
        self.vocal = vocal
        for source in (ROOT / "src/ytvideos").glob("*.py"):
            destination = self.project / "src/ytvideos" / source.name
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, destination)
        for relative in {*ENGINE, "automation/audio_mix.py"}:
            path = self.project / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / relative, path)
        self.profile = json.loads((ROOT / "channels/nuviko_videos/channel.json").read_text())
        self.profile.update(status="active", name="Synthetic music-render software fixture", readiness_blockers=[])
        self.canvas = [1080, 1920] if vocal else [90, 160]
        self.profile["production"]["formats"]["short"]["video"]["canvas"] = self.canvas
        family, style = ImageFont.truetype(str(FONT), 16).getname()
        self.profile["production"]["captions"]["font"] = {"family": family, "style": style}
        self.profile_path = write(self.project / "channels/nuviko_videos/channel.json", self.profile)
        self.variant = "vocal" if vocal else "instrumental"
        self.text = "Stay here" if vocal else ""
        self.script_path = write(directory / "accepted-edit.json", {
            "schema": "ytv-edit-script-v1", "production_variant": self.variant,
            "intent": "Synthetic regression: two independent source patterns reveal a cut; no creative review is asserted.",
            "speech": {"mode": "source" if vocal else "none", "text": self.text},
            "segments": [{"id": "s0", "description": "Synthetic pattern opens the edit", "spoken_text": "Stay" if vocal else ""},
                         {"id": "s1", "description": "A different pattern reveals the change", "spoken_text": "here" if vocal else ""}]})
        self.script = read_script(self.script_path, self.profile, "short")
        self.script["artifact_sha256"] = file_digest(self.script_path)
        self.requirements = bind_requirements(production_requirements(self.profile, "short", variant=self.variant), self.script)
        self.rights = write(directory / "rights.txt", "All footage and music here are synthetic local software test fixtures.")
        self.source_track = directory / "original-recording.wav"
        ffmpeg("-f", "lavfi", "-i", "sine=frequency=440:sample_rate=48000:duration=1.5", self.source_track)
        self.source_plan = write(directory / "source-audio.json", {"schema": "ytv-source-audio-v1", "segments": [
            {"id": "s0", **file_record(self.source_track), "start_seconds": .1, "end_seconds": .5, "gain": 1},
            {"id": "s1", **file_record(self.source_track), "start_seconds": .5, "end_seconds": .9, "gain": 1}]})
        if fade_out_seconds is not None:
            value = json.loads(self.source_plan.read_text())
            write(self.source_plan, {**value, "fade_out_seconds": fade_out_seconds})
        self.audio = directory / "mix.wav"
        receipt_path = directory / "mix-execution.json"
        self.mix_execution = LocalMediaAdapter(self.project, guard=lambda request: None, clock=lambda: 1000).execute(
            "mix", [str(self.source_plan), "--output", str(self.audio)], run_id="synthetic-run", task_id="audio",
            claim={"token": "synthetic-claim", "expires_at": 2000, "input_hash": "synthetic-input"}, input_hash="synthetic-input",
            inputs=[file_record(self.source_plan), file_record(self.source_track)], outputs=[self.audio], receipt_path=receipt_path)
        if self.mix_execution["state"] != "completed":
            raise AssertionError(self.mix_execution)
        self.mix_proof = write(directory / "mix-evidence.json", {"schema": MIX_SCHEMA, "audio_sha256": file_digest(self.audio),
            "track_sha256": [file_digest(self.source_track)], "returncode": 0, "argv": self.mix_execution["argv"],
            "execution": file_record(receipt_path), "source_plan": file_record(self.source_plan)})
        self.originals, self.clips = [], []
        for index, frames in enumerate((14, 13)):
            original, clip = directory / f"original-{index}.mp4", directory / f"clip-{index}.mp4"
            color = "0x303050" if index == 0 else "0x705030"
            ffmpeg("-f", "lavfi", "-i", f"color={color}:s=90x160:r=30:d=1,drawbox=x=20:y=35:w=14:h=90:color=white:t=fill",
                   "-an", "-c:v", "libx264", "-pix_fmt", "yuv420p", original)
            ffmpeg("-ss", "0.1", "-i", original, "-frames:v", frames, "-an", "-c:v", "libx264", "-pix_fmt", "yuv420p", clip)
            self.originals.append(original)
            self.clips.append(clip)
        accent_evidence = write(directory / "accent-evidence.txt", "Synthetic test cut selected at frame 12; no listening claim.")
        planner = {"media": str(self.audio), "fps": 30, "frames": 24, "pulse": None,
                   "profile": {"holds": [.4], "min": .35, "max": .45, "opening_max": .45, "required": [12]},
                   "approved_accents": [{"frame": 12, "attack_seconds": .4, "strength": 3,
                                         "reason": "Synthetic fixed-cut regression", "evidence": file_record(accent_evidence)}],
                   "shots": [{"id": f"s{index}", "path": str(path), "source_in": .1, "max_seconds": .8,
                              "scale": "wide" if index == 0 else "close", "subject": str(index),
                              "motion": "active", "priority": 1} for index, path in enumerate(self.originals)],
                   "first": "s0", "last": "s1"}
        planner_input = write(directory / "planner-input.json", planner)
        planner_output = write(directory / "planner-output.json", helper(self.project, "automation/music_montage.py", "test_music_planner").plan_timeline(planner))
        policy = self.requirements["music_edit"]
        self.plan = {"schema": MANIFEST_SCHEMA, "channel": "nuviko_videos", "format": "short", "purpose": "production",
                     "production_variant": self.variant, "canvas": self.canvas, "fps": 30, "has_speech": vocal,
                     "script": str(self.script_path), "audio": str(self.audio), "color": policy["color"],
                     "transition": {**policy["transition"], "blur_sigma_px": 3, "brightness": .08},
                     "planner": {"input": file_record(planner_input), "output": file_record(planner_output)},
                     "music": {"status": "present", "tracks": [{**file_record(self.source_track), "source_in_seconds": .1,
                                "start_frame": 0, "end_frame": 24}], "mix_evidence": file_record(self.mix_proof),
                               "rights_evidence": file_record(self.rights)},
                     "subtitles": {"mode": "none"}, "scenes": []}
        for index, frames in enumerate((14, 13)):
            self.plan["scenes"].append({"id": f"s{index}", "clip": str(self.clips[index]), "start_frame": index * 12,
                "end_frame": (index + 1) * 12, "direction": "none", "zoom": "in" if index == 0 else "out",
                "scale": policy["zoom"] if index == 0 else list(reversed(policy["zoom"])), "easing": "smoothstep",
                "source": {**file_record(self.originals[index]), "start_seconds": .1, "end_seconds": .1 + frames / 30,
                           "rights_evidence": file_record(self.rights)}})
        if vocal:
            word_map = write(directory / "words.json", {"audio_sha256": file_digest(self.audio),
                "transcript_sha256": hashlib.sha256(self.text.encode()).hexdigest(),
                "words": [{"text": "Stay", "start_seconds": .03, "end_seconds": .3},
                          {"text": "here", "start_seconds": .4, "end_seconds": .73}]})
            self.plan["subtitles"] = {"mode": "lyrics", "words": file_record(word_map),
                                       "font": {**file_record(FONT), "index": 0}, "settings": policy["lyrics"]}
            self.plan["srt"] = str(write(directory / "manual.srt", "1\n00:00:00,030 --> 00:00:00,730\nStay here\n"))
        self.manifest = write(directory / "manifest.json", self.plan)
        self.renderer = helper(self.project, "automation/music_render.py", "test_music_renderer")

    def validate(self, plan):
        return validate_plan(plan, self.requirements, base=self.directory, project=self.project, script=self.script)


@unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe") and FONT.exists(), "requires local FFmpeg and fixture font")
class MusicRenderTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temporary = tempfile.TemporaryDirectory()
        cls.addClassCleanup(cls.temporary.cleanup)
        cls.fixture = MusicFixture(Path(cls.temporary.name))
        cls.output = cls.fixture.directory / "final.mp4"
        cls.delivery = cls.fixture.renderer.render(cls.fixture.manifest, cls.output, cls.fixture.directory / "work",
                                                   cls.fixture.requirements, project=cls.fixture.project)

    def test_actual_instrumental_export_and_journal_bind_original_intervals(self):
        f = self.fixture
        measured = probe_media(self.output)
        self.assertEqual(int(measured["video"][0]["nb_frames"]), 24)
        self.assertEqual(measured["video"][0]["codec"], "h264")
        self.assertEqual(measured["audio"][0]["codec"], "aac")
        self.assertEqual(self.delivery["review_status"], "UNVERIFIED")
        records = f.renderer.validate_receipt(str(self.output) + ".delivery.json", f.plan, f.requirements,
                                               self.output, project=f.project)
        self.assertIn(file_record(f.originals[0]), records)
        journal = json.loads(Path(self.delivery["fragments"]["path"]).read_text())[0]
        self.assertEqual(journal["sha256"], file_digest(self.output))
        self.assertEqual(journal["audio"]["source_sha256"], file_digest(f.source_track))
        self.assertEqual(journal["audio"]["source_in_seconds"], .1)
        self.assertEqual(journal["video"][1]["visible_timeline_frames"], [11, 24])
        self.assertFalse(list(f.directory.glob("*.srt")))

    def test_final_rgb_conversion_uses_rec709_samples_not_only_tags(self):
        data = subprocess.check_output(["ffmpeg", "-nostdin", "-v", "error", "-f", "lavfi", "-i",
            "nullsrc=s=16x16,format=gbrp,geq=r=255:g=0:b=0", "-vf", self.fixture.renderer.final_color_filter(),
            "-frames:v", "1", "-f", "rawvideo", "-pix_fmt", "yuv420p", "-"])
        # Limited-range BT.709 red is Y≈63, Cb≈102, Cr≈240. BT.601 is 81/90/240.
        self.assertEqual([data[0], data[16 * 16], data[16 * 16 + 8 * 8]], [63, 102, 240])

    def test_static_color_transition_and_wrong_format_shortcuts_are_rejected(self):
        cases = {
            "static": lambda p: p["scenes"][0].update(zoom="none"),
            "wrong_zoom": lambda p: p["scenes"][0].update(scale=[1, 1.05]),
            "stepped_motion": lambda p: p["scenes"][0].update(easing="integer_crop"),
            "no_fade": lambda p: p["transition"].update(components=["gaussian_blur", "brightness"]),
            "old_transition": lambda p: p["transition"].update(duration_frames=12),
            "wrong_beat_weight": lambda p: p["transition"].update(peak_incoming=.5),
            "no_blur": lambda p: p["transition"].update(blur_sigma_px=0),
            "no_brightness": lambda p: p["transition"].update(brightness=0),
            "missing_color": lambda p: p.update(color={"contrast": 1, "saturation": 1}),
            "wrong_canvas": lambda p: p.update(canvas=[1080, 1920]),
            "invented_captions": lambda p: p.update(subtitles={"mode": "lyrics"}),
            "wrong_variant": lambda p: p.update(production_variant="vocal"),
        }
        for name, edit in cases.items():
            with self.subTest(name=name), self.assertRaises(WorkflowError):
                plan = copy.deepcopy(self.fixture.plan)
                edit(plan)
                self.fixture.validate(plan)

    def test_ordered_sources_stale_planner_and_fabricated_mix_are_rejected(self):
        f = self.fixture
        plan = copy.deepcopy(f.plan)
        plan["scenes"][0]["source"] = plan["scenes"][1]["source"]
        with self.assertRaises(WorkflowError):
            f.validate(plan)
        plan = copy.deepcopy(f.plan)
        plan["scenes"][0]["id"], plan["scenes"][1]["id"] = "s1", "s0"
        with self.assertRaisesRegex(WorkflowError, "ordered"):
            f.validate(plan)
        plan = copy.deepcopy(f.plan)
        altered = json.loads(Path(plan["planner"]["output"]["path"]).read_text())
        altered["accents"][0]["frame"] = 13
        plan["planner"]["output"] = file_record(write(f.directory / "wrong-planner.json", altered))
        with self.assertRaisesRegex(WorkflowError, "stale"):
            f.validate(plan)
        plan = copy.deepcopy(f.plan)
        plan["music"]["mix_evidence"] = file_record(write(f.directory / "fake-mix.json", {"audio_sha256": file_digest(f.audio), "returncode": 0}))
        with self.assertRaisesRegex(WorkflowError, "mix must bind"):
            f.validate(plan)

    def test_production_music_policy_is_complete_only_for_explicit_supported_variant(self):
        profile = json.loads((ROOT / "channels/nuviko_videos/channel.json").read_text())
        self.assertTrue(production_requirements(profile, "short", variant="vocal")["configured"])
        self.assertTrue(production_requirements(profile, "short", variant="instrumental")["configured"])
        self.assertIn("production_variant", production_requirements(profile, "short")["unresolved"])
        self.assertFalse(production_requirements(profile, "long")["configured"])
        path = write(self.fixture.directory / "fake-narration.txt", "Invented narration. " * 40)
        with self.assertRaisesRegex(WorkflowError, "never narration"):
            read_script(path, profile, "short")

    def test_canonical_beat_cli_emits_bound_full_frame_count(self):
        f = self.fixture
        source, output = f.directory / "beat-cli-audio.wav", f.directory / "beat-cli-output.json"
        ffmpeg("-f", "lavfi", "-i", "sine=frequency=440:sample_rate=48000:duration=3.2", source)
        import sys
        subprocess.run([sys.executable, str(f.project / "automation/music_beats.py"), str(source),
                        "--fps", "30", "--output", str(output)], check=True, capture_output=True, timeout=30)
        data = json.loads(output.read_text())
        self.assertEqual(data["sha256"], file_digest(source))
        self.assertEqual((data["fps"], data["frames"], data["source_start_seconds"]), (30, 96, 0))
        self.assertTrue(all(0 <= item["frame"] < data["frames"] for item in data["candidates"]))

    def test_receipt_cannot_substitute_changed_command_or_another_export(self):
        f = self.fixture
        altered = copy.deepcopy(self.delivery)
        command = json.loads(Path(altered["command"]["path"]).read_text())
        command[command.index("-crf") + 1] = "40"
        altered["command"] = file_record(write(f.directory / "work/changed-command.json", command))
        receipt = write(f.directory / "changed-receipt.json", altered)
        with self.assertRaisesRegex(WorkflowError, "composition effects"):
            f.renderer.validate_receipt(receipt, f.plan, f.requirements, self.output, project=f.project)
        other = f.directory / "changed-output.mp4"
        other.write_bytes(self.output.read_bytes() + b"changed")
        with self.assertRaisesRegex(WorkflowError, "exact production output"):
            f.renderer.validate_receipt(str(self.output) + ".delivery.json", f.plan, f.requirements, other, project=f.project)

    def test_real_transition_has_brightness_and_blur_and_motion_changes_every_shot(self):
        import numpy as np
        f = self.fixture
        prepared = f.validate(f.plan)
        reference_plan = copy.deepcopy(f.plan)
        reference_plan["transition"].update(blur_sigma_px=0, brightness=0)
        reference = f.directory / "test-only-no-effects.mp4"
        # Deliberately bypass the manifest validator only for a measurement reference;
        # this file has no production receipt and is never accepted by the runtime.
        command = f.renderer.build_command(reference_plan, prepared, f.requirements, f.directory / "work", reference)
        subprocess.run(command, check=True, capture_output=True, timeout=90)
        def pixels(path):
            data = subprocess.check_output(["ffmpeg", "-nostdin", "-v", "error", "-i", str(path), "-f", "rawvideo", "-pix_fmt", "rgb24", "-"])
            return np.frombuffer(data, np.uint8).reshape((24, 160, 90, 3)).astype(float)
        actual, baseline = pixels(self.output), pixels(reference)
        # .08 brightness is about 20 luma code values; broad codec/color conversion tolerance.
        self.assertGreater((actual[12] - baseline[12]).mean(), 10)
        self.assertLess(np.abs(np.diff(actual[12], axis=1)).sum(), np.abs(np.diff(baseline[12], axis=1)).sum())
        self.assertLess(np.abs(actual[10] - baseline[10]).mean(), 2)
        self.assertLess(np.abs(actual[14] - baseline[14]).mean(), 2)
        self.assertGreater(np.abs(actual[1] - actual[9]).mean(), 1)
        self.assertGreater(np.abs(actual[15] - actual[23]).mean(), 1)


@unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe") and FONT.exists(), "requires local FFmpeg and fixture font")
class MusicVocalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temporary = tempfile.TemporaryDirectory()
        cls.addClassCleanup(cls.temporary.cleanup)
        cls.fixture = MusicFixture(Path(cls.temporary.name), vocal=True)

    def test_actual_vocal_masks_keep_every_word_and_pinned_recipe(self):
        f = self.fixture
        output = f.directory / "vocal.mp4"
        receipt = f.renderer.render(f.manifest, output, f.directory / "work", f.requirements, project=f.project)
        f.renderer.validate_receipt(str(output) + ".delivery.json", f.plan, f.requirements, output, project=f.project)
        lyric = json.loads(Path(receipt["lyrics"]["plan"]["path"]).read_text())
        self.assertEqual([word["text"] for group in lyric["groups"] for word in group["words"]], ["Stay", "here"])
        self.assertEqual(lyric["groups"][0]["end_frame_exclusive"], 12)
        self.assertEqual(lyric["font_size_px"], 147)
        self.assertEqual(lyric["color_mode"], "inversion_masks")
        self.assertEqual(probe_media(output)["video"][0]["height"], 1920)

    def test_actual_wrong_font_and_incomplete_or_zero_length_words_are_rejected(self):
        f = self.fixture
        production = json.loads((ROOT / "channels/nuviko_videos/channel.json").read_text())
        requirements = bind_requirements(production_requirements(production, "short", variant="vocal"), f.script)
        with self.assertRaisesRegex(WorkflowError, "brand face"):
            validate_plan(f.plan, requirements, base=f.directory, project=f.project, script=f.script)
        for name, entries in (("missing", [{"text": "Stay", "start_seconds": .03, "end_seconds": .3}]),
                              ("rounded_zero", [{"text": "Stay", "start_seconds": .01, "end_seconds": .011},
                                                {"text": "here", "start_seconds": .4, "end_seconds": .73}])):
            plan = copy.deepcopy(f.plan)
            words = json.loads(Path(plan["subtitles"]["words"]["path"]).read_text())
            words["words"] = entries
            plan["subtitles"]["words"] = file_record(write(f.directory / (name + ".json"), words))
            with self.subTest(name=name), self.assertRaises(WorkflowError):
                f.validate(plan)

    def test_numeric_lyrics_remain_exact_ordered_words(self):
        f = self.fixture
        value = json.loads(f.script_path.read_text())
        value["speech"]["text"] = "0 1 2"
        value["segments"][0]["spoken_text"], value["segments"][1]["spoken_text"] = "0 1", "2"
        script_path = write(f.directory / "numeric-script.json", value)
        script = read_script(script_path, f.profile, "short") | {"artifact_sha256": file_digest(script_path)}
        requirements = bind_requirements(production_requirements(f.profile, "short", variant="vocal"), script)
        plan = copy.deepcopy(f.plan)
        plan["script"] = str(script_path)
        words = {"audio_sha256": file_digest(f.audio), "transcript_sha256": hashlib.sha256(b"0 1 2").hexdigest(),
                 "words": [{"text": str(index), "start_seconds": .03 + index * .2, "end_seconds": .18 + index * .2}
                           for index in range(3)]}
        word_path = write(f.directory / "numeric-words.json", words)
        plan["subtitles"]["words"] = file_record(word_path)
        prepared = validate_plan(plan, requirements, base=f.directory, project=f.project, script=script)
        lyrics = helper(f.project, "automation/captions/music_lyrics.py", "numeric_lyric_helper")
        loaded = lyrics.load_words(words, 0, 30, prepared["frames"])
        self.assertEqual([word["text"] for word in loaded], ["0", "1", "2"])
        words["words"][0]["text"], words["words"][1]["text"] = "1", "0"
        write(word_path, words)
        plan["subtitles"]["words"] = file_record(word_path)
        with self.assertRaisesRegex(WorkflowError, "omit, change or invent"):
            validate_plan(plan, requirements, base=f.directory, project=f.project, script=script)

    def beat_plan(self, name):
        f = self.fixture
        plan = copy.deepcopy(f.plan)
        words = json.loads(Path(plan["subtitles"]["words"]["path"]).read_text())
        # Word one rounds to frame1 and snaps to extra beat2. Word two rounds to11;
        # cut12 must win even though the additional beat11 is closer.
        words["words"][1]["start_seconds"] = .34
        plan["subtitles"]["words"] = file_record(write(f.directory / (name + "-words.json"), words))
        beats = {"source": str(f.audio), "sha256": file_digest(f.audio), "fps": 30, "frames": 24,
                 "source_start_seconds": 0, "duration_seconds": .8, "status": "synthetic_signal_candidates",
                 "candidates": [{"frame": 2}, {"frame": 11}]}
        plan["subtitles"]["beats"] = file_record(write(f.directory / (name + "-beats.json"), beats))
        return plan, beats

    def test_additional_beats_are_rendered_bound_and_cut_priority_is_preserved(self):
        f = self.fixture
        plan, _ = self.beat_plan("with-beats")
        manifest = write(f.directory / "with-beats.json", plan)
        output, work = f.directory / "with-beats.mp4", f.directory / "with-beats-work"
        receipt = f.renderer.render(manifest, output, work, f.requirements, project=f.project)
        records = f.renderer.validate_receipt(str(output) + ".delivery.json", plan, f.requirements, output, project=f.project)
        self.assertIn(plan["subtitles"]["beats"], records)
        command = receipt["lyrics"]["command"]
        self.assertEqual(command[command.index("--beats") + 1], plan["subtitles"]["beats"]["path"])
        lyric = json.loads(Path(receipt["lyrics"]["plan"]["path"]).read_text())
        self.assertEqual(lyric["beat_snaps"], {"1": 2, "11": 12})
        self.assertEqual([group["start_frame"] for group in lyric["groups"]], [2, 12])
        omitted_command = copy.deepcopy(receipt)
        index = omitted_command["lyrics"]["command"].index("--beats")
        del omitted_command["lyrics"]["command"][index:index + 2]
        path = write(f.directory / "ignored-beats-command.json", omitted_command)
        with self.assertRaisesRegex(WorkflowError, "canonical one-word lyric execution"):
            f.renderer.validate_receipt(path, plan, f.requirements, output, project=f.project)
        ignored_plan = copy.deepcopy(receipt)
        lyric["beat_snaps"].pop("1")
        ignored_plan["lyrics"]["plan"] = file_record(write(work / "ignored-beats-plan.json", lyric))
        path = write(f.directory / "ignored-beats-result.json", ignored_plan)
        with self.assertRaisesRegex(WorkflowError, "animation recipe"):
            f.renderer.validate_receipt(path, plan, f.requirements, output, project=f.project)

    def test_stale_wrong_audio_or_invalid_extra_beat_map_is_rejected(self):
        f = self.fixture
        plan, beats = self.beat_plan("invalid-map")
        path = Path(plan["subtitles"]["beats"]["path"])
        path.write_text(path.read_text() + "\n")
        with self.assertRaisesRegex(WorkflowError, "input changed"):
            f.validate(plan)
        for name, value in (("sha256", "0" * 64), ("fps", 24), ("frames", 25),
                            ("source_start_seconds", 1), ("duration_seconds", .9),
                            ("candidates", [{"frame": 24}]), ("candidates", [{"frame": True}]),
                            ("candidates", [{"frame": 11}, {"frame": 2}])):
            changed = copy.deepcopy(beats)
            changed[name] = value
            write(path, changed)
            plan["subtitles"]["beats"] = file_record(path)
            with self.subTest(name=name, value=value), self.assertRaises(WorkflowError):
                f.validate(plan)
        plan = copy.deepcopy(f.plan)
        plan["subtitles"]["unrecognized_beat_option"] = []
        with self.assertRaisesRegex(WorkflowError, "unsupported settings"):
            f.validate(plan)


@unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe") and FONT.exists(), "requires local FFmpeg and fixture font")
class MusicEndingTests(unittest.TestCase):
    def test_explicit_fade_retains_continuous_recording_and_native_render_provenance(self):
        with tempfile.TemporaryDirectory() as temporary:
            f = MusicFixture(Path(temporary), fade_out_seconds=.2)
            prepared = f.validate(f.plan)
            self.assertEqual(prepared["fade_out_seconds"], .2)
            output = f.directory / "faded.mp4"
            receipt = f.renderer.render(f.manifest, output, f.directory / "faded-work", f.requirements, project=f.project)
            f.renderer.validate_receipt(str(output) + ".delivery.json", f.plan, f.requirements, output, project=f.project)
            ending = json.loads(Path(receipt["fragment_contract"]["path"]).read_text())["ending"]
            self.assertEqual(ending, {"source_end_seconds": .9, "fade_out_seconds": .2})
            self.assertAlmostEqual(float(probe_media(output)["audio"][0]["duration"]), .8, places=3)
            from ytvideos.music_contract import validate_mix
            for field, value in (("gain", .8), ("start_seconds", .51)):
                source_plan = json.loads(f.source_plan.read_text())
                source_plan["segments"][1][field] = value
                plan_path = write(f.directory / (field + "-invalid-plan.json"), source_plan)
                proof = json.loads(f.mix_proof.read_text())
                execution = copy.deepcopy(f.mix_execution)
                execution["argv"][2] = str(plan_path)
                proof.update(source_plan=file_record(plan_path), argv=execution["argv"],
                             execution=file_record(write(f.directory / (field + "-execution.json"), execution)))
                record = file_record(write(f.directory / (field + "-mix.json"), proof))
                with self.subTest(field=field), self.assertRaisesRegex(WorkflowError, "continuous accepted excerpt"):
                    validate_mix(record, audio_sha256=file_digest(f.audio), track=f.plan["music"]["tracks"][0], project=f.project)

    def test_mismatched_native_mix_duration_is_rejected_before_picture_encoding(self):
        with tempfile.TemporaryDirectory() as temporary:
            f = MusicFixture(Path(temporary))
            short = f.directory / "short.wav"
            ffmpeg("-i", f.audio, "-t", "0.4", short)
            execution = copy.deepcopy(f.mix_execution)
            execution["argv"][-1] = str(short)
            execution["outputs"] = [str(short)]
            execution["output_artifacts"] = [file_record(short)]
            proof = json.loads(f.mix_proof.read_text())
            proof.update(audio_sha256=file_digest(short), argv=execution["argv"],
                         execution=file_record(write(f.directory / "short-execution.json", execution)))
            plan = copy.deepcopy(f.plan)
            plan["audio"] = str(short)
            plan["music"]["mix_evidence"] = file_record(write(f.directory / "short-mix.json", proof))
            with self.assertRaisesRegex(WorkflowError, "complete source excerpt"):
                f.validate(plan)


if __name__ == "__main__":
    unittest.main()
