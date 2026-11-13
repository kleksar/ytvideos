"""Complete software lifecycle with synthetic media and explicit fake providers.

These tests exercise real state transitions, Ed25519 approvals, content-addressed
files and read-back contracts. They do not test creative quality or a live API.
No task state or approval is installed by direct database fixture mutation.
"""

import base64
from datetime import datetime, timedelta, timezone
import json
from pathlib import Path
import shutil
import struct
import subprocess
import tempfile
import unittest
from unittest.mock import patch
import uuid
import wave
import zlib

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat

from ytvideos.errors import Conflict, WorkflowError
from ytvideos.media_checks import probe_media
from ytvideos.release import ReleasePolicy, ReleaseSpec, requirement_matrix
from ytvideos.service import Production
from ytvideos.store import Store
from ytvideos.util import canonical, file_digest
from ytvideos.workflow import REQUIRED_CHECKS, STAGES


ROOT = Path(__file__).resolve().parents[1]
VIDEO_ID = "VID00000001"
SCRIPT = (
    "This synthetic story follows a traveller choosing between two routes. The short route looks easy, "
    "but a closed bridge forces a return. A map shows a longer path that reaches the same destination. "
    "The traveller follows the longer route and arrives. The contrast explains why distance alone does "
    "not determine the time a journey takes. These events are invented software fixtures, not research."
)


