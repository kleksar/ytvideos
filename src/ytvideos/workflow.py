"""Pure dependency graph. Preparation and human publication authority are separate."""

from .util import digest


WORKFLOW_VERSION = "1"
STAGES = {
    "research": ([], [], ["web.search"], "ytv-write-script"),
    "script": (["research"], [], ["model.text", "sessions.independent"], "ytv-write-script"),
    "storyboard": (["script"], ["script"], ["model.text"], "ytv-produce-video"),
    "audio": (["script"], ["script"], ["audio.produce", "audio.listen"], "ytv-produce-video"),
    "packaging": (["script"], ["script"], ["model.text"], "ytv-release-video"),
    "subtitles": (["audio"], ["script"], ["subtitle.align"], "ytv-produce-video"),
    "render": (["storyboard", "audio", "subtitles"], ["script"], ["video.render"], "ytv-produce-video"),
    "review": (["render"], ["script"], ["video.inspect", "audio.listen", "model.vision"], "ytv-review-video"),
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


def execution_capabilities(task):
    """Production can precede listening; final review still requires real audio QA.

    Keep stored capabilities intact for compatible pinned-run migration and for
    plan/doctor visibility of the outstanding completion requirement.
    """
    return [name for name in task["capabilities"]
            if not (task["stage"] in {"audio", "subtitles"} and name == "audio.listen")]


def required_checks(stage, requirements=None, *, purpose=None):
    """One completion contract for task packets, plans and the receipt validator."""
    checks = set(REQUIRED_CHECKS[stage])
    if stage == "review" and requirements is not None:
        checks.update(requirements["review_checks"])
    if stage == "script" and requirements is not None and requirements.get("narrative_loop") == "required":
        checks.add("narrative_loop")
    if stage == "scene_image" and purpose == "thumbnail":
        checks.add("thumbnail_review")
    speech_mode = (requirements or {}).get("speech", {}).get("mode", (requirements or {}).get("speech_mode"))
    if stage == "audio" and "music_edit" in (requirements or {}) and speech_mode is None:
        checks = {"source_identity", "listening", "excerpt_mode"}
    if stage == "audio" and speech_mode in {"source", "none"}:
        checks = {"source_identity", "listening", "exact_text" if speech_mode == "source" else "no_speech"}
    if stage == "subtitles" and speech_mode == "none":
        checks = {"no_speech"}
    if stage == "review" and speech_mode == "none":
        checks.difference_update({"subtitles", "captions"})
        checks.add("no_speech")
    return checks


def output_kind(stage, requirements=None):
    if stage == "subtitles" and (requirements or {}).get("speech", {}).get("mode") == "none":
        return "no_speech"
    return OUTPUT_KINDS[stage]


def configure_speech_tasks(run, mode):
    """Keep the pending graph aligned with the accepted content, including revisions."""
    if mode is None and run["profile"]["recipe"] == "music_first":
        run["tasks"]["audio"]["capabilities"] = ["audio.mix", "audio.listen"]
        run["tasks"]["subtitles"]["capabilities"] = ["audio.listen"]
        return
    run["tasks"]["audio"]["capabilities"] = [
        "audio.mix" if mode in {"source", "none"} else "audio.produce", "audio.listen"]
    run["tasks"]["subtitles"]["capabilities"] = ["audio.listen" if mode == "none" else "subtitle.align"]


def task_references(task):
    """Compatibility entry for callers needing only stage-level standards."""
    from .context import task_references as select
    return select(task)


def new_tasks(recipe=None):
    tasks = {stage: make_task(stage, stage, deps, gates, capabilities, skill)
             for stage, (deps, gates, capabilities, skill) in STAGES.items()}
    if recipe == "music_first":
        tasks["audio"]["capabilities"] = ["audio.mix", "audio.listen"]
        # Vocal alignment becomes required only after that variant is accepted.
        tasks["subtitles"]["capabilities"] = ["audio.listen"]
    return tasks


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
