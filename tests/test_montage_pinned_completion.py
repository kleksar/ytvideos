"""Synthetic service.complete regression; no real production QA is claimed."""

import json
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

import test_workflow
from ytvideos.errors import WorkflowError
from ytvideos.util import canonical, digest, file_digest
from ytvideos.workflow import input_hash

ROOT = Path(__file__).resolve().parents[1]
HELPERS = ROOT / "automation/ffmpeg_montage/tests"
sys.path.insert(0, str(HELPERS))
import test_delivery  # noqa: E402 -- fixture path is added immediately above
from export_fixture import passport  # noqa: E402 -- fixture path is added immediately above


class PinnedMontageComplete(unittest.TestCase):
    def setUp(self):
        self.state = test_workflow.WorkflowContract()
        self.state.setUp()
        self.addCleanup(self.state.doCleanups)
        self.addCleanup(self.state.tearDown)
        self.state.production_ready()
        self.service = self.state.service
        self.run_id = self.state.run_id
        self.fixture = test_delivery.DeliveryTests("test_complete_evidence_and_exact_media_pass_local_gate")
        self.fixture.setUp()
        self.addCleanup(self.fixture.tearDown)

    def test_service_complete_revalidates_real_pinned_montage_receipt(self):
        f = self.fixture
        m = test_delivery.m
        run = self.state.store.get(self.run_id)
        pinned = dict(run["profile"])
        pinned["production"] = json.loads(json.dumps(pinned["production"]))
        pinned["production"]["video"].pop("minimum_shot_seconds")
        pin = digest(pinned)
        p = f.p / "profile.json"
        p.write_text(canonical(pinned))
        self.assertEqual(file_digest(p), pin)
        self.addCleanup(setattr, m.delivery.channel_config, "PINNED", None)
        m.delivery.channel_config.configure_pinned_profile(p, pin)
        words = ("Sailors came home safely after the difficult rescue " * 5).split()
        (f.p / "words.json").write_text(
            json.dumps([{"text": w, "start": i * 0.09, "end": i * 0.09 + 0.08} for i, w in enumerate(words)])
        )
        test_delivery.bind_plan(f.plan, f.p)
        plan = f.plan
        plan["channel"] = "paper_detour"
        plan["canvas"] = [1440, 2560]
        plan["srt"] = "manual.srt"
        (f.p / "manual.srt").write_text("1\n00:00:00,000 --> 00:00:01,200\nSailors came home.\n")
        audio_path = f.p / "audio.m4a"
        audio_sha = file_digest(audio_path)
        mix = f.p / "mix.json"
        mix.write_text(
            json.dumps(
                {
                    "audio_sha256": audio_sha,
                    "returncode": 0,
                    "argv": ["synthetic"],
                    "track_sha256": [audio_sha],
                }
            )
        )
        plan["music"] = {
            "status": "present",
            "tracks": [{"path": "audio.m4a", "sha256": audio_sha, "start_frame": 0, "end_frame": 120}],
            "mix_evidence": m.delivery.file_record(mix),
        }
        f.manifest.write_text(json.dumps(plan))
        work = f.p / "pinned-work"
        work.mkdir()
        m.caption_sequence(plan, f.p, work, [1440, 2560], 120)
        contract = json.loads((work / "subtitle_contract.json").read_text())
        prepared = m.validate(plan, f.p)
        command = m.final_command(plan, f.p, prepared, work, f.video, None, "libx264", "800k", f.audio)
        command_path = work / "command.json"
        command_path.write_text(json.dumps(command))
        passport_path = f.p / "pinned-passport.json"
        passport_path.write_text(json.dumps(passport(m, f.manifest, prepared, f.audio, f.video)))
        frozen = m.delivery.freeze_render(
            work, passport_path, command_path, contract["engine"], prepared, f.audio, f.manifest, f.video
        )
        f.receipt.unlink()
        m.delivery.write_receipt(
            f.video, "paper_detour", contract, m.delivery.render_inputs(f.manifest, plan, f.p), render=frozen
        )
        script = self.service.artifacts.put(f.p / "transcript.txt", "script")
        audio = self.service.artifacts.put(audio_path, "audio")
        image = self.service.artifacts.put(f.p / "image.png", "image")
        srt = self.service.artifacts.put(f.p / "manual.srt", "subtitles")

        def setup(tx, r):
            r["profile"] = pinned
            r["pins"]["profile"] = pin
            for a in (script, audio, image, srt):
                r["artifacts"][a["id"]] = a
            for name, a in [("script", script), ("audio", audio), ("subtitles", srt)]:
                r["tasks"][name].update(status="complete", outputs=[a["id"]])
            r["approvals"]["script"].update(artifact_id=script["id"], sha256=script["sha256"])
            r["tasks"]["image:test"] = {
                "id": "image:test",
                "stage": "scene_image",
                "status": "complete",
                "outputs": [image["id"]],
                "dependencies": [],
            }
            task = r["tasks"]["render"]
            task["dependencies"] = ["audio", "subtitles", "image:test"]
            task["status"] = "running"
            task["claim"] = {
                "token": "pinned-synthetic",
                "worker": "fixture",
                "input_hash": input_hash(r, task),
                "estimated_units": 0,
                "expires_at": self.state.clock + 900,
            }

        self.state.store.mutate(self.run_id, setup)
        run = self.state.store.get(self.run_id)
        task = run["tasks"]["render"]
        claim = task["claim"]
        records = [
            m.delivery.file_record(x)
            for x in (f.manifest, audio_path, f.p / "image.png", f.p / "manual.srt", mix, p)
        ]
        execution = f.p / "execution.json"
        execution.write_text(
            json.dumps(
                {
                    "run_id": self.run_id,
                    "task_id": "render",
                    "kind": "montage",
                    "claim_token": claim["token"],
                    "input_hash": claim["input_hash"],
                    "state": "completed",
                    "returncode": 0,
                    "script_sha256": file_digest(ROOT / "automation/ffmpeg_montage/montage.py"),
                    "argv": [
                        sys.executable,
                        str(ROOT / "automation/ffmpeg_montage/montage.py"),
                        str(f.manifest),
                        "--pinned-profile",
                        str(p),
                        "--pinned-profile-sha256",
                        pin,
                    ],
                    "outputs": [str(f.video.resolve())],
                    "output_artifacts": [m.delivery.file_record(f.video)],
                    "inputs": records,
                }
            )
        )
        proof = f.p / "proof.json"
        proof.write_text(
            json.dumps(
                {
                    "schema": "ytv-production-delivery-v1",
                    "media_sha256": file_digest(f.video),
                    "requirements_sha256": self.service.requirements(run)["sha256"],
                    "manifest": m.delivery.file_record(f.manifest),
                    "execution": m.delivery.file_record(execution),
                    "renderer_receipt": m.delivery.file_record(f.receipt),
                }
            )
        )
        receipt = self.state.receipt("render", claim, f.video)
        data = json.loads(receipt.read_text())
        data["delivery_evidence"] = m.delivery.file_record(proof)
        receipt.write_text(json.dumps(data))
        measured = {"video": [{"nb_frames": "120", "duration": "4"}], "duration_seconds": 4}
        m.delivery.channel_config.PINNED = None
        # Only media decoding and installed-font checks are mocked for synthetic bytes;
        # actual completion, canonical receipt, profile and provenance checks execute.
        with (
            patch("ytvideos.media_checks.validate_video", return_value=measured),
            patch("ytvideos.service.validate_delivery_summary"),
            patch("ytvideos.media_checks.validate_font_face"),
        ):
            original = p.read_bytes()
            p.write_text('{"tampered":true}')
            with self.assertRaises(WorkflowError):
                self.service.complete(self.run_id, "render", claim["token"], f.video, receipt, actual_units=0)
            p.write_bytes(original)
            result = self.service.complete(
                self.run_id, "render", claim["token"], f.video, receipt, actual_units=0
            )
        self.assertEqual(result["status"], "complete")
