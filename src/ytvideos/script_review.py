"""Bind one independent review result to the exact material supplied to its reader.

File hashes and session/tool references make an audit possible. They do not
authenticate the host, prove that a reader read every word or classify meaning.
The coordinator must preserve the reader's own response without rewriting it.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re

from .errors import WorkflowError
from .narrative_loop import _note, validate_evidence, validate_seam
from .util import file_digest, require_text


SCHEMA = "ytv-script-review-v1"
INPUT_SCHEMA = "ytv-script-review-input-v1"
READING_INSTRUCTIONS = (
    "Work as an independent first reader, without an author's verdict or explanation. "
    "For a typed edit-plan, assess the intended image/sound sequence and audience understanding; "
    "do not invent a narrator, spoken words or a narrator loop. "
    "Read the opening on its own, then the full script. State what you understood, "
    "what would keep or lose your attention, and concrete unresolved findings with exact quotes. "
    "When narrative_loop is supplied, read its literal two_cycles as continuous narration. "
    "Explain how the ending's actual meaning or grammar continues into the opening; test whether "
    "it instead sounds like a fresh introduction or only repeats a subject. Read the opening cold "
    "and identify the payoff already delivered before replay. Write your own complete review JSON "
    "bound to this input hash. Use revise or unverified when an applicable check fails or was not done. "
    "Do not let the author fill missing observations or reinterpret a non-passing answer."
)


def build_review_input(script_text, script_sha256, *, opening=None, ending=None):
    require_text(script_text, "exact script text")
    if hashlib.sha256(script_text.encode("utf-8")).hexdigest() != script_sha256:
        raise WorkflowError("review input text differs from the exact script SHA-256")
    loop = None
    if opening is not None or ending is not None:
        joined = str(ending) + "\n" + str(opening)
        validate_seam(opening, ending, joined, script_text=script_text)
        loop = {"opening": opening, "ending": ending, "joined_excerpt": joined,
                "two_cycles": script_text + "\n\n" + script_text}
    return {"schema": INPUT_SCHEMA, "script_sha256": script_sha256, "script_text": script_text,
            "instructions": READING_INSTRUCTIONS, "narrative_loop": loop}


def _read_object(record, label):
    if (not isinstance(record, dict) or set(record) != {"path", "sha256"}
            or not isinstance(record["path"], str) or not record["path"].strip()
            or not isinstance(record["sha256"], str) or not re.fullmatch(r"[0-9a-f]{64}", record["sha256"])):
        raise WorkflowError(label + " needs an exact path and SHA-256")
    path = Path(record["path"])
    try:
        if file_digest(path) != record["sha256"]:
            raise WorkflowError(label + " is stale or identifies different bytes")
        value = json.loads(path.read_bytes().decode("utf-8"))
    except (OSError, ValueError, UnicodeError) as exc:
        raise WorkflowError(label + " must contain a readable JSON object") from exc
    if not isinstance(value, dict):
        raise WorkflowError(label + " must be a JSON object, not a serialized string or list")
    return value


def validate_review(observed, *, script_text, script_sha256, worker, narrative_loop_required):
    if not isinstance(observed, dict) or observed.get("artifact_sha256") != script_sha256:
        raise WorkflowError("script review must bind the exact script SHA-256")
    reviewer = require_text(observed.get("reviewer"), "independent script reviewer")
    if reviewer.strip() == worker.strip():
        raise WorkflowError("script review requires a reader distinct from the script author")
    evidence = observed.get("evidence")
    document = _read_object(evidence, "independent script review")
    fields = {"schema", "script_sha256", "reviewer", "source", "input", "decision", "first_listener", "findings", "narrative_loop"}
    if (set(document) != fields or document.get("schema") != SCHEMA or document.get("script_sha256") != script_sha256
            or document.get("reviewer") != reviewer):
        raise WorkflowError("script review result must bind this reader and exact script using the current schema")
    source = document["source"]
    if (not isinstance(source, dict) or set(source) - {"tool", "session_id", "response_id"}
            or source.get("session_id") != reviewer):
        raise WorkflowError("script review needs its actual independent session identity")
    require_text(source.get("tool"), "independent review source tool")
    if "response_id" in source:
        require_text(source["response_id"], "observed independent response id")
    if document["decision"] != "pass":
        raise WorkflowError("independent script review is not passed; retain its findings and revise or resolve the blocker")
    first = document["first_listener"]
    if not isinstance(first, dict) or set(first) != {"understood", "attention", "quotes"}:
        raise WorkflowError("script review needs the reader's understanding, attention and exact supporting quotes")
    _note(first["understood"], "first-reader understanding")
    _note(first["attention"], "first-reader attention")
    if (not isinstance(first["quotes"], list) or not first["quotes"]
            or any(not isinstance(quote, str) or not quote.strip() or quote not in script_text for quote in first["quotes"])):
        raise WorkflowError("first-reader quotes must come from the exact script")
    findings = document["findings"]
    if not isinstance(findings, list):
        raise WorkflowError("script review findings must be a list")
    for finding in findings:
        if (not isinstance(finding, dict) or set(finding) != {"severity", "quote", "finding"}
                or finding["severity"] not in {"blocking", "non_blocking"}
                or not isinstance(finding["quote"], str) or not finding["quote"].strip() or finding["quote"] not in script_text):
            raise WorkflowError("script review findings require severity, an exact quote and an observation")
        _note(finding["finding"], "script review finding")
        if finding["severity"] == "blocking":
            raise WorkflowError("script review contains an unresolved blocking finding")
    loop = document["narrative_loop"]
    if narrative_loop_required:
        if not isinstance(loop, dict):
            raise WorkflowError("independent script review is missing the required narrative-loop reading")
        loop_observed = {"artifact_sha256": script_sha256, "reviewer": reviewer,
                         **{name: loop.get(name) for name in ("opening", "ending", "joined_excerpt")}}
        validate_seam(loop_observed["opening"], loop_observed["ending"], loop_observed["joined_excerpt"], script_text=script_text)
        validate_evidence(document, loop_observed, script_text=script_text)
    elif loop is not None:
        raise WorkflowError("non-narrative review must not invent a required narrator loop")
    reading = _read_object(document["input"], "independent review input")
    expected = build_review_input(script_text, script_sha256,
                                  opening=loop["opening"] if loop else None, ending=loop["ending"] if loop else None)
    if reading != expected:
        raise WorkflowError("independent review input must contain the exact script and literal two-cycle reading when required")
    return {"document": document, "evidence": evidence, "input": document["input"]}


def main():
    parser = argparse.ArgumentParser(description="Prepare exact independent review input; this performs no review.")
    parser.add_argument("--script", required=True, type=Path)
    parser.add_argument("--seam", type=Path, help="JSON containing exact opening and ending; omit only when narrator loop is not applicable")
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    seam = json.loads(args.seam.read_text(encoding="utf-8")) if args.seam else {}
    if not isinstance(seam, dict) or set(seam) not in ({}, {"opening", "ending"}):
        raise WorkflowError("seam input must contain only exact opening and ending")
    document = build_review_input(args.script.read_bytes().decode("utf-8"), file_digest(args.script), **seam)
    with args.output.open("x", encoding="utf-8") as output:
        output.write(json.dumps(document, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"path": str(args.output.resolve()), "sha256": file_digest(args.output),
                      "script_sha256": document["script_sha256"], "review_performed": False}))


if __name__ == "__main__":
    main()
