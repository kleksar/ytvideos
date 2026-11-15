"""Materialize pinned instructions once, preserving their repository-relative links."""
import hashlib
import json
from pathlib import Path

from .context import reference_path, validate_documents
from .errors import WorkflowError
from .util import canonical, file_digest, require_text


MATERIALIZATION_VERSION = 2


def instruction_files(packet):
    """Return a detached task descriptor and its files; never change pinned data."""
    payload = json.loads(canonical(packet))
    documents = validate_documents(payload["references"], payload["reference_documents"])
    skill = payload.get("skill")
    if not isinstance(skill, dict):
        raise WorkflowError("missing pinned skill")
    path = reference_path(skill.get("path"))
    data = require_text(skill.get("text"), "pinned skill text").encode("utf-8")
    sha256 = hashlib.sha256(data).hexdigest()
    if "sha256" in skill and skill["sha256"] != sha256:
        raise WorkflowError("pinned skill hash mismatch")
    local_path = "requirements/" + path
    files = {local_path: data}
    payload["skill"] = {key: value for key, value in skill.items() if key != "text"}
    payload["skill"].update(local_path=local_path, sha256=sha256)
    payload["materialization_version"] = MATERIALIZATION_VERSION
    payload["requirements"] = []
    payload["reference_manifest"] = []
    for document in documents:
        name = "requirements/" + document["path"]
        content = document["text"].encode("utf-8")
        if name in files and files[name] != content:
            raise WorkflowError("skill and reference document conflict at the same path")
        files[name] = content
        payload["requirements"].append(name)
        payload["reference_manifest"].append({"path": document["path"], "sha256": document["sha256"],
                                              "local_path": name})
    del payload["reference_documents"]
    files["TASK.json"] = (json.dumps(payload, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    return payload, files


def materialized_skill_file(directory):
    """Resolve and verify a new descriptor or an unchanged legacy worker skill."""
    directory = Path(directory).resolve()
    packet = json.loads((directory / "TASK.json").read_text(encoding="utf-8"))
    if not isinstance(packet, dict) or not isinstance(packet.get("skill"), dict):
        raise WorkflowError("missing materialized skill descriptor")
    skill = packet["skill"]
    version = packet.get("materialization_version")
    if version is None and "local_path" not in skill:
        # Saved jobs from the original layout keep their files and input hashes.
        name = "SKILL.md"
        expected = hashlib.sha256(require_text(skill.get("text"), "legacy skill text").encode()).hexdigest()
    elif version == MATERIALIZATION_VERSION:
        name = reference_path(skill.get("local_path"))
        if name != "requirements/" + reference_path(skill.get("path")):
            raise WorkflowError("materialized skill path differs from its source path")
        expected = skill.get("sha256")
    else:
        raise WorkflowError("unsupported materialized instruction layout")
    path = directory / name
    if (path.is_symlink() or not path.resolve().is_relative_to(directory) or not path.is_file()
            or not isinstance(expected, str) or file_digest(path) != expected):
        raise WorkflowError("materialized skill file or hash differs from its descriptor")
    return path
