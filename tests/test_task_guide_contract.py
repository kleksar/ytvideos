"""Shared execution guidance must resolve to pinned bytes without hiding task data."""

import unittest

import test_pool_service as fixtures
from ytvideos.context import TASK_EXECUTION_REFERENCE


class TaskGuideContractTests(unittest.TestCase):
    def setUp(self):
        self.fixture = fixtures.PoolServiceTests()
        self.fixture.setUp()
        self.addCleanup(self.fixture.doCleanups)
        self.production = self.fixture.production

    def test_context_and_plan_point_to_saved_execution_procedure_after_checkout_changes(self):
        run = self.production.create("test_channel", "inspect the saved task procedure")
        saved_document = run["reference_snapshot"]["documents"][TASK_EXECUTION_REFERENCE]
        source = self.production.project / TASK_EXECUTION_REFERENCE

        for contents in ("Different instructions for future runs.\n", None):
            if contents is None:
                source.unlink()
            else:
                source.write_text(contents)
            plan = self.production.plan(run["id"])
            cards = {item["id"]: item for item in [*plan["steps"], *plan["release_steps"]]}
            for task_id in run["tasks"]:
                with self.subTest(source_present=contents is not None, task=task_id):
                    packet = self.production.context(run["id"], task_id)
                    for guide in (packet["task_guide"], cards[task_id]):
                        pointer = guide["execution_reference"]
                        self.assertEqual(pointer, TASK_EXECUTION_REFERENCE)
                        self.assertIn(pointer, guide["read"])
                    self.assertIn(pointer, packet["references"])
                    documents = {item["path"]: item for item in packet["reference_documents"]}
                    self.assertEqual(documents[pointer], saved_document)
            self.assertEqual(self.fixture.store.get(run["id"]), run)

    def test_shared_procedure_keeps_task_specific_dependencies_gates_and_checks(self):
        run = self.production.create("test_channel", "inspect task-specific obligations")
        plan = self.production.plan(run["id"])
        cards = {item["id"]: item for item in [*plan["steps"], *plan["release_steps"]]}

        for task_id, task in run["tasks"].items():
            with self.subTest(task=task_id):
                packet = self.production.context(run["id"], task_id)
                for guide in (packet["task_guide"], cards[task_id]):
                    self.assertEqual(guide["dependencies"], task["dependencies"])
                    self.assertEqual(guide["approval_gates"], task["gates"])
                    self.assertEqual(guide["capabilities"], task["capabilities"])
                    self.assertEqual(guide["required_checks"], packet["required_checks"])
                    self.assertEqual(guide["output_kind"], packet["output_kind"])
                    self.assertEqual(guide["read"], packet["references"])
                    self.assertEqual(guide["skill"]["name"], task["skill"])
                    self.assertEqual(guide["skill"]["path"], run["skills"][task["skill"]]["path"])
        self.assertEqual(self.fixture.store.get(run["id"]), run)


if __name__ == "__main__":
    unittest.main()
