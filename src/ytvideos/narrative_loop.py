"""Bind an independent end-to-start reading to exact narrated-Short text.

This validates the review's identity, excerpts and coverage, not the meaning of
the story. A declared relationship is an accountable human/model observation;
it is never a machine classification of a narrative or a substitute for audio QA.
"""
import re

from .errors import WorkflowError
from .util import require_text


OBSERVATIONS = {"continuation", "cold_open", "payoff_quote", "payoff_before_repeat", "two_cycle_read", "restart_test"}
SEAM_FIELDS = ("opening", "ending", "joined_excerpt")
LOOP_FIELDS = (*SEAM_FIELDS, "decision", "observations")
PLACEHOLDERS = {"pass", "ok", "yes", "true", "verified", "unverified", "n/a", "none", "placeholder",
                "loop", "готово", "проверено", "да", "нормально", "ок"}


def _note(value, name):
    require_text(value, name)
    if not any(character.isalpha() for character in value) or value.strip().casefold().rstrip(".!:") in PLACEHOLDERS:
        raise WorkflowError(name + " requires an observation, not a verdict placeholder")
    return value


def validate_seam(opening, ending, joined_excerpt, *, script_text):
    """Verify literal edge context without guessing utterance or sentence boundaries."""
    text = script_text.strip()
    opening = require_text(opening, "narrative_loop opening excerpt")
    ending = require_text(ending, "narrative_loop ending excerpt")
    if not text.startswith(opening) or not text.endswith(ending):
        raise WorkflowError("narrative_loop excerpts must be the exact script prefix and suffix")
    if len(opening) + len(ending) > len(text):
        raise WorkflowError("narrative_loop needs bounded, non-overlapping edge excerpts")
    if ((opening[-1].isalnum() and text[len(opening)].isalnum())
            or (ending[0].isalnum() and text[-len(ending)-1].isalnum())):
        raise WorkflowError("narrative_loop excerpts cannot cut through a word")
    if joined_excerpt != ending + "\n" + opening:
        raise WorkflowError("narrative_loop must show the literal ending followed by the opening")


def validate_observation(observed, *, script_text, script_sha256, worker):
    """The full reading packet supplies context; excerpts identify its exact seam."""
    if not isinstance(observed, dict) or observed.get("artifact_sha256") != script_sha256:
        raise WorkflowError("narrative_loop must bind the exact script SHA-256")
    reviewer = require_text(observed.get("reviewer"), "narrative_loop independent reviewer")
    if reviewer.strip() == worker.strip():
        raise WorkflowError("narrative_loop needs a reviewer distinct from the script author")
    validate_seam(observed.get("opening"), observed.get("ending"), observed.get("joined_excerpt"), script_text=script_text)
    record = observed.get("evidence")
    if (not isinstance(record, dict) or set(record) != {"path", "sha256"}
            or not isinstance(record.get("path"), str) or not record["path"].strip()
            or not isinstance(record.get("sha256"), str) or not re.fullmatch(r"[0-9a-f]{64}", record["sha256"])):
        raise WorkflowError("narrative_loop requires a hash-bound independent evidence file")
    return record


def validate_evidence(document, observed, *, script_text, require_pass=True):
    """Use the narrative section of the same verbatim independent review result."""
    from .script_review import DECISIONS, SCHEMA
    expected = {"schema": SCHEMA, "script_sha256": observed["artifact_sha256"], "reviewer": observed["reviewer"]}
    if not isinstance(document, dict) or any(document.get(key) != value for key, value in expected.items()):
        raise WorkflowError("narrative_loop evidence does not bind the exact reviewed script and seam")
    loop = document.get("narrative_loop")
    if not isinstance(loop, dict) or set(loop) != set(LOOP_FIELDS):
        raise WorkflowError("narrative_loop requires the independent reviewer's complete narrative section")
    if any(loop.get(name) != observed[name] for name in SEAM_FIELDS):
        raise WorkflowError("narrative_loop evidence does not bind the exact reviewed script and seam")
    if document.get("decision") not in DECISIONS or loop.get("decision") not in DECISIONS:
        raise WorkflowError("narrative_loop decisions must be pass, revise or unverified")
    if require_pass and (document.get("decision") != "pass" or loop.get("decision") != "pass"):
        raise WorkflowError("narrative_loop review is not passed; a thematic callback or unverified seam needs revision")
    observations = loop.get("observations")
    if not isinstance(observations, dict) or set(observations) != OBSERVATIONS:
        raise WorkflowError("narrative_loop needs continuation, cold opening, payoff, two-cycle and restart-test observations")
    for name in OBSERVATIONS:
        _note(observations[name], "narrative_loop observation " + name)
    if observations["payoff_quote"] not in script_text:
        raise WorkflowError("narrative_loop payoff_quote must occur in the exact script")
    return document