@unittest.skipUnless(shutil.which("ffmpeg"), "ffmpeg is required for the local synthetic MP4 fixture")
class SyntheticLifecycleTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.directory = Path(temporary.name)
        self.now = 1000.0
        source_pin = patch("ytvideos.service.code_identity", return_value="lifecycle-fixture-source-v1")
        source_pin.start()
        self.addCleanup(source_pin.stop)
        self.key = Ed25519PrivateKey.generate()
        self.public_key = base64.b64encode(self.key.public_key().public_bytes(Encoding.Raw, PublicFormat.Raw)).decode()
        self.db = self.directory / "state.sqlite3"
        self.store = Store(self.db)
        self.service = self.restarted_service()
        capabilities = {cap: {"available": True, "billing": "included", "evidence": "explicit fake provider fixture"}
                        for _, _, caps, _ in STAGES.values() for cap in caps}
        capabilities["image.generate"] = {"available": True, "billing": "included", "evidence": "synthetic PNG fixture"}
        # Test a small-media policy, never pretend that a 160px fixture is a Paper delivery.
        profile = json.loads((ROOT / "channels/paper_detour/channel.json").read_text())
        profile.update(id="synthetic_lifecycle", name="Synthetic lifecycle fixture")
        profile["production"]["formats"]["long"] = {
            "video": {"canvas": [160, 90], "fps": "5/1"}, "end_screen_seconds": 0}
        profile["production"]["audio"]["music"] = "none"
        profile["production"]["visual"]["motion"] = "none"
        profile["production"]["captions"] = {"mode": "none", "srt": "required"}
        profile_dir = self.directory / "profiles" / profile["id"]
        profile_dir.mkdir(parents=True)
        (profile_dir / "channel.json").write_text(json.dumps(profile))
        self.run = self.service.create(profile["id"], "Full lifecycle software fixture", format="long",
                                       profiles=profile_dir.parent, capabilities=capabilities, budget_units=10)
        self.run_id = self.run["id"]
        self.delivery_proofs = {}
        self.audio = self.directory / "synthetic-silence.wav"
        with wave.open(str(self.audio), "wb") as output:
            output.setparams((1, 2, 8000, 0, "NONE", "not compressed"))
            output.writeframes(b"\x00\x00" * 8000 * 30)
        self.image = self.directory / "synthetic-scene.png"
        def chunk(kind, body):
            return struct.pack(">I", len(body)) + kind + body + struct.pack(">I", zlib.crc32(kind + body))
        row = b"\x00" + b"\xff\x88\x00" * 16
        self.image.write_bytes(b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", 16, 9, 8, 2, 0, 0, 0))
                               + chunk(b"IDAT", zlib.compress(row * 9)) + chunk(b"IEND", b""))
        self.caption = self.write("1\n00:00:00,000 --> 00:00:29,500\nSynthetic software fixture narration.\n", "captions.srt")
        self.plan = {
            "run_id": self.run_id, "revision": 1, "channel_id": self.run["profile"]["youtube_channel_id"],
            "format": "long", "has_speech": True,
            "metadata": {"title": "Synthetic lifecycle fixture", "description": "A synthetic software test.",
                         "tags": ["software", "test fixture"], "category_id": "27", "language": "en", "audio_language": "en",
                         "made_for_kids": False, "contains_synthetic_media": True, "license": "youtube",
                         "age_restricted": False, "paid_promotion": False},
            "playlist_id": "PL_SYNTHETIC_FIXTURE_01",
            "ab_variants": [{"title": "Fixture option one", "thumbnail_sha256": file_digest(self.image)},
                            {"title": "Fixture option two", "thumbnail_sha256": file_digest(self.image)}],
        }

    def restarted_service(self):
        return Production(Store(self.db), self.directory / "workspace", ROOT,
                          approval_public_key=self.public_key, clock=lambda: self.now)

    def write(self, value, filename=None):
        path = self.directory / (filename or str(uuid.uuid4()) + ".json")
        path.write_text(value if isinstance(value, str) else json.dumps(value))
        return path

    def qa_receipt(self, task_id, claim, output):
        run = self.store.get(self.run_id)
        stage = run["tasks"][task_id]["stage"]
        names = set(REQUIRED_CHECKS[stage])
        if stage == "review":
            names.update(self.service.requirements(run)["review_checks"])
        checks = [{"name": name, "status": "pass", "method": "synthetic fixture checker",
                   "observed": {"fixture_only": True, "artifact_sha256": file_digest(output)}}
                  for name in sorted(names)]
        for check in checks:
            if check["name"] == "independent_review":
                check["observed"]["reviewer"] = "separate-fixture-reviewer"
            if stage == "review":
                media = self.service._artifact(run, "render")
                evidence = self.write({"synthetic_test_only": True, "check": check["name"],
                                       "media_sha256": media["sha256"],
                                       "note": "Schema/state test, no claim of creative or perceptual QA."})
                check["observed"] = {"artifact_sha256": media["sha256"], "reviewer": "synthetic-fixture-reviewer",
                    "notes": "Synthetic state transition with an explicit test-only policy and evidence.",
                    "coverage": [{"start_seconds": 0, "end_seconds": 30}],
                    "evidence": {"path": str(evidence), "sha256": file_digest(evidence)}}
        receipt = {"run_id": self.run_id, "task_id": task_id, "worker": claim["worker"],
                   "input_hash": claim["input_hash"], "output_sha256": file_digest(output), "checks": checks}
        if stage == "render":
            receipt["delivery_evidence"] = self.delivery_proofs[file_digest(output)]
        return self.write(receipt)

    def observe(self, operation, values, *, method="adapter_execution"):
        evidence = self.write({"operation_key": operation["key"], "attempt_id": operation["attempt_id"],
            "task_input_hash": operation["task_input_hash"], "status": "confirmed",
            "provider_evidence": {"method": method, "observation_id": "fixture-observation-" + uuid.uuid4().hex,
                                  "observed": {"fixture_only": True, **values}}})
        return self.service.observe_operation(self.run_id, operation["key"], "confirmed", evidence,
                                              event_id="fixture-provider-event-" + uuid.uuid4().hex)

    def begin(self, task_id, claim, action):
        payload = self.service.operation_payload(self.run_id, task_id, action)
        return self.service.begin_operation(self.run_id, task_id, claim["token"], action, payload)

    def finish(self, task_id, output, *, claim=None, action=None, values=None):
        output = output if isinstance(output, Path) else self.write(output)
        claim = claim or self.service.claim(self.run_id, task_id, "fixture-worker-" + task_id)
        if action:
            operation = self.begin(task_id, claim, action)
            self.observe(operation, values or {"output_sha256": file_digest(output)})
        result = self.service.complete(self.run_id, task_id, claim["token"], output,
                                       self.qa_receipt(task_id, claim, output), actual_units=0)
        self.assertEqual(result["status"], "complete")
        return claim

    def approval(self, kind):
        run = self.store.get(self.run_id)
        stage = "script" if kind == "script" else "render"
        artifact = run["artifacts"][run["tasks"][stage]["outputs"][0]]
        event = {"event_id": "fixture-user-event-" + uuid.uuid4().hex, "actor": "fixture-user",
                 "source": "test://actual-signed-fixture-event", "run_id": self.run_id, "kind": kind,
                 "artifact_id": artifact["id"], "sha256": artifact["sha256"],
                 "created_at": (datetime.now(timezone.utc) - timedelta(seconds=1)).isoformat(),
                 "scope": "produce_video" if kind == "script" else "schedule_publication"}
        return {"event": event, "signature": base64.b64encode(self.key.sign(canonical(event).encode())).decode()}

    def render(self, color, filename):
        path = self.directory / filename
        claim = self.service.claim(self.run_id, "render", "fixture-worker-render")
        command = ["ffmpeg", "-v", "error", "-nostdin", "-f", "lavfi", "-i",
                   f"color=c={color}:s=160x90:r=5:d=30", "-i", str(self.audio),
                   "-c:v", "libx264", "-preset", "ultrafast", "-pix_fmt", "yuv420p", "-vf",
                   "setsar=1,setparams=color_primaries=bt709:color_trc=bt709:colorspace=bt709:range=limited",
                   "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-color_range", "tv",
                   "-c:a", "aac", "-shortest", "-movflags", "+faststart", str(path)]
        subprocess.run(command, check=True, capture_output=True, timeout=30)
        manifest = self.write({"channel": self.run["channel"], "format": "long", "canvas": [160, 90], "fps": "5/1",
            "audio": str(self.audio), "srt": str(self.caption), "subtitles": {"mode": "none"},
            "scenes": [{"id": "route", "image": str(self.image), "start_frame": 0, "end_frame": 150}]})

        def record(source):
            return {"path": str(source), "sha256": file_digest(source)}

        execution = self.write({"run_id": self.run_id, "task_id": "render", "claim_token": claim["token"],
            "input_hash": claim["input_hash"], "kind": "host_render", "state": "completed", "returncode": 0,
            "argv": command, "outputs": [str(path)], "output_artifacts": [record(path)],
            "inputs": [record(item) for item in (manifest, self.audio, self.image, self.caption)]})
        requirements = self.service.requirements(self.store.get(self.run_id))
        proof = self.write({"schema": "ytv-production-delivery-v1", "media_sha256": file_digest(path),
                           "requirements_sha256": requirements["sha256"], "manifest": record(manifest),
                           "execution": record(execution)})
        self.delivery_proofs[file_digest(path)] = record(proof)
        self.finish("render", path, claim=claim)
        self.finish("review", {"fixture_only": True, "reviewed_sha256": file_digest(path),
                               "requirements_sha256": requirements["sha256"], "probe": probe_media(path)})
        return path

    def produce_to_mp4_review(self):
        self.finish("research", {"selected_topic": {"title": "A route choice", "angle": "Cause and consequence",
            "viewer_value": "Explain why the shortest route can take longer"},
            "sources": [{"url": "https://example.com/synthetic-fixture", "fixture_only": True}]})
        self.finish("script", SCRIPT)
        self.assertEqual(self.service.next(self.run_id)["status"], "awaiting_script_approval")
        self.service.approve(self.approval("script"))
        claims = {task: self.service.claim(self.run_id, task, "fixture-worker-" + task)
                  for task in ("storyboard", "audio", "packaging")}
        self.finish("packaging", self.plan, claim=claims["packaging"])
        parallel = self.store.get(self.run_id)
        self.assertEqual(parallel["tasks"]["packaging"]["status"], "complete")
        self.assertEqual(parallel["tasks"]["audio"]["status"], "running")
        self.assertEqual(parallel["tasks"]["storyboard"]["status"], "running")
        self.assertEqual(parallel["tasks"]["render"]["status"], "pending")
        self.finish("storyboard", {"scenes": [{"id": "route", "prompt": "A synthetic map scene",
                                                "visual_intent": "Illustrate a route choice"}]}, claim=claims["storyboard"])
        self.finish("audio", self.audio, claim=claims["audio"], action="tts")
        self.finish("image:route", self.image, action="image")
        self.finish("subtitles", self.caption)
        video = self.render("orange", "synthetic-v1.mp4")
        self.assertEqual(self.service.next(self.run_id)["status"], "awaiting_mp4_approval")
        with self.assertRaises(Conflict):
            self.service.claim(self.run_id, "upload", "premature-uploader")
        return video

    def bound_spec(self, video):
        data = {**self.plan, "media_sha256": file_digest(video), "duration_seconds": 30,
                "publish_at": (datetime.now(timezone.utc) + timedelta(days=2)).isoformat(),
                "thumbnail_sha256": file_digest(self.image),
                "caption": {"sha256": file_digest(self.caption), "language": "en"},
                "end_screen": {"start_seconds": 20, "end_seconds": 30,
                               "elements": [{"type": "subscribe", "target_id": self.plan["channel_id"]}]}}
        spec = ReleaseSpec.from_dict(data)
        path = self.write(spec.to_dict())
        result = self.service.prepare_release(self.run_id, path, assets=[self.image, self.caption])
        self.assertEqual(result["blockers"], [])
        return spec, path

    def readbacks(self, spec, phase):
        policy = ReleasePolicy.from_dict(self.run["profile"]["release_policy"])
        receipts, files = [], []
        phases = {"pre_schedule"} if phase == "pre_schedule" else {"pre_schedule", "scheduled"}
        for requirement in requirement_matrix(spec, policy):
            if not requirement.applicable or requirement.phase not in phases:
                continue
            evidence = self.write({"fixture_only": True, "video_id": VIDEO_ID, "channel_id": spec.channel_id,
                                   "saved": {requirement.key: requirement.expected}})
            files.append(str(evidence))
            receipts.append({"key": requirement.key, "channel_id": spec.channel_id, "video_id": VIDEO_ID,
                "release_sha256": spec.sha256, "method": "studio_readback" if requirement.provider == "studio" else "api_readback",
                "observation_id": "fixture-readback-" + uuid.uuid4().hex, "evidence_sha256": file_digest(evidence),
                "observed_at": (datetime.now(timezone.utc) - timedelta(seconds=1)).isoformat(),
                "observed_value": requirement.expected})
        return {"receipts": receipts, "evidence_files": files}

    def test_full_signed_lifecycle_reaches_verified_private_future_schedule(self):
        video = self.produce_to_mp4_review()
        spec, _ = self.bound_spec(video)  # Preparation is permitted before MP4 approval.
        self.service.approve(self.approval("mp4"))
        uploaded = {"channel_id": spec.channel_id, "video_id": VIDEO_ID, "privacy": "private",
                    "media_sha256": file_digest(video), "processing_status": "succeeded"}
        self.finish("upload", uploaded, action="upload", values=uploaded)
        configure = self.service.claim(self.run_id, "configure_release", "fixture-studio-worker")
        for action in ("metadata", "thumbnail", "captions", "playlist", "end_screen"):
            operation = self.begin("configure_release", configure, action)
            self.observe(operation, operation["payload"], method="studio_readback" if action == "end_screen" else "api_readback")
        configured = self.readbacks(spec, "pre_schedule")
        self.finish("configure_release", configured, claim=configure)
        # Original bridge scratch paths disappear; immutable evidence copies must survive.
        for path in configured["evidence_files"]:
            Path(path).unlink()
        self.service = self.restarted_service()
        scheduled = self.service.claim(self.run_id, "schedule", "fixture-scheduler")
        operation = self.begin("schedule", scheduled, "schedule")
        self.assertEqual(operation["payload"]["privacy"], "private")
        self.assertEqual(operation["payload"]["publish_at"], spec.to_dict()["publish_at"])
        with self.assertRaises(Conflict):
            self.begin("schedule", scheduled, "schedule")
        self.observe(operation, operation["payload"], method="api_readback")
        self.finish("schedule", self.readbacks(spec, "scheduled"), claim=scheduled)
        final_readbacks = self.readbacks(spec, "scheduled")
        self.finish("verify_publication", final_readbacks)
        final = self.service.next(self.run_id)
        self.assertEqual(final["status"], "scheduled")
        self.assertEqual(final["tasks"], [])
        self.assertEqual(final["approval_requests"], [])
        self.assertEqual({r["key"]: r["observed_value"] for r in final_readbacks["receipts"]}["visibility"], "private")
        self.assertGreater(datetime.fromisoformat(spec.to_dict()["publish_at"].replace("Z", "+00:00")), datetime.now(timezone.utc))
        run = self.store.get(self.run_id)
        approvals = [e for e in self.store.events(self.run_id) if e["kind"] == "user.approved"]
        self.assertEqual([e["payload"]["kind"] for e in approvals], ["script", "mp4"])
        self.assertTrue(all(task["status"] == "complete" for task in run["tasks"].values()))
        self.assertTrue(any(a["kind"] == "remote_evidence" for a in run["artifacts"].values()))
        for artifact in run["artifacts"].values():
            self.assertTrue(self.service.artifacts.resolve(artifact).is_file())

    def test_changed_mp4_requires_its_own_approval_and_release_binding(self):
        old_video = self.produce_to_mp4_review()
        _, old_spec_path = self.bound_spec(old_video)
        old_approval = self.approval("mp4")
        self.service.approve(old_approval)
        self.service.revise(self.run_id, "render", "Change the synthetic render fixture")
        changed = self.store.get(self.run_id)
        self.assertIn("script", changed["approvals"])
        self.assertNotIn("mp4", changed["approvals"])
        self.assertNotIn("release_spec", changed["publication"])
        self.assertEqual(changed["tasks"]["packaging"]["status"], "complete")
        new_video = self.render("blue", "synthetic-v2.mp4")
        self.assertNotEqual(file_digest(old_video), file_digest(new_video))
        with self.assertRaises(Conflict):
            self.service.approve(old_approval)
        with self.assertRaises(WorkflowError):
            self.service.prepare_release(self.run_id, old_spec_path)
        with self.assertRaises(Conflict):
            self.service.claim(self.run_id, "upload", "stale-uploader")
        self.bound_spec(new_video)
        self.service.approve(self.approval("mp4"))
        claim = self.service.claim(self.run_id, "upload", "current-uploader")
        operation = self.begin("upload", claim, "upload")
        self.assertEqual(operation["payload"]["media_sha256"], file_digest(new_video))
        self.assertEqual(operation["payload"]["privacy"], "private")


if __name__ == "__main__":
    unittest.main()
