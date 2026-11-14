"""Concrete local media execution using the same authoritative run/task guards.

This executor runs existing CLIs. It never claims creative review or marks the
audio/montage stage complete merely because a subprocess produced a file.
"""
import json
from pathlib import Path
import uuid

from .adapters.media import LocalMediaAdapter
from .errors import Conflict, WorkflowError
from .media_script import accepted_script
from .profiles import load_profile
from .production_contract import DELIVERY_SCHEMA, validate_render_manifest
from .util import canonical, digest, file_digest
from .workflow import valid_approval


def validate_helper_profile(production, current, pinned_hash):
    """Permit a changed on-disk profile only with its exact migration receipt."""
    if digest(current["profile"]) != current["pins"]["profile"] or current["pins"]["profile"] != pinned_hash:
        raise Conflict("saved profile changed before media dispatch")
    if digest(load_profile(production.project / "channels", current["channel"])) == pinned_hash:
        return
    from .migration import _target_context
    _, _, compatibility = _target_context(production, current)
    history = current.get("runtime_migrations", [])
    if not history or compatibility is None:
        raise Conflict("montage helper channel profile changed; use the pinned checkout")
    artifact = current["artifacts"][history[-1]["receipt_artifact_id"]]
    migrated = json.loads(production.artifacts.resolve(artifact).read_text())
    if (migrated.get("target", {}).get("pins") != current["pins"] or
            migrated.get("target", {}).get("profile_compatibility") != compatibility):
        raise Conflict("profile difference lacks matching migration receipt")


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
        requirements = production.requirements(run) if kind in {"montage", "music_render"} else None
        allowed = {"audio": {"tts", "mix"}, "subtitles": {"srt"}, "render": {"montage", "music_render"}, "review": {"inspect"}}
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
        script_content = accepted_script(run, production.artifacts)
        if kind == "tts":
            if script_content["mode"] != "narration":
                raise WorkflowError("accepted source/no-speech edits use source audio mixing, never TTS")
            if set(request) - {"kind", "timeout"}:
                raise WorkflowError("TTS arguments are derived from the accepted script/channel, not caller overrides")
            language = run["profile"]["language"]
            if language not in {"en", "ru"}:
                raise WorkflowError("the existing TTS CLI needs a language adapter for this profile")
            script = production._artifact(run, "script")
            narration_path = production.artifacts.resolve(script)
            if script_content["kind"] == "edit_script":
                narration_path = attempt / "accepted-narration.txt"
                narration_path.write_text(script_content["text"], encoding="utf-8")
                inputs.append({"path": str(narration_path), "sha256": file_digest(narration_path)})
            output_dir = attempt / "voice"
            args = [f"--{language}-text", str(narration_path), "--channel", run["channel"],
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
            if kind == "srt" and script_content["mode"] == "none":
                raise WorkflowError("a no-speech edit produces its bound no_speech result, not an SRT")
            if kind == "mix":
                if script_content["mode"] not in {"source", "none"}:
                    raise WorkflowError("source audio mixing is for accepted source/no-speech edit scripts")
                if len(args) != 3 or args[1] != "--output":
                    raise WorkflowError("source audio mixing requires MANIFEST --output OWNED_WAV")
                manifest = Path(args[0]).resolve()
                destination = Path(args[2]).resolve()
                if (str(manifest) not in {item["path"] for item in inputs} or destination not in outputs
                        or len(outputs) != 1):
                    raise WorkflowError("source audio manifest and output must be bound to this attempt")
                import importlib.util
                spec = importlib.util.spec_from_file_location("ytv_source_audio", production.project / "automation/audio_mix.py")
                helper = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(helper)
                segments = helper.validate_plan(json.loads(manifest.read_text()), manifest.parent)
                if [item["id"] for item in segments] != script_content["segment_ids"]:
                    raise WorkflowError("source audio must preserve the accepted edit segment order")
                registered = {artifact["sha256"] for artifact in run["artifacts"].values()}
                for segment in segments:
                    if segment["sha256"] not in registered:
                        raise WorkflowError("register source audio artifacts before mixing")
                    inputs.append({"path": str(segment["path"]), "sha256": segment["sha256"]})
                args = [str(manifest), "--output", str(destination)]
            if kind == "music_render":
                from .music_contract import file_record, validate_plan
                if run["profile"]["recipe"] != "music_first":
                    raise WorkflowError("music_render belongs to the registered music-first recipe")
                if len(args) != 3 or args[1] != "--output" or len(outputs) != 1:
                    raise WorkflowError("music_render requires MANIFEST --output OWNED_MP4; settings come from the pinned profile")
                manifest, destination = Path(args[0]).resolve(), Path(args[2]).resolve()
                if str(manifest) not in {item["path"] for item in inputs} or destination not in outputs:
                    raise WorkflowError("music manifest and output must be bound to this attempt")
                plan = json.loads(manifest.read_text())
                if file_digest(plan["audio"]) != production._artifact(run, "audio")["sha256"]:
                    raise Conflict("music render differs from the accepted exact audio")
                if [file_digest(scene["clip"]) for scene in plan["scenes"]] != [
                        item["sha256"] for item in production.render_sources(run, task)]:
                    raise Conflict("music render must preserve accepted scene order and multiplicity")
                prepared = validate_plan(plan, requirements, base=manifest.parent, project=production.project, script=script_content)
                if prepared["requires_srt"] and file_digest(plan["srt"]) != production._artifact(run, "subtitles")["sha256"]:
                    raise Conflict("music render SRT differs from the accepted subtitles")
                inputs.extend(prepared["inputs"])
                inputs.extend(production.music_inputs(run, task, plan))
                requirement_path = attempt / ("music-requirements-" + requirements["sha256"] + ".json")
                if not requirement_path.exists():
                    with requirement_path.open("x") as stream:
                        stream.write(canonical(requirements) + "\n")
                if json.loads(requirement_path.read_text()) != requirements:
                    raise Conflict("owned music requirements changed before execution")
                inputs.append(file_record(requirement_path))
                args = [str(manifest), "--output", str(destination), "--work-dir", str(attempt / "music-work"),
                        "--requirements", str(requirement_path)]
            if kind == "montage":
                if run["profile"]["recipe"] != "illustrated":
                    raise WorkflowError("the montage adapter renders illustrated scenes; licensed clips need a bound host_render execution")
                if "--technical-probe" in args:
                    raise WorkflowError("a technical probe is not a production render task")
                if not args or args[0].startswith("-"):
                    raise WorkflowError("montage requires a frozen input manifest")
                manifest = Path(args[0]).resolve()
                args = [str(manifest), *args[1:]]
                if str(manifest) not in {item["path"] for item in inputs}:
                    raise WorkflowError("montage manifest must be a bound prepared input")
                plan = json.loads(manifest.read_text())
                validate_render_manifest(plan, requirements)
                def manifest_file(value):
                    path = Path(value)
                    return path.resolve() if path.is_absolute() else (manifest.parent / path).resolve()
                expected_audio = production._artifact(run, "audio")["sha256"]
                actual_audio = manifest_file(plan["audio"])
                if file_digest(actual_audio) != expected_audio:
                    raise Conflict("montage audio differs from the accepted audio task")
                expected_images = [artifact["sha256"] for artifact in production.render_sources(run, task)]
                actual_images = [manifest_file(scene["image"]) for scene in plan["scenes"]]
                if [file_digest(path) for path in actual_images] != expected_images:
                    raise Conflict("montage must preserve accepted scene order and multiplicity")
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
                args[args.index("--output") + 1] = str(Path(args[args.index("--output") + 1]).resolve())
                if "--export-contract" not in args:
                    raise WorkflowError("montage requires the validated export passport")
                export_path = manifest_file(args[args.index("--export-contract") + 1])
                args[args.index("--export-contract") + 1] = str(export_path)
                additional = [export_path]
                if plan.get("srt"):
                    srt_path = manifest_file(plan["srt"])
                    if file_digest(srt_path) != production._artifact(run, "subtitles")["sha256"]:
                        raise Conflict("montage SRT differs from the accepted manual subtitles")
                    additional.append(srt_path)
                for layer in plan.get("overlays", []):
                    path = manifest_file(layer["path"])
                    if file_digest(path) != layer["sha256"]:
                        raise Conflict("overlay source differs from the declared asset")
                    additional.append(path)
                music = plan.get("music", {})
                if music.get("status") == "present":
                    for track in music["tracks"]:
                        path = manifest_file(track["path"])
                        if file_digest(path) != track["sha256"]:
                            raise Conflict("music source differs from the declared track")
                        additional.append(path)
                    mix_path = Path(music["mix_evidence"]["path"]).resolve()
                    if file_digest(mix_path) != music["mix_evidence"]["sha256"]:
                        raise Conflict("music mix execution evidence changed")
                    additional.append(mix_path)
                inputs.extend({"path": str(path), "sha256": file_digest(path)} for path in additional)
        if kind in {"montage", "music_render"}:
            if any(arg in {"--pinned-profile", "--pinned-profile-sha256"} or
                   arg.startswith("--pinned-profile=") or arg.startswith("--pinned-profile-sha256=") for arg in args):
                raise WorkflowError("pinned profile is derived from the saved run, not caller arguments")
            pinned_hash = run["pins"]["profile"]
            if digest(run["profile"]) != pinned_hash:
                raise Conflict("saved channel profile differs from its pin")
            pinned_path = attempt / ("pinned-profile-" + pinned_hash + ".json")
            if not pinned_path.exists():
                with pinned_path.open("x", encoding="utf-8") as stream:
                    stream.write(canonical(run["profile"]))
            if file_digest(pinned_path) != pinned_hash:
                raise Conflict("owned pinned profile bytes changed")
            inputs.append({"path": str(pinned_path), "sha256": pinned_hash})
            args += ["--pinned-profile", str(pinned_path), "--pinned-profile-sha256", pinned_hash]
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
                if observed_request["kind"] in {"montage", "music_render"}:
                    validate_helper_profile(production, current, pinned_hash)
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
        delivery_evidence = None
        mix_evidence = None
        if kind == "mix" and result["state"] == "completed":
            from .music_contract import MIX_SCHEMA, file_record
            summary = {"schema": MIX_SCHEMA, "audio_sha256": file_digest(outputs[0]),
                       "track_sha256": sorted({segment["sha256"] for segment in segments}),
                       "returncode": result["returncode"], "argv": result["argv"],
                       "execution": file_record(receipt), "source_plan": file_record(manifest)}
            summary_path = attempt / ("mix-evidence-" + digest(summary)[:16] + ".json")
            with summary_path.open("x") as stream:
                stream.write(canonical(summary) + "\n")
            mix_evidence = file_record(summary_path)
        if kind in {"montage", "music_render"} and result["state"] == "completed" and not any(
                mode in args for mode in ("--plan-only", "--prepare-subtitles", "--check-settings")):
            output_path = Path(args[args.index("--output") + 1]).resolve()
            canonical_receipt = Path(str(output_path) + ".delivery.json")
            if not canonical_receipt.is_file():
                raise WorkflowError("renderer did not preserve the canonical caption/delivery receipt")
            proof = {"schema": DELIVERY_SCHEMA, "media_sha256": file_digest(output_path),
                     "requirements_sha256": requirements["sha256"],
                     "manifest": {"path": str(manifest), "sha256": file_digest(manifest)},
                     "execution": {"path": str(receipt), "sha256": file_digest(receipt)},
                     "renderer_receipt": {"path": str(canonical_receipt), "sha256": file_digest(canonical_receipt)}}
            proof_path = attempt / ("delivery-" + digest(proof)[:16] + ".json")
            with proof_path.open("x") as output:
                output.write(canonical(proof) + "\n")
            delivery_evidence = {"path": str(proof_path), "sha256": file_digest(proof_path)}
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
        return {"execution": result, "receipt": str(receipt), "delivery_evidence": delivery_evidence,
                "mix_evidence": mix_evidence,
                "audio_processing": {"raw_tts_speed": 1.0, "target_master_speed": run["profile"].get("voice", {}).get("speed"),
                                     "final_speed_processing_performed": False} if kind == "tts" else None,
                "next": "Complete mixing/content QA and required checks; subprocess success is not stage completion."}
