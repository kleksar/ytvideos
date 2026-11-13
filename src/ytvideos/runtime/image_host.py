"""Run the native image outbox on a deliberately configured App Server host.

Only image dispatch is automated here. Native completion never supplies artistic
QA, user approvals or publication authority. A restarted host READS existing
threads; it never replays thread/start or turn/start from an uncertain journal.
"""
from __future__ import annotations

import argparse
import base64
import json
import os
from pathlib import Path
import shutil
import tempfile
import time

from ..context import validate_documents
from ..errors import Conflict, WorkflowError
from ..pool_service import PoolService
from ..service import Production
from ..store import Store
from ..util import canonical, digest, file_digest
from ..workflow import input_hash
from .app_server import AppServer, ImageNotSent, RpcUnavailable, StdioRpc


class ImageHost:
    def __init__(self, production, server, config):
        self.production, self.store, self.server = production, production.store, server
        self.config = dict(config)
        self._transport_failed = False
        for name in ("host_id", "runtime_key", "model", "work_root"):
            if not isinstance(config.get(name), str) or not config[name].strip():
                raise WorkflowError(f"host configuration requires {name}")
        channels = config.get("channels")
        if (not isinstance(channels, list) or not channels
                or any(not isinstance(x, str) or not x for x in channels)):
            raise WorkflowError("host configuration requires an explicit channel allowlist")
        if type(config.get("estimated_units", 0)) is not int or config.get("estimated_units", 0) < 0:
            raise WorkflowError("estimated_units must be nonnegative")
        if server.model != config["model"]:
            raise WorkflowError("server model differs from the configured model")
        self.root = Path(config["work_root"]).resolve()
        for protected in (production.project, production.workspace):
            if self.root.is_relative_to(protected) or protected.is_relative_to(self.root):
                raise WorkflowError("worker workspace must be separate from code and production state")
        self.root.mkdir(parents=True, exist_ok=True)
        self.pools = PoolService(production)
        with self.store.transaction() as tx:
            tx.execute("CREATE TABLE IF NOT EXISTS image_host_jobs "
                       "(id TEXT PRIMARY KEY, host_id TEXT NOT NULL, version INTEGER NOT NULL, doc TEXT NOT NULL)")

    def _jobs(self):
        with self.store.transaction() as tx:
            return [json.loads(row[0]) for row in tx.execute(
                "SELECT doc FROM image_host_jobs WHERE host_id=? ORDER BY id", (self.config["host_id"],)).fetchall()]

    def _save(self, job, *, create=False):
        with self.store.transaction() as tx:
            if create:
                cursor = tx.execute("INSERT INTO image_host_jobs VALUES (?,?,?,?) ON CONFLICT(id) DO NOTHING",
                                    (job["id"], self.config["host_id"], job["version"], canonical(job)))
                if cursor.rowcount != 1:
                    raise Conflict("native dispatch journal already exists; reconcile instead of sending")
            else:
                updated = {**job, "version": job["version"] + 1}
                cursor = tx.execute("UPDATE image_host_jobs SET doc=?,version=? WHERE id=? AND host_id=? AND version=?",
                                    (canonical(updated), updated["version"], job["id"], self.config["host_id"], job["version"]))
                if cursor.rowcount != 1:
                    raise Conflict("native dispatch journal changed; reload before recording an observation")
                job.update(updated)

    def _materialize(self, run, request):
        self.pools.validate_packet(run, request)
        packet = request["packet"]
        context = json.loads(canonical(packet["context"]))
        if digest(context) != packet["input_hash"]:
            raise WorkflowError("native packet hash does not match its content")
        if "reference_documents" not in context:
            # Older outbox packets predate document snapshots. Use only their
            # verified pinned checkout, and label that boundary in TASK.json.
            task = self.production._task(run, context["task_id"])
            context.update(self.production._reference_context(run, task))
        documents = validate_documents(context["references"], context["reference_documents"])
        # ChannelSpec owns document selection; some channels use AGENTS.md and
        # recipes instead of PROFILE.md. Require their pinned channel context,
        # without introducing a second filename-based selector in the worker.
        channel_prefix = f"channels/{run['channel']}/"
        if not any(path.startswith(channel_prefix) for path in context["references"]):
            raise WorkflowError("missing pinned production requirement: channel document")
        directory = self.root / digest({"run": run["id"], "operation": request["operation_id"]})
        if directory.exists():
            raise Conflict("worker directory already exists; inspect it instead of reusing another context")
        artifacts = list(context["inputs"])
        references = context.get("scene", {}).get("references", [])
        if not isinstance(references, list):
            raise WorkflowError("scene references must be registered artifact IDs")
        reason = context.get("scene", {}).get("reference_na_reason")
        if not references and (not isinstance(reason, str) or not reason.strip()):
            raise WorkflowError("resolve the scene's visual references or explain why none are needed")
        for reference in references:
            key = reference.get("artifact_id") if isinstance(reference, dict) else reference
            if not isinstance(key, str) or key not in run["artifacts"]:
                raise WorkflowError("register every required scene reference before native dispatch")
            artifacts.append(run["artifacts"][key])
        staging = Path(tempfile.mkdtemp(prefix=".prepare-", dir=self.root))
        try:
            context["local_inputs"] = []
            files = {}
            for index, artifact in enumerate(artifacts):
                source = self.production.artifacts.resolve(artifact)
                extension = Path(artifact["filename"]).suffix
                if extension.lower() not in {".png", ".jpg", ".jpeg", ".webp", ".txt", ".json", ".md"}:
                    extension = ".bin"
                name = f"input-{index}{extension}"
                shutil.copyfile(source, staging / name)
                if file_digest(staging / name) != artifact["sha256"]:
                    raise WorkflowError("input changed while preparing native task")
                files[name] = artifact["sha256"]
                context["local_inputs"].append({"artifact_id": artifact["id"], "path": name,
                                                "sha256": artifact["sha256"]})
            context["requirements"] = []
            context["reference_manifest"] = []
            for document in documents:
                name = "requirements/" + document["path"]
                destination = staging / name
                destination.parent.mkdir(parents=True, exist_ok=True)
                destination.write_bytes(document["text"].encode("utf-8"))
                files[name] = document["sha256"]
                context["requirements"].append(name)
                context["reference_manifest"].append({"path": document["path"], "sha256": document["sha256"],
                                                      "local_path": name})
            # The immutable packet keeps the texts; the worker reads each local
            # requirement once instead of receiving a second copy in TASK.json.
            del context["reference_documents"]
            (staging / "TASK.json").write_text(canonical(context) + "\n")
            (staging / "SKILL.md").write_text(context["skill"]["text"])
            for name in ("TASK.json", "SKILL.md"):
                files[name] = file_digest(staging / name)
            staging.rename(directory)
            return directory, files
        finally:
            if staging.exists():
                shutil.rmtree(staging)

    def _block_unsent(self, candidate, reason):
        """Quarantine only an unchanged, unclaimed outbox packet before any send.

        Bump its generation so PoolService retires the old unsent local slot on
        the next tick. Existing unblock/revise can resume after the input is fixed.
        Never use this path for a claimed or potentially dispatched generation.
        """
        def change(tx, run):
            self.production._runtime(run)
            request = run["pool"]["backend"]["requests"][candidate["operation_id"]]
            binding = run["pool"]["bindings"][request["packet"]["job_id"]]
            task = self.production._task(run, binding["task_id"])
            if (request["status"] != "queued" or task["status"] != "pending" or task.get("claim")
                    or binding.get("operation_key") or input_hash(run, task) != binding["task_input_hash"]):
                raise Conflict("preflight packet changed; do not block another attempt")
            task.update(status="blocked", blocker=reason, generation=task["generation"] + 1)
            tx.event("image-host-preflight:" + candidate["operation_id"], run["id"],
                     "task.preflight_blocked", {"task_id": task["id"], "reason": reason})
        self.store.mutate(candidate["run_id"], change)

    def dispatch(self, candidate):
        run_id = candidate["run_id"]
        run = self.store.get(run_id)
        if (run["channel"] not in self.config["channels"] or run["profile"]["status"] != "active"
                or run["pool"]["runtime_key"] != self.config["runtime_key"]):
            raise WorkflowError("run is outside this host's verified scope")
        self.production._runtime(run)
        status = self.pools.operate(run_id, "status")
        if status["review"]["capacity"] is None:
            raise WorkflowError("configure the shared coordinator review limit before native dispatch")
        request = run["pool"]["backend"]["requests"][candidate["operation_id"]]
        try:
            directory, files = self._materialize(run, request)
        except Conflict:
            raise  # Existing directories/changed packets require inspection.
        except (WorkflowError, OSError, ValueError) as exc:
            reason = str(exc) if isinstance(exc, WorkflowError) else "native task input preparation failed"
            self._block_unsent(candidate, reason)
            raise
        try:
            grant = self.pools.operate(run_id, "claim", {
                "operation_id": request["operation_id"], "worker": self.config["host_id"],
                "estimated_units": self.config.get("estimated_units", 0)})
        except BaseException:
            shutil.rmtree(directory)  # This call created it; no native call has run.
            raise
        request = grant["request"]
        job = {"id": request["operation_id"], "run_id": run_id, "runtime_key": self.config["runtime_key"],
               "model": self.server.model, "directory": str(directory), "inputs": files, "version": 0,
               "prompt": self.server.image_prompt(request["operation_id"]),
               "claim_token": request["claim_token"], "task_id": candidate["task_id"],
               "task_token": grant["task_claim"]["token"], "state": "thread_starting",
               "thread_id": None, "turn_id": None, "observation": None,
               "included": run["capabilities"]["image.generate"].get("billing") == "included"}
        self._save(job, create=True)
        # Committed journal and workflow intent precede every native mutation.
        # On any exception leave them intact. Never send again from recovery.
        started = time.monotonic()
        job["thread_id"] = self.server.start_thread(directory)
        job["state"] = "thread_created"
        self._save(job)
        def before_send():
            self._verify_inputs(job)
            fresh = self.store.get(run_id)
            self.production._runtime(fresh)
            self.production._current_claim(fresh, fresh["tasks"][job["task_id"]], job["task_token"])
            job["state"] = "turn_dispatching"
            self._save(job)
            self.pools.operate(run_id, "submitted", {
                "operation_id": job["id"], "claim_token": job["claim_token"], "reconnectable": True,
                "provider": {"tool": "codex.app-server", "session_id": job["thread_id"]}})
        try:
            job["turn_id"] = self.server.start_image(job["thread_id"], directory, job["prompt"],
                                                     before_send=before_send)
        except ImageNotSent as exc:
            # Only the current dispatch stack can prove it never invoked
            # turn/start. Recovery must not infer this from an old state label.
            job["observation"] = {
                "operation_id": job["id"], "claim_token": job["claim_token"],
                "receipt_id": "app-server:not-sent:" + job["id"], "status": "failed",
                "actual_units": 0, "detail": str(exc),
                "evidence": {"tool": "codex.app-server", "session_id": job["thread_id"],
                             "method": "host_preflight_no_dispatch", "turn_start_sent": False}}
            job["state"] = "observed"
            self._save(job)
            self.poll(job)
            if isinstance(exc.__cause__, RpcUnavailable):
                self._transport_failed = True
            return {"operation_id": job["id"], "status": "not_sent", "reason": str(exc)}
        job["state"] = "running"
        self._save(job)
        self.pools.operate(run_id, "submitted", {
            "operation_id": job["id"], "claim_token": job["claim_token"], "reconnectable": True,
            "provider": {"tool": "codex.app-server", "session_id": job["thread_id"]},
            "dispatch_service_seconds": max(0.001, time.monotonic() - started)})
        return {"operation_id": job["id"], "thread_id": job["thread_id"], "turn_id": job["turn_id"]}

    def _verify_inputs(self, job):
        directory = Path(job["directory"]).resolve()
        if directory.parent != self.root:
            raise WorkflowError("worker directory is outside the configured host")
        for name, sha in job["inputs"].items():
            source = directory / name
            if (source.is_symlink() or not source.resolve().is_relative_to(directory)
                    or not source.is_file() or file_digest(source) != sha):
                raise WorkflowError("worker modified a pinned input; result needs investigation")
        return directory

    def _image(self, job, item):
        directory = self._verify_inputs(job)
        saved = item.get("savedPath")
        if saved:
            source = Path(saved)
            if (not source.is_absolute() or source.is_symlink() or not source.resolve().is_relative_to(directory)
                    or source.name in job["inputs"] or not source.is_file()):
                raise WorkflowError("native image path is not an owned generated output")
            if source.stat().st_size > 30 * 1024 * 1024:
                raise WorkflowError("native image exceeds import limit")
        else:
            value = item.get("result")
            if not isinstance(value, str) or not value or len(value) > 40 * 1024 * 1024:
                raise WorkflowError("native attachment has no local bytes; fileId alone is not a completed artifact")
            data = base64.b64decode(value, validate=True)
            source = directory / ("native-" + digest({"item": item["id"], "sha": digest(value)}) + ".png")
            if source.exists():
                if source.read_bytes() != data:
                    raise WorkflowError("persisted native image differs from the observed bytes")
            else:
                with source.open("xb") as output:
                    output.write(data)
        from PIL import Image
        with Image.open(source) as image:
            image.verify()
        with Image.open(source) as image:
            image.load()
        # Import before storing the terminal observation, so replay never depends
        # on the worker's mutable output file surviving a restart.
        artifact = self.production.artifacts.put(source, "image")
        return self.production.artifacts.resolve(artifact), artifact

    def poll(self, job):
        if job["model"] != self.server.model or job["runtime_key"] != self.config["runtime_key"]:
            raise WorkflowError("saved session belongs to another configured model/runtime")
        if job["state"] == "delivered":
            return {"operation_id": job["id"], "status": "delivered"}
        if job["observation"]:
            self.pools.operate(job["run_id"], "result", job["observation"])
            job["state"] = "delivered"
            self._save(job)
            return {"operation_id": job["id"], "status": "delivered"}
        if not job["thread_id"]:
            return {"operation_id": job["id"], "status": "unknown", "reason": "thread ID was not observed; no resend"}
        turns = self.server.turns(job["thread_id"])
        if job["turn_id"]:
            matches = [turn for turn in turns if turn.get("id") == job["turn_id"]]
        else:
            # One fresh thread is dedicated to one dispatch. More than one turn
            # means another writer intervened; do not guess which image is ours.
            matches = turns if len(turns) == 1 else []
        if len(matches) != 1:
            return {"operation_id": job["id"], "status": "unknown", "reason": "exact turn not observed; no resend"}
        turn = matches[0]
        items = turn.get("items")
        if not isinstance(items, list) or any(not isinstance(item, dict) for item in items):
            raise WorkflowError("native turn has malformed item history; reconcile this operation")
        messages = [item for item in items if item.get("type") == "userMessage"]
        for message in messages:
            content = message.get("content")
            if not isinstance(content, list) or any(not isinstance(value, dict) for value in content):
                raise WorkflowError("native turn has malformed user input; reconcile this operation")
        if not any(value.get("type") == "text" and value.get("text") == job["prompt"]
                   for message in messages for value in message["content"]):
            return {"operation_id": job["id"], "status": "unknown", "reason": "turn input does not match this dispatch"}
        if turn.get("status") == "inProgress":
            try:
                self.production.heartbeat(job["run_id"], job["task_id"], job["task_token"])
            except Conflict:
                pass  # Expired/cancelled tasks still need the provider outcome.
            return {"operation_id": job["id"], "status": "running"}
        if turn.get("status") != "completed":
            return {"operation_id": job["id"], "status": "unknown",
                    "reason": "turn failed/interrupted; image provider outcome requires reconciliation"}
        images = [item for item in items if isinstance(item, dict) and item.get("type") == "imageGeneration"]
        if len(images) != 1 or images[0].get("status") != "completed" or images[0].get("failure"):
            return {"operation_id": job["id"], "status": "unknown",
                    "reason": "exactly one successful native image item is required"}
        item = images[0]
        if not isinstance(item.get("id"), str) or not item["id"]:
            raise RpcUnavailable("image item has no observed identity")
        path, artifact = self._image(job, item)
        job["turn_id"] = turn["id"]
        job["observation"] = {
            "operation_id": job["id"], "claim_token": job["claim_token"],
            "receipt_id": "app-server:" + digest({"thread": job["thread_id"], "turn": turn["id"], "item": item["id"]}),
            "status": "completed", "artifact_path": str(path),
            "actual_units": 0 if job["included"] else None,
            "evidence": {"tool": "codex.app-server", "session_id": job["thread_id"], "turn_id": turn["id"],
                         "item_id": item["id"], "generation_id": item.get("generationId"),
                         "sha256": artifact["sha256"], "method": "native_image_item_readback"}}
        duration = turn.get("durationMs")
        if type(duration) in (int, float) and 0 < duration < 86400000:
            job["observation"]["generation_seconds"] = duration / 1000
        job["state"] = "observed"
        self._save(job)
        return self.poll(job)  # Repeatable local delivery, never another generation.

    def tick(self):
        result = {"observations": [], "dispatches": [], "blockers": []}
        for job in self._jobs():
            if job["state"] == "delivered":
                continue
            try:
                result["observations"].append(self.poll(job))
            except RpcUnavailable:
                self._transport_failed = True
                result["blockers"].append({"operation_id": job["id"], "error": "RpcUnavailable"})
                return result  # A disconnected/unresponsive transport cannot accept new work.
            except (WorkflowError, OSError, ValueError) as exc:
                result["blockers"].append({"operation_id": job["id"], "error": type(exc).__name__,
                    "reason": str(exc) if isinstance(exc, WorkflowError) else "inspect local files and configuration"})
        if self._transport_failed:
            result["blockers"].append({"error": "RpcUnavailable",
                                       "reason": "restart the disconnected host; no new claims are issued"})
            return result
        runs = [run for run in self.store.list() if run["channel"] in self.config["channels"] and run.get("pool")
                and run["pool"]["runtime_key"] == self.config["runtime_key"] and run["status"] not in {"cancelled", "scheduled"}]
        for run in runs:
            try:
                status = self.pools.operate(run["id"], "status")
                if status["review"]["capacity"] is None:
                    raise WorkflowError("configure the shared coordinator review limit before running the host")
                self.pools.operate(run["id"], "enqueue")
                self.pools.operate(run["id"], "tick", {"coordinator_idle": status["review"]["available"] > 0})
            except (WorkflowError, ValueError) as exc:
                result["blockers"].append({"run_id": run["id"], "error": type(exc).__name__,
                    "reason": str(exc) if isinstance(exc, WorkflowError) else "inspect local files and configuration"})
        if runs:
            candidates = self.pools.candidates(self.config["runtime_key"],
                                               estimated_units=self.config.get("estimated_units", 0))
            if candidates["active"] < candidates["capacity"] and candidates["candidates"]:
                candidate = candidates["candidates"][0]
                # One new dispatch per tick: stagger startup, never create a batch
                # barrier, and do not bypass another channel's fair turn.
                try:
                    run = self.store.get(candidate["run_id"])
                    status = self.pools.operate(run["id"], "status")
                    if status["review"]["capacity"] is not None and status["review"]["available"] > 0:
                        dispatched = self.dispatch(candidate)
                        if dispatched.get("status") == "not_sent":
                            result["blockers"].append({**dispatched, "error": "ImageNotSent"})
                        else:
                            result["dispatches"].append(dispatched)
                except (WorkflowError, OSError, ValueError) as exc:
                    if isinstance(exc, RpcUnavailable):
                        self._transport_failed = True
                    result["blockers"].append({"run_id": candidate["run_id"], "error": type(exc).__name__,
                    "reason": str(exc) if isinstance(exc, WorkflowError) else "inspect local files and configuration"})
        return result


