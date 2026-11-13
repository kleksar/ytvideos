"""Read-only plans and task cards derived from the authoritative run graph."""

from .workflow import output_kind, required_checks, valid_approval


GOALS = {
    "research": "Проверить источники и выбрать историю с причиной досмотра.",
    "script": "Подготовить и независимо проверить полный текст для принятия пользователем.",
    "storyboard": "Связать принятый текст со сценами, точными ассетами и планом движения.",
    "scene_image": "Получить и проверить точный визуальный материал выданной сцены.",
    "audio": "Подготовить и прослушать полный микс по голосу, скорости и музыке канала.",
    "subtitles": "Связать точный текст с фактическим аудио и подготовить субтитры.",
    "render": "Собрать MP4 из принятых входов по требованиям канала и проверить параметры файла.",
    "review": "Проверить точный MP4 целиком: изображение, движение, звук, субтитры и применимые элементы.",
    "packaging": "Подготовить названия, обложки и metadata параллельно производству.",
    "upload": "Загрузить проверенный файл в подтверждённый канал в разрешённой области.",
    "configure_release": "Настроить выпуск и проверить сохранённые значения на стороне платформы.",
    "schedule": "Применить разрешённое расписание и сверить результат.",
    "verify_publication": "Проверить фактическое состояние выпуска и сохранить результат.",
}
RELEASE_STAGES = {"upload", "configure_release", "schedule", "verify_publication"}


def task_guide(run, task, references=(), requirements=None):
    """Describe one graph node without introducing a second workflow definition."""
    stage = task["stage"]
    goal = GOALS[stage]
    if run.get("source_script_id") and stage in {"research", "script"}:
        goal = ("Проверить факты и источники присланного текста, сохранив выбранный сюжет."
                if stage == "research" else
                "Проверить точный присланный текст; изменение narration требует отдельного принятия версии.")
    speech_mode = (requirements or {}).get("speech", {}).get("mode")
    if stage == "audio" and speech_mode in {"source", "none"}:
        goal = "Собрать и прослушать точный исходный звук/музыку принятого edit-script; TTS не применяется."
    if stage == "subtitles" and speech_mode == "none":
        goal = "Прослушать принятое аудио и сохранить hash-bound no_speech JSON; SRT и слова не придумывать."
    guidance = {
        "goal": goal,
        "skill": {"name": task["skill"], "path": run["skills"][task["skill"]]["path"]},
        "read": list(references),
        "dependencies": list(task["dependencies"]),
        "approval_gates": list(task["gates"]),
        "output_kind": output_kind(stage, requirements),
        "capabilities": list(task["capabilities"]),
        "required_checks": sorted(required_checks(stage, requirements,
                                                  purpose=task.get("payload", {}).get("purpose"))),
        "next_tasks": [item["id"] for item in run["tasks"].values() if task["id"] in item["dependencies"]],
        "execution_order": [
            "Read this task's pinned skill, requirements and exact input artifacts.",
            "Use the current claim and available tools to produce the required artifact.",
            "Measure and inspect the actual output; save evidence for each required check.",
            "Complete with exact artifact and receipt, then request next from the same runtime.",
        ],
        "on_blocker": "Save the real failure or unverified check; continue independent ready tasks. "
                      "Reconcile an unknown provider outcome before retrying.",
        "completion_command": ["complete", "--run", run["id"], "--task", task["id"]],
    }
    if run["profile"]["recipe"] == "licensed_clips" and stage == "script":
        guidance["edit_script"] = {
            "schema": "ytv-edit-script-v1", "speech_modes": ["none", "source", "narration"],
            "instruction": "Use the typed edit-script contract for a licensed edit. Bind its exact spoken words "
                           "and ordered visible segments; use empty speech.text only for an explicitly no-speech edit. "
                           "Do not invent 40 words of narration for an original-sound or silent clip. "
                           "Ordinary full narration remains supported when narration is actually intended.",
        }
    if stage == "script" and requirements is not None:
        from .capabilities import DISCOVERY
        guidance["independent_review"] = {
            "capability": "sessions.independent", "discovery": DISCOVERY["sessions.independent"],
            "evidence": "Use the actual separate reviewer/session result and exact script hash. "
                        "An invented reviewer identity or author role-play does not complete this task.",
        }
        applicability = requirements.get("narrative_loop", "unresolved")
        guidance["narrative_loop"] = {
            "applicability": applicability,
            "action": ("Read the last two and first two utterances in that order, then the opening alone and "
                       "two full cycles. Preserve exact prefix/suffix excerpts and ending + newline + opening; "
                       "an independent reviewer must explain continuous narration, cold-opening clarity and "
                       "the payoff already delivered before replay. Save hash-bound ytv-narrative-loop-v1 evidence. "
                       "A thematic callback or a JSON verdict is not proof of a continuous narrative seam."
                       if applicability == "required" else
                       "Do not invent narration to create a loop; use the recipe's applicable audiovisual check."
                       if applicability == "not_applicable" else
                       "Resolve the pinned short narrative-loop policy before completing this script."),
            "source_script": ("Keep the supplied source artifact intact. If its seam fails, retain the diagnosis "
                              "and present a separate proposed correction through the existing revision/acceptance flow; "
                              "do not silently rewrite or approve the provided script."),
        }
    return guidance


