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
from ytvideos.script_review import build_review_input, validate_review
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
        self.assertIsNone(json.loads(Path(result["input"]["path"]).read_text())["narrative_loop"])

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


if __name__ == "__main__":
    unittest.main()
