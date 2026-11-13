"""Narrated Shorts bind a real end-to-start review, not a thematic callback flag."""
import copy
import json
from pathlib import Path
import tempfile
import unittest

import test_workflow as fixtures
from ytvideos.errors import WorkflowError
from ytvideos.narrative_loop import validate_evidence, validate_observation
from ytvideos.production_contract import production_requirements
from ytvideos.util import file_digest
from ytvideos.workflow import required_checks


class NarrativeLoopContractTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.directory = Path(temporary.name)
        self.script = self.directory / "script.txt"
        self.script.write_text(fixtures.SCRIPT + "\n")
        self.evidence = self.directory / "reading.json"
        self.observed = fixtures.loop_observation(self.script, self.evidence)
        self.document = json.loads(self.evidence.read_text())

    def validate(self, observed=None, document=None):
        observed = observed if observed is not None else self.observed
        validate_observation(observed, script_text=self.script.read_text(),
                             script_sha256=file_digest(self.script), worker="fixture-author")
        validate_evidence(document if document is not None else self.document,
                          observed, script_text=self.script.read_text())

    def test_exact_prefix_suffix_join_and_independent_observations_form_valid_evidence(self):
        self.validate()

    def test_modified_script_or_different_excerpts_invalidate_the_reading(self):
        for field, value in (("artifact_sha256", "0" * 64), ("opening", "An invented opening appears here."),
                             ("ending", "A different ending appears here."),
                             ("joined_excerpt", fixtures.OPENING + "\n" + fixtures.ENDING)):
            observed = {**self.observed, field: value}
            with self.subTest(field=field), self.assertRaises(WorkflowError):
                self.validate(observed)
        self.script.write_text(self.script.read_text() + " ")
        with self.assertRaisesRegex(WorkflowError, "exact script SHA"):
            self.validate()

    def test_single_word_or_overlapping_whole_script_is_not_edge_context(self):
        for opening, ending in (("Nobody", "why"), (fixtures.SCRIPT, fixtures.ENDING)):
            observed = {**self.observed, "opening": opening, "ending": ending,
                        "joined_excerpt": ending + "\n" + opening}
            with self.subTest(opening=opening[:20]), self.assertRaises(WorkflowError):
                self.validate(observed)

    def test_self_review_and_unbound_evidence_fail(self):
        for field, value in (("reviewer", " fixture-author "), ("evidence", {"placeholder": True})):
            with self.subTest(field=field), self.assertRaises(WorkflowError):
                self.validate({**self.observed, field: value})

    def test_classified_thematic_callback_is_not_accepted_as_continuous_narration(self):
        # This checks the supplied review classification. It does not infer the
        # meaning of arbitrary prose from an enum or detect a dishonest reviewer.
        for relationship in ("thematic_callback", "broken", "unverified", "UNVERIFIED"):
            with self.subTest(relationship=relationship), self.assertRaisesRegex(WorkflowError, "thematic callback"):
                self.validate(document={**self.document, "relationship": relationship})

    def test_two_cycles_complete_utterances_and_specific_observations_are_required(self):
        cases = []
        for field, value in (("full_script_cycles", 1), ("opening_utterances", 1), ("complete_edge_utterances", False)):
            changed = copy.deepcopy(self.document)
            changed["coverage"][field] = value
            cases.append(changed)
        for field, value in (("cold_open", "PASS"), ("continuation", ""), ("payoff_quote", "This did not occur.")):
            changed = copy.deepcopy(self.document)
            changed["observations"][field] = value
            cases.append(changed)
        for changed in cases:
            with self.subTest(document=changed), self.assertRaises(WorkflowError):
                self.validate(document=changed)

    def test_evidence_cannot_describe_a_different_seam_under_a_valid_record_hash(self):
        with self.assertRaisesRegex(WorkflowError, "exact reviewed script and seam"):
            self.validate(document={**self.document, "opening": "Different complete opening excerpt."})

    def test_long_and_nonnarrated_recipes_do_not_inherit_a_narrator_loop(self):
        for channel in ("paper_detour", "nuviko_history", "two_ways_lab"):
            profile = json.loads((fixtures.ROOT / "channels" / channel / "channel.json").read_text())
            self.assertIn("narrative_loop", required_checks("script", production_requirements(profile, "short")))
            self.assertNotIn("narrative_loop", required_checks("script", production_requirements(profile, "long")))
        for channel in ("scenes_on_repeat", "nuviko_videos"):
            profile = json.loads((fixtures.ROOT / "channels" / channel / "channel.json").read_text())
            requirements = production_requirements(profile, "short")
            self.assertNotIn("narrative_loop", required_checks("script", requirements))
            self.assertIn("av_loop", required_checks("review", requirements))


