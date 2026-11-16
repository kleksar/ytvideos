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
from .narrative_loop import LOOP_FIELDS, OBSERVATIONS, SEAM_FIELDS, _note, validate_evidence, validate_seam
from .util import file_digest, require_text


SCHEMA = "ytv-script-review-v1"
INPUT_SCHEMA = "ytv-script-review-input-v1"
DECISIONS = ("pass", "revise", "unverified")
REVIEW_FIELDS = ("schema", "script_sha256", "reviewer", "source", "input", "decision", "first_listener", "findings", "narrative_loop")
SOURCE_FIELDS = ("tool", "session_id")
SOURCE_OPTIONAL = ("response_id",)
RECORD_FIELDS = ("path", "sha256")
FIRST_LISTENER_FIELDS = ("understood", "attention", "quotes")
FINDING_FIELDS = ("severity", "quote", "finding")
SEVERITIES = ("blocking", "non_blocking")
LEGACY_READING_INSTRUCTIONS = (
    "Work as an independent first reader, without an author's verdict or explanation. "
    "For a typed edit-plan, assess the intended image/sound sequence and audience understanding; "
    "do not invent a narrator, spoken words or a narrator loop. "
    "Read the opening on its own, then the full script. State what you understood, "
    "what would keep or lose your attention, and concrete unresolved findings with exact quotes. "
    "For narration, assess natural spoken language: concrete actions rather than generic judgments, "
    "repeated explanations, formulaic contrasts, monotonous fragments and an over-explained ending. "
    "Quote the exact line and explain its effect; do not fail a word, punctuation mark or quiet tone "
    "by itself. Do not invent dialogue, motives or danger to improve it. A lively rewrite must preserve "
    "facts and material uncertainty. Put these observations in existing first_listener and findings "
    "fields, not a new score or schema. Do not infer AI authorship or audience metrics from style. "
    "When narrative_loop is supplied, read its literal two_cycles as continuous narration. "
    "Explain how the ending's actual meaning or grammar continues into the opening; test whether "
    "it instead sounds like a fresh introduction or only repeats a subject. Read the opening cold "
    "and identify the payoff already delivered before replay. Write your own complete review JSON "
    "bound to this input hash, following output_contract exactly: it is the response JSON Schema, "
    "not a response to copy. Return one object, without Markdown fences or a JSON-encoded string. "
    "Use revise or unverified when an applicable check fails or was not done; describe the failure or "
    "unperformed check in its observation instead of claiming it passed. Do not add top-level summary, "
    "understood, attention or limitations; put understanding/attention under first_listener, and "
    "specific problems or limitations under findings. The host must supply this input file's absolute "
    "path/hash and your actual invocation tool/session ID in the assignment (or a follow-up after "
    "session creation). Set reviewer and source.session_id to that actual independent identity; "
    "source.tool to the actual invocation tool; input to this exact saved packet's path/hash. "
    "You may compute the input hash from its bytes; it is not script_sha256. Do not invent missing "
    "identities or hashes: request the missing host metadata. Omit source.response_id unless actually "
    "observed. Do not let the author fill missing observations or reinterpret a non-passing answer."
)

# Preserve previously issued exact packets while new readers receive the current policy.
READING_INSTRUCTIONS = LEGACY_READING_INSTRUCTIONS + (
    " Review as entertainment: preserve the story's force, pace and clarity. "
    "Block material distortions, invented facts or quotes, and real risks; identify the "
    "specific harm and a concise correction within the authorized scope. Minor imprecision, "
    "unproven perfection and matters of taste alone are non-blocking. Do not demand "
    "academic caveats or expanded narration. Do not invent evidence, a pass, or guarantees "
    "of retention or profit; unperformed required checks remain unverified."
)


def _object(properties, required):
    return {"type": "object", "required": list(required), "additionalProperties": False, "properties": properties}


