"""One executable entrance: saved run, current plan and readable pinned task files.

This prepares the existing workflow. It does not claim tasks, call providers,
grant approvals or create an alternative sequence of production stages.
"""
import errno
from pathlib import Path
import shutil
import tempfile

from .doctor import inspect
from .errors import Conflict, WorkflowError
from .packets import MATERIALIZATION_VERSION, instruction_files
from .util import digest, file_digest


def reading_packet(production, packet):
    payload, files = instruction_files(packet)
    identity = digest({"materialization_version": MATERIALIZATION_VERSION, "packet": packet})
    directory = production.workspace / "runs" / packet["run_id"] / "entry" / identity
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
            except OSError as exc:
                # Another delivery of the same request may have published this
                # complete packet. Accept only exactly the same saved bytes.
                if exc.errno not in {errno.EEXIST, errno.ENOTEMPTY}:
                    raise
        finally:
            if staging.exists():
                shutil.rmtree(staging)
    verify_saved()
    return {"task_id": packet["task_id"], "input_hash": packet["input_hash"],
            "task_file": str(directory / "TASK.json"), "task_file_sha256": file_digest(directory / "TASK.json"),
            "skill_file": str(directory / payload["skill"]["local_path"]),
            "requirement_files": [str(directory / item["local_path"]) for item in payload["reference_manifest"]],
            "task_guide": packet["task_guide"],
            "instruction": "Read task_file, skill_file and every requirement_file before executing this task. "
                           "These files contain the pinned rules. Record actual capabilities, claim, "
                           "complete with evidence, then request next. Do not replace this run with an ad-hoc draft."}


def start_packet(production, run_id, *, session_id=None):
    from .session_guard import bind_session
    binding = bind_session(production, run_id, session_id)
    # Capture all run-dependent views together. The current claim will still
    # revalidate inputs if another worker changes this state after the read.
    with production.store.transaction() as tx:
        run = tx.get_run(run_id)
        plan = production._plan(run)
        packets = [production._context_packet(tx, run, task["id"]) for task in plan["next"]["tasks"]]
    return {"run_id": run_id, "run_version": run["version"], "session_guard": binding,
            "first_response": plan["first_response"],
            "plan_summary": {"channel": plan["channel"], "format": plan["format"],
                             "intent": plan["intent"], "source_script": plan["source_script"],
                             "target": plan["target"], "accepted": plan["accepted"],
                             "production_requirements": plan["production_requirements"],
                             "steps": [{key: item[key] for key in ("id", "status", "goal", "skill")}
                                       for item in plan["steps"]], "runtime": plan["runtime"]},
            "next": plan["next"],
            "read_next": [reading_packet(production, packet) for packet in packets],
            "doctor": inspect(production, run_id, run_snapshot=run),
            "completion_boundary": "A new story is ready for the user only after research and script completion "
                                   "with the required independent evidence and the script approval gate. "
                                   "An unfinished draft is not a completed episode. A video requires completed review."}
