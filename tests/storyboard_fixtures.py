"""Synthetic storyboard and reviewer records for software tests only."""

import json

from ytvideos.storyboard_contract import SCHEMA
from ytvideos.util import file_digest


def board_fixture(service, run, scene_id, narration):
    return {"schema": SCHEMA, "script_sha256": service._artifact(run, "script")["sha256"],
            "scenes": [{"id": scene_id, "prompt": "Synthetic map scene", "visual_intent": "Show a route choice",
                        "narration": narration, "visible_action": "The selected route is marked on the map",
                        "framing": "Overhead map view", "state_before": "No route marked",
                        "state_after": "Route marked", "event_order": 1}]}


def review_fixture(board_path, *, reviewer="synthetic-board-reviewer"):
    board = json.loads(board_path.read_text())
    result_path = board_path.with_name(board_path.name + ".continuity.json")
    result_path.write_text(json.dumps({
        "storyboard_sha256": file_digest(board_path), "script_sha256": board.get("script_sha256"),
        "reviewer": reviewer, "tool": "synthetic fixture only", "decision": "pass",
        "sequence_observation": "Fixture exercises exact scene coverage without live model review.",
        "scenes": [{"id": scene["id"], "observation": "Synthetic observation for this scene only."}
                   for scene in board.get("scenes", [])],
    }))
    return {"evidence": {"path": str(result_path), "sha256": file_digest(result_path)}}
