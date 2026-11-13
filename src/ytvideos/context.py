"""Select and pin the documents needed by one task, including channel recipes."""

import hashlib
from pathlib import Path, PurePosixPath

from .documentation import current_reference_error
from .errors import WorkflowError
from .util import digest


STAGE_REFERENCES = {
    "research": ["docs/standards/editorial.md", "docs/standards/thumbnails.md"],
    "script": ["docs/standards/editorial.md", "docs/standards/narration.md", "docs/standards/thumbnails.md"],
    "storyboard": ["docs/standards/visual.md"],
    "scene_image": ["docs/standards/visual.md"],
    "audio": ["docs/standards/audio.md"],
    "subtitles": ["docs/standards/audio.md", "docs/standards/delivery.md"],
    "render": ["docs/standards/delivery.md", "docs/standards/visual.md", "docs/standards/audio.md"],
    "review": ["docs/standards/delivery.md", "docs/standards/visual.md", "docs/standards/audio.md",
               "docs/standards/editorial.md", "docs/standards/narration.md", "docs/standards/thumbnails.md"],
    "packaging": ["docs/standards/release.md", "docs/standards/thumbnails.md"],
    "upload": ["docs/standards/release.md", "docs/standards/thumbnails.md"],
    "configure_release": ["docs/standards/release.md", "docs/standards/thumbnails.md",
                          "docs/operations/thumbnail-experiments.md"],
    "schedule": ["docs/standards/release.md"],
    "verify_publication": ["docs/standards/release.md", "docs/operations/thumbnail-experiments.md"],
}


def reference_path(value):
    """Accept only unambiguous repository-relative paths, also inside workers."""
    if (not isinstance(value, str) or not value or "\\" in value or ":" in value or "\0" in value
            or PurePosixPath(value).is_absolute() or str(PurePosixPath(value)) != value
            or any(part in {".", ".."} for part in value.split("/"))):
        raise WorkflowError("reference path must stay inside the repository")
    return value


def _entries(profile):
    entries = profile.get("context_references", [])
    if not isinstance(entries, list):
        raise WorkflowError("context_references must be a list")
    choices = {"stages": set(STAGE_REFERENCES), "formats": {"short", "long"},
               "purposes": {"scene", "thumbnail"}}
    for entry in entries:
        if (not isinstance(entry, dict) or set(entry) - {"path", *choices} or "path" not in entry):
            raise WorkflowError("invalid context reference entry")
        reference_path(entry["path"])
        for name, allowed in choices.items():
            if name in entry and (not isinstance(entry[name], list) or not entry[name]
                                  or any(not isinstance(value, str) or value not in allowed for value in entry[name])):
                raise WorkflowError(f"invalid context reference {name}")
        yield entry


def task_references(task, *, profile=None, format=None, project_root=None):
    """Select standards and explicitly declared channel documents for this task."""
    stage = task["stage"]
    paths = list(STAGE_REFERENCES.get(stage, []))
    purpose = task.get("payload", {}).get("purpose", "scene") if stage == "scene_image" else None
    if stage == "scene_image" and purpose == "thumbnail":
        paths.append("docs/standards/thumbnails.md")
    # The production skill requires the accepted Shorts loop at these stages.
    if format == "short" and stage in {"storyboard", "audio", "render"}:
        paths.append("docs/standards/editorial.md")
    if profile is not None:
        if project_root is not None:
            path = reference_path(f"channels/{profile['id']}/PROFILE.md")
            if (Path(project_root) / path).exists():
                paths.append(path)
        for entry in _entries(profile):
            if (("stages" not in entry or stage in entry["stages"])
                    and ("formats" not in entry or format in entry["formats"])
                    and ("purposes" not in entry or purpose in entry["purposes"])):
                paths.append(entry["path"])
    return list(dict.fromkeys(paths))


def _read_document(root, path, *, current=False):
    path = reference_path(path)
    root = Path(root).resolve()
    source = (root / path).resolve()
    if not source.is_relative_to(root) or not source.is_file():
        raise WorkflowError(f"missing or outside-repository task reference: {path}")
    try:
        text = source.read_bytes().decode("utf-8")
    except (OSError, UnicodeError) as exc:
        raise WorkflowError(f"cannot read task reference: {path}") from exc
    if current:
        error = (current_reference_error(path, text)
                 or current_reference_error(source.relative_to(root).as_posix(), text))
        if error:
            raise WorkflowError(error)
    return {"path": path, "sha256": hashlib.sha256(text.encode()).hexdigest(), "text": text}


def _route(task):
    return "thumbnail" if task["stage"] == "scene_image" and task.get("payload", {}).get("purpose") == "thumbnail" else task["stage"]


def snapshot_references(root, profile, format):
    """One run snapshot owns document contents and routing, without per-task copies."""
    tasks = [{"stage": stage} for stage in STAGE_REFERENCES]
    tasks.append({"stage": "scene_image", "payload": {"purpose": "thumbnail"}})
    routes = {_route(task): task_references(task, profile=profile, format=format, project_root=root)
              for task in tasks}
    paths = dict.fromkeys(path for values in routes.values() for path in values)
    return {"routes": routes, "documents": {path: _read_document(root, path, current=True) for path in paths}}


def validate_documents(paths, documents):
    """Reject incomplete or modified manifests before materializing worker files."""
    if (not isinstance(paths, list) or any(not isinstance(path, str) for path in paths)
            or len(paths) != len(set(paths)) or not isinstance(documents, list)):
        raise WorkflowError("invalid task reference manifest")
    by_path = {}
    for item in documents:
        if not isinstance(item, dict) or set(item) != {"path", "sha256", "text"}:
            raise WorkflowError("invalid task reference document")
        path = reference_path(item["path"])
        if path in by_path or not isinstance(item["text"], str):
            raise WorkflowError("duplicate or invalid task reference document")
        if hashlib.sha256(item["text"].encode()).hexdigest() != item["sha256"]:
            raise WorkflowError(f"task reference hash mismatch: {path}")
        by_path[path] = item
    if set(paths) != set(by_path):
        raise WorkflowError("task reference manifest is incomplete")
    return [by_path[reference_path(path)] for path in paths]


def reference_context(run, task, project_root):
    snapshot = run.get("reference_snapshot")
    if snapshot is None:
        # The caller must check the original code pin before reading a legacy
        # checkout. These texts were not saved when that run was created.
        paths = task_references(task, profile=run["profile"], format=run["format"], project_root=project_root)
        documents = [_read_document(project_root, path) for path in paths]
        source = "legacy_checkout"
    else:
        if digest(snapshot) != run["pins"].get("references"):
            raise WorkflowError("run reference snapshot differs from its pin")
        paths = snapshot["routes"][_route(task)]
        documents = [snapshot["documents"][path] for path in paths]
        source = "pinned"
    return {"references": list(paths), "reference_documents": validate_documents(paths, documents),
            "reference_source": source}
