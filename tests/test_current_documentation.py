"""Keep historical evidence out of new production instructions, without losing pins."""

import hashlib
import json
import tempfile
from pathlib import Path
import unittest

import test_repository_check as repository_fixtures
from ytvideos.context import STAGE_REFERENCES, TASK_EXECUTION_REFERENCE, reference_context, snapshot_references
from ytvideos.documentation import DATA_ONLY_PATHS
from ytvideos.errors import WorkflowError
from ytvideos.util import digest


class CurrentTaskDocumentsTest(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        for name in {TASK_EXECUTION_REFERENCE, *(name for names in STAGE_REFERENCES.values() for name in names)}:
            self.write(name, "# Current standard\nUse the accepted input.\n")
        self.profile = {"id": "example", "context_references": []}

    def write(self, name, text):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return path

    def snapshot(self, name=None):
        self.profile["context_references"] = [{"path": name}] if name else []
        return snapshot_references(self.root, self.profile, "short")

    def test_historical_locations_are_not_new_task_requirements(self):
        for name in ("archive/rules.md", "channels/example/legacy/rules.md",
                     ".agents/consultations/result.md", ".agent/reports/result.md",
                     "channels/example/docs/proposals/editing.md", "evals/results/review.md",
                     "channels/example/videos/001/AGENTS.md", ".agent/research/drafts/story.md"):
            with self.subTest(path=name):
                self.write(name, "# Recorded evidence\nPreserve these facts.\n")
                with self.assertRaisesRegex(WorkflowError, "historical"):
                    self.snapshot(name)

    def test_changelog_sections_are_rejected_in_current_profile(self):
        for heading in ("## История изменений", "## Changelog", "## Change history",
                        "История изменений\n-----------------"):
            with self.subTest(heading=heading):
                self.write("channels/example/PROFILE.md", "# Profile\n\n" + heading + "\nOld decisions.\n")
                with self.assertRaisesRegex(WorkflowError, "change history"):
                    self.snapshot()

    def test_retained_inventories_and_episode_drafts_cannot_be_rules(self):
        for name in DATA_ONLY_PATHS:
            with self.subTest(path=name):
                path = self.write(name, "# Retained record\nExact recorded state.\n")
                original = path.read_bytes()
                with self.assertRaisesRegex(WorkflowError, "historical"):
                    self.snapshot(name)
                self.assertEqual(path.read_bytes(), original)

    def test_explicit_historical_frontmatter_is_not_a_current_recipe(self):
        name = "channels/example/docs/recipe.md"
        for metadata in ("document_role: history", "status: archived", "document_role: historical"):
            with self.subTest(metadata=metadata):
                self.write(name, "---\n" + metadata + "\n---\n# Record\n")
                with self.assertRaisesRegex(WorkflowError, "historical"):
                    self.snapshot(name)

    def test_history_in_story_content_and_fenced_examples_is_allowed(self):
        name = "channels/example/docs/recipe.md"
        text = ("# Historical narration example\nIn 1859 the telegraph worked without its batteries.\n"
                "Раньше люди передавали сообщения иначе.\n\n```markdown\n## История изменений\n```\n"
                "~~~yaml\nstatus: archived\n~~~\n")
        self.write(name, text)
        self.assertEqual(self.snapshot(name)["documents"][name]["text"], text)

    def test_dated_actual_brand_reference_is_allowed(self):
        name = "channels/example/brand/References/paper_20261113/REFERENCE.md"
        self.write(name, "# Actual accepted reference\nUse image.png with its verified hash.\n")
        self.assertIn(name, self.snapshot(name)["routes"]["render"])

    def test_current_alias_cannot_hide_a_historical_rule(self):
        archived = self.write("archive/rules.md", "# Historical rules\n")
        name = "channels/example/docs/current.md"
        alias = self.root / name
        alias.parent.mkdir(parents=True, exist_ok=True)
        alias.symlink_to(archived)
        with self.assertRaisesRegex(WorkflowError, "historical"):
            self.snapshot(name)

    def test_existing_pinned_historical_packet_is_not_reinterpreted_or_rewritten(self):
        name = "archive/old-rule.md"
        text = "# Previous pinned rule\n## Change history\nOld accepted requirements.\n"
        document = {"path": name, "text": text, "sha256": hashlib.sha256(text.encode()).hexdigest()}
        snapshot = {"routes": {"render": [name]}, "documents": {name: document}}
        run = {"reference_snapshot": snapshot, "pins": {"references": digest(snapshot)}}
        packet = reference_context(run, {"stage": "render"}, self.root)
        self.assertEqual(packet["reference_source"], "pinned")
        self.assertEqual(packet["reference_documents"], [document])
        self.assertEqual(run["pins"]["references"], digest(snapshot))


class CurrentDocumentationCheckerTest(unittest.TestCase):
    def setUp(self):
        self.fixture = repository_fixtures.RepositoryCheckTest()
        self.fixture.setUp()
        self.addCleanup(self.fixture.doCleanups)

    def configure(self, name, text):
        self.fixture.write(name, text)
        self.fixture.write("channels/example/channel.json", json.dumps({
            "context_references": [{"path": name}],
        }))

    def test_checker_rejects_historical_reference_using_the_runtime_rule(self):
        self.configure("archive/old.md", "# Evidence\n")
        self.assertTrue(any("historical" in error for error in self.fixture.errors()))

    def test_checker_rejects_changelog_only_when_it_enters_runtime_context(self):
        self.fixture.write("docs/migration.md", "# Migration\n## Change history\nRecorded boundary.\n")
        self.assertEqual(self.fixture.errors(), [])
        self.configure("channels/example/docs/recipe.md", "# Current recipe\n## Changelog\nOld values.\n")
        self.assertTrue(any("change history" in error for error in self.fixture.errors()))

    def test_checker_keeps_accepted_reference_assets_accessible(self):
        self.configure("channels/example/brand/References/20261113/REFERENCE.md", "# Accepted reference\n")
        self.assertEqual(self.fixture.errors(), [])

    def test_checker_checks_automatic_stage_documents_without_extra_profile_entries(self):
        self.fixture.write("docs/standards/audio.md", "# Audio\n## История изменений\nOld mixes.\n")
        self.assertTrue(any("change history" in error for error in self.fixture.errors()))

    def test_checker_rejects_history_in_the_mandatory_execution_procedure(self):
        self.fixture.write(TASK_EXECUTION_REFERENCE, "# Execution\n## Changelog\nOld procedure.\n")
        self.assertTrue(any("change history" in error for error in self.fixture.errors()))


if __name__ == "__main__":
    unittest.main()
