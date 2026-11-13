"""Bind an independent end-to-start reading to exact narrated-Short text.

This validates the review's identity, excerpts and coverage, not the meaning of
the story. A declared relationship is an accountable human/model observation;
it is never a machine classification of a narrative or a substitute for audio QA.
"""
import re

from .errors import WorkflowError
from .util import require_text


SCHEMA = "ytv-narrative-loop-v1"
OBSERVATIONS = {"continuation", "cold_open", "payoff_quote", "payoff_before_repeat", "two_cycle_read"}
PLACEHOLDERS = {"pass", "ok", "yes", "true", "verified", "unverified", "n/a", "none", "placeholder",
                "loop", "готово", "проверено", "да", "нормально", "ок"}


def _note(value, name):
    require_text(value, name)
    if not any(character.isalpha() for character in value) or value.strip().casefold().rstrip(".!:") in PLACEHOLDERS:
        raise WorkflowError(name + " requires an observation, not a verdict placeholder")
    return value


def validate_observation(observed, *, script_text, script_sha256, worker):
    """Validate exact bounded excerpts; complete utterances remain reviewer evidence."""
    if not isinstance(observed, dict) or observed.get("artifact_sha256") != script_sha256:
        raise WorkflowError("narrative_loop must bind the exact script SHA-256")
    reviewer = require_text(observed.get("reviewer"), "narrative_loop independent reviewer")
    if reviewer.strip() == worker.strip():
        raise WorkflowError("narrative_loop needs a reviewer distinct from the script author")
    text = script_text.strip()
    opening = require_text(observed.get("opening"), "narrative_loop opening excerpt")
    ending = require_text(observed.get("ending"), "narrative_loop ending excerpt")
    # These are evidence-context bounds, not a quota for the story's sentences.
    # Read the edge utterances in context; a matching pronoun/punctuation token
    # cannot stand in for a reviewed beginning or ending.
    if any(len(excerpt.split()) < 4 for excerpt in (opening, ending)):
        raise WorkflowError("narrative_loop excerpts need at least four words of edge-utterance context")
    if not text.startswith(opening) or not text.endswith(ending):
        raise WorkflowError("narrative_loop excerpts must be the exact script prefix and suffix")
    if len(opening) + len(ending) > len(text):
        raise WorkflowError("narrative_loop needs bounded, non-overlapping edge excerpts")
    if ((opening[-1].isalnum() and text[len(opening)].isalnum())
            or (ending[0].isalnum() and text[-len(ending)-1].isalnum())):
        raise WorkflowError("narrative_loop excerpts cannot cut through a word")
    if observed.get("joined_excerpt") != ending + "\n" + opening:
        raise WorkflowError("narrative_loop must show the literal ending followed by the opening")
    record = observed.get("evidence")
    if (not isinstance(record, dict) or set(record) != {"path", "sha256"}
            or not isinstance(record.get("path"), str) or not record["path"].strip()
            or not isinstance(record.get("sha256"), str) or not re.fullmatch(r"[0-9a-f]{64}", record["sha256"])):
        raise WorkflowError("narrative_loop requires a hash-bound independent evidence file")
    return record


def validate_evidence(document, observed, *, script_text):
    """Require specific reviewer observations; JSON itself cannot prove good writing."""
    expected = {"schema": SCHEMA, "script_sha256": observed["artifact_sha256"],
                **{name: observed[name] for name in ("reviewer", "opening", "ending", "joined_excerpt")}}
    if not isinstance(document, dict) or any(document.get(key) != value for key, value in expected.items()):
        raise WorkflowError("narrative_loop evidence does not bind the exact reviewed script and seam")
    if document.get("relationship") != "continuous_narration":
        raise WorkflowError("narrative_loop review must establish continuous narration; a thematic callback or unverified seam is insufficient")
    _note(document.get("method"), "narrative_loop review method")
    coverage = document.get("coverage")
    if (not isinstance(coverage, dict) or coverage.get("complete_edge_utterances") is not True
            or any(type(coverage.get(name)) is not int or coverage[name] < 2
                   for name in ("opening_utterances", "ending_utterances", "full_script_cycles"))):
        raise WorkflowError("narrative_loop review must cover complete edge utterances and two full-script cycles")
    observations = document.get("observations")
    if not isinstance(observations, dict) or set(observations) != OBSERVATIONS:
        raise WorkflowError("narrative_loop needs separate continuity, cold opening, payoff and two-cycle observations")
    for name in OBSERVATIONS:
        _note(observations[name], "narrative_loop observation " + name)
    if observations["payoff_quote"] not in script_text:
        raise WorkflowError("narrative_loop payoff_quote must occur in the exact script")
    return document
