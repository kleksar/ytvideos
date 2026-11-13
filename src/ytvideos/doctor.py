"""Read-only local capability checks, not inferred provider access."""
import os
import shutil

from .capabilities import capability_check


def inspect(production, run_id=None, *, run_snapshot=None):
    checks = [dict(capability="state.store", available=True, evidence=production.store.health()),
              dict(capability="artifact.local_storage", available=os.access(production.artifacts.root, os.W_OK),
                   evidence=str(production.artifacts.root)),
              dict(capability="approval.verifier", available=bool(production.approvals.public_key),
                   evidence="Ed25519 public verifier configured" if production.approvals.public_key else
                   "no public verifier; writing the script can proceed, approvals require trusted bridge setup")]
    for binary in ("ffmpeg", "ffprobe"):
        path = shutil.which(binary)
        checks.append(dict(capability=f"local.{binary}", available=bool(path), evidence=path or "binary not found"))
    if run_id:
        run = run_snapshot if run_snapshot is not None else production.store.get(run_id)
        if run["id"] != run_id:
            raise ValueError("doctor snapshot belongs to another run")
        for name, observation in sorted(run["capabilities"].items()):
            if name != "approval.verifier":
                checks.append(capability_check(name, observation))
        known = {entry["capability"] for entry in checks}
        required = {name for task in run["tasks"].values() for name in task["capabilities"]}
        # Scene tasks do not exist until storyboard completion. Report the
        # recipe's generation/extraction requirement before paying for audio.
        required.add("image.generate" if run["profile"]["recipe"] == "illustrated" else "media.licensed_clip")
        for name in sorted(required - known):
            checks.append(capability_check(name, None))
    if not any(check["capability"] == "approval.bridge" for check in checks):
        checks.append(capability_check("approval.bridge", None))
    return {"checks": checks, "policy": "Missing downstream capability does not block independent upstream work.",
            "limits": ["Local files are not a verified shared backup.",
                       "The CLI does not create ChatGPT sessions by itself; a supported host dispatcher is required.",
                       "A configured verifier is not proof that a live user-event bridge is connected."]}
