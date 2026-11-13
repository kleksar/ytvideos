"""Licensed edits must not invent narration, TTS or caption words to satisfy the DAG."""
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
from unittest.mock import Mock

import test_workflow
from ytvideos.errors import WorkflowError
from ytvideos.executor import MediaExecutor
from ytvideos.media_checks import probe_media
from ytvideos.media_script import EDIT_SCHEMA, NO_SPEECH_SCHEMA, read_script
from ytvideos.production_contract import DELIVERY_SCHEMA, validate_render_manifest
from ytvideos.util import file_digest
from ytvideos.workflow import required_checks


ROOT = Path(__file__).resolve().parents[1]


def edit_script(mode="none"):
    text = "Look at that!" if mode != "none" else ""
    return {"schema": EDIT_SCHEMA, "production_variant": "scene",
            "intent": "A complete licensed edit: the visible action reaches its outcome without invented dialogue.",
            "speech": {"mode": mode, "text": text},
            "segments": [{"id": "shot", "description": "The source shot completes the action, then loops.",
                          "spoken_text": text}]}


class EditScriptTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.directory = Path(self.temporary.name)
        self.profile = json.loads((ROOT / "channels/scenes_on_repeat/channel.json").read_text())

    def write(self, value):
        path = self.directory / "script.json"
        path.write_text(json.dumps(value))
        return path

    def test_licensed_silence_or_short_source_quote_is_a_complete_edit_script(self):
        for mode in ("none", "source", "narration"):
            with self.subTest(mode=mode):
                result = read_script(self.write(edit_script(mode)), self.profile, "short")
                self.assertEqual(result["mode"], mode)
                self.assertEqual(result["text"], edit_script(mode)["speech"]["text"])

    def test_no_speech_cannot_bypass_illustrated_narration(self):
        self.profile["recipe"] = "illustrated"
        with self.assertRaisesRegex(WorkflowError, "only.*licensed"):
            read_script(self.write(edit_script()), self.profile, "short")

    def test_shortcuts_cannot_hide_spoken_words_or_reorder_them(self):
        for defect in ("none_with_text", "dropped_word", "unknown_variant", "duplicate_id"):
            value = edit_script("source")
            if defect == "none_with_text":
                value["speech"]["mode"] = "none"
            elif defect == "dropped_word":
                value["segments"][0]["spoken_text"] = "Look!"
            elif defect == "unknown_variant":
                value["production_variant"] = "invented"
            else:
                value["segments"].append(value["segments"][0].copy())
            with self.subTest(defect=defect), self.assertRaises(WorkflowError):
                read_script(self.write(value), self.profile, "short")


@unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe"), "requires local FFmpeg")
class LicensedSilentLifecycle(unittest.TestCase):
    def setUp(self):
        self.fixture = test_workflow.WorkflowContract()
        self.fixture.setUp()
        self.addCleanup(self.fixture.doCleanups)
        self.addCleanup(self.fixture.tearDown)
        self.service = self.fixture.service
        self.directory = self.fixture.directory
        profile = json.loads((ROOT / "channels/scenes_on_repeat/channel.json").read_text())
        # Explicit small software fixture, never a production channel export.
        profile["production"]["formats"]["short"]["video"]["canvas"] = [90, 160]
        profiles = self.directory / "profiles"
        path = profiles / "scenes_on_repeat/channel.json"
        path.parent.mkdir(parents=True)
        path.write_text(json.dumps(profile))
        capabilities = {"web.search": {"available": True, "evidence": "synthetic test"},
                        "model.text": {"available": True, "evidence": "synthetic test"},
                        "audio.mix": {"available": True, "evidence": "observed local ffmpeg"},
                        "audio.listen": {"available": True, "evidence": "synthetic perception-contract fixture"},
                        "media.licensed_clip": {"available": True, "evidence": "generated source fixture", "billing": "included"},
                        "video.render": {"available": True, "evidence": "local ffmpeg"},
                        "video.inspect": {"available": True, "evidence": "local ffprobe"},
                        "model.vision": {"available": True, "evidence": "synthetic review-contract fixture"}}
        self.script_path = self.write(edit_script(), "accepted-edit.json")
        run = self.service.create("scenes_on_repeat", "Synthetic licensed edit with source sound and no speech",
                                  profiles=profiles, capabilities=capabilities, source_script=self.script_path)
        self.run_id = run["id"]
        self.fixture.run_id = self.run_id
        self.finish("research", self.write({"selected_topic": {"title": "Software fixture", "angle": "Silent action",
                    "viewer_value": "Tests the no-speech path"}, "sources": [{"url": "https://example.com/test-only"}]}, "research.json"))
        self.finish("script", self.script_path)

    def write(self, value, name):
        path = self.directory / name
        path.write_text(value if isinstance(value, str) else json.dumps(value))
        return path

    def record(self, path):
        return {"path": str(path), "sha256": file_digest(path)}

    def receipt(self, task_id, claim, path, *, media=None, duration=None):
        run = self.service.store.get(self.run_id)
        requirements = self.service.requirements(run)
        names = required_checks(run["tasks"][task_id]["stage"], requirements)
        checks = []
        for name in sorted(names):
            observed = {"synthetic_fixture": True}
            if name == "independent_review":
                observed = {"reviewer": "test-independent-script-reviewer", "artifact_sha256": file_digest(path)}
            if name == "no_speech" or task_id == "review":
                evidence = self.write("Synthetic software evidence only; no human listening or live creative QA is claimed.",
                                      task_id + "-" + name + "-observation.txt")
                observed = {"artifact_sha256": file_digest(media), "reviewer": "test-independent-media-reviewer",
                            "notes": "The generated synthetic tone fixture tests complete interval evidence, not real perception.",
                            "coverage": [{"start_seconds": 0, "end_seconds": duration}], "evidence": self.record(evidence)}
            checks.append({"name": name, "status": "pass", "method": "explicit synthetic regression fixture", "observed": observed})
        return self.write({"run_id": self.run_id, "task_id": task_id, "worker": claim["worker"],
                           "input_hash": claim["input_hash"], "output_sha256": file_digest(path), "checks": checks}, task_id.replace(":", "-") + "-receipt.json")

    def finish(self, task_id, path, *, media=None, duration=None, claim=None, delivery=None):
        claim = claim or self.service.claim(self.run_id, task_id, "test-author-" + task_id)
        receipt = self.receipt(task_id, claim, path, media=media, duration=duration)
        if delivery:
            value = json.loads(receipt.read_text())
            value["delivery_evidence"] = self.record(delivery)
            receipt.write_text(json.dumps(value))
        return self.service.complete(self.run_id, task_id, claim["token"], path, receipt, actual_units=0)

    def test_signed_source_audio_to_mp4_has_no_tts_or_fake_srt(self):
        self.assertEqual(self.service.next(self.run_id)["status"], "awaiting_script_approval")
        self.service.approve(self.fixture.signed("script"))
        context = self.service.context(self.run_id, "audio")
        self.assertEqual(set(context["required_checks"]), {"source_identity", "listening", "no_speech"})
        self.assertEqual(context["task"]["capabilities"], ["audio.mix", "audio.listen"])
        context = self.service.context(self.run_id, "subtitles")
        self.assertEqual(context["output_kind"], "no_speech")
        self.assertEqual(context["task"]["capabilities"], ["audio.listen"])
        self.assertEqual(context["task_guide"]["output_kind"], "no_speech")
        subtitle_plan = next(step for step in self.service.plan(self.run_id)["steps"] if step["id"] == "subtitles")
        self.assertEqual(subtitle_plan["output_kind"], "no_speech")
        claim = self.service.claim(self.run_id, "audio", "test-audio-editor")
        never_called = Mock()
        with self.assertRaisesRegex(WorkflowError, "never TTS"):
            MediaExecutor(self.service, runner=never_called).execute(self.run_id, "audio", claim["token"], {"kind": "tts"})
        never_called.assert_not_called()
        run = self.service.store.get(self.run_id)
        with self.assertRaisesRegex(WorkflowError, "must not dispatch TTS"):
            self.service._operation_payload(run, run["tasks"]["audio"], "tts")

        clip = self.directory / "source.mp4"
        subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-f", "lavfi", "-i", "color=orange:s=90x160:r=24:d=0.5",
                        "-f", "lavfi", "-i", "sine=frequency=440:sample_rate=48000:duration=0.5", "-t", "0.5",
                        "-c:v", "libx264", "-preset", "ultrafast", "-pix_fmt", "yuv420p", "-vf",
                        "setsar=1,setparams=color_primaries=bt709:color_trc=bt709:colorspace=bt709:range=limited",
                        "-c:a", "aac", str(clip)], check=True, capture_output=True, timeout=30)
        source = self.service.attach(self.run_id, clip, kind="licensed_source", source="locally generated software test fixture")
        rights = self.service.attach(self.run_id, self.write("This fixture was generated locally by the test.", "rights.txt"),
                                     kind="rights", source="test generator")
        manifest = self.write({"schema": "ytv-source-audio-v1", "segments": [{"id": "shot", "path": str(clip),
            "sha256": source["sha256"], "start_seconds": 0, "end_seconds": .5, "gain": 1}]}, "source-audio.json")
        output = self.service.workspace / "runs" / self.run_id / "attempts" / claim["token"] / "mix.wav"
        mixed = MediaExecutor(self.service).execute(self.run_id, "audio", claim["token"],
            {"kind": "mix", "args": [str(manifest), "--output", str(output)], "outputs": [str(output)], "prepared_inputs": [str(manifest)]})
        self.assertEqual(mixed["execution"]["state"], "completed")
        self.assertFalse(mixed["execution"]["paid"])
        self.assertEqual(mixed["execution"]["kind"], "mix")
        duration = probe_media(output)["duration_seconds"]
        self.finish("audio", output, claim=claim, media=output, duration=duration)
        run = self.service.store.get(self.run_id)
        no_speech = self.write({"schema": NO_SPEECH_SCHEMA, "script_sha256": file_digest(self.script_path),
                               "audio_sha256": file_digest(output), "has_speech": False}, "no-speech.json")
        completed = self.finish("subtitles", no_speech, media=output, duration=duration)
        self.assertEqual(self.service.store.get(self.run_id)["artifacts"][completed["outputs"][0]]["kind"], "no_speech")
        self.finish("storyboard", self.write({"production_variant": "scene", "scenes": [{"id": "shot", "prompt": "Use the exact synthetic source",
            "visual_intent": "Test a licensed clip instead of a still image", "source_clip": {"source_artifact_id": source["id"],
                "rights_artifact_id": rights["id"], "start_seconds": 0, "end_seconds": .5, "authority": "local synthetic test generator"}}]}, "board.json"))
        self.finish("image:shot", clip)

        render_claim = self.service.claim(self.run_id, "render", "test-render-producer")
        rendered = self.directory / "final.mp4"
        command = ["ffmpeg", "-nostdin", "-v", "error", "-i", str(clip), "-i", str(output), "-map", "0:v:0", "-map", "1:a:0",
                   "-c:v", "copy", "-c:a", "aac", "-t", "0.5", str(rendered)]
        process = subprocess.run(command, check=True, capture_output=True, timeout=30)
        plan = self.write({"channel": "scenes_on_repeat", "format": "short", "production_variant": "scene", "has_speech": False,
            "audio": str(output), "subtitles": {"mode": "none"}, "music": {"status": "not_used", "reason": "Synthetic source tone only"},
            "scenes": [{"clip": str(clip), "start_frame": 0, "end_frame": 12}]}, "render.json")
        execution = self.write({"run_id": self.run_id, "task_id": "render", "claim_token": render_claim["token"],
            "input_hash": render_claim["input_hash"], "state": "completed", "returncode": process.returncode, "kind": "host_render",
            "argv": command, "inputs": [self.record(plan), self.record(output), self.record(clip)], "outputs": [str(rendered)],
            "output_artifacts": [self.record(rendered)]}, "host-execution.json")
        requirements = self.service.requirements(self.service.store.get(self.run_id))
        invalid = json.loads(plan.read_text())
        invalid["has_speech"] = True
        with self.assertRaisesRegex(WorkflowError, "accepted script"):
            validate_render_manifest(invalid, requirements)
        proof = self.write({"schema": DELIVERY_SCHEMA, "media_sha256": file_digest(rendered), "requirements_sha256": requirements["sha256"],
                            "manifest": self.record(plan), "execution": self.record(execution)}, "delivery.json")
        self.finish("render", rendered, claim=render_claim, delivery=proof)
        probe = probe_media(rendered)
        qa = self.write({"reviewed_sha256": file_digest(rendered), "requirements_sha256": requirements["sha256"], "probe": probe}, "qa.json")
        self.finish("review", qa, media=rendered, duration=probe["duration_seconds"])
        self.assertEqual(self.service.next(self.run_id)["status"], "awaiting_mp4_approval")
        self.service.approve(self.fixture.signed("mp4"))
        approvals = [event["payload"]["kind"] for event in self.service.store.events(self.run_id) if event["kind"] == "user.approved"]
        self.assertEqual(approvals, ["script", "mp4"])
        self.assertEqual(self.service.store.get(self.run_id)["budget"]["spent"], 0)
        self.assertFalse(any(self.directory.rglob("*.srt")))

    def test_revision_restores_capabilities_then_selects_new_source_mode(self):
        self.service.revise(self.run_id, "script", "replace silent edit with verified source dialogue")
        run = self.service.store.get(self.run_id)
        self.assertEqual(run["tasks"]["subtitles"]["capabilities"], ["subtitle.align"])
        self.finish("script", self.write(edit_script("source"), "source-dialogue.json"))
        context = self.service.context(self.run_id, "audio")
        self.assertEqual(set(context["required_checks"]), {"source_identity", "exact_text", "listening"})
        self.assertEqual(context["task"]["capabilities"], ["audio.mix", "audio.listen"])
        self.assertEqual(self.service.context(self.run_id, "subtitles")["output_kind"], "srt")

    def test_typed_narration_sends_only_spoken_text_to_tts(self):
        self.service.revise(self.run_id, "script", "explicit approved narration version")
        path = self.write(edit_script("narration"), "narration-edit.json")
        self.finish("script", path)
        self.service.approve(self.fixture.signed("script"))
        self.service.capabilities(self.run_id, {"audio.produce": {"available": True, "billing": "included"}}, evidence="synthetic provider stub")
        claim = self.service.claim(self.run_id, "audio", "test-narrator")
        def generate(command, **kwargs):
            spoken = Path(command[command.index("--en-text") + 1]).read_text()
            self.assertEqual(spoken, "Look at that!")
            output = Path(command[command.index("--output-dir") + 1])
            output.mkdir(parents=True)
            (output / "voice_en.mp3").write_bytes(b"synthetic provider output; not accepted audio")
            return subprocess.CompletedProcess(command, 0, "", "")
        result = MediaExecutor(self.service, runner=Mock(side_effect=generate)).execute(self.run_id, "audio", claim["token"], {"kind": "tts"})
        self.assertEqual(result["execution"]["state"], "completed")


if __name__ == "__main__":
    unittest.main()