class NarrativeLoopWorkflowTests(unittest.TestCase):
    def setUp(self):
        self.fixture = fixtures.WorkflowContract()
        self.fixture.setUp()
        self.addCleanup(self.fixture.doCleanups)
        self.addCleanup(self.fixture.tearDown)
        self.service = self.fixture.service

    def research(self):
        self.fixture.complete("research", {"selected_topic": {"title": "Fixture", "angle": "Causality", "viewer_value": "A tested lesson"},
                                           "sources": [{"url": "https://example.com/fixture"}]})

    def test_plan_context_and_completion_share_the_exact_required_loop_check(self):
        context = self.service.context(self.fixture.run_id, "script")
        step = next(item for item in self.service.plan(self.fixture.run_id)["steps"] if item["id"] == "script")
        self.assertIn("narrative_loop", context["required_checks"])
        self.assertEqual(context["required_checks"], context["task_guide"]["required_checks"])
        self.assertEqual(context["required_checks"], step["required_checks"])
        self.assertEqual(step["narrative_loop"]["applicability"], "required")
        self.research()
        claim = self.service.claim(self.fixture.run_id, "script", "fixture-author")
        script = self.fixture.output(fixtures.SCRIPT)
        receipt = self.fixture.receipt("script", claim, script, remove="narrative_loop")
        with self.assertRaisesRegex(WorkflowError, "missing checks: narrative_loop"):
            self.service.complete(self.fixture.run_id, "script", claim["token"], script, receipt, actual_units=0)

    def test_fresh_file_hash_cannot_cover_changed_or_placeholder_reading(self):
        self.research()
        claim = self.service.claim(self.fixture.run_id, "script", "fixture-author")
        script = self.fixture.output(fixtures.SCRIPT)
        receipt_path = self.fixture.receipt("script", claim, script)
        receipt = json.loads(receipt_path.read_text())
        observed = next(check["observed"] for check in receipt["checks"] if check["name"] == "narrative_loop")
        evidence = Path(observed["evidence"]["path"])
        evidence.write_text(evidence.read_text() + "\n")
        with self.assertRaisesRegex(WorkflowError, "stale"):
            self.service.complete(self.fixture.run_id, "script", claim["token"], script, receipt_path, actual_units=0)
        document = json.loads(evidence.read_text())
        document["relationship"] = "thematic_callback"
        evidence.write_text(json.dumps(document))
        observed["evidence"]["sha256"] = file_digest(evidence)
        receipt_path.write_text(json.dumps(receipt))
        with self.assertRaisesRegex(WorkflowError, "thematic callback"):
            self.service.complete(self.fixture.run_id, "script", claim["token"], script, receipt_path, actual_units=0)

    def test_completed_loop_evidence_is_preserved_in_the_artifact_store(self):
        self.fixture.script_ready()
        run = self.fixture.store.get(self.fixture.run_id)
        identities = run["tasks"]["script"]["receipt_evidence_ids"]
        self.assertEqual(len(identities), 1)
        document = json.loads(self.service.artifacts.resolve(run["artifacts"][identities[0]]).read_text())
        script = self.service._artifact(run, "script")
        self.assertEqual(document["script_sha256"], script["sha256"])
        self.assertEqual(self.service.next(run["id"])["status"], "awaiting_script_approval")
        self.assertFalse(run["approvals"])

    def test_failed_loop_preserves_the_exact_supplied_source_and_exposes_separate_revision(self):
        source = self.fixture.output(fixtures.SCRIPT, "provided.txt")
        run = self.service.create("paper_detour", "Produce this exact provided narration", source_script=source,
                                  capabilities=self.fixture.run["capabilities"], budget_units=10)
        self.fixture.run = run
        self.fixture.run_id = run["id"]
        original_hash = file_digest(source)
        self.research()
        claim = self.service.claim(run["id"], "script", "fixture-author")
        receipt_path = self.fixture.receipt("script", claim, source)
        receipt = json.loads(receipt_path.read_text())
        check = next(check for check in receipt["checks"] if check["name"] == "narrative_loop")
        check["status"] = "unverified"
        receipt_path.write_text(json.dumps(receipt))
        with self.assertRaises(WorkflowError):
            self.service.complete(run["id"], "script", claim["token"], source, receipt_path, actual_units=0)
        context = self.service.context(run["id"], "script")
        self.assertEqual(file_digest(self.service.artifacts.resolve(context["source_script"])), original_hash)
        self.assertEqual(file_digest(source), original_hash)
        self.assertIn("separate proposed correction", context["task_guide"]["narrative_loop"]["source_script"])
        self.assertEqual(self.fixture.store.get(run["id"])["tasks"]["script"]["outputs"], [])


if __name__ == "__main__":
    unittest.main()
