"""Behavioral tests of the gates, restart safety, concurrency and artifact identity."""
import base64
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit
import uuid

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat

from ytvideos.errors import Conflict, WorkflowError
from ytvideos.service import Production
from ytvideos.store import Store
from ytvideos.util import canonical, file_digest
from ytvideos.workflow import STAGES, input_hash, required_checks


ROOT = Path(__file__).resolve().parents[1]
OPENING = "Nobody was waiting at the bridge. I thought I had found the fastest road home."
ENDING = "The empty shortcut had saved no time at all. I finally understood why"
PAYOFF = "The longer road took me safely across the river."
SCRIPT = (OPENING + " The empty lane looked inviting, but the bridge deck was missing. "
          "The map had marked that crossing as closed. I went back to the junction and followed the longer route. "
          + PAYOFF + " " + ENDING)


def script_review_observation(script_path, evidence_path, *, loop=False, reviewer="separate-test-reviewer"):
    """Synthetic software evidence only; no real independent/model review is claimed."""
    from ytvideos.script_review import build_review_input
    text = script_path.read_bytes().decode("utf-8")
    observed = {"artifact_sha256": file_digest(script_path), "reviewer": reviewer}
    packet_path = evidence_path.with_name(evidence_path.name + ".input.json")
    packet = build_review_input(text, observed["artifact_sha256"],
                               **({"opening": OPENING, "ending": ENDING} if loop else {}))
    packet_path.write_text(json.dumps(packet))
    document = {"schema": "ytv-script-review-v1", "script_sha256": observed["artifact_sha256"],
                "reviewer": reviewer, "source": {"tool": "synthetic-fixture-only", "session_id": reviewer},
                "input": {"path": str(packet_path), "sha256": file_digest(packet_path)}, "decision": "pass",
                "first_listener": {"understood": "Synthetic fixture: the text supplies the exact test input.",
                                   "attention": "Synthetic fixture tests artifact binding, never real audience interest.",
                                   "quotes": [text.strip()]}, "findings": [], "narrative_loop": None}
    if loop:
        document["narrative_loop"] = {"opening": OPENING, "ending": ENDING,
            "joined_excerpt": ENDING + "\n" + OPENING, "decision": "pass", "observations": {
                    "continuation": "Fixture: 'I finally understood why' continues into the empty-bridge observation.",
                    "cold_open": "Fixture: an empty bridge and a route choice introduce the situation without prior playback.",
                    "payoff_quote": PAYOFF,
                    "payoff_before_repeat": "Fixture: the traveller has crossed safely before the repeated observation explains the empty road.",
                    "two_cycle_read": "Fixture: the exact doubled input tests the preserved replay material, not actual reading.",
                    "restart_test": "Fixture: the why clause continues into its explanation; this does not claim semantic classification."}}
    evidence_path.write_text(json.dumps(document))
    observed["evidence"] = {"path": str(evidence_path), "sha256": file_digest(evidence_path)}
    return observed


def loop_observation(script_path, evidence_path):
    observed = script_review_observation(script_path, evidence_path, loop=True)
    return {**observed, "opening": OPENING, "ending": ENDING, "joined_excerpt": ENDING + "\n" + OPENING}