def supporting_inputs(run, task):
    """Include accepted ancestors needed by a fresh reviewer or subtitle worker.

    Artifact descriptors are small. The artifacts remain in the shared store;
    this does not copy scripts/media or create new scheduling dependencies.
    """
    direct = set(task["dependencies"])
    seen, result = set(), []

    def visit(task_id):
        if task_id in seen:
            return
        seen.add(task_id)
        ancestor = run["tasks"][task_id]
        for dependency in ancestor["dependencies"]:
            visit(dependency)
        if task_id not in direct and ancestor["status"] == "complete" and ancestor["outputs"]:
            result.append({"task_id": task_id,
                           "artifacts": [run["artifacts"][key] for key in ancestor["outputs"]]})

    for task_id in task["dependencies"]:
        visit(task_id)
    return result


def run_plan(run, next_state, requirements, *, code_matches_pin, capable):
    """Project saved state into a bounded plan. Never call a provider or mutate it."""
    routes = run.get("reference_snapshot", {}).get("routes", {})
    steps, release_steps, gaps = [], [], {}
    for task in run["tasks"].values():
        route = "thumbnail" if task["stage"] == "scene_image" and task.get("payload", {}).get("purpose") == "thumbnail" else task["stage"]
        item = {"id": task["id"], "stage": task["stage"], "status": task["status"],
                **task_guide(run, task, routes.get(route, []), requirements)}
        item["blocker"] = task.get("blocker")
        (release_steps if task["stage"] in RELEASE_STAGES else steps).append(item)
        if task["stage"] not in RELEASE_STAGES and task["status"] not in {"complete", "cancelled"}:
            for name in task["capabilities"]:
                if not capable(run, name):
                    gaps.setdefault(name, []).append(task["id"])
    # Scene nodes appear only after storyboard; disclose their capability early.
    if run["tasks"]["storyboard"]["status"] != "complete":
        name = "image.generate" if run["profile"]["recipe"] == "illustrated" else "media.licensed_clip"
        if not capable(run, name):
            gaps.setdefault(name, []).append("scene_image")
    code_problem = None if code_matches_pin else "Use the pinned checkout or explicitly migrate this run before execution."
    return {
        "schema_version": 1, "run_id": run["id"], "intent": run["intent"],
        "channel": {key: run["profile"][key] for key in ("id", "name", "language", "recipe", "status")},
        "format": run["format"], "revision": run["revision"], "pins": run["pins"],
        "production_requirements": requirements,
        "source_script": run["artifacts"].get(run.get("source_script_id")),
        "target": {"artifact": "mp4", "ready_after": "review", "plan_is_approval": False,
                   "publication_requires": "explicit user instruction"},
        "accepted": {"script": valid_approval(run, "script"), "mp4": valid_approval(run, "mp4")},
        "steps": steps, "release_steps": release_steps, "next": next_state,
        "capability_gaps": [{"capability": name, "tasks": ids, "observation": run["capabilities"].get(name),
                             "action": "Verify in the actual runtime and record evidence; an absent observation is not proof of unavailability."}
                            for name, ids in sorted(gaps.items())],
        "runtime": {"code_matches_pin": code_matches_pin, "blocker": code_problem,
                    "capabilities_source": "saved observations; run doctor to inspect the current environment"},
        "commands": {name: [name, "--run", run["id"]] for name in ("doctor", "status", "next", "plan")},
        "commands_note": "Subcommands use the same database, workspace and project-root as this invocation.",
        "first_response": "Before generation, briefly tell the user the channel/format, applicable production "
                          "requirements, the next steps and genuine blockers. Continue authorized work without "
                          "asking the user to approve this plan.",
    }
