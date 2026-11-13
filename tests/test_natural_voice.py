"""Packet routing/integrity, not a naturalness classifier or model evaluation."""
import hashlib
import json
from pathlib import Path
import unittest

from ytvideos.context import STAGE_REFERENCES
from ytvideos.script_review import FIRST_LISTENER_FIELDS, REVIEW_FIELDS, build_review_input

ROOT = Path(__file__).resolve().parents[1]


class NaturalVoiceContractTests(unittest.TestCase):
    def test_standard_reaches_script_and_final_review_only(self):
        for stage in ("script", "review"):
            self.assertIn("docs/standards/narration.md", STAGE_REFERENCES[stage])
        for stage in ("scene_image", "upload", "schedule"):
            self.assertNotIn("docs/standards/narration.md", STAGE_REFERENCES[stage])

    def test_real_reader_packet_has_voice_checks_without_new_schema(self):
        script = "A rope snapped. The chair rose. Which rope?"
        sha = hashlib.sha256(script.encode()).hexdigest()
        packet = build_review_input(script, sha, opening="A rope snapped.", ending="Which rope?")
        self.assertEqual(packet["script_text"], script)
        self.assertEqual(packet["narrative_loop"]["two_cycles"], script + "\n\n" + script)
        instructions = packet["instructions"]
        for phrase in ("natural spoken language", "exact line", "material uncertainty", "Do not invent dialogue"):
            self.assertIn(phrase, instructions)
        schema = packet["output_contract"]
        self.assertEqual(set(schema["required"]), set(REVIEW_FIELDS))
        self.assertEqual(set(schema["properties"]["first_listener"]["required"]), set(FIRST_LISTENER_FIELDS))
        self.assertFalse(schema["additionalProperties"])

    def test_non_narration_guard_survives(self):
        text = '{"kind":"instrumental_edit_plan"}'
        packet = build_review_input(text, hashlib.sha256(text.encode()).hexdigest())
        self.assertIsNone(packet["narrative_loop"])
        self.assertIn("do not invent a narrator", packet["instructions"])

    def test_examples_are_pinned_preferences_not_live_results(self):
        data = json.loads((ROOT / "evals/natural_voice/examples.json").read_text())
        self.assertEqual(data["independent_model_eval"], "NOT_RUN")
        self.assertEqual({e["pr"] for e in data["examples"]}, {20, 25})
        for example in data["examples"]:
            self.assertEqual(hashlib.sha256(example["after"].encode()).hexdigest(), example["after_sha256"])
            self.assertEqual(len(example["source_commit"]), 40)
            self.assertTrue(example["ru_after"])
            self.assertNotIn("actual_result", example)

    def test_skill_links_stay_small_and_dont_change_approvals(self):
        for name in ("ytv-write-script", "ytv-review-video"):
            text = (ROOT / f".agents/skills/{name}/SKILL.md").read_text()
            self.assertIn("../../../docs/standards/narration.md", text)
            self.assertLess(len(text.encode()), 12000)
        standard = (ROOT / "docs/standards/narration.md").read_text()
        self.assertIn("не менять JSON schema", standard)
        self.assertIn("UNVERIFIED", standard)


if __name__ == "__main__":
    unittest.main()