class WorkflowContract(unittest.TestCase):
    postgres = False

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.directory = Path(self.temp.name)
        self.clock = 1000.0
        self.private_key = Ed25519PrivateKey.generate()
        public = base64.b64encode(self.private_key.public_key().public_bytes(Encoding.Raw, PublicFormat.Raw)).decode()
        self.db = str(self.directory / "state.sqlite3")
        if self.postgres:
            import psycopg
            from psycopg import sql
            url = os.environ["YTV_TEST_POSTGRES_URL"]
            schema = "ytv_test_" + uuid.uuid4().hex
            with psycopg.connect(url, autocommit=True) as connection:
                connection.execute(sql.SQL("CREATE SCHEMA {}").format(sql.Identifier(schema)))

            def cleanup_schema():
                with psycopg.connect(url, autocommit=True) as connection:
                    connection.execute(sql.SQL("DROP SCHEMA {} CASCADE").format(sql.Identifier(schema)))

            self.addCleanup(cleanup_schema)
            parts = urlsplit(url)
            query = parse_qsl(parts.query, keep_blank_values=True)
            options = " ".join(value for key, value in query if key == "options")
            query = [(key, value) for key, value in query if key != "options"]
            query.append(("options", (options + " -csearch_path=" + schema).strip()))
            self.db = urlunsplit((parts.scheme, parts.netloc, parts.path, urlencode(query), parts.fragment))
        self.store = Store(self.db)
        # Isolate these state-machine tests from concurrent edits to the source checkout.
        self.pin = patch("ytvideos.service.code_identity", return_value="test-code-v1")
        self.pin.start()
        self.addCleanup(self.pin.stop)
        self.service = Production(self.store, self.directory / "workspace", ROOT,
                                  approval_public_key=public, clock=lambda: self.clock)
        capabilities = {cap: {"available": True, "evidence": "test harness", "billing": "included"}
                        for _, _, caps, _ in STAGES.values() for cap in caps}
        capabilities["image.generate"] = {"available": True, "evidence": "test harness", "billing": "included"}
        self.run = self.service.create("paper_detour", "software fixture", capabilities=capabilities, budget_units=10)
        self.run_id = self.run["id"]

    def tearDown(self):
        self.temp.cleanup()

    def output(self, value, name=None):
        path = self.directory / (name or str(uuid.uuid4()))
        path.write_text(value if isinstance(value, str) else json.dumps(value))
        return path

    def receipt(self, task_id, claim, path, *, remove=None):
        run = self.store.get(self.run_id)
        task = run["tasks"][task_id]
        checks = [{"name": name, "status": "pass", "method": "unit-test fixture",
                   "observed": {"fixture": True}} for name in sorted(required_checks(task["stage"], self.service.requirements(run)))
                  if name != remove]
        review = None
        if task["stage"] == "script":
            review = script_review_observation(path, self.directory / (str(uuid.uuid4()) + "-review.json"),
                                               loop="narrative_loop" in required_checks(task["stage"], self.service.requirements(run)))
        for check in checks:
            if task["stage"] == "audio" and check["name"] == "listening":
                from ytvideos.media_checks import probe_media
                proof = self.output({"schema": "ytv-audio-listening-v1", "artifact_sha256": file_digest(path), "reviewer": "fixture-listener", "decision": "pass", "listened_complete": True, "source": "synthetic-test", "message": "Synthetic positive full-listening fixture; accepted."})
                check["observed"] = {"artifact_sha256": file_digest(path), "reviewer": "fixture-listener",
                    "notes": "Synthetic listening contract fixture.",
                    "inspection": {"mode": "audio_listening", "tool": "synthetic fixture", "playback_speed": 1.0},
                    "coverage": [{"start_seconds": 0, "end_seconds": probe_media(path)["duration_seconds"]}],
                    "evidence": {"path": str(proof), "sha256": file_digest(proof)}}
            if check["name"] == "thumbnail_plan":
                from thumbnail_fixtures import plan_fixture
                check["observed"] = plan_fixture(json.loads(path.read_text()), self.service._artifact(run, "script")["sha256"])
            if check["name"] == "independent_review":
                check["observed"] = review
            if check["name"] == "narrative_loop":
                check["observed"] = {**review, "opening": OPENING, "ending": ENDING, "joined_excerpt": ENDING + "\n" + OPENING}
        return self.output({"run_id": self.run_id, "task_id": task_id, "worker": claim["worker"],
                            "input_hash": claim["input_hash"], "output_sha256": file_digest(path), "checks": checks})

    def complete(self, task_id, value):
        path = self.output(value)
        claim = self.service.claim(self.run_id, task_id, "unit-author")
        receipt = self.receipt(task_id, claim, path)
        self.service.complete(self.run_id, task_id, claim["token"], path, receipt, actual_units=0)
        return claim, path, receipt

    def script_ready(self):
        self.complete("research", {"selected_topic": {"title": "Fixture", "angle": "Causality", "viewer_value": "A tested lesson"},
                                   "sources": [{"url": "https://example.com/fixture"}]})
        self.complete("script", SCRIPT)

    def signed(self, kind="script", **changes):
        task = "script" if kind == "script" else "render"
        run = self.store.get(self.run_id)
        artifact = run["artifacts"][run["tasks"][task]["outputs"][0]]
        event = {"event_id": "test-" + str(uuid.uuid4()), "actor": "unit-test-user", "source": "test://message/1",
                 "run_id": self.run_id, "kind": kind, "artifact_id": artifact["id"], "sha256": artifact["sha256"],
                 "created_at": (datetime.now(timezone.utc) - timedelta(seconds=1)).isoformat(),
                 "scope": "produce_video" if kind == "script" else "schedule_publication", **changes}
        return {"event": event, "signature": base64.b64encode(self.private_key.sign(canonical(event).encode())).decode()}

    def production_ready(self):
        self.script_ready()
        self.service.approve(self.signed())

    def test_new_request_does_not_require_existing_bundle(self):
        result = self.service.next(self.run_id)
        self.assertEqual([t["id"] for t in result["tasks"]], ["research"])
        self.assertEqual(self.service.context(self.run_id, "research")["output_kind"], "research")
        self.assertIn("ytv-write-script", self.run["skills"])

    def test_task_context_returns_relevant_standards(self):
        expected = {
            "research": {"docs/standards/editorial.md", "docs/standards/thumbnails.md"},
            "script": {"docs/standards/editorial.md", "docs/standards/thumbnails.md"},
            "packaging": {"docs/standards/release.md", "docs/standards/thumbnails.md"},
            "review": {"docs/standards/delivery.md", "docs/standards/editorial.md",
                       "docs/standards/thumbnails.md"},
        }
        for task_id, references in expected.items():
            with self.subTest(task=task_id):
                actual = self.service.context(self.run_id, task_id)["references"]
                self.assertTrue(references.issubset(actual))
                self.assertIn("channels/paper_detour/PROFILE.md", actual)
        self.assertNotIn("docs/standards/thumbnails.md",
                         self.service.context(self.run_id, "storyboard")["references"])

    def test_request_deduplication_rejects_changed_intent(self):
        same = self.service.create("paper_detour", "software fixture", request_id=self.run["request_id"])
        self.assertEqual(same["id"], self.run_id)
        with self.assertRaises(Conflict):
            self.service.create("paper_detour", "changed intent", request_id=self.run["request_id"])

    def test_repeated_create_uses_saved_run_after_a_required_recipe_is_removed(self):
        project = self.directory / "retry-project"
        entries = []
        for name, skill in self.run["skills"].items():
            path = project / skill["path"]
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(skill["text"])
            entries.append({"name": name, "path": skill["path"]})
        for document in self.run["reference_snapshot"]["documents"].values():
            path = project / document["path"]
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(document["text"])
        (project / ".agent").mkdir(exist_ok=True)
        (project / ".agent/skill-catalog.json").write_text(json.dumps({"skills": entries}))
        recipe = project / "docs/retry-recipe.md"
        recipe.write_text("The accepted recipe must survive request redelivery.")
        profile = {**self.run["profile"], "context_references": [
            *self.run["profile"].get("context_references", []),
            {"path": "docs/retry-recipe.md", "stages": ["render"]}]}
        (project / "channels/paper_detour/channel.json").write_text(json.dumps(profile))
        service = Production(self.store, self.directory / "retry-workspace", project)
        request_id = "retry-" + uuid.uuid4().hex
        original = service.create("paper_detour", "repeat this request", request_id=request_id)
        context = service.context(original["id"], "render")
        recipe.unlink()
        self.assertEqual(context, service.context(original["id"], "render"))
        self.assertEqual(original, service.create("paper_detour", "repeat this request", request_id=request_id))
        for changes in ({"channel": "nonexistent_channel"}, {"intent": "different request"}, {"format": "long"}):
            with self.subTest(changes=changes), self.assertRaises(Conflict):
                service.create(**{"channel": "paper_detour", "intent": "repeat this request",
                                  "request_id": request_id, **changes})
        self.assertEqual(len([run for run in self.store.list() if run["request_id"] == request_id]), 1)
        self.assertEqual(len([event for event in self.store.events(original["id"])
                              if event["kind"] == "run.created"]), 1)

    def test_new_channel_uses_same_graph_without_code_edits(self):
        profile_dir = self.directory / "profiles" / "channel_ten"
        profile_dir.mkdir(parents=True)
        profile = {**self.run["profile"], "id": "channel_ten", "name": "Tenth test channel"}
        (profile_dir / "channel.json").write_text(json.dumps(profile))
        run = self.service.create("channel_ten", "new request", profiles=profile_dir.parent)
        self.assertEqual(set(run["tasks"]), set(self.run["tasks"]))

    def test_frozen_channel_is_not_started(self):
        profile_dir = self.directory / "profiles" / "frozen_fixture"
        profile_dir.mkdir(parents=True)
        profile = {**self.run["profile"], "id": "frozen_fixture", "status": "frozen"}
        (profile_dir / "channel.json").write_text(json.dumps(profile))
        with self.assertRaisesRegex(WorkflowError, "frozen"):
            self.service.create("frozen_fixture", "not an unfreeze", profiles=profile_dir.parent)

    def test_active_channel_roster_uses_the_common_workflow(self):
        for channel in ("paper_detour", "scenes_on_repeat", "nuviko_history", "two_ways_lab"):
            with self.subTest(channel=channel):
                run = self.service.create(channel, "channel activation fixture")
                self.assertEqual(run["profile"]["status"], "active")
                self.assertEqual(set(run["tasks"]), set(self.run["tasks"]))
                self.assertEqual([t["id"] for t in self.service.next(run["id"])["tasks"]], ["research"])
                self.assertEqual(run["approvals"], {})

    def test_manual_stories_is_not_admitted_to_automatic_production(self):
        with self.assertRaisesRegex(WorkflowError, "channel profile is missing"):
            self.service.create("nuviko_stories", "must remain manual")

    def test_claim_is_exclusive_across_connections(self):
        def attempt(number):
            other = Production(Store(self.db), self.directory / "workspace", ROOT, clock=lambda: self.clock)
            try:
                return other.claim(self.run_id, "research", f"worker-{number}")["token"]
            except Conflict:
                return None
        with ThreadPoolExecutor(max_workers=2) as pool:
            results = list(pool.map(attempt, [1, 2]))
        self.assertEqual(sum(result is not None for result in results), 1)

    def test_required_checks_cannot_be_empty_or_missing(self):
        claim = self.service.claim(self.run_id, "research", "worker")
        path = self.output({"selected_topic": {"title": "A", "angle": "B", "viewer_value": "C"},
                            "sources": [{"url": "https://example.com/fixture"}]})
        receipt = self.receipt("research", claim, path, remove="sources")
        with self.assertRaisesRegex(WorkflowError, "missing checks"):
            self.service.complete(self.run_id, "research", claim["token"], path, receipt)

    def test_script_is_first_human_gate(self):
        self.script_ready()
        result = self.service.next(self.run_id)
        self.assertEqual(result["status"], "awaiting_script_approval")
        self.assertEqual(result["tasks"], [])
        self.assertEqual(result["approval_requests"][0]["kind"], "script")

    def test_signature_and_exact_target_are_required(self):
        self.script_ready()
        envelope = self.signed()
        envelope["event"]["actor"] = "forged"
        with self.assertRaisesRegex(WorkflowError, "signature"):
            self.service.approve(envelope)
        with self.assertRaises(Conflict):
            self.service.approve(self.signed(sha256="0" * 64))

    def test_approval_is_idempotent_and_persisted_before_dispatch(self):
        self.script_ready()
        envelope = self.signed()
        self.service.approve(envelope)
        self.service.approve(envelope)
        restarted = Production(Store(self.db), self.directory / "workspace", ROOT, clock=lambda: self.clock)
        result = restarted.next(self.run_id)
        self.assertEqual({task["id"] for task in result["tasks"]}, {"storyboard", "audio", "packaging"})
        events = [e for e in self.store.events(self.run_id) if e["kind"] == "user.approved"]
        self.assertEqual(len(events), 1)

    def test_packaging_parallel_with_production(self):
        self.production_ready()
        self.service.claim(self.run_id, "audio", "audio-worker")
        self.service.claim(self.run_id, "packaging", "package-worker")
        self.service.claim(self.run_id, "storyboard", "board-worker")
        self.assertEqual(self.store.get(self.run_id)["tasks"]["render"]["status"], "pending")

    def test_packaging_rejects_another_format_before_asset_generation(self):
        from test_release import payload
        self.production_ready()
        data = payload()
        data.update(run_id=self.run_id, channel_id=self.run["profile"]["youtube_channel_id"])
        with self.assertRaisesRegex(WorkflowError, "format"):
            self.complete("packaging", data)
        self.assertEqual(self.store.get(self.run_id)["tasks"]["packaging"]["outputs"], [])

    def test_packaging_rejects_stale_revision_before_asset_generation(self):
        from test_release import payload
        self.production_ready()
        data = payload()
        data.update(run_id=self.run_id, channel_id=self.run["profile"]["youtube_channel_id"],
                    format="short", revision=999)
        data.pop("end_screen")
        with self.assertRaisesRegex(WorkflowError, "revision"):
            self.complete("packaging", data)
        self.assertEqual(self.store.get(self.run_id)["tasks"]["packaging"]["outputs"], [])

    def test_budget_reserved_atomically(self):
        self.production_ready()
        self.service.claim(self.run_id, "audio", "a", estimated_units=7)
        with self.assertRaisesRegex(WorkflowError, "budget"):
            self.service.claim(self.run_id, "packaging", "b", estimated_units=4)
        self.assertEqual(self.store.get(self.run_id)["budget"]["reserved"], 7)

    def test_expired_external_lease_is_unknown_not_retried(self):
        self.production_ready()
        claim = self.service.claim(self.run_id, "audio", "worker", lease_seconds=30, estimated_units=2)
        payload = self.service.operation_payload(self.run_id, "audio", "tts")
        self.service.begin_operation(self.run_id, "audio", claim["token"], "tts", payload)
        self.clock += 31
        self.service.resume(self.run_id)
        self.assertEqual(self.store.get(self.run_id)["tasks"]["audio"]["status"], "unknown")
        with self.assertRaises(Conflict):
            self.service.claim(self.run_id, "audio", "replacement")
        self.assertEqual(self.store.get(self.run_id)["budget"]["reserved"], 2)

    def test_expired_local_lease_requeues_and_fences_old_worker(self):
        claim = self.service.claim(self.run_id, "research", "old", lease_seconds=30)
        self.clock += 31
        self.service.resume(self.run_id)
        replacement = self.service.claim(self.run_id, "research", "new")
        self.assertNotEqual(claim["token"], replacement["token"])
        with self.assertRaises(Conflict):
            self.service.heartbeat(self.run_id, "research", claim["token"])

    def test_cancel_stops_new_side_effects(self):
        self.production_ready()
        claim = self.service.claim(self.run_id, "audio", "worker")
        result = self.service.cancel(self.run_id, "user cancelled")
        self.assertIn("audio", result["reconcile"])
        with self.assertRaises(Conflict):
            self.service.begin_operation(self.run_id, "audio", claim["token"], "tts", {})

    def test_unknown_operation_is_never_reissued(self):
        self.production_ready()
        claim = self.service.claim(self.run_id, "audio", "worker")
        payload = self.service.operation_payload(self.run_id, "audio", "tts")
        operation = self.service.begin_operation(self.run_id, "audio", claim["token"], "tts", payload)
        with self.assertRaises(Conflict):
            self.service.begin_operation(self.run_id, "audio", claim["token"], "tts", payload)
        self.assertEqual(operation["status"], "dispatched")

    def test_revision_invalidates_descendants_and_previous_approval(self):
        self.production_ready()
        before = input_hash(self.store.get(self.run_id), self.store.get(self.run_id)["tasks"]["script"])
        changed = self.service.revise(self.run_id, "script", "user requested a different ending")
        run = self.store.get(self.run_id)
        self.assertIn("render", changed["invalidated"])
        self.assertEqual(run["approvals"], {})
        self.assertNotEqual(before, input_hash(run, run["tasks"]["script"]))
        self.assertEqual(run["tasks"]["research"]["status"], "complete")

    def test_changed_code_pin_requires_explicit_migration(self):
        with patch("ytvideos.service.code_identity", return_value="other-version"):
            with self.assertRaisesRegex(Conflict, "pinned checkout"):
                self.service.claim(self.run_id, "research", "worker")

    def test_artifact_mutation_detected_before_use(self):
        self.script_ready()
        run = self.store.get(self.run_id)
        artifact = run["artifacts"][run["tasks"]["script"]["outputs"][0]]
        path = self.service.artifacts.resolve(artifact)
        path.write_text("changed behind content address")
        with self.assertRaisesRegex(WorkflowError, "corrupt"):
            self.service.next(self.run_id)

    def test_completion_acknowledgement_can_be_retried(self):
        claim, output, receipt = self.complete("research", {"selected_topic": {"title": "T", "angle": "A", "viewer_value": "V"},
                                                          "sources": [{"url": "https://example.com/test"}]})
        result = self.service.complete(self.run_id, "research", claim["token"], output, receipt, actual_units=0)
        self.assertEqual(result["status"], "complete")


@unittest.skipUnless(os.environ.get("YTV_TEST_POSTGRES_URL"), "set YTV_TEST_POSTGRES_URL for real PostgreSQL contracts")
class PostgreSQLContract(WorkflowContract):
    postgres = True


if __name__ == "__main__":
    unittest.main()