def main(argv=None):
    parser = argparse.ArgumentParser(description="Native image host. Probe is read-only; run dispatches approved image tasks.")
    parser.add_argument("mode", choices=("probe", "run"))
    parser.add_argument("--config", required=True, type=Path)
    parser.add_argument("--db", default=os.environ.get("YTV_DATABASE_URL", ".ytvideos/state.sqlite3"))
    parser.add_argument("--workspace", default=os.environ.get("YTV_WORKSPACE", ".ytvideos"))
    parser.add_argument("--project-root", type=Path, default=Path(__file__).resolve().parents[3])
    args = parser.parse_args(argv)
    rpc = None
    try:
        config = json.loads(args.config.read_text())
        interval = config.get("poll_seconds", 2)
        if type(interval) not in (int, float) or not 0.5 <= interval <= 60:
            raise WorkflowError("poll_seconds must be between 0.5 and 60")
        rpc = StdioRpc(config["command"], timeout=config.get("rpc_timeout_seconds", 30))
        server = AppServer(rpc, config["model"])
        probe = server.probe()
        print(canonical({"probe": probe}), flush=True)
        if args.mode == "probe":
            return 0
        production = Production(Store(args.db), args.workspace, args.project_root,
                                approval_public_key=os.environ.get("YTV_APPROVAL_PUBLIC_KEY"))
        host = ImageHost(production, server, config)
        while True:
            print(canonical(host.tick()), flush=True)
            time.sleep(interval)
    except KeyboardInterrupt:
        return 0
    except (WorkflowError, OSError, ValueError, KeyError, TypeError) as exc:
        # Do not emit raw subprocess/provider responses or credentials.
        print(canonical({"error": type(exc).__name__, "action": "inspect host configuration and saved state"}), flush=True)
        return 2
    finally:
        if rpc:
            rpc.close()


if __name__ == "__main__":
    raise SystemExit(main())
