"""Production delivery regressions using real, deliberately inadequate media."""
import json
import copy
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

from ytvideos.errors import WorkflowError
from ytvideos.media_checks import probe_media, validate_font_face
from ytvideos.production_contract import (production_requirements, validate_delivery_summary,
                                         validate_render_manifest, validate_review_observation)
from ytvideos.service import Production
from ytvideos.store import Store
from ytvideos.util import file_digest


ROOT = Path(__file__).resolve().parents[1]


class ProductionContractTests(unittest.TestCase):
    def setUp(self):
        self.profile = json.loads((ROOT / "channels/paper_detour/channel.json").read_text())

    def manifest(self, format="short"):
        plan = {"channel": self.profile["id"], "format": format, "audio": "accepted-mix.wav", "srt": "accepted.srt",
                "subtitles": {"mode": "words"}, "transitions": "direct_cuts",
                "scenes": [{"image": "first.png", "start_frame": 0, "end_frame": 120,
                            "direction": "left_to_right", "zoom": "in"}],
                "music": {"status": "present", "tracks": [{"path": "music.wav", "sha256": "1" * 64,
                            "start_frame": 0, "end_frame": 120}],
                          "mix_evidence": {"path": "mix.json", "sha256": "2" * 64}}}
        if format == "long":
            plan["scenes"].append({"image": "end.png", "start_frame": 120, "end_frame": 420,
                                   "role": "end_screen", "direction": "none", "zoom": "none"})
            plan["music"]["tracks"][0]["end_frame"] = 420
        return plan

    def test_resolved_manifest_and_explicit_music_pause_are_valid(self):
        requirements = production_requirements(self.profile, "short")
        plan = self.manifest()
        plan["music"]["tracks"][0]["end_frame"] = 110
        plan["music"]["silences"] = [{"start_frame": 110, "end_frame": 120,
                                       "reason": "Deliberate complete silence for the final visual beat."}]
        self.assertEqual(validate_render_manifest(plan, requirements)["duration_seconds"], 4)

    def test_channel_format_fps_canvas_and_probe_cannot_override_pinned_policy(self):
        requirements = production_requirements(self.profile, "short")
        for field, value in [("channel", "another_channel"), ("format", "long"), ("fps", 24),
                             ("canvas", [1080, 1920]), ("purpose", "technical_probe")]:
            with self.subTest(field=field), self.assertRaises(WorkflowError):
                validate_render_manifest({**self.manifest(), field: value}, requirements)

    def test_unsupported_paid_motion_input_cannot_be_silently_rendered_as_still(self):
        for channel in ("paper_detour", "nuviko_history"):
            profile = json.loads((ROOT / "channels" / channel / "channel.json").read_text())
            for field, value in (("motion_clip", "/synthetic/paid-flow.mp4"), ("motion_clip", None),
                                 ("clip", "/synthetic/paid-flow.mp4")):
                plan = self.manifest()
                plan["channel"] = channel
                plan["scenes"][0][field] = value
                with self.subTest(channel=channel, field=field, value=value), self.assertRaisesRegex(WorkflowError, "unsupported motion inputs"):
                    validate_render_manifest(plan, production_requirements(profile, "short"))

    def test_static_scene_missing_word_captions_or_music_coverage_fail(self):
        requirements = production_requirements(self.profile, "short")
        for defect in ("static", "vertical", "captions", "music", "gap"):
            plan = self.manifest()
            if defect == "static":
                plan["scenes"][0].update(direction="none", zoom="none")
            elif defect == "vertical":
                plan["scenes"][0]["direction"] = "top_to_bottom"
            elif defect == "captions":
                plan["subtitles"]["mode"] = "none"
            elif defect == "music":
                del plan["music"]
            else:
                plan["music"]["tracks"][0]["end_frame"] = 119
            with self.subTest(defect=defect), self.assertRaises(WorkflowError):
                validate_render_manifest(plan, requirements)

    def test_current_no_frame_policy_includes_legacy_role(self):
        for role in ("decorative_frame", "paper_frame", "frame"):
            plan = self.manifest()
            plan["overlays"] = [{"role": role, "path": "two-lines.png", "sha256": "3" * 64,
                                  "start_frame": 0, "end_frame": 120}]
            with self.subTest(role=role), self.assertRaisesRegex(WorkflowError, "forbids"):
                validate_render_manifest(plan, production_requirements(self.profile, "short"))

    def test_required_brand_asset_cannot_be_replaced_with_drawn_lines(self):
        profile = copy.deepcopy(self.profile)
        profile["production"]["visual"].update(decorative_frame="required",
            frame_asset={"path": "approved-brand.webm", "sha256": "4" * 64})
        plan = self.manifest()
        plan["overlays"] = [{"role": "decorative_frame", "path": "two-lines.png", "sha256": "3" * 64,
                              "start_frame": 0, "end_frame": 120}]
        with self.assertRaisesRegex(WorkflowError, "exact approved asset"):
            validate_render_manifest(plan, production_requirements(profile, "short"))
        plan["overlays"][0].update(path="approved-brand.webm", sha256="4" * 64)
        validate_render_manifest(plan, production_requirements(profile, "short"))

    def test_end_screen_is_exact_and_format_specific(self):
        validate_render_manifest(self.manifest("long"), production_requirements(self.profile, "long"))
        plan = self.manifest("long")
        plan["scenes"][-1]["end_frame"] -= 1
        with self.assertRaisesRegex(WorkflowError, "end-screen"):
            validate_render_manifest(plan, production_requirements(self.profile, "long"))
        plan = self.manifest()
        plan["scenes"][0]["role"] = "end_screen"
        with self.assertRaisesRegex(WorkflowError, "no end-screen"):
            validate_render_manifest(plan, production_requirements(self.profile, "short"))

    def test_variant_and_unconfigured_profile_never_pick_arbitrary_defaults(self):
        profile = json.loads((ROOT / "channels/scenes_on_repeat/channel.json").read_text())
        for variant in (None, "invented"):
            requirements = production_requirements(profile, "short", variant=variant)
            self.assertFalse(requirements["configured"])
            self.assertIn("production_variant", requirements["unresolved"])
        self.assertEqual(production_requirements(profile, "short", variant="scene")["video"]["fps"], "24/1")
        self.assertEqual(production_requirements(profile, "short", variant="meme_time_machine")["video"]["fps"], "48/1")
        self.assertFalse(production_requirements(profile, "long")["configured"])
        self.assertFalse(production_requirements({"id": "unconfigured"}, "short")["configured"])

    def test_review_requires_exact_hash_complete_coverage_and_evidence(self):
        check = {"name": "listening", "observed": {"artifact_sha256": "1" * 64, "reviewer": "independent reviewer",
            "inspection": {"mode": "av_playback", "tool": "synthetic fixture, no human perception asserted", "playback_speed": 1.0},
            "notes": "Synthetic schema example only; no real listening asserted.",
            "coverage": [{"start_seconds": 0, "end_seconds": 2}, {"start_seconds": 2, "end_seconds": 4}],
            "evidence": {"path": "review.txt", "sha256": "2" * 64}}}
        self.assertEqual(validate_review_observation(check, media_sha256="1" * 64, duration=4), check["observed"]["evidence"])
        for field, value in [("artifact_sha256", "3" * 64), ("coverage", [{"start_seconds": 0, "end_seconds": 1}]),
                             ("evidence", {"placeholder": True})]:
            changed = copy.deepcopy(check)
            changed["observed"][field] = value
            with self.subTest(field=field), self.assertRaises(WorkflowError):
                validate_review_observation(changed, media_sha256="1" * 64, duration=4)

    def review_observation(self, name="visual_review"):
        return {"name": name, "observed": {"artifact_sha256": "1" * 64, "reviewer": "fixture reviewer",
            "notes": "Synthetic contract fixture; no real perception asserted.",
            "inspection": {"mode": "frame_inspection", "tool": "fixture contact sheet", "sampling": "all_frames",
                           "source_fps": 2, "frame_count": 8, "inspected_frames": list(range(8)), "display_size": [144, 256]},
            "coverage": [{"start_seconds": 0, "end_seconds": 4}],
            "evidence": {"path": "fixture.json", "sha256": "2" * 64}}}

    def inspect_review(self, check, duration=4):
        return validate_review_observation(check, media_sha256="1" * 64, duration=duration,
                                           media_probe={"video": [{"nb_frames": "8", "avg_frame_rate": "2/1"}]})

    def test_all_frames_establish_visual_coverage_but_not_playback_or_listening(self):
        check = self.review_observation()
        self.assertEqual(self.inspect_review(check), check["observed"]["evidence"])
        for name in ("motion", "subtitles", "captions", "listening", "music", "no_speech", "av_loop"):
            with self.subTest(name=name), self.assertRaisesRegex(WorkflowError, "cannot establish"):
                self.inspect_review({**check, "name": name})

    def test_sparse_frames_cannot_claim_continuous_or_complete_visual_coverage(self):
        check = self.review_observation("frame_detail")
        check["observed"]["inspection"].update(sampling="sampled_frames", inspected_frames=[0, 7])
        with self.assertRaisesRegex(WorkflowError, "actual inspected samples"):
            self.inspect_review(check)
        check["observed"]["coverage"] = [{"start_seconds": 0, "end_seconds": .5}, {"start_seconds": 3.5, "end_seconds": 4}]
        self.inspect_review(check)
        with self.assertRaisesRegex(WorkflowError, "complete visual review"):
            self.inspect_review({**check, "name": "visual_review"})

    def test_playback_modes_match_the_perceptual_check(self):
        for name, mode in [("visual_review", "video_playback"), ("motion", "video_playback"),
                           ("listening", "audio_listening"), ("no_speech", "audio_listening"), ("music", "av_playback"),
                           ("av_loop", "av_playback")]:
            check = self.review_observation(name)
            check["observed"]["inspection"] = {"mode": mode, "tool": "synthetic player fixture", "playback_speed": 1.0}
            self.inspect_review(check)
        for name, mode in [("motion", "audio_listening"), ("listening", "video_playback"),
                           ("visual_review", "media_probe"), ("captions", "document_inspection"),
                           ("av_loop", "video_playback"), ("av_loop", "audio_listening")]:
            check = self.review_observation(name)
            check["observed"]["inspection"] = {"mode": mode, "tool": "synthetic fixture", "playback_speed": 1.0}
            with self.subTest(name=name, mode=mode), self.assertRaises(WorkflowError):
                self.inspect_review(check)

    def test_inspection_missing_spoofed_or_nonfinite_metadata_is_rejected(self):
        cases = [("mode", "contact_sheet_playback"), ("mode", []), ("tool", ""),
                 ("sampling", "all_frames_with_gaps"), ("sampling", {}),
                 ("source_fps", float("nan")), ("source_fps", float("inf")), ("source_fps", True),
                 ("source_fps", 10 ** 1000), ("frame_count", 10 ** 1000),
                 ("frame_count", 7), ("frame_count", True), ("inspected_frames", [0, 0]),
                 ("inspected_frames", [True]), ("inspected_frames", [-1, 8]), ("inspected_frames", [7, 0]),
                 ("display_size", [0, 256]), ("display_size", [144, float("inf")])]
        for field, value in cases:
            check = self.review_observation()
            check["observed"]["inspection"][field] = value
            with self.subTest(field=field, value=value), self.assertRaises(WorkflowError):
                self.inspect_review(check)
        check = self.review_observation()
        del check["observed"]["inspection"]
        with self.assertRaisesRegex(WorkflowError, "typed inspection"):
            self.inspect_review(check)
        for duration in [0, -1, True, float("nan"), float("inf")]:
            with self.subTest(duration=duration), self.assertRaises(WorkflowError):
                self.inspect_review(self.review_observation(), duration=duration)

    def test_all_frames_cannot_be_forged_by_lowering_fps_and_count(self):
        check = self.review_observation()
        check["observed"]["inspection"].update(source_fps=.25, frame_count=1, inspected_frames=[0])
        with self.assertRaisesRegex(WorkflowError, "measured video frame"):
            self.inspect_review(check)
        with self.assertRaisesRegex(WorkflowError, "measured video frame"):
            validate_review_observation(self.review_observation(), media_sha256="1" * 64, duration=4)

    def test_slow_motion_cannot_replace_normal_speed_motion_review(self):
        for name, mode in (("motion", "video_playback"), ("av_loop", "av_playback")):
            check = self.review_observation(name)
            check["observed"]["inspection"] = {"mode": mode, "tool": "synthetic fixture", "playback_speed": .25}
            with self.subTest(name=name), self.assertRaisesRegex(WorkflowError, "normal-speed"):
                self.inspect_review(check)

    def test_playback_requires_finite_speed_and_rejects_disguised_sampling(self):
        for speed in [None, True, 0, -1, float("nan"), float("inf"), 10 ** 1000]:
            check = self.review_observation("motion")
            check["observed"]["inspection"] = {"mode": "video_playback", "tool": "synthetic player", "playback_speed": speed}
            with self.subTest(speed=speed), self.assertRaises(WorkflowError):
                self.inspect_review(check)
        check = self.review_observation("motion")
        check["observed"]["inspection"]["mode"] = "video_playback"
        check["observed"]["inspection"]["playback_speed"] = 1
        with self.assertRaisesRegex(WorkflowError, "not frame sampling"):
            self.inspect_review(check)

    def test_renamed_font_is_checked_by_actual_face(self):
        source = Path("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf")
        if not source.is_file():
            self.skipTest("requires the explicit DejaVu font fixture")
        with tempfile.TemporaryDirectory() as temporary:
            renamed = Path(temporary) / "Chalkboard-SE-Bold.ttf"
            renamed.write_bytes(source.read_bytes())
            with self.assertRaisesRegex(WorkflowError, "font family/style"):
                validate_font_face(renamed, 0, {"family": "Chalkboard SE", "style": "Bold"})
            self.assertEqual(validate_font_face(renamed, 0, {"family": "DejaVu Sans", "style": "Bold"})["sha256"], file_digest(source))

    def test_missing_policy_stops_before_claim_cost_or_provider_dispatch(self):
        import test_workflow
        fixture = test_workflow.WorkflowContract()
        fixture.setUp()
        self.addCleanup(fixture.doCleanups)
        self.addCleanup(fixture.tearDown)
        profile = copy.deepcopy(fixture.run["profile"])
        profile.update(id="unresolved_fixture", name="Unresolved policy fixture")
        profile.pop("production")
        profile["production"] = {"formats": {"short": {"narrative_loop": "required"}}}
        profiles = fixture.directory / "profiles"
        path = profiles / profile["id"] / "channel.json"
        path.parent.mkdir(parents=True)
        path.write_text(json.dumps(profile))
        fixture.run = fixture.service.create(profile["id"], "Unresolved production fixture", profiles=profiles,
                                             capabilities=fixture.run["capabilities"], budget_units=10)
        fixture.run_id = fixture.run["id"]
        fixture.production_ready()  # Research and script still work before production is configured.
        with self.assertRaisesRegex(WorkflowError, "requirements unresolved"):
            fixture.service.claim(fixture.run_id, "audio", "fixture-audio-worker", estimated_units=2)
        run = fixture.store.get(fixture.run_id)
        self.assertEqual(run["budget"]["reserved"], 0)
        self.assertEqual(run["tasks"]["audio"]["status"], "pending")
        self.assertFalse(any(event["kind"] == "operation.dispatched" for event in fixture.store.events(fixture.run_id)))

    def test_audio_can_precede_variant_but_scene_dispatch_cannot(self):
        with tempfile.TemporaryDirectory() as directory:
            service = Production(Store(Path(directory) / "state.db"), Path(directory) / "work", ROOT)
            profile = json.loads((ROOT / "channels/scenes_on_repeat/channel.json").read_text())
            run = {"profile": profile, "format": "short", "tasks": {"storyboard": {"status": "pending"}}}
            service._production_ready(run, {"stage": "audio"})
            with self.assertRaisesRegex(WorkflowError, "production_variant"):
                service._production_ready(run, {"stage": "scene_image"})
            run["format"] = "long"
            with self.assertRaisesRegex(WorkflowError, "requirements unresolved"):
                service._production_ready(run, {"stage": "audio"})

    def test_optional_audio_policy_is_validated_without_forcing_other_channels(self):
        for name in ("channels", "sample_rate"):
            for value in (True, 0, -1, "48000", None):
                profile = copy.deepcopy(self.profile)
                profile["production"]["audio"][name] = value
                with self.subTest(name=name, value=value):
                    self.assertIn("audio." + name, production_requirements(profile, "short")["unresolved"])
        scenes = json.loads((ROOT / "channels/scenes_on_repeat/channel.json").read_text())
        for variant in ("scene", "character_edit", "meme_time_machine"):
            audio = production_requirements(scenes, "short", variant=variant)["audio"]
            self.assertEqual((audio["channels"], audio["sample_rate"]), (2, 48000))
        self.assertNotIn("channels", production_requirements(self.profile, "short")["audio"])


@unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe"), "requires FFmpeg")
class ProductionDeliveryTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.directory = Path(temporary.name)
        self.service = Production(Store(self.directory / "state.db"), self.directory / "work", ROOT)
        self.profile = json.loads((ROOT / "channels/paper_detour/channel.json").read_text())

    def media(self, *, sound=True, canvas="1080x1920"):
        path = self.directory / ("sound.mp4" if sound else "silent.mp4")
        command = ["ffmpeg", "-nostdin", "-v", "error", "-f", "lavfi", "-i",
                   f"color=c=orange:s={canvas}:r=30:d=0.2"]
        if sound:
            command += ["-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo"]
        command += ["-t", "0.2", "-c:v", "libx264", "-preset", "ultrafast", "-pix_fmt", "yuv420p",
                    "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709",
                    "-color_range", "tv", "-vf",
                    "setsar=1,setparams=color_primaries=bt709:color_trc=bt709:colorspace=bt709:range=limited"]
        if sound:
            command += ["-c:a", "aac"]
        subprocess.run([*command, str(path)], check=True, capture_output=True, timeout=30)
        return path

    def run_document(self):
        return {"id": "synthetic-production-regression", "format": "short", "profile": self.profile,
                "channel": self.profile["id"], "tasks": {"packaging": {"status": "pending"}},
                "artifacts": {}}

    def test_actual_audio_must_cover_video_and_meet_explicit_channel_rate_policy(self):
        profile = copy.deepcopy(self.profile)
        profile["production"]["formats"]["short"]["video"]["canvas"] = [90, 160]
        for duration in (.2, .8):
            path = self.directory / f"audio-{duration}.mp4"
            subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-f", "lavfi", "-i",
                "color=orange:s=90x160:r=30:d=0.5", "-f", "lavfi", "-i", f"sine=sample_rate=44100:duration={duration}",
                "-c:v", "libx264", "-pix_fmt", "yuv420p", "-vf",
                "setsar=1,setparams=color_primaries=bt709:color_trc=bt709:colorspace=bt709:range=limited",
                "-c:a", "aac", str(path)], check=True, capture_output=True, timeout=30)
            measured = probe_media(path)
            with self.subTest(audio_duration=duration), self.assertRaisesRegex(WorkflowError, "complete video timeline"):
                validate_delivery_summary(measured, production_requirements(profile, "short"))
        profile["production"]["audio"].update(channels=2, sample_rate=48000)
        with self.assertRaisesRegex(WorkflowError, "channels"):
            validate_delivery_summary(measured, production_requirements(profile, "short"))
        profile["production"]["audio"]["channels"] = 1
        with self.assertRaisesRegex(WorkflowError, "sample_rate"):
            validate_delivery_summary(measured, production_requirements(profile, "short"))

    def delivery_fixture(self):
        """A small explicit software policy with real media, never a Paper release."""
        from PIL import Image
        media = self.media(canvas="90x160")
        profile = copy.deepcopy(self.profile)
        profile["production"]["formats"]["short"]["video"]["canvas"] = [90, 160]
        profile["production"]["visual"]["motion"] = "none"
        profile["production"]["captions"] = {"mode": "none", "srt": "none"}
        run = {**self.run_document(), "profile": profile}
        audio = self.directory / "mix.wav"
        subprocess.run(["ffmpeg", "-v", "error", "-i", str(media), "-vn", str(audio)],
                       check=True, capture_output=True, timeout=30)
        run["tasks"] = {}
        sources = [audio]
        for name, color in (("first", "red"), ("second", "blue")):
            path = self.directory / (name + ".png")
            Image.new("RGB", (16, 16), color).save(path)
            sources.append(path)
        for name, path in zip(("audio", "image:first", "image:second"), sources):
            item = self.service.artifacts.put(path, "audio" if name == "audio" else "image")
            run["artifacts"][item["id"]] = item
            run["tasks"][name] = {"status": "complete", "outputs": [item["id"]]}
        task = {"id": "render", "stage": "render", "dependencies": ["audio", "image:first", "image:second"],
                "claim": {"token": "fixture-claim", "input_hash": "fixture-input", "worker": "fixture-renderer"}}
        run["tasks"]["render"] = task
        manifest = self.directory / "manifest.json"
        mix = self.directory / "mix-evidence.json"
        mix.write_text(json.dumps({"audio_sha256": file_digest(audio), "returncode": 0,
            "argv": ["synthetic-mix-fixture"], "track_sha256": [file_digest(audio)]}))
        plan = {"channel": run["channel"], "format": "short", "canvas": [90, 160], "fps": 30,
            "audio": str(audio), "subtitles": {"mode": "none"},
            "scenes": [{"image": str(source), "start_frame": i * 3, "end_frame": (i + 1) * 3}
                       for i, source in enumerate(sources[1:])],
            "music": {"status": "present", "tracks": [{**self.record(audio), "start_frame": 0, "end_frame": 6}],
                      "mix_evidence": self.record(mix)}}
        manifest.write_text(json.dumps(plan))
        execution = self.directory / "execution.json"
        execution.write_text(json.dumps({"run_id": run["id"], "task_id": "render", "kind": "host_render",
            "claim_token": "fixture-claim", "input_hash": "fixture-input", "state": "completed", "returncode": 0,
            "argv": ["synthetic-render-fixture"], "outputs": [str(media)], "output_artifacts": [self.record(media)],
            "inputs": [self.record(path) for path in [manifest, *sources, mix]]}))
        proof = self.directory / "delivery.json"
        proof.write_text(json.dumps({"schema": "ytv-production-delivery-v1", "media_sha256": file_digest(media),
            "requirements_sha256": self.service.requirements(run)["sha256"], "manifest": self.record(manifest),
            "execution": self.record(execution)}))
        return run, task, media, proof, manifest, execution, mix

    @staticmethod
    def record(path):
        return {"path": str(path), "sha256": file_digest(path)}

    def test_exact_delivery_proof_accepts_real_media(self):
        run, task, media, proof, _, _, _ = self.delivery_fixture()
        artifact = self.service.artifacts.put(media, "mp4")
        self.service._validate_output(run, task, artifact, receipt={"delivery_evidence": self.record(proof)})
        self.assertEqual(task["media_validation"]["observed"]["video"][0]["nb_frames"], "6")
        self.assertGreater(len(task["media_validation"]["evidence_artifacts"]), 5)

    def test_delivery_accepts_equivalent_symlink_input_paths(self):
        run, task, media, proof, _, execution, _ = self.delivery_fixture()
        alias = self.directory / "source-alias"
        alias.symlink_to(self.directory, target_is_directory=True)
        dispatch = json.loads(execution.read_text())
        for item in dispatch["inputs"]:
            item["path"] = str(alias / Path(item["path"]).name)
        execution.write_text(json.dumps(dispatch))
        bound = json.loads(proof.read_text())
        bound["execution"] = self.record(execution)
        proof.write_text(json.dumps(bound))
        self.service._validate_output(run, task, self.service.artifacts.put(media, "mp4"),
                                      receipt={"delivery_evidence": self.record(proof)})
        dispatch["inputs"][0]["sha256"] = "0" * 64
        execution.write_text(json.dumps(dispatch))
        bound["execution"] = self.record(execution)
        proof.write_text(json.dumps(bound))
        with self.assertRaisesRegex(WorkflowError, "required bound input"):
            self.service._validate_output(run, task, self.service.artifacts.put(media, "mp4"),
                                          receipt={"delivery_evidence": self.record(proof)})

    def test_final_scene_order_cannot_be_swapped_even_with_fresh_manifest_hash(self):
        run, task, media, proof, manifest, execution, _ = self.delivery_fixture()
        plan = json.loads(manifest.read_text())
        plan["scenes"][0]["image"], plan["scenes"][1]["image"] = plan["scenes"][1]["image"], plan["scenes"][0]["image"]
        manifest.write_text(json.dumps(plan))
        dispatch = json.loads(execution.read_text())
        dispatch["inputs"][0] = self.record(manifest)
        execution.write_text(json.dumps(dispatch))
        bound = json.loads(proof.read_text())
        bound.update(manifest=self.record(manifest), execution=self.record(execution))
        proof.write_text(json.dumps(bound))
        with self.assertRaisesRegex(WorkflowError, "scene order"):
            self.service._validate_output(run, task, self.service.artifacts.put(media, "mp4"),
                                          receipt={"delivery_evidence": self.record(proof)})

    def test_mix_evidence_is_rehashed_before_completion(self):
        run, task, media, proof, _, _, mix = self.delivery_fixture()
        mix.write_text(mix.read_text() + "\n")
        with self.assertRaisesRegex(WorkflowError, "stale"):
            self.service._validate_output(run, task, self.service.artifacts.put(media, "mp4"),
                                          receipt={"delivery_evidence": self.record(proof)})

    def test_changed_media_cannot_reuse_a_delivery_proof(self):
        run, task, media, proof, _, _, _ = self.delivery_fixture()
        media.write_bytes(media.read_bytes() + b"synthetic changed container bytes")
        with self.assertRaisesRegex(WorkflowError, "bind this MP4"):
            self.service._validate_output(run, task, self.service.artifacts.put(media, "mp4"),
                                          receipt={"delivery_evidence": self.record(proof)})

    def test_licensed_clip_receipt_resolves_to_exact_media_in_scene_order(self):
        run, task, media, _, _, _, _ = self.delivery_fixture()
        run["profile"]["recipe"] = "licensed_clips"
        clip = self.service.artifacts.put(media, "clip")
        run["artifacts"][clip["id"]] = clip
        receipt_path = self.directory / "accepted-clip.json"
        receipt_path.write_text(json.dumps({"clip_artifact_id": clip["id"]}))
        receipt = self.service.artifacts.put(receipt_path, "image")
        run["artifacts"][receipt["id"]] = receipt
        run["tasks"]["image:first"]["outputs"] = [receipt["id"]]
        sources = self.service.render_sources(run, task)
        self.assertEqual(sources[0]["sha256"], clip["sha256"])
        self.assertEqual(sources[1]["id"], run["tasks"]["image:second"]["outputs"][0])

    def test_render_producer_cannot_be_its_independent_final_reviewer(self):
        run, render, media, _, _, _, _ = self.delivery_fixture()
        artifact = self.service.artifacts.put(media, "mp4")
        run["artifacts"][artifact["id"]] = artifact
        render["outputs"] = [artifact["id"]]
        qa_path = self.directory / "qa.json"
        qa_path.write_text(json.dumps({"reviewed_sha256": artifact["sha256"], "probe": probe_media(media)}))
        qa = self.service.artifacts.put(qa_path, "qa")
        evidence = self.directory / "review.txt"
        evidence.write_text("Explicit synthetic schema fixture; no real listening asserted.")
        claim = {"worker": "fixture-renderer", "input_hash": "review-input"}
        receipt = {"run_id": run["id"], "task_id": "review", "worker": claim["worker"],
            "input_hash": claim["input_hash"], "output_sha256": qa["sha256"],
            "checks": [{"name": name, "status": "pass", "method": "synthetic schema test",
                        "observed": {"artifact_sha256": artifact["sha256"], "reviewer": "fixture-reviewer",
                            "inspection": {"mode": "av_playback", "tool": "synthetic fixture, no human perception asserted", "playback_speed": 1.0},
                            "notes": "Synthetic QA contract example, not audiovisual verification.",
                            "coverage": [{"start_seconds": 0, "end_seconds": .2}], "evidence": self.record(evidence)}}
                       for name in self.service.requirements(run)["review_checks"]]}
        with self.assertRaisesRegex(WorkflowError, "distinct from the render producer"):
            self.service._validate_receipt(run, {"id": "review", "stage": "review"}, claim, qa, receipt)

    def test_core_rejects_1080p_in_a_2k_production_run(self):
        artifact = self.service.artifacts.put(self.media(), "mp4")
        with self.assertRaisesRegex(WorkflowError, "canvas|dimensions"):
            self.service._validate_output(self.run_document(), {"stage": "render"}, artifact)

    def test_no_speech_does_not_remove_the_audio_requirement(self):
        run = self.run_document()
        packaging = self.directory / "packaging.json"
        packaging.write_text(json.dumps({"has_speech": False}))
        spec = self.service.artifacts.put(packaging, "release_spec")
        run["artifacts"][spec["id"]] = spec
        run["tasks"]["packaging"] = {"status": "complete", "outputs": [spec["id"]]}
        media = self.service.artifacts.put(self.media(sound=False, canvas="1440x2560"), "mp4")
        with self.assertRaisesRegex(WorkflowError, "audio"):
            self.service._validate_output(run, {"stage": "render"}, media)

    def test_placeholder_delivery_and_listening_are_not_review_evidence(self):
        run = self.run_document()
        path = self.media()
        media = self.service.artifacts.put(path, "mp4")
        run["artifacts"][media["id"]] = media
        run["tasks"]["render"] = {"outputs": [media["id"]]}
        qa_path = self.directory / "qa.json"
        qa_path.write_text(json.dumps({"reviewed_sha256": file_digest(path), "probe": probe_media(path)}))
        qa = self.service.artifacts.put(qa_path, "qa")
        claim = {"worker": "synthetic-reviewer", "input_hash": "synthetic-input"}
        receipt = {"run_id": run["id"], "task_id": "review", "worker": claim["worker"],
                   "input_hash": claim["input_hash"], "output_sha256": qa["sha256"],
                   "checks": [{"name": name, "status": "pass", "method": "placeholder",
                               "observed": {"placeholder": True}} for name in self.service.requirements(run)["review_checks"]]}
        with self.assertRaisesRegex(WorkflowError, "exact rendered media hash"):
            self.service._validate_receipt(run, {"id": "review", "stage": "review"}, claim, qa, receipt)


if __name__ == "__main__":
    unittest.main()
