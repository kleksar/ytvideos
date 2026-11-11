"""Execute established media CLIs behind a live task-lease guard.

No shell interpolation, credentials in argv, approval creation, or blind retries.
The host supplies a guard that re-reads authoritative state; a claimed-task dict
alone is not authority. Output receipts must still pass the stage's real QA.
"""
from __future__ import annotations

import hashlib
import json
import math
import os
from pathlib import Path
import re
import subprocess
import sys
import time
from typing import Callable

from ..errors import Conflict, WorkflowError


TOOLS = {
    'tts': 'automation/elevenlabs/tts.py',
    'montage': 'automation/ffmpeg_montage/montage.py',
    'inspect': 'automation/helpers/video-qa/scripts/inspect_video.py',
    'srt': 'automation/helpers/srt/scripts/srt_tool.py',
}


def file_sha256(path):
    result = hashlib.sha256()
    with Path(path).open('rb') as incoming:
        for block in iter(lambda: incoming.read(1024 * 1024), b''):
            result.update(block)
    return result.hexdigest()


def checked_inputs(inputs):
    if type(inputs) not in (list, tuple) or not inputs:
        raise WorkflowError('A media command requires bound input artifacts')
    result = []
    for artifact in inputs:
        if type(artifact) is not dict or set(artifact) != {'path', 'sha256'}:
            raise WorkflowError('Media input requires path and sha256')
        if not isinstance(artifact['sha256'], str) or not re.fullmatch(r'[0-9a-f]{64}', artifact['sha256']):
            raise WorkflowError('Invalid media input hash')
        path = Path(artifact['path']).resolve(strict=True)
        if not path.is_file() or file_sha256(path) != artifact['sha256']:
            raise Conflict('Media input is missing or changed')
        result.append({'path': str(path), 'sha256': artifact['sha256']})
    return result


class LocalMediaAdapter:
    def __init__(self, project_root, *, guard: Callable[[dict], None], runner=subprocess.run, clock=time.time):
        if not callable(guard):
            raise WorkflowError('A trusted live-state guard is required')
        self.project_root = Path(project_root).resolve(strict=True)
        self.guard = guard
        self.runner = runner
        self.clock = clock

    def execute(self, kind, args, *, run_id, task_id, claim, input_hash,
                inputs, outputs, receipt_path, timeout=900):
        if kind not in TOOLS:
            raise WorkflowError('Unsupported media CLI')
        if type(args) not in (list, tuple) or any(type(x) is not str or '\0' in x for x in args):
            raise WorkflowError('CLI arguments must be a string list')
        for identity in (run_id, task_id, input_hash):
            if not isinstance(identity, str) or not identity.strip():
                raise WorkflowError('Run, task and input identities are required')
        if (not isinstance(claim, dict) or not isinstance(claim.get('token'), str) or not claim['token']
                or type(claim.get('expires_at')) not in (int, float) or not math.isfinite(claim['expires_at'])
                or claim['expires_at'] <= self.clock()
                or claim.get('input_hash') != input_hash):
            raise Conflict('Missing, expired or mismatched task claim')
        if type(timeout) not in (int, float) or not math.isfinite(timeout) or not 0 < timeout <= 86400:
            raise WorkflowError('Timeout must be between 0 and 86400 seconds')
        script = (self.project_root / TOOLS[kind]).resolve(strict=True)
        if not script.is_relative_to(self.project_root) or not script.is_file():
            raise WorkflowError('CLI script is outside the pinned project')
        bound = checked_inputs(inputs)
        if type(outputs) not in (list, tuple) or not outputs:
            raise WorkflowError('Expected output paths are required')
        destinations = [Path(path).resolve() for path in outputs]
        if len(set(destinations)) != len(destinations) or any(path.exists() for path in destinations):
            raise Conflict('Output already exists or output paths repeat; reconcile before retrying')
        receipt_path = Path(receipt_path).resolve()
        if receipt_path.exists() or receipt_path in destinations or str(receipt_path) in {x['path'] for x in bound}:
            raise Conflict('Receipt path already used or overlaps an artifact')
        command = [sys.executable, str(script), *args]
        paid = kind == 'tts' and '--generate' in args
        request = {'run_id': run_id, 'task_id': task_id, 'claim_token': claim['token'],
                   'input_hash': input_hash, 'kind': kind, 'paid': paid, 'inputs': bound,
                   'script_sha256': file_sha256(script), 'argv': command,
                   'outputs': [str(x) for x in destinations]}
        # The guard must validate the real current lease, input version, script
        # approval, budget reservation, and authority for this exact operation.
        self.guard(request)
        checked_inputs(bound)
        if claim['expires_at'] <= self.clock():
            raise Conflict('Task lease expired before dispatch')
        receipt_path.parent.mkdir(parents=True, exist_ok=True)
        # Reserve a durable dispatch marker BEFORE invoking a possibly paid CLI.
        # An interrupted process leaves outcome_unknown; callers reconcile it.
        pending = {**request, 'state': 'outcome_unknown', 'started_at': self.clock()}
        fd = os.open(receipt_path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        with os.fdopen(fd, 'w') as stream:
            json.dump(pending, stream, ensure_ascii=False, indent=2)
            stream.flush()
            os.fsync(stream.fileno())
        result = {**pending, 'returncode': None, 'stdout': '', 'stderr': '', 'output_artifacts': []}
        try:
            process = self.runner(command, cwd=str(self.project_root), shell=False,
                                  stdin=subprocess.DEVNULL, capture_output=True, text=True,
                                  timeout=timeout, check=False)
            result.update(returncode=process.returncode, stdout=process.stdout, stderr=process.stderr)
            result['state'] = 'completed' if process.returncode == 0 else ('outcome_unknown' if paid else 'failed')
            checked_inputs(bound)
            if request['script_sha256'] != file_sha256(script):
                raise Conflict('CLI implementation changed while running')
            for path in destinations:
                if path.is_file() and path.stat().st_size:
                    result['output_artifacts'].append({'path': str(path), 'sha256': file_sha256(path), 'size': path.stat().st_size})
                elif result['state'] == 'completed':
                    result['state'] = 'outcome_unknown' if paid else 'failed'
                    result['error'] = 'CLI returned success without the expected nonempty output'
        except subprocess.TimeoutExpired:
            result.update(state='outcome_unknown' if paid else 'failed', error='CLI timed out; inspect preserved outputs before retrying')
        except (OSError, Conflict) as exc:
            result.update(state='outcome_unknown' if paid else 'failed', error=type(exc).__name__)
        result['finished_at'] = self.clock()
        # Logs are kept in the receipt, never interpreted as approval or QA PASS.
        temporary = receipt_path.with_name(receipt_path.name + '.complete.tmp')
        fd = os.open(temporary, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        with os.fdopen(fd, 'w') as stream:
            json.dump(result, stream, ensure_ascii=False, indent=2)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, receipt_path)
        return result