def output_contract(script_sha256, loop):
    """Self-contained machine-readable shape; no authored verdict or invented identity."""
    def text(description):
        return {"type": "string", "minLength": 1, "description": description}
    decision = {"type": "string", "enum": list(DECISIONS),
                "description": "Your actual decision; an unperformed check is unverified, a failed check needs revision."}
    quote = text("A nonempty verbatim excerpt from script_text; preserve its exact bytes.")
    narrative = {"type": "null", "description": "This input has no required narrator-loop review."}
    if loop:
        observations = {name: text({
            "continuation": "Explain the actual semantic/grammatical connection, or why the seam fails.",
            "cold_open": "Assess whether the opening is understandable without prior playback.",
            "payoff_quote": "Quote the actual delivered payoff, or the exact passage showing the missing payoff.",
            "payoff_before_repeat": "Explain what is resolved before replay, or what remains unresolved.",
            "two_cycle_read": "Your observation from reading the supplied two full cycles; state explicitly if not performed.",
            "restart_test": "Explain whether the replay is continuation, a fresh introduction, or only a repeated topic."
        }[name]) for name in sorted(OBSERVATIONS)}
        observations["payoff_quote"] = {**observations["payoff_quote"],
                                         "description": observations["payoff_quote"]["description"] + " Must occur verbatim in script_text."}
        narrative = _object({**{name: {"type": "string", "const": loop[name]} for name in SEAM_FIELDS},
                             "decision": decision, "observations": _object(observations, sorted(OBSERVATIONS))}, LOOP_FIELDS)
    return {"$schema": "https://json-schema.org/draft/2020-12/schema", **_object({
        "schema": {"type": "string", "const": SCHEMA},
        "script_sha256": {"type": "string", "const": script_sha256},
        "reviewer": text("Actual independent reviewer session ID supplied by the host; identical to source.session_id."),
        "source": _object({"tool": text("Actual host tool that invoked this independent review."),
                           "session_id": text("Actual independent session ID; identical to reviewer."),
                           "response_id": text("Optional: include only a response ID actually returned by the host.")}, SOURCE_FIELDS),
        "input": _object({"path": text("Absolute path of this exact saved reading packet, supplied by the host."),
                          "sha256": {"type": "string", "pattern": "^[0-9a-f]{64}$",
                                     "description": "SHA-256 of this input file's bytes; use its descriptor or compute it, never guess."}}, RECORD_FIELDS),
        "decision": decision,
        "first_listener": _object({"understood": text("Your understanding from the first reading."),
                                   "attention": text("What would keep/lose attention and why."),
                                   "quotes": {"type": "array", "minItems": 1, "items": quote}}, FIRST_LISTENER_FIELDS),
        "findings": {"type": "array", "items": _object({"severity": {"type": "string", "enum": list(SEVERITIES)},
                                                         "quote": quote, "finding": text("Your concrete finding or limitation.")}, FINDING_FIELDS)},
        "narrative_loop": narrative}, REVIEW_FIELDS)}


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
            "instructions": READING_INSTRUCTIONS, "narrative_loop": loop,
            "output_contract": output_contract(script_sha256, loop)}


