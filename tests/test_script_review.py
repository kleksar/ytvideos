"""Review bytes, actual input coverage and conflicting decisions; no semantic classifier."""
import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

import test_workflow as fixtures
from ytvideos.errors import WorkflowError
from ytvideos.script_review import (DECISIONS, FINDING_FIELDS, FIRST_LISTENER_FIELDS, RECORD_FIELDS,
                                    REVIEW_FIELDS, SOURCE_FIELDS, SOURCE_OPTIONAL,
                                    LEGACY_READING_INSTRUCTIONS, build_review_input, validate_response, validate_review)
from ytvideos.util import file_digest


class ScriptReviewTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.directory = Path(temporary.name)
        self.script = self.directory / "script.txt"
        self.script.write_text(fixtures.SCRIPT + "\n")
        self.response = self.directory / "reader-response.json"
        self.observed = fixtures.script_review_observation(self.script, self.response, loop=True)
        self.document = json.loads(self.response.read_text())

    def validate(self, *, loop=True):
        return validate_review(self.observed, script_text=self.script.read_bytes().decode("utf-8"),
                               script_sha256=file_digest(self.script), worker="fixture-author", narrative_loop_required=loop)

    def check_response(self, *, loop=True):
        return validate_response(self.observed, script_text=self.script.read_bytes().decode("utf-8"),
                                 script_sha256=file_digest(self.script), worker="fixture-author", narrative_loop_required=loop)

    def save_response(self, document):
        self.response.write_text(json.dumps(document))
        self.observed["evidence"]["sha256"] = file_digest(self.response)

    def test_one_reader_response_and_exact_doubled_input_are_bound(self):
        result = self.validate()
        self.assertEqual(result["evidence"], self.observed["evidence"])
        packet = json.loads(Path(result["input"]["path"]).read_text())
        text = self.script.read_text()
        self.assertEqual(packet["narrative_loop"]["two_cycles"], text + "\n\n" + text)
        self.assertEqual(result["document"]["source"]["session_id"], self.observed["reviewer"])

    def test_input_contains_the_complete_response_contract_without_fabricated_metadata_or_pass(self):
        from ytvideos.narrative_loop import LOOP_FIELDS, OBSERVATIONS
        packet = build_review_input(self.script.read_text(), file_digest(self.script),
                                    opening=fixtures.OPENING, ending=fixtures.ENDING)
        contract = packet["output_contract"]
        self.assertEqual(set(contract["required"]), set(REVIEW_FIELDS))
        self.assertEqual(set(contract["properties"]), set(REVIEW_FIELDS))
        self.assertFalse(contract["additionalProperties"])
        fields = contract["properties"]
        self.assertEqual(fields["schema"]["const"], "ytv-script-review-v1")
        self.assertEqual(fields["script_sha256"]["const"], file_digest(self.script))
        self.assertEqual(fields["decision"]["enum"], list(DECISIONS))
        for key, required in (("source", SOURCE_FIELDS), ("input", RECORD_FIELDS), ("first_listener", FIRST_LISTENER_FIELDS)):
            self.assertEqual(set(fields[key]["required"]), set(required))
            self.assertFalse(fields[key]["additionalProperties"])
        self.assertEqual(set(fields["source"]["properties"]), set(SOURCE_FIELDS + SOURCE_OPTIONAL))
        self.assertEqual(set(fields["findings"]["items"]["required"]), set(FINDING_FIELDS))
        loop = fields["narrative_loop"]
        self.assertEqual(set(loop["required"]), set(LOOP_FIELDS))
        self.assertEqual(set(loop["properties"]["observations"]["required"]), OBSERVATIONS)
        self.assertEqual(loop["properties"]["joined_excerpt"]["const"], fixtures.ENDING + "\n" + fixtures.OPENING)
        self.assertNotIn('"default"', json.dumps(contract))
        for metadata in (fields["reviewer"], fields["source"]["properties"]["session_id"], fields["input"]["properties"]["sha256"]):
            self.assertNotIn("const", metadata)
        self.assertIn("actual invocation tool/session ID", packet["instructions"])
        self.assertIn("not script_sha256", packet["instructions"])

    def test_editorial_policy_and_legacy_exact_packet(self):
        path = Path(self.document["input"]["path"])
        packet = json.loads(path.read_text())
        for phrase in ("Minor imprecision", "matters of taste", "invented facts or quotes",
                       "unperformed required checks remain unverified"):
            self.assertIn(phrase, packet["instructions"])
        packet["instructions"] = LEGACY_READING_INSTRUCTIONS
        path.write_text(json.dumps(packet))
        self.document["input"]["sha256"] = file_digest(path)
        self.document["findings"] = [{"severity": "non_blocking", "quote": fixtures.ENDING,
                                      "finding": "A minor optional clarification."}]
        self.save_response(self.document)
        self.assertEqual(self.validate()["document"]["decision"], "pass")
        packet["instructions"] += " Tampered."
        path.write_text(json.dumps(packet))
        self.document["input"]["sha256"] = file_digest(path)
        self.save_response(self.document)
        with self.assertRaisesRegex(WorkflowError, "exact script and literal"):
            self.check_response()

    def test_valid_negative_decisions_are_checkable_evidence_but_cannot_complete(self):
        for decision in ("revise", "unverified"):
            with self.subTest(decision=decision):
                document = copy.deepcopy(self.document)
                document["decision"] = decision
                document["narrative_loop"]["decision"] = decision
                document["findings"] = [{"severity": "blocking", "quote": fixtures.ENDING,
                                         "finding": "Synthetic reader identifies an unresolved seam concern."}]
                self.save_response(document)
                before = self.response.read_bytes()
                self.assertEqual(self.check_response()["document"]["decision"], decision)
                with self.assertRaisesRegex(WorkflowError, "not passed"):
                    self.validate()
                self.assertEqual(self.response.read_bytes(), before)

    def test_noncanonical_negative_shape_is_not_silently_repaired(self):
        # The observed fresh readers returned negative content using guessed v2
        # top-level understanding/attention/limitations. Preserve it, reject shape.
        for schema in ("ytv-script-review-v1", "ytv-script-review-v2"):
            with self.subTest(schema=schema):
                document = copy.deepcopy(self.document)
                document.update(schema=schema, decision="revise")
                first = document.pop("first_listener")
                document.update(understood=first["understood"], attention=first["attention"], limitations=[])
                self.save_response(document)
                before = self.response.read_bytes()
                with self.assertRaisesRegex(WorkflowError, "current schema"):
                    self.check_response()
                self.assertEqual(self.response.read_bytes(), before)

    def test_rehashed_alternative_output_contract_is_not_the_supplied_canonical_input(self):
        path = Path(self.document["input"]["path"])
        packet = json.loads(path.read_text())
        packet["output_contract"]["properties"]["schema"]["const"] = "ytv-script-review-v2"
        path.write_text(json.dumps(packet))
        self.document["input"]["sha256"] = file_digest(path)
        self.save_response(self.document)
        with self.assertRaisesRegex(WorkflowError, "exact script and literal"):
            self.check_response()

    def test_serialized_json_string_is_not_a_review_object(self):
        # Reproduces the observed cold-run serialization failure exactly: the
        # file contains a JSON string holding another serialized JSON value.
        self.save_response(json.dumps(self.document))
        with self.assertRaisesRegex(WorkflowError, "JSON object"):
            self.validate()

    def test_legacy_author_summary_and_declared_counters_are_not_reader_evidence(self):
        self.save_response({"schema": "ytv-narrative-loop-v1", "script_sha256": file_digest(self.script),
            "reviewer": self.observed["reviewer"], "relationship": "continuous_narration",
            "coverage": {"opening_utterances": 2, "ending_utterances": 2, "full_script_cycles": 2},
            "observations": {"two_cycle_read": "Full text read twice by the writer; independent reader confirmed a callback."}})
        with self.assertRaisesRegex(WorkflowError, "current schema"):
            self.validate()

    def test_rehashed_partial_or_changed_reader_input_is_rejected(self):
        for field in ("two_cycles", "script_text"):
            with self.subTest(field=field):
                changed = copy.deepcopy(self.document)
                path = Path(changed["input"]["path"])
                packet = build_review_input(self.script.read_text(), file_digest(self.script), opening=fixtures.OPENING, ending=fixtures.ENDING)
                if field == "two_cycles":
                    packet["narrative_loop"][field] = fixtures.ENDING + "\n" + fixtures.OPENING
                else:
                    packet[field] = self.script.read_text().replace("bridge", "road")
                path.write_text(json.dumps(packet))
                changed["input"]["sha256"] = file_digest(path)
                self.save_response(changed)
                with self.assertRaisesRegex(WorkflowError, "literal two-cycle"):
                    self.validate()

    def test_self_wrong_session_stale_hash_and_nonpassing_reader_fail(self):
        for defect in ("self", "session", "sha", "revise", "unverified"):
            with self.subTest(defect=defect):
                changed = copy.deepcopy(self.document)
                if defect == "self":
                    changed["reviewer"] = "fixture-author"
                    self.observed["reviewer"] = "fixture-author"
                elif defect == "session":
                    changed["source"]["session_id"] = "somebody-else"
                elif defect == "sha":
                    changed["script_sha256"] = "0" * 64
                else:
                    changed["decision"] = defect
                self.save_response(changed)
                with self.assertRaises(WorkflowError):
                    self.validate()
                self.observed["reviewer"] = self.document["reviewer"]

    def test_aggregate_pass_cannot_hide_blocking_or_nonpassing_loop_findings(self):
        for defect in ("blocking_finding", "loop_revision", "missing_loop"):
            changed = copy.deepcopy(self.document)
            if defect == "blocking_finding":
                changed["findings"] = [{"severity": "blocking", "quote": fixtures.ENDING,
                    "finding": "Synthetic reader finding: the story would need a revision."}]
            elif defect == "loop_revision":
                changed["narrative_loop"]["decision"] = "revise"
            else:
                changed["narrative_loop"] = None
            self.save_response(changed)
            with self.subTest(defect=defect), self.assertRaises(WorkflowError):
                self.validate()

    def test_long_or_edit_plan_uses_same_review_result_without_a_fictional_loop(self):
        self.script.write_text('{"schema":"synthetic-edit-plan","speech":{"mode":"none","text":""}}')
        self.observed = fixtures.script_review_observation(self.script, self.response)
        result = self.validate(loop=False)
        self.assertIsNone(result["document"]["narrative_loop"])
        packet = json.loads(Path(result["input"]["path"]).read_text())
        self.assertIsNone(packet["narrative_loop"])
        self.assertEqual(packet["output_contract"]["properties"]["narrative_loop"]["type"], "null")

    def test_exact_short_edge_phrases_do_not_require_an_arbitrary_word_quota(self):
        text = "Why? The complete text supplies the middle and its payoff. Because."
        import hashlib
        packet = build_review_input(text, hashlib.sha256(text.encode()).hexdigest(), opening="Why?", ending="Because.")
        self.assertEqual(packet["narrative_loop"]["joined_excerpt"], "Because.\nWhy?")
        # This is byte preservation, not a claim that the short seam is good.

    def test_cli_prepares_exact_input_without_claiming_review(self):
        output = self.directory / "prepared.json"
        seam = self.directory / "seam.json"
        seam.write_text(json.dumps({"opening": fixtures.OPENING, "ending": fixtures.ENDING}))
        process = subprocess.run([sys.executable, "-m", "ytvideos.script_review", "--script", str(self.script),
                                  "--seam", str(seam), "--output", str(output)], check=True, capture_output=True, text=True)
        result = json.loads(process.stdout)
        self.assertIs(result["review_performed"], False)
        self.assertEqual(result["sha256"], file_digest(output))
        self.assertEqual(json.loads(output.read_text())["script_text"], self.script.read_text())

    def test_cli_checks_valid_negative_response_without_review_approval_or_rewriting(self):
        self.document["decision"] = "revise"
        self.document["narrative_loop"]["decision"] = "revise"
        self.save_response(self.document)
        seam = self.directory / "seam.json"
        seam.write_text(json.dumps({"opening": fixtures.OPENING, "ending": fixtures.ENDING}))
        before = file_digest(self.response)
        process = subprocess.run([sys.executable, "-m", "ytvideos.script_review", "--script", str(self.script),
                                  "--seam", str(seam), "--check-response", str(self.response), "--author", "fixture-author"],
                                 check=True, capture_output=True, text=True)
        result = json.loads(process.stdout)
        self.assertTrue(result["structurally_valid"])
        self.assertEqual(result["decision"], "revise")
        self.assertFalse(result["pass_consistent"])
        self.assertFalse(result["review_performed"])
        self.assertFalse(result["script_accepted"])
        self.assertEqual(file_digest(self.response), before)

    def test_cli_rejects_a_different_valid_requested_seam_without_changing_evidence(self):
        seam = self.directory / "different-seam.json"
        evidence_input = Path(self.document["input"]["path"])
        originals = {path: path.read_bytes() for path in (self.script, self.response, evidence_input)}
        alternatives = (
            {"opening": "Nobody was waiting at the bridge.", "ending": fixtures.ENDING},
            {"opening": fixtures.OPENING, "ending": "I finally understood why"},
        )
        for alternative in alternatives:
            with self.subTest(seam=alternative):
                # Both are valid literal edge excerpts; only their identity
                # differs from the packet actually given to this reviewer.
                build_review_input(self.script.read_text(), file_digest(self.script), **alternative)
                seam.write_text(json.dumps(alternative))
                process = subprocess.run([sys.executable, "-m", "ytvideos.script_review", "--script", str(self.script),
                                          "--seam", str(seam), "--check-response", str(self.response), "--author", "fixture-author"],
                                         capture_output=True, text=True)
                self.assertNotEqual(process.returncode, 0)
                self.assertIn("differs from the requested script/seam", process.stderr)
                self.assertNotIn('"structurally_valid": true', process.stdout)
                for path, data in originals.items():
                    self.assertEqual(path.read_bytes(), data)


if __name__ == "__main__":
    unittest.main()
