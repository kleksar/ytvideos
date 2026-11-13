"""Accepted editorial inputs for licensed edits, including source sound and silence.

The edit script is an approved content plan. It never asserts source rights or
that audio has been listened to; those remain observed production checks.
"""
import copy
import hashlib
import json
import re

from .errors import WorkflowError
from .util import digest, require_text


EDIT_SCHEMA = "ytv-edit-script-v1"
NO_SPEECH_SCHEMA = "ytv-no-speech-v1"


def _words(text):
    return " ".join(text.split())


def read_script(path, profile, format):
    text = path.read_text(encoding="utf-8")
    require_text(text, "complete script")
    try:
        value = json.loads(text)
    except ValueError:
        value = None
    if isinstance(value, dict):
        if profile.get("recipe") != "licensed_clips" or value.get("schema") != EDIT_SCHEMA:
            raise WorkflowError("typed edit scripts apply only to the registered licensed-clips recipe")
        if set(value) != {"schema", "production_variant", "intent", "speech", "segments"}:
            raise WorkflowError("edit script requires schema, production_variant, intent, speech and segments")
        require_text(value["intent"], "complete editorial intent")
        variants = profile.get("production", {}).get("formats", {}).get(format, {}).get("variants", {})
        variant = value["production_variant"]
        if not isinstance(variant, str) or variant not in variants:
            raise WorkflowError("edit script must select a registered production_variant")
        speech = value["speech"]
        if not isinstance(speech, dict) or set(speech) != {"mode", "text"}:
            raise WorkflowError("edit script speech requires an explicit mode and exact text")
        if (not isinstance(speech["mode"], str) or speech["mode"] not in {"none", "source", "narration"}
                or not isinstance(speech["text"], str)):
            raise WorkflowError("edit script speech mode must be none, source or narration")
        if speech["mode"] == "none":
            if speech["text"] != "":
                raise WorkflowError("a no-speech edit must contain no invented narration or dialogue")
        else:
            require_text(speech["text"], "exact spoken text")
        segments = value["segments"]
        if not isinstance(segments, list) or not segments:
            raise WorkflowError("edit script requires a complete ordered segment plan")
        ids, spoken = [], []
        for segment in segments:
            if not isinstance(segment, dict) or set(segment) != {"id", "description", "spoken_text"}:
                raise WorkflowError("each edit segment requires id, description and spoken_text")
            if not isinstance(segment["id"], str) or not re.fullmatch(r"[a-zA-Z0-9_-]{1,80}", segment["id"]):
                raise WorkflowError("edit segment has an invalid id")
            if segment["id"] in ids:
                raise WorkflowError("edit segment ids must be unique")
            ids.append(segment["id"])
            require_text(segment["description"], "visible edit segment and outcome")
            if not isinstance(segment["spoken_text"], str):
                raise WorkflowError("edit segment spoken_text must be exact text or an empty string")
            if speech["mode"] == "none" and segment["spoken_text"] != "":
                raise WorkflowError("a no-speech segment must have empty spoken_text")
            spoken.append(segment["spoken_text"])
        if _words(" ".join(spoken)) != _words(speech["text"]):
            raise WorkflowError("ordered edit segments must preserve every spoken word")
        return {"kind": "edit_script", "mode": speech["mode"], "text": speech["text"],
                "production_variant": variant, "segment_ids": ids}
    if len(text.split()) < 40:
        raise WorkflowError("deliver a complete narration, not a topic or outline")
    return {"kind": "narration", "mode": "narration", "text": text,
            "production_variant": None, "segment_ids": None}


def accepted_script(run, artifacts):
    task = run.get("tasks", {}).get("script", {})
    if task.get("status") != "complete" or not task.get("outputs"):
        return None
    artifact = run["artifacts"][task["outputs"][0]]
    result = read_script(artifacts.resolve(artifact), run["profile"], run["format"])
    return {**result, "artifact_sha256": artifact["sha256"]}


def bind_requirements(requirements, script):
    """Bind conditional obligations to accepted script bytes, never caller flags."""
    if script is None:
        return requirements
    result = copy.deepcopy(requirements)
    result["speech"] = {"mode": script["mode"], "script_kind": script["kind"],
                        "script_sha256": script["artifact_sha256"],
                        "text_sha256": hashlib.sha256(script["text"].encode("utf-8")).hexdigest()}
    if script["mode"] == "none":
        result["review_checks"] = sorted(set(result["review_checks"]) - {"subtitles", "captions"} | {"no_speech"})
    result.pop("sha256", None)
    result["sha256"] = digest(result)
    return result


def validate_no_speech_artifact(value, *, script_sha256, audio_sha256):
    expected = {"schema": NO_SPEECH_SCHEMA, "script_sha256": script_sha256,
                "audio_sha256": audio_sha256, "has_speech": False}
    if not isinstance(value, dict) or value.get("has_speech") is not False or value != expected:
        raise WorkflowError("no-speech subtitle result must bind the accepted edit script and exact audio")
    return expected
