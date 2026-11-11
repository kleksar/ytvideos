"""Cross-stage and concurrent-delivery regressions; no provider traffic."""
import os
import threading
import unittest
import uuid
from concurrent.futures import ThreadPoolExecutor
from unittest.mock import patch

import test_workflow
from test_release import payload
from ytvideos.doctor import inspect
from ytvideos.errors import Conflict
from ytvideos.service import Production
from ytvideos.store import Store, Transaction
from ytvideos.workflow import new_tasks


class RequirementsRecheck(unittest.TestCase):
    postgres = False

    def setUp(self):
        self.fixture = test_workflow.WorkflowContract()
        self.fixture.postgres = self.postgres
        self.fixture.setUp()
        self.addCleanup(self.fixture.doCleanups)
        self.addCleanup(self.fixture.tearDown)
        self.service = self.fixture.service
        self.run_id = self.fixture.run_id

    def race(self, statement, invoke):
        """Separate connections with a deterministic pre-write barrier on PG."""
        stores = [Store(self.fixture.db), Store(self.fixture.db)]
        barrier = threading.Barrier(2)
        original = Transaction.execute

        def execute(tx, sql, params=()):
            if tx.postgres and sql.startswith(statement):
                barrier.wait(timeout=10)
            return original(tx, sql, params)

        with patch.object(Transaction, "execute", execute):
            with ThreadPoolExecutor(max_workers=2) as executor:
                futures = [executor.submit(invoke, stores[i], i) for i in range(2)]
                return [future.result(timeout=20) for future in futures]

    def test_duplicate_create_returns_one_run_across_connections(self):
        request_id = "replayed-request-" + uuid.uuid4().hex

        def create(store, index):
            service = Production(store, self.service.workspace, self.service.project)
            return service.create("paper_detour", "same user request", request_id=request_id)["id"]

        results = self.race("INSERT INTO runs", create)
        self.assertEqual(results[0], results[1])
        self.assertEqual(len([run for run in self.fixture.store.list() if run["request_id"] == request_id]), 1)
        self.assertEqual(len([event for event in self.fixture.store.events(results[0])
                              if event["kind"] == "run.created"]), 1)

    def test_conflicting_create_returns_domain_conflict_not_driver_error(self):
        request_id = "conflicting-request-" + uuid.uuid4().hex

        def create(store, index):
            service = Production(store, self.service.workspace, self.service.project)
            try:
                service.create("paper_detour", f"different request {index}", request_id=request_id)
                return "created"
            except Conflict:
                return "conflict"

        self.assertEqual(sorted(self.race("INSERT INTO runs", create)), ["conflict", "created"])
        self.assertEqual(len([run for run in self.fixture.store.list() if run["request_id"] == request_id]), 1)

    def test_duplicate_event_is_idempotent_across_connections(self):
        event_id = "redelivered-event-" + uuid.uuid4().hex

        def deliver(store, index):
            with store.transaction() as tx:
                return tx.event(event_id, self.run_id, "fixture.delivery", {"result": "same"})

        self.assertEqual(sorted(self.race("INSERT INTO events", deliver)), [False, True])

    def test_conflicting_event_delivery_is_a_domain_conflict(self):
        event_id = "conflicting-event-" + uuid.uuid4().hex

        def deliver(store, index):
            try:
                with store.transaction() as tx:
                    tx.event(event_id, self.run_id, "fixture.delivery", {"result": index})
                return "inserted"
            except Conflict:
                return "conflict"

        self.assertEqual(sorted(self.race("INSERT INTO events", deliver)), ["conflict", "inserted"])

    def test_thumbnail_revision_invalidates_bound_release_not_accepted_media(self):
        fixture = self.fixture
        fixture.production_ready()
        data = payload()
        data.update(run_id=self.run_id, channel_id=fixture.run["profile"]["youtube_channel_id"], format="short")
        data.pop("end_screen")
        fixture.complete("packaging", data)
        task = self.service.add_thumbnail_task(self.run_id, {
            "id": "cover", "prompt": "Synthetic cover brief", "visual_intent": "Test release invalidation"})

        # Isolate dependency invalidation from media decoding/approval validation,
        # which the full synthetic lifecycle suite exercises with actual media.
        def prepared(tx, run):
            run["publication"]["release_spec"] = "fixture-bound-release"
            run["approvals"]["mp4"] = {"artifact_id": "fixture-accepted-mp4", "revision": run["revision"]}
            run["tasks"]["render"].update(status="complete", outputs=["fixture-accepted-mp4"])
        fixture.store.mutate(self.run_id, prepared)
        before = fixture.store.get(self.run_id)
        self.service.revise(self.run_id, task["id"], "replace the selected cover")
        after = fixture.store.get(self.run_id)
        self.assertNotIn("release_spec", after["publication"])
        self.assertEqual(after["tasks"]["render"], before["tasks"]["render"])
        self.assertEqual(after["approvals"], before["approvals"])

    def test_new_or_changed_thumbnail_plan_requires_release_rebinding(self):
        fixture = self.fixture
        fixture.production_ready()
        data = payload()
        data.update(run_id=self.run_id, channel_id=fixture.run["profile"]["youtube_channel_id"], format="short")
        data.pop("end_screen")
        fixture.complete("packaging", data)
        brief = {"id": "cover", "prompt": "Synthetic cover brief", "visual_intent": "A specific story promise"}

        def bound(tx, run):
            run["publication"]["release_spec"] = "fixture-bound-release"

        fixture.store.mutate(self.run_id, bound)
        self.service.add_thumbnail_task(self.run_id, brief)
        self.assertNotIn("release_spec", fixture.store.get(self.run_id)["publication"])
        fixture.store.mutate(self.run_id, bound)
        self.service.add_thumbnail_task(self.run_id, brief)
        self.assertIn("release_spec", fixture.store.get(self.run_id)["publication"])
        self.service.add_thumbnail_task(self.run_id, {**brief, "prompt": "A revised synthetic composition"})
        self.assertNotIn("release_spec", fixture.store.get(self.run_id)["publication"])

    def test_doctor_reports_future_image_capability_before_storyboard(self):
        run = self.service.create("paper_detour", "preflight before expensive production")
        checks = {item["capability"]: item for item in inspect(self.service, run["id"])["checks"]}
        self.assertIn("image.generate", checks)
        self.assertFalse(checks["image.generate"]["available"])
        self.assertEqual(self.service.next(run["id"])["tasks"][0]["id"], "research")

    def test_doctor_does_not_report_unverified_observation_as_available(self):
        run = self.service.create("paper_detour", "unverified runtime capability", capabilities={
            "model.text": {"available": True}})
        checks = {item["capability"]: item for item in inspect(self.service, run["id"])["checks"]}
        self.assertFalse(checks["model.text"]["available"])

    def test_new_task_graphs_do_not_share_mutable_dependencies(self):
        first, second = new_tasks(), new_tasks()
        original = list(first["upload"]["dependencies"])
        try:
            first["upload"]["dependencies"].append("thumbnail:isolated-fixture")
            self.assertNotIn("thumbnail:isolated-fixture", second["upload"]["dependencies"])
        finally:
            first["upload"]["dependencies"][:] = original


@unittest.skipUnless(os.environ.get("YTV_TEST_POSTGRES_URL"), "requires real PostgreSQL")
class PostgreSQLRequirementsRecheck(RequirementsRecheck):
    postgres = True