def _read_object(record, label):
    if (not isinstance(record, dict) or set(record) != set(RECORD_FIELDS)
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


def validate_response(observed, *, script_text, script_sha256, worker, narrative_loop_required):
    """Validate the actual envelope/bindings, including negative reviewer decisions.

    Structural validity does not accept a script or prove host provenance.
    """
    if not isinstance(observed, dict) or observed.get("artifact_sha256") != script_sha256:
        raise WorkflowError("script review must bind the exact script SHA-256")
    reviewer = require_text(observed.get("reviewer"), "independent script reviewer")
    if reviewer.strip() == worker.strip():
        raise WorkflowError("script review requires a reader distinct from the script author")
    evidence = observed.get("evidence")
    document = _read_object(evidence, "independent script review")
    if (set(document) != set(REVIEW_FIELDS) or document.get("schema") != SCHEMA or document.get("script_sha256") != script_sha256
            or document.get("reviewer") != reviewer):
        raise WorkflowError("script review result must bind this reader and exact script using the current schema")
    source = document["source"]
    if (not isinstance(source, dict) or set(source) - set(SOURCE_FIELDS + SOURCE_OPTIONAL)
            or source.get("session_id") != reviewer):
        raise WorkflowError("script review needs its actual independent session identity")
    require_text(source.get("tool"), "independent review source tool")
    if "response_id" in source:
        require_text(source["response_id"], "observed independent response id")
    if document["decision"] not in DECISIONS:
        raise WorkflowError("independent script review decision must be pass, revise or unverified")
    first = document["first_listener"]
    if not isinstance(first, dict) or set(first) != set(FIRST_LISTENER_FIELDS):
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
        if (not isinstance(finding, dict) or set(finding) != set(FINDING_FIELDS)
                or finding["severity"] not in SEVERITIES
                or not isinstance(finding["quote"], str) or not finding["quote"].strip() or finding["quote"] not in script_text):
            raise WorkflowError("script review findings require severity, an exact quote and an observation")
        _note(finding["finding"], "script review finding")
    loop = document["narrative_loop"]
    if narrative_loop_required:
        if not isinstance(loop, dict):
            raise WorkflowError("independent script review is missing the required narrative-loop reading")
        loop_observed = {"artifact_sha256": script_sha256, "reviewer": reviewer,
                         **{name: loop.get(name) for name in SEAM_FIELDS}}
        validate_seam(loop_observed["opening"], loop_observed["ending"], loop_observed["joined_excerpt"], script_text=script_text)
        validate_evidence(document, loop_observed, script_text=script_text, require_pass=False)
    elif loop is not None:
        raise WorkflowError("non-narrative review must not invent a required narrator loop")
    reading = _read_object(document["input"], "independent review input")
    expected = build_review_input(script_text, script_sha256,
                                  opening=loop["opening"] if loop else None, ending=loop["ending"] if loop else None)
    legacy_expected = {**expected, "instructions": LEGACY_READING_INSTRUCTIONS}
    if reading != expected and reading != legacy_expected:
        raise WorkflowError("independent review input must contain the exact script and literal two-cycle reading when required")
    return {"document": document, "evidence": evidence, "input": document["input"]}


def _require_pass(document):
    if document["decision"] != "pass":
        raise WorkflowError("independent script review is not passed; retain its findings and revise or resolve the blocker")
    if any(finding["severity"] == "blocking" for finding in document["findings"]):
        raise WorkflowError("script review contains an unresolved blocking finding")
    if document["narrative_loop"] and document["narrative_loop"]["decision"] != "pass":
        raise WorkflowError("narrative_loop review is not passed; a thematic callback or unverified seam needs revision")


def validate_review(observed, *, script_text, script_sha256, worker, narrative_loop_required):
    result = validate_response(observed, script_text=script_text, script_sha256=script_sha256,
                               worker=worker, narrative_loop_required=narrative_loop_required)
    _require_pass(result["document"])
    return result


def main():
    parser = argparse.ArgumentParser(description="Prepare review input or check a reader's response; this performs no review or approval.")
    parser.add_argument("--script", required=True, type=Path)
    parser.add_argument("--seam", type=Path, help="JSON containing exact opening and ending; omit only when narrator loop is not applicable")
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--output", type=Path)
    action.add_argument("--check-response", type=Path, help="Check structure/bindings; valid revise/unverified decisions remain negative evidence")
    parser.add_argument("--author", help="Actual script author worker ID; required for --check-response")
    args = parser.parse_args()
    seam = json.loads(args.seam.read_text(encoding="utf-8")) if args.seam else {}
    if not isinstance(seam, dict) or set(seam) not in ({}, {"opening", "ending"}):
        raise WorkflowError("seam input must contain only exact opening and ending")
    text, sha256 = args.script.read_bytes().decode("utf-8"), file_digest(args.script)
    document = build_review_input(text, sha256, **seam)
    if args.check_response:
        require_text(args.author, "actual script author for response check")
        evidence = {"path": str(args.check_response.resolve()), "sha256": file_digest(args.check_response)}
        response = _read_object(evidence, "independent script review")
        observed = {"artifact_sha256": sha256, "reviewer": response.get("reviewer"), "evidence": evidence}
        result = validate_response(observed, script_text=text, script_sha256=sha256,
                                   worker=args.author, narrative_loop_required=bool(seam))
        supplied = _read_object(result["input"], "independent review input")
        legacy_document = {**document, "instructions": LEGACY_READING_INSTRUCTIONS}
        if supplied != document and supplied != legacy_document:
            raise WorkflowError("independent review input differs from the requested script/seam")
        consistent = True
        try:
            _require_pass(result["document"])
        except WorkflowError:
            consistent = False
        print(json.dumps({"structurally_valid": True, "decision": response["decision"], "pass_consistent": consistent,
                          "review_performed": False, "script_accepted": False, "evidence": evidence}))
        return
    with args.output.open("x", encoding="utf-8") as output:
        output.write(json.dumps(document, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"path": str(args.output.resolve()), "sha256": file_digest(args.output),
                      "script_sha256": document["script_sha256"], "review_performed": False}))


if __name__ == "__main__":
    main()
