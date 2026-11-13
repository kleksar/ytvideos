"""Synthetic thumbnail plans; these records do not assert human or model QA."""
import json

from ytvideos.image_review import PLAN_SCHEMA


def plan_fixture(spec, script_sha256, *, ids=None):
    ids = ids or (["main", "alternative", "intro"] if spec["format"] == "long" else ["main"])
    return {"schema": PLAN_SCHEMA, "script_sha256": script_sha256, "selected_id": ids[0],
            "concepts": [{"id": key, "title": spec["metadata"]["title"],
                          "description": spec["metadata"]["description"],
                          "prompt": "Synthetic image instruction for " + key,
                          "visual_intent": "Synthetic geometric relation for " + key,
                          "overlay_text": "FIXTURE", "promise": "Synthetic promise " + key,
                          "first_confirmation": "Synthetic opening observation, not a real scene.",
                          "payoff": "Synthetic final observation, no real film or audience claim.",
                          "false_reading": "Fixture geometry must not be reported as real media.",
                          "intro_connection": "Synthetic opening links to the geometric fixture." if index == 0 else ""}
                         for index, key in enumerate(ids)]}


def seed_packaging(production, run_id, directory, *, title, ids):
    """Start native-host tests at accepted packaging without generating fake media."""
    from test_release import payload
    run = production.store.get(run_id)
    spec = payload()
    spec.update(run_id=run_id, channel_id=run["profile"]["youtube_channel_id"],
                revision=run["revision"], format=run["format"])
    if spec["format"] == "short":
        spec.pop("end_screen")
    spec["metadata"]["title"] = title
    output = directory / (run_id + "-packaging.json")
    output.write_text(json.dumps(spec))
    artifact = production.artifacts.put(output, "release_spec")
    receipt_path = directory / (run_id + "-packaging-receipt.json")
    plan = plan_fixture(spec, production._artifact(run, "script")["sha256"], ids=ids)
    receipt_path.write_text(json.dumps({"checks": [{"name": "thumbnail_plan", "observed": plan}]}))
    receipt = production.artifacts.put(receipt_path, "receipt")
    def seed(tx, state):
        state["artifacts"].update({artifact["id"]: artifact, receipt["id"]: receipt})
        state["tasks"]["packaging"].update(status="complete", outputs=[artifact["id"]], receipt=receipt["id"])
    production.store.mutate(run_id, seed)
