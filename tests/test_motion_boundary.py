"""The canonical runtime cannot turn an episode fork into a video permit."""
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import test_workflow
from ytvideos.context import (TASK_EXECUTION_REFERENCE, VIDEO_CLIPS_REFERENCE,
                             snapshot_references, validate_reference_routes)
from ytvideos.errors import Conflict, WorkflowError
from ytvideos.util import digest


class MotionBoundaryTests(unittest.TestCase):
    def setUp(self):
        self.fixture = test_workflow.WorkflowContract()
        self.fixture.setUp()
        self.addCleanup(self.fixture.doCleanups)
        self.addCleanup(self.fixture.tearDown)
        self.service = self.fixture.service
        self.run_id = self.fixture.run_id

    def snapshot(self):
        with self.fixture.store.transaction() as tx:
            operations = [json.loads(row[0]) for row in tx.execute(
                "SELECT doc FROM operations WHERE run_id=? ORDER BY key", (self.run_id,)).fetchall()]
        return (self.fixture.store.get(self.run_id), self.fixture.store.events(self.run_id), operations)

    def incomplete_migration(self, route, path):
        def change(tx, run):
            run["reference_snapshot"]["routes"][route].remove(path)
            # Models an incomplete migration, not accidental hash corruption.
            run["pins"]["references"] = digest(run["reference_snapshot"])
        self.fixture.store.mutate(self.run_id, change)

    def test_matching_snapshot_hash_cannot_hide_missing_required_route(self):
        self.incomplete_migration("research", TASK_EXECUTION_REFERENCE)
        before = self.snapshot()
        with self.assertRaisesRegex(WorkflowError, "route research is incompatible.*explicit migration"):
            self.service.claim(self.run_id, "research", "fixture-worker")
        with self.assertRaisesRegex(WorkflowError, "task-execution"):
            self.service.context(self.run_id, "research")
        self.assertEqual(self.snapshot(), before)

    def test_incomplete_video_route_blocks_existing_claim_before_dispatch(self):
        self.fixture.production_ready()
        claim = self.service.claim(self.run_id, "audio", "fixture-worker", estimated_units=2)
        payload = self.service.operation_payload(self.run_id, "audio", "tts")
        self.incomplete_migration("render", VIDEO_CLIPS_REFERENCE)
        before = self.snapshot()
        with self.assertRaisesRegex(WorkflowError, "route render is incompatible.*video-clips"):
            self.service.begin_operation(self.run_id, "audio", claim["token"], "tts", payload)
        self.assertEqual(self.snapshot(), before)

    def test_saved_approved_batch_does_not_enable_unsupported_video_action(self):
        self.fixture.production_ready()
        self.fixture.store.mutate(self.run_id, lambda tx, run: run.update(motion_batch={
            "status": "approved", "approval": {"source": "fixture-owner-decision", "message": "approved"}}))
        claim = self.service.claim(self.run_id, "audio", "fixture-worker", estimated_units=2)
        before = self.snapshot()
        for action in ("flow_video", "external_video", "scene_motion"):
            with self.subTest(action=action), self.assertRaisesRegex(WorkflowError, "not permitted"):
                self.service.begin_operation(self.run_id, "audio", claim["token"], action, {"approved": True})
        self.assertEqual(self.snapshot(), before)

    def test_changed_code_after_claim_cannot_dispatch_or_change_pins(self):
        self.fixture.production_ready()
        claim = self.service.claim(self.run_id, "audio", "fixture-worker", estimated_units=2)
        payload = self.service.operation_payload(self.run_id, "audio", "tts")
        before = self.snapshot()
        with patch("ytvideos.service.code_identity", return_value="incompatible-episode-fork"):
            with self.assertRaisesRegex(Conflict, "pinned checkout"):
                self.service.begin_operation(self.run_id, "audio", claim["token"], "tts", payload)
        self.assertEqual(self.snapshot(), before)


class ReferenceRouteCompatibilityTests(unittest.TestCase):
    def test_saved_channel_profile_cannot_disappear_from_routes_on_any_channel(self):
        root = Path(__file__).resolve().parents[1]
        for path in sorted((root / "channels").glob("*/channel.json")):
            profile = json.loads(path.read_text())
            for format in ("short", "long"):
                with self.subTest(channel=profile["id"], format=format):
                    snapshot = snapshot_references(root, profile, format)
                    channel_profile = f"channels/{profile['id']}/PROFILE.md"
                    validate_reference_routes(snapshot, profile, format)
                    if channel_profile not in snapshot["documents"]:
                        self.assertFalse((root / channel_profile).is_file())
                        continue
                    for paths in snapshot["routes"].values():
                        paths.remove(channel_profile)
                    with self.assertRaisesRegex(WorkflowError, "incompatible.*PROFILE"):
                        validate_reference_routes(snapshot, profile, format)

    def test_generic_profile_without_channel_document_remains_supported(self):
        root = Path(__file__).resolve().parents[1]
        profile = {"id": "generic_unconfigured"}
        snapshot = snapshot_references(root, profile, "short")
        self.assertNotIn("channels/generic_unconfigured/PROFILE.md", snapshot["documents"])
        validate_reference_routes(snapshot, profile, "short")

    def test_auto_added_profile_without_context_declaration_stays_required(self):
        root = Path(__file__).resolve().parents[1]
        profile = {"id": "generic_channel"}
        baseline = snapshot_references(root, profile, "short")
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            channel_profile = "channels/generic_channel/PROFILE.md"
            for path in [*baseline["documents"], channel_profile]:
                target = project / path
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text("Synthetic instruction fixture.\n")
            snapshot = snapshot_references(project, profile, "short")
            validate_reference_routes(snapshot, profile, "short")
            for paths in snapshot["routes"].values():
                paths.remove(channel_profile)
            with self.assertRaisesRegex(WorkflowError, "incompatible.*PROFILE"):
                validate_reference_routes(snapshot, profile, "short")


if __name__ == "__main__":
    unittest.main()
