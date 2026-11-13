"""Native source mix → music compositor → completion, with explicit synthetic QA."""
import copy
import json
from pathlib import Path
import shutil
import unittest

import test_workflow
from test_music_render import FONT, MusicFixture, ROOT, write
from ytvideos.errors import Conflict, WorkflowError
from ytvideos.executor import MediaExecutor
from ytvideos.media_checks import probe_media
from ytvideos.media_script import NO_SPEECH_SCHEMA
from ytvideos.music_contract import file_record, helper
from ytvideos.util import file_digest


@unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe") and FONT.exists(), "requires local media tools")
class MusicLifecycleTests(unittest.TestCase):
    def setUp(self):
        self.state = test_workflow.WorkflowContract()
        self.state.setUp()
        self.addCleanup(self.state.doCleanups)
        self.addCleanup(self.state.tearDown)
        self.fixture = MusicFixture(self.state.directory / "music")
        f = self.fixture
        for relative in (".agent", ".agents", "docs"):
            shutil.copytree(ROOT / relative, f.project / relative)
        shutil.copyfile(ROOT / "AGENTS.md", f.project / "AGENTS.md")
        shutil.copyfile(ROOT / "channels/nuviko_videos/AGENTS.md", f.project / "channels/nuviko_videos/AGENTS.md")
        shutil.copytree(ROOT / "channels/nuviko_videos/docs", f.project / "channels/nuviko_videos/docs")
        self.service = self.state.service
        self.service.project = f.project
        capabilities = {name: {"available": True, "evidence": "explicit synthetic software test", "billing": "included"}
                        for name in ("web.search", "model.text", "sessions.independent", "audio.mix", "audio.listen",
                                     "media.licensed_clip", "video.render", "video.inspect", "model.vision")}
        self.run = self.service.create("nuviko_videos", "Synthetic music-first software regression", capabilities=capabilities,
                                       source_script=f.script_path)
        self.run_id = self.run["id"]
        self.state.run_id = self.run_id

    def finish(self, task_id, path, *, claim=None, media=None, mix=None, delivery=None,
               reviewer="separate-synthetic-media-reviewer"):
        claim = claim or self.service.claim(self.run_id, task_id, "synthetic-" + task_id)
        receipt_path = self.state.receipt(task_id, claim, path)
        receipt = json.loads(receipt_path.read_text())
        for check in receipt["checks"]:
            if check["name"] == "source_identity":
                check["observed"] = {"mix_evidence": mix, "artifact_sha256": file_digest(path)}
            if check["name"] == "no_speech" or task_id == "review":
                evidence = write(self.state.directory / (task_id + "-" + check["name"] + "-observation.txt"),
                                 "Synthetic evidence for contract/state tests only. No live or human perceptual QA is claimed.")
                check["observed"] = {"artifact_sha256": file_digest(media), "reviewer": reviewer,
                                     "inspection": {"mode": "av_playback", "tool": "synthetic fixture, no human perception asserted", "playback_speed": 1.0},
                                     "notes": "The synthetic tone/pattern fixture covers the software contract only.",
                                     "coverage": [{"start_seconds": 0, "end_seconds": probe_media(media)["duration_seconds"]}],
                                     "evidence": file_record(evidence)}
        if delivery:
            receipt["delivery_evidence"] = delivery
        write(receipt_path, receipt)
        return self.service.complete(self.run_id, task_id, claim["token"], path, receipt_path, actual_units=0)

    def test_start_is_music_first_and_native_end_to_end_does_not_fabricate_tts_or_srt(self):
        self.produce_to_review()

    def test_expired_native_mix_and_render_reuse_exact_outputs_under_current_leases(self):
        self.produce_to_review(recover=True)

    def produce_to_review(self, *, recover=False):
        f = self.fixture
        plan = self.service.plan(self.run_id)
        audio_step = next(step for step in plan["steps"] if step["id"] == "audio")
        self.assertEqual(audio_step["capabilities"], ["audio.mix", "audio.listen"])
        self.assertNotIn("voice_identity", audio_step["required_checks"])
        self.assertFalse(any(gap["capability"] in {"audio.produce", "subtitle.align"} for gap in plan["capability_gaps"]))
        self.assertIn("запись", self.service.context(self.run_id, "research")["task_guide"]["goal"])
        research = write(f.directory / "research.json", {"selected_topic": {"title": "Synthetic source sequence",
            "angle": "Fixture melody and pattern change", "viewer_value": "Exercise the exact music-first contract"},
            "sources": [{"url": "https://example.com/synthetic-test-only"}]})
        self.finish("research", research)
        self.finish("script", f.script_path)
        self.service.approve(self.state.signed("script"))
        rights = self.service.attach(self.run_id, f.rights, kind="rights", source="synthetic test generator")
        originals = [self.service.attach(self.run_id, source, kind="licensed_source", source="synthetic test generator")
                     for source in f.originals]
        self.service.attach(self.run_id, f.source_track, kind="music_source", source="synthetic tone generator")
        audio_claim = self.service.claim(self.run_id, "audio", "synthetic-music-editor")
        with self.assertRaisesRegex(WorkflowError, "never TTS"):
            MediaExecutor(self.service).execute(self.run_id, "audio", audio_claim["token"], {"kind": "tts"})
        audio = self.service.workspace / "runs" / self.run_id / "attempts" / audio_claim["token"] / "accepted-mix.wav"
        executed = MediaExecutor(self.service).execute(self.run_id, "audio", audio_claim["token"], {
            "kind": "mix", "args": [str(f.source_plan), "--output", str(audio)],
            "outputs": [str(audio)], "prepared_inputs": [str(f.source_plan)]})
        self.assertEqual(executed["execution"]["state"], "completed", executed["execution"])
        # Placeholder source-identity JSON cannot complete even a decodable WAV.
        with self.assertRaises(WorkflowError):
            self.finish("audio", audio, claim=audio_claim, media=audio, mix=file_record(f.rights))
        original_audio_claim = audio_claim
        if recover:
            self.state.clock += 901
            self.service.resume(self.run_id)
            audio_claim = self.service.claim(self.run_id, "audio", "synthetic-recovery-editor")
            self.assertEqual(audio_claim["input_hash"], original_audio_claim["input_hash"])
            with self.assertRaisesRegex(Conflict, "stale or missing"):
                self.finish("audio", audio, claim=original_audio_claim, media=audio, mix=executed["mix_evidence"])
            mix = json.loads(Path(executed["mix_evidence"]["path"]).read_text())
            original_execution = json.loads(Path(mix["execution"]["path"]).read_text())
            for defect in ("argv", "inputs", "outputs", "origin_token", "input_hash", "paid", "host"):
                altered = copy.deepcopy(original_execution)
                if defect == "argv":
                    altered["argv"][0] += "-changed"
                elif defect == "inputs":
                    altered["inputs"].append(file_record(f.rights))
                elif defect == "outputs":
                    altered["outputs"].append(str(audio.parent / "unrecorded-output.wav"))
                elif defect == "origin_token":
                    altered["claim_token"] = "unrecorded-origin-token"
                elif defect == "input_hash":
                    altered["input_hash"] = "unrecorded-input-hash"
                elif defect == "paid":
                    altered["paid"] = True
                else:
                    altered["kind"] = "host_render"
                altered_mix = {**mix, "argv": altered["argv"],
                               "execution": file_record(write(f.directory / (defect + "-execution.json"), altered))}
                proof = file_record(write(f.directory / (defect + "-mix.json"), altered_mix))
                with self.subTest(defect=defect), self.assertRaises(WorkflowError):
                    self.finish("audio", audio, claim=audio_claim, media=audio, mix=proof)
        self.finish("audio", audio, claim=audio_claim, media=audio, mix=executed["mix_evidence"])
        accepted_audio = self.service.store.get(self.run_id)["tasks"]["audio"]
        self.assertEqual(accepted_audio["completed_token"], audio_claim["token"])
        self.assertEqual(accepted_audio["media_validation"]["execution_claim_token"], original_audio_claim["token"])
        none = write(f.directory / "no-speech.json", {"schema": NO_SPEECH_SCHEMA,
            "script_sha256": file_digest(f.script_path), "audio_sha256": file_digest(audio), "has_speech": False})
        self.finish("subtitles", none, media=audio)
        scenes = []
        for index, source in enumerate(originals):
            interval = f.plan["scenes"][index]["source"]
            scenes.append({"id": f"s{index}", "prompt": "Use this exact synthetic source excerpt", "visual_intent": "Tests source binding",
                           "source_clip": {"source_artifact_id": source["id"], "rights_artifact_id": rights["id"],
                                           "start_seconds": interval["start_seconds"], "end_seconds": interval["end_seconds"],
                                           "authority": "Local test-fixture generator"}})
        self.finish("storyboard", write(f.directory / "board.json", {"production_variant": "instrumental", "scenes": scenes}))
        for index, clip in enumerate(f.clips):
            self.finish(f"image:s{index}", clip)
        render_plan = copy.deepcopy(f.plan)
        render_plan["audio"] = str(audio)
        render_plan["music"]["mix_evidence"] = executed["mix_evidence"]
        planner = json.loads(Path(render_plan["planner"]["input"]["path"]).read_text())
        planner["media"] = str(audio)
        render_plan["planner"] = {
            "input": file_record(write(f.directory / "accepted-planner-input.json", planner)),
            "output": file_record(write(f.directory / "accepted-planner-output.json",
                                          helper(f.project, "automation/music_montage.py", "accepted_music_planner").plan_timeline(planner)))}
        manifest = write(f.directory / "accepted-render.json", render_plan)
        render_claim = self.service.claim(self.run_id, "render", "synthetic-render-producer")
        output = self.service.workspace / "runs" / self.run_id / "attempts" / render_claim["token"] / "final.mp4"
        result = MediaExecutor(self.service).execute(self.run_id, "render", render_claim["token"], {
            "kind": "music_render", "args": [str(manifest), "--output", str(output)],
            "outputs": [str(output)], "prepared_inputs": [str(manifest)]})
        self.assertEqual(result["execution"]["state"], "completed", result["execution"])
        original_render_claim = render_claim
        if recover:
            self.state.clock += 901
            self.service.resume(self.run_id)
            render_claim = self.service.claim(self.run_id, "render", "synthetic-recovery-renderer")
            self.assertEqual(render_claim["input_hash"], original_render_claim["input_hash"])
            with self.assertRaisesRegex(Conflict, "stale or missing"):
                self.finish("render", output, claim=original_render_claim, delivery=result["delivery_evidence"])
        self.finish("render", output, claim=render_claim, delivery=result["delivery_evidence"])
        accepted_render = self.service.store.get(self.run_id)["tasks"]["render"]
        self.assertEqual(accepted_render["media_validation"]["execution_claim_token"], original_render_claim["token"])
        self.assertEqual(accepted_render["media_validation"]["execution_worker"], original_render_claim["worker"])
        self.assertEqual(accepted_render["completed_token"], render_claim["token"])
        dispatches = [event["payload"]["kind"] for event in self.service.store.events(self.run_id)
                      if event["kind"] == "media.dispatch"]
        self.assertEqual(dispatches.count("mix"), 1)
        self.assertEqual(dispatches.count("music_render"), 1)
        requirements = self.service.requirements(self.service.store.get(self.run_id))
        qa = write(f.directory / "qa.json", {"reviewed_sha256": file_digest(output),
            "requirements_sha256": requirements["sha256"], "probe": probe_media(output)})
        review_claim = None
        if recover:
            producers = (original_render_claim["worker"], render_claim["worker"])
            for producer in producers:
                rejected = self.service.claim(self.run_id, "review", producer)
                with self.subTest(author_claim=producer), self.assertRaisesRegex(WorkflowError, "distinct from the render producer"):
                    self.finish("review", qa, claim=rejected, media=output)
                self.service.fail(self.run_id, "review", rejected["token"], "Synthetic producer cannot own independent review",
                                  known_not_sent=True)
                self.service.unblock(self.run_id, "review", "Assign a genuinely separate synthetic reviewer")
            review_claim = self.service.claim(self.run_id, "review", "synthetic-independent-review-worker")
            for producer in producers:
                with self.subTest(evidence_reviewer=producer), self.assertRaisesRegex(WorkflowError, "distinct from the render producer"):
                    self.finish("review", qa, claim=review_claim, media=output, reviewer=producer)
        self.finish("review", qa, claim=review_claim, media=output)
        run = self.service.store.get(self.run_id)
        self.assertEqual(self.service.next(self.run_id)["status"], "awaiting_mp4_approval")
        self.assertEqual(run["budget"]["spent"], 0)
        self.assertFalse(list(f.directory.glob("*.srt")))
        preserved = [item["kind"] for item in run["tasks"]["render"]["media_validation"]["evidence_artifacts"]]
        self.assertIn("canonical_music_receipt", preserved)
        # Revisions keep the recipe-specific discovery path even before a new variant.
        self.service.revise(self.run_id, "script", "Synthetic test: select a different exact excerpt")
        reset = self.service.store.get(self.run_id)
        self.assertEqual(reset["tasks"]["audio"]["capabilities"], ["audio.mix", "audio.listen"])
        self.assertEqual(reset["tasks"]["subtitles"]["capabilities"], ["audio.listen"])


if __name__ == "__main__":
    unittest.main()
