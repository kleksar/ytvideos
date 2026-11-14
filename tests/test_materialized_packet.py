"""Portable instruction files are a projection of the unchanged pinned packet."""
import copy
import hashlib
import json
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest

from ytvideos.entry import reading_packet
from ytvideos.errors import WorkflowError
from ytvideos.util import digest, file_digest


def instruction_fixture():
    path = ".agents/skills/ytv-write-script/SKILL.md"
    reference = ".agents/skills/ytv-start/references/task-execution.md"
    text = "# Write\n\nRead [the procedure](../ytv-start/references/task-execution.md).\n"
    procedure = "# Procedure\n\nRead [the standard](../../../../docs/standards/editorial.md).\n"
    documents = [{"path": name, "text": content,
                  "sha256": hashlib.sha256(content.encode()).hexdigest()}
                 for name, content in ((reference, procedure),
                                       ("docs/standards/editorial.md", "# Standard\n"))]
    return {"run_id": "fixture-run", "task_id": "research", "input_hash": "fixture-input",
            "skill": {"name": "ytv-write-script", "path": path, "text": text},
            "references": [item["path"] for item in documents],
            "reference_documents": documents, "task_guide": {"goal": "Fixture only"}}


class MaterializedPacketTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.workspace = Path(temporary.name)
        self.production = SimpleNamespace(workspace=self.workspace)
        self.packet = instruction_fixture()

    def test_skill_has_one_text_copy_and_a_verified_descriptor(self):
        original = copy.deepcopy(self.packet)
        result = reading_packet(self.production, self.packet)
        task = json.loads(Path(result["task_file"]).read_text())
        skill_file = Path(result["skill_file"])
        self.assertNotIn("text", task["skill"])
        self.assertEqual(task["skill"]["sha256"], file_digest(skill_file))
        self.assertEqual(Path(result["task_file"]).parent / task["skill"]["local_path"], skill_file)
        self.assertEqual(skill_file.read_text(), original["skill"]["text"])
        self.assertEqual(self.packet, original)

    def test_included_relative_links_resolve_from_the_materialized_skill(self):
        result = reading_packet(self.production, self.packet)
        skill_file = Path(result["skill_file"])
        procedure = (skill_file.parent / "../ytv-start/references/task-execution.md").resolve()
        self.assertTrue(procedure.is_file())
        standard = (procedure.parent / "../../../../docs/standards/editorial.md").resolve()
        self.assertEqual(standard.read_text(), "# Standard\n")
        self.assertTrue(standard.is_relative_to(Path(result["task_file"]).parent))

    def test_new_layout_leaves_an_existing_legacy_packet_untouched(self):
        legacy = self.workspace / "runs" / self.packet["run_id"] / "entry" / digest(self.packet)
        legacy.mkdir(parents=True)
        saved = legacy / "TASK.json"
        saved.write_text("old saved packet; do not overwrite\n")
        result = reading_packet(self.production, self.packet)
        self.assertNotEqual(Path(result["task_file"]).parent, legacy)
        self.assertEqual(saved.read_text(), "old saved packet; do not overwrite\n")
        self.assertEqual(reading_packet(self.production, self.packet), result)

    def test_supplied_skill_hash_is_checked_before_materialization(self):
        self.packet["skill"]["sha256"] = "0" * 64
        with self.assertRaisesRegex(WorkflowError, "skill.*hash"):
            reading_packet(self.production, self.packet)
        self.assertEqual(list(self.workspace.iterdir()), [])

    def test_skill_path_cannot_escape_the_instruction_root(self):
        self.packet["skill"]["path"] = "../escaped.md"
        with self.assertRaises(WorkflowError):
            reading_packet(self.production, self.packet)
        self.assertEqual(list(self.workspace.iterdir()), [])


if __name__ == "__main__":
    unittest.main()
