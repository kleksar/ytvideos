"""Fixture integrity and rule routing only, never a semantic or audience score."""
import ast
import hashlib
import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
EVAL = ROOT / "evals/story_selection"
OWNER = "docs/standards/editorial.md"


def read(path):
    return (ROOT / path).read_text(encoding="utf-8")


class StorySelectionContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads((EVAL / "cases.json").read_text(encoding="utf-8"))

    def test_baseline_bytes_match_pinned_pr(self):
        baseline = self.data["baseline"]
        raw = (EVAL / baseline["file"]).read_bytes()
        self.assertEqual(hashlib.sha256(raw).hexdigest(), baseline["sha256"])
        header = f"blob {len(raw)}\0".encode()
        self.assertEqual(hashlib.sha1(header + raw).hexdigest(), baseline["git_blob_sha"])
        self.assertEqual(baseline["commit"], "722beb29e49ff182969d7ac17ffa444de76c07a4")
        self.assertEqual(baseline["pr_number"], 13)

    def test_cases_have_unique_ids_and_separate_expectations(self):
        cases = self.data["cases"]
        self.assertEqual(len(cases), len({case["id"] for case in cases}))
        for case in cases:
            with self.subTest(case=case["id"]):
                self.assertTrue(case["input"]["request"])
                self.assertTrue(case["input"]["material"])
                self.assertTrue(case["expected_observations"])
                self.assertNotIn("expected_observations", case["input"])
                self.assertNotIn("actual_result", case)

    def test_probes_are_not_fabricated_executed_results(self):
        self.assertEqual(self.data["schema_version"], 1)
        self.assertEqual(self.data["execution_status"], "NOT_RUN")
        self.assertIn("NOT_RUN", (EVAL / "README.md").read_text(encoding="utf-8"))

    def test_failure_and_positive_control_coverage(self):
        required = {"candidate_diversity", "structure_is_not_interest", "retention_middle",
                    "truth_over_sensationalism", "non_dramatic_positive", "demand_evidence",
                    "no_candidate_and_owner_veto", "bilingual_fidelity"}
        self.assertTrue(required.issubset({case["focus"] for case in self.data["cases"]}))

    def test_input_script_paths_exist_and_do_not_escape_eval(self):
        for case in self.data["cases"]:
            path = case["input"].get("script_file")
            if path is not None:
                resolved = (EVAL / path).resolve()
                self.assertTrue(resolved.is_relative_to(EVAL.resolve()))
                self.assertTrue(resolved.is_file())

    def test_selection_links_resolve_to_shared_owner(self):
        text = read(OWNER)
        self.assertIn("## Тема и ценность", text)
        self.assertIn("### Отбор до полного сценария", text)
        self.assertIn("### Причина смотреть", text)
        self.assertIn("### Сигналы аудитории и границы вывода", text)
        self.assertIn("editorial.md#отбор-до-полного-сценария", read("docs/workflow.md"))
        skill = read(".agents/skills/ytv-write-script/SKILL.md")
        self.assertIn("editorial.md#отбор-до-полного-сценария", skill)
        self.assertLess(len(skill.encode("utf-8")), 12000)

    def test_existing_shared_context_routes_include_owner(self):
        tree = ast.parse(read("src/ytvideos/context.py"))
        node = next(node for node in tree.body if isinstance(node, ast.Assign)
                    and any(isinstance(t, ast.Name) and t.id == "STAGE_REFERENCES"
                            for t in node.targets))
        routes = ast.literal_eval(node.value)
        for stage in ("research", "script", "review"):
            with self.subTest(stage=stage):
                self.assertIn(OWNER, routes[stage])

    def test_existing_script_constraints_remain(self):
        text = read(OWNER)
        for phrase in ("Для каждого Short обязательна естественная смысловая петля.",
                       "Уже утверждённые тексты и MP4 автоматически не переписывать.",
                       "Не обещать 120–150%"):
            self.assertIn(phrase, text)
        skill = read(".agents/skills/ytv-write-script/SKILL.md")
        self.assertIsNotNone(re.search(r'^description: "Research and write .*"$', skill, re.M))


if __name__ == "__main__":
    unittest.main()
