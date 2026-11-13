"""Offline signing utility for a trusted human operator, outside worker hosts."""

import argparse
import base64
import getpass
import json
import os
import re
import stat
import sys
from datetime import datetime, timezone
from pathlib import Path
from uuid import UUID

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from ytvideos.errors import WorkflowError
from ytvideos.util import canonical, file_digest, parse_time, require_text


def write_new(path, data):
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, "wb") as stream:
        stream.write(data)


def read_key(path):
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    with os.fdopen(fd, "rb") as stream:
        info = os.fstat(stream.fileno())
        if not stat.S_ISREG(info.st_mode) or info.st_uid != os.getuid() or info.st_mode & 0o077:
            raise ValueError("signing key must be an operator-owned file with owner-only permissions")
        key = serialization.load_pem_private_key(stream.read(), password=passphrase("Key passphrase: "))
    if not isinstance(key, Ed25519PrivateKey):
        raise ValueError("signing key must be Ed25519")
    return key


def encode(data):
    return base64.b64encode(data).decode("ascii")


def passphrase(prompt):
    if not sys.stdin.isatty():
        raise ValueError("enter the signing key passphrase in the operator's interactive terminal")
    return getpass.getpass(prompt).encode("utf-8")


def event_from_observation(observation, script, actor):
    if observation.get("record_type") != "historical_codex_chat_observation":
        raise ValueError("expected a historical Codex chat observation")
    sha256 = observation["artifact_sha256"]
    if not isinstance(sha256, str) or not re.fullmatch(r"[a-f0-9]{64}", sha256) or file_digest(script) != sha256:
        raise ValueError("script bytes differ from the observation")
    artifact_id = observation["artifact_id"]
    if artifact_id != f"script:sha256:{sha256}":
        raise ValueError("observation must target an exact script artifact")
    created_at = parse_time(observation["approval_turn_started_at"]).astimezone(timezone.utc)
    if created_at > datetime.now(timezone.utc):
        raise ValueError("approval message cannot be in the future")
    thread_id = UUID(observation["thread_id"])
    message_id = UUID(observation["approval_message_id"])
    return {
        "event_id": f"codex:{thread_id}:{message_id}",
        "actor": require_text(actor, "operator identity"),
        "source": "operator_verified_codex_chat",
        "run_id": str(UUID(observation["run_id"])),
        "kind": "script",
        "artifact_id": artifact_id,
        "sha256": sha256,
        "created_at": created_at.isoformat(),
        "scope": "produce_video",
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    initialize = commands.add_parser("init-key")
    initialize.add_argument("--key", type=Path, required=True)
    sign = commands.add_parser("sign")
    sign.add_argument("--key", type=Path, required=True)
    sign.add_argument("--observation", type=Path, required=True)
    sign.add_argument("--script", type=Path, required=True)
    sign.add_argument("--actor", required=True, help="Identity of the operator recording the decision")
    sign.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        if args.command == "init-key":
            password = passphrase("New key passphrase: ")
            if not password or password != passphrase("Repeat key passphrase: "):
                raise ValueError("passphrases must be nonempty and match")
            key = Ed25519PrivateKey.generate()
            write_new(args.key, key.private_bytes(serialization.Encoding.PEM,
                                                 serialization.PrivateFormat.PKCS8,
                                                 serialization.BestAvailableEncryption(password)))
            print(encode(key.public_key().public_bytes_raw()))
        else:
            observation = json.loads(args.observation.read_text(encoding="utf-8"))
            event = event_from_observation(observation, args.script, args.actor)
            print(json.dumps(event, ensure_ascii=False, indent=2))
            print("Observed message:", json.dumps(require_text(observation.get("approval_message"), "message"),
                                                   ensure_ascii=False))
            print("Check the original Codex message, displayed script and current run on the operator host.")
            if input("Type RECORD to record the existing decision: ") != "RECORD":
                raise ValueError("operator did not record the decision")
            signature = read_key(args.key).sign(canonical(event).encode())
            write_new(args.output, (canonical({"event": event, "signature": encode(signature)}) + "\n").encode())
        return 0
    except (EOFError, KeyError, OSError, TypeError, ValueError, WorkflowError) as exc:
        parser.exit(2, f"Operator import failed: {exc}\n")


if __name__ == "__main__":
    raise SystemExit(main())
