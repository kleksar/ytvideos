"""Validate an illustrated storyboard before creating scene tasks."""

from .errors import WorkflowError
from .util import require_text


SCHEMA = "ytv-illustrated-storyboard-v1"


def validate_storyboard(board, script, continuity_check, *, worker, board_sha256):
    if (script is None or not isinstance(board, dict) or board.get("schema") != SCHEMA
            or board.get("script_sha256") != script["artifact_sha256"]):
        raise WorkflowError("illustrated storyboard must identify its schema and exact accepted script")

    scenes = board.get("scenes")
    if (not isinstance(scenes, list) or not scenes
            or any(not isinstance(scene, dict) or not isinstance(scene.get("id"), str) for scene in scenes)):
        raise WorkflowError("illustrated storyboard requires ordered scene objects with IDs")
    excerpts = []
    previous_event = None
    for scene in scenes:
        label = f"storyboard scene {scene['id']}"
        excerpt = scene.get("narration")
        if not isinstance(excerpt, str):
            raise WorkflowError(f"{label}: narration must be a verbatim excerpt or an empty string")
        if not excerpt.strip():
            require_text(scene.get("silence_reason"), f"{label} silence_reason")
        excerpts.extend(excerpt.split())
        for field in ("visible_action", "framing", "state_before", "state_after"):
            require_text(scene.get(field), f"{label} {field}")
        event = scene.get("event_order")
        if type(event) is not int or event < 1:
            raise WorkflowError(f"{label}: event_order must be a positive integer")
        if previous_event is not None and event < previous_event:
            require_text(scene.get("order_note"), f"{label} order_note for a backward jump")
        previous_event = event
    if excerpts != script["text"].split():
        raise WorkflowError("storyboard narration must cover every accepted word in order without omissions or repeats")

    if not isinstance(continuity_check, dict):
        raise WorkflowError("storyboard requires independent scene-by-scene continuity evidence")
    if (continuity_check.get("storyboard_sha256") != board_sha256
            or continuity_check.get("script_sha256") != script["artifact_sha256"]):
        raise WorkflowError("storyboard continuity evidence must bind the exact storyboard and script")
    if continuity_check.get("decision") != "pass":
        raise WorkflowError("storyboard continuity review must resolve defects before completion")
    reviewer = require_text(continuity_check.get("reviewer"), "storyboard reviewer session")
    require_text(continuity_check.get("tool"), "storyboard reviewer invocation tool")
    if reviewer.strip() == worker.strip():
        raise WorkflowError("storyboard continuity reviewer must differ from the storyboard author")
    require_text(continuity_check.get("sequence_observation"), "storyboard sequence observation")
    observations = continuity_check.get("scenes")
    if (not isinstance(observations, list) or any(not isinstance(item, dict) for item in observations)
            or [item.get("id") for item in observations] != [scene["id"] for scene in scenes]):
        raise WorkflowError("storyboard continuity evidence must cover each scene in playback order")
    for item in observations:
        require_text(item.get("observation"), f"storyboard continuity observation for {item['id']}")


def validate_scene_match(observed, *, scene, image_sha256):
    if (observed.get("scene_id") != scene["id"] or observed.get("image_sha256") != image_sha256):
        raise WorkflowError("scene_match must bind the assigned scene and exact generated image")
    require_text(observed.get("visible_action"), "scene_match observation from the actual image")
