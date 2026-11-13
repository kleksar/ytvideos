"""Pure dependency graph. Preparation and human publication authority are separate."""

from .util import digest


WORKFLOW_VERSION = "1"
STAGES = {
    "research": ([], [], ["web.search"], "ytv-write-script"),
    "script": (["research"], [], ["model.text"], "ytv-write-script"),
    "storyboard": (["script"], ["script"], ["model.text"], "ytv-produce-video"),
    "audio": (["script"], ["script"], ["audio.produce"], "ytv-produce-video"),
    "packaging": (["script"], ["script"], ["model.text"], "ytv-release-video"),
    "subtitles": (["audio"], ["script"], ["subtitle.align"], "ytv-produce-video"),
    "render": (["storyboard", "audio", "subtitles"], ["script"], ["video.render"], "ytv-produce-video"),
    "review": (["render"], ["script"], ["video.inspect", "model.vision"], "ytv-review-video"),
    "upload": (["review", "packaging"], ["script", "mp4"], ["youtube.upload"], "ytv-release-video"),
    "configure_release": (["upload", "packaging"], ["script", "mp4"], ["youtube.configure"], "ytv-release-video"),
    "schedule": (["configure_release"], ["script", "mp4"], ["youtube.schedule"], "ytv-release-video"),
    "verify_publication": (["schedule"], ["script", "mp4"], ["youtube.read"], "ytv-release-video"),
}
EXTERNAL_STAGES = {"audio", "scene_image", "upload", "configure_release", "schedule"}
OUTPUT_KINDS = {"research": "research", "script": "script", "storyboard": "storyboard", "audio": "audio",
                "scene_image": "image", "subtitles": "srt", "render": "mp4", "review": "qa",
                "packaging": "release_spec", "upload": "upload_receipt", "configure_release": "release_receipts",
                "schedule": "schedule_receipt", "verify_publication": "publication_receipt"}
REQUIRED_CHECKS = {
    "research": {"sources", "topic_overlap", "viewer_value"},
    "script": {"factual_support", "first_listener", "viewer_value", "independent_review"},
    "storyboard": {"coverage", "visual_continuity", "rights"},
    "audio": {"voice_identity", "exact_text", "speed_once", "listening"},
    "scene_image": {"image_decoded", "scene_match", "visual_review"},
    "subtitles": {"exact_speech", "timing"},
    "render": {"streams", "duration", "provenance"},
    "review": {"visual_review", "listening", "subtitles", "rights", "delivery_contract"},
    "packaging": {"promise_matches_script", "metadata", "thumbnail_plan"},
    "upload": {"channel_identity", "private_upload", "processing"},
    "configure_release": {"release_completeness"},
    "schedule": {"saved_schedule"},
    "verify_publication": {"remote_readback"},
}


def task_references(task):
    """Compatibility entry for callers needing only stage-level standards."""
    from .context import task_references as select
    return select(task)


def new_tasks():
    return {stage: make_task(stage, stage, deps, gates, capabilities, skill)
            for stage, (deps, gates, capabilities, skill) in STAGES.items()}


def make_task(task_id, stage, dependencies, gates, capabilities, skill):
    return {"id": task_id, "stage": stage, "dependencies": list(dependencies), "gates": list(gates),
            "capabilities": list(capabilities), "skill": skill, "status": "pending", "attempt": 0,
            "generation": 1, "outputs": [], "blocker": None, "claim": None}


def missing_dependencies(run, task):
    return [key for key in task["dependencies"] if run["tasks"][key]["status"] != "complete"]


def valid_approval(run, kind):
    proof = run["approvals"].get(kind)
    task_id = "script" if kind == "script" else "render"
    if not proof or run["tasks"][task_id]["status"] != "complete":
        return False
    return proof["artifact_id"] in run["tasks"][task_id]["outputs"] and proof["revision"] == run["revision"]


def ready(run, task):
    return (run["status"] not in {"cancelled", "scheduled"} and task["status"] == "pending"
            and not missing_dependencies(run, task) and all(valid_approval(run, gate) for gate in task["gates"]))


def input_hash(run, task):
    return digest({"pins": run["pins"], "revision": run["revision"], "task": task["id"],
                   "generation": task["generation"],
                   "payload": task.get("payload"),
                   "inputs": {key: run["tasks"][key]["outputs"] for key in task["dependencies"]}})


def derive_status(run):
    if run["status"] == "cancelled":
        return "cancelled"
    if run["tasks"]["verify_publication"]["status"] == "complete":
        return "scheduled"
    if run["tasks"]["review"]["status"] == "complete" and not valid_approval(run, "mp4"):
        return "awaiting_mp4_approval"
    if run["tasks"]["script"]["status"] == "complete" and not valid_approval(run, "script"):
        return "awaiting_script_approval"
    return "working"
