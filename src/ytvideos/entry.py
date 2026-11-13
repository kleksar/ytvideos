"""One executable entrance: saved run, current plan and readable pinned task files.

This prepares the existing workflow. It does not claim tasks, call providers,
grant approvals or create an alternative sequence of production stages.
"""
import json
from pathlib import Path
import shutil
import tempfile

from .context import validate_documents
from .doctor import inspect
from .errors import Conflict, WorkflowError
from .util import canonical, digest, file_digest


def reading_packet(production, packet):
    documents = validate_documents(packet["references"], packet["reference_documents"])
    payload = json.loads(canonical(packet))
    files = {"SKILL.md": payload["skill"]["text"].encode("utf-8")}
    payload["reference_manifest"] = []
    for document in documents:
        name = "requirements/" + document["path"]
        files[name] = document["text"].encode("utf-8")
        payload["reference_manifest"].append({"path": document["path"], "sha256": document["sha256"],
                                               "local_path": name})
    del payload["reference_documents"]
    files["TASK.json"] = (json.dumps(payload, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    directory = production.workspace / "runs" / packet["run_id"] / "entry" / digest(packet)
    if not directory.resolve().is_relative_to(production.workspace):
        raise WorkflowError("entry packet must stay inside its workspace")
    directory.parent.mkdir(parents=True, exist_ok=True)
    def verify_saved():
        for name, data in files.items():
            target = directory / name
            if target.is_symlink() or not target.resolve().is_relative_to(directory.resolve()) or not target.is_file() or target.read_bytes() != data:
                raise Conflict("existing entry packet differs from its pinned context; inspect the modified file")
    if not directory.exists():
        staging = Path(tempfile.mkdtemp(prefix=".entry-", dir=directory.parent))
        try:
            for name, data in files.items():
                target = staging / name
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(data)
            try:
                staging.rename(directory)
            except FileExistsError:
                # Another delivery of the same request may have published this
                # complete packet. Accept only exactly the same saved bytes.
                pass
        finally:
            if staging.exists():
                shutil.rmtree(staging)
    verify_saved()
    return {"task_id": packet["task_id"], "input_hash": packet["input_hash"],
            "task_file": str(directory / "TASK.json"), "task_file_sha256": file_digest(directory / "TASK.json"),
            "skill_file": str(directory / "SKILL.md"),
            "requirement_files": [str(directory / item["local_path"]) for item in payload["reference_manifest"]],
            "task_guide": packet["task_guide"],
            "instruction": "Read task_file, skill_file and every requirement_file before executing this task. "
                           "These files contain the pinned rules. Record actual capabilities, claim, "
                           "complete with evidence, then request next. Do not replace this run with an ad-hoc draft."}


def start_packet(production, run_id):
    plan = production.plan(run_id)
    return {"run_id": run_id, "first_response": plan["first_response"],
            "plan_summary": {"channel": plan["channel"], "format": plan["format"],
                             "intent": plan["intent"], "source_script": plan["source_script"],
                             "target": plan["target"], "accepted": plan["accepted"],
                             "production_requirements": plan["production_requirements"],
                             "steps": [{key: item[key] for key in ("id", "status", "goal", "skill")}
                                       for item in plan["steps"]], "runtime": plan["runtime"]},
            "next": plan["next"],
            "read_next": [reading_packet(production, production.context(run_id, task["id"]))
                          for task in plan["next"]["tasks"]],
            "doctor": inspect(production, run_id),
            "completion_boundary": "A new story is ready for the user only after research and script completion "
                                   "with the required independent evidence and the script approval gate. "
                                   "An unfinished draft is not a completed episode. A video requires completed review."}
