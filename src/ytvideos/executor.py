"""Concrete local media execution using the same authoritative run/task guards.

This executor runs existing CLIs. It never claims creative review or marks the
audio/montage stage complete merely because a subprocess produced a file.
"""
import json
from pathlib import Path
import uuid

from .adapters.media import LocalMediaAdapter
from .errors import Conflict, WorkflowError
from .profiles import load_profile
from .util import canonical, digest, file_digest
from .workflow import valid_approval


class MediaExecutor:
    def __init__(self, production, *, runner=None):
        self.production = production
        self.runner = runner

    def execute(self, run_id, task_id, token, request):
        production = self.production
        run = production.store.get(run_id)
        task = production._task(run, task_id)
        claim = production._current_claim(run, task, token)
        kind = request["kind"]
        allowed = {"audio": {"tts"}, "subtitles": {"srt"}, "render": {"montage"}, "review": {"inspect"}}
        if kind not in allowed.get(task["stage"], set()):
            raise WorkflowError("media command does not belong to the claimed task")
        if not valid_approval(run, "script"):
            raise WorkflowError("media execution requires the accepted exact script")
        attempt = production.workspace / "runs" / run_id / "attempts" / token
        attempt.mkdir(parents=True, exist_ok=True)
        artifacts = [run["artifacts"][key] for dependency in task["dependencies"]
                     for key in run["tasks"][dependency]["outputs"]]
        inputs = [{"path": str(production.artifacts.resolve(artifact)), "sha256": artifact["sha256"]}
                  for artifact in artifacts]
        if kind == "tts":
            if set(request) - {"kind", "timeout"}:
                raise WorkflowError("TTS arguments are derived from the accepted script/channel, not caller overrides")
            language = run["profile"]["language"]
            if language not in {"en", "ru"}:
                raise WorkflowError("the existing TTS CLI needs a language adapter for this profile")
            script = production._artifact(run, "script")
            output_dir = attempt / "voice"
            args = [f"--{language}-text", str(production.artifacts.resolve(script)), "--channel", run["channel"],
                    "--voice-id", run["profile"]["voice"]["id"], "--speed", "1.0",
                    "--output-dir", str(output_dir), "--generate"]
            outputs = [output_dir / f"voice_{language}.mp3"]
        else:
            # Manifest/contract files are supplied by the claimed task. Freeze them
            # before execution and bind their actual bytes into the adapter receipt.
            args = request.get("args")
            if not isinstance(args, list) or not all(isinstance(x, str) for x in args):
                raise WorkflowError("args must be an argv list")
            outputs = [Path(path).resolve() for path in request.get("outputs", [])]
            if not outputs or any(not path.is_relative_to(attempt) for path in outputs):
                raise WorkflowError("all new outputs must be inside this task's owned attempt directory")
            for path in request.get("prepared_inputs", []):
                artifact = production.artifacts.put(path, "prepared_media_input")
                # Keep the original relative-manifest location; hash it before/after.
                inputs.append({"path": str(Path(path).resolve()), "sha256": artifact["sha256"]})
            if kind == "montage":
                if not args or args[0].startswith("-"):
                    raise WorkflowError("montage requires a frozen input manifest")
                manifest = Path(args[0]).resolve()
                if str(manifest) not in {item["path"] for item in inputs}:
                    raise WorkflowError("montage manifest must be a bound prepared input")
                plan = json.loads(manifest.read_text())
                if plan.get("channel") != run["channel"]:
                    raise WorkflowError("montage manifest uses another channel")
                def manifest_file(value):
                    path = Path(value)
                    return path.resolve() if path.is_absolute() else (manifest.parent / path).resolve()
                expected_audio = production._artifact(run, "audio")["sha256"]
                actual_audio = manifest_file(plan["audio"])
                if file_digest(actual_audio) != expected_audio:
                    raise Conflict("montage audio differs from the accepted audio task")
                expected_images = {run["artifacts"][artifact_id]["sha256"]
                                   for dependency in task["dependencies"] if dependency.startswith("image:")
                                   for artifact_id in run["tasks"][dependency]["outputs"]}
                actual_images = [manifest_file(scene["image"]) for scene in plan["scenes"]]
                if {file_digest(path) for path in actual_images} != expected_images:
                    raise Conflict("montage scenes differ from the accepted scene artifacts")
                inputs += [{"path": str(path), "sha256": file_digest(path)}
                           for path in [actual_audio, *actual_images]]
                # The existing delivery engine checks word-map text/audio binding,
                # exact fonts, overlays, timings and passport before encoding.
                sub = plan.get("subtitles", {})
                if sub.get("mode") == "words":
                    for name in ("words", "transcript", "review"):
                        if sub.get(name):
                            path = manifest_file(sub[name])
                            inputs.append({"path": str(path), "sha256": file_digest(path)})
                    words = json.loads(manifest_file(sub["words"]).read_text())
                    if not isinstance(words, dict) or words.get("audio_sha256") != expected_audio:
                        raise Conflict("subtitle word map is not bound to accepted audio")
                    if sub.get("transcript") and file_digest(manifest_file(sub["transcript"])) != production._artifact(run, "script")["sha256"]:
                        raise Conflict("subtitle transcript differs from the accepted narration")
                if "--output" not in args or Path(args[args.index("--output") + 1]).resolve() not in outputs:
                    raise WorkflowError("montage output does not match the owned output contract")
                if "--export-contract" not in args:
                    raise WorkflowError("montage requires the validated export passport")
        receipt = attempt / f"{kind}-{digest(args)[:16]}.json"
        operation = None

        def guard(observed_request):
            nonlocal operation
            def validate(tx, current):
                nonlocal operation
                production._runtime(current)
                current_task = production._task(current, task_id)
                production._current_claim(current, current_task, token)
                if not valid_approval(current, "script"):
                    raise Conflict("script approval changed before execution")
                if observed_request["kind"] == "montage" and digest(load_profile(production.project / "channels", current["channel"])) != current["pins"]["profile"]:
                    raise Conflict("montage helper channel profile changed; use the pinned checkout")
                if observed_request["kind"] == "tts":
                    payload = production._operation_payload(current, current_task, "tts")
                    operation = production._begin_operation_tx(tx, current, task_id, token, "tts", payload)
                tx.event(str(uuid.uuid4()), run_id, "media.dispatch", observed_request)
            production.store.mutate(run_id, validate)

        kwargs = {"guard": guard, "clock": production.clock}
        if self.runner is not None:
            kwargs["runner"] = self.runner
        adapter = LocalMediaAdapter(production.project, **kwargs)
        result = adapter.execute(kind, args, run_id=run_id, task_id=task_id, claim=claim,
                                 input_hash=claim["input_hash"], inputs=inputs, outputs=outputs,
                                 receipt_path=receipt, timeout=request.get("timeout", 900))
        if operation:
            status = "confirmed" if result["state"] == "completed" else "unknown"
            observation = {"operation_key": operation["key"], "attempt_id": operation["attempt_id"],
                           "task_input_hash": operation["task_input_hash"], "status": status,
                           "provider_evidence": {"method": "adapter_execution", "observation_id": str(receipt),
                                                 "observed": {"receipt_sha256": file_digest(receipt),
                                                              "state": result["state"],
                                                              "output_artifacts": result["output_artifacts"]}}}
            observed_path = attempt / f"{kind}-observation.json"
            observed_path.write_text(canonical(observation) + "\n")
            production.observe_operation(run_id, operation["key"], status, observed_path,
                                         event_id=f"media:{operation['attempt_id']}")
        return {"execution": result, "receipt": str(receipt),
                "audio_processing": {"raw_tts_speed": 1.0, "target_master_speed": run["profile"].get("voice", {}).get("speed"),
                                     "final_speed_processing_performed": False} if kind == "tts" else None,
                "next": "Complete mixing/content QA and required checks; subprocess success is not stage completion."}
