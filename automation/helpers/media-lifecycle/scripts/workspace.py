#!/usr/bin/env python3
"""Episode storage roles, owned runs, verified promotion and exact scratch cleanup."""
from __future__ import annotations
import argparse
from contextlib import contextmanager
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import sys
import uuid

# Same owner as the bounded read-only audit; no live-editor APIs.
import media_lifecycle as inventory

LAYOUT = ('Source', 'Assets/Generated', 'Work', 'Edit/MediaLifecycle', 'Deliverables')


def save(path, data):
    inventory.no_symlinks(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + '.' + uuid.uuid4().hex + '.tmp')
    with temporary.open('x') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write('\n'); f.flush(); os.fsync(f.fileno())
    temporary.replace(path)


def initialize(episode):
    episode = Path(episode).absolute()
    inventory.no_symlinks(episode)
    if not episode.is_dir():
        raise ValueError('Episode must already exist')
    for rel in LAYOUT:
        path = inventory.relative_path(episode, rel)
        path.mkdir(parents=True, exist_ok=True)
    path = episode / 'Edit/MediaLifecycle/layout.json'
    if not path.exists():
        save(path, {'version': 1, 'episode': str(episode), 'created_utc': inventory.now(),
                    'roles': {'source': 'Source', 'dependency': 'Assets/Generated',
                              'scratch': 'Work/<run>/scratch', 'preview': 'Work/<run>/previews',
                              'evidence': 'Edit', 'current': 'Deliverables'},
                    'legacy_dependencies': 'Preserve imported paths; index them without moving automatically',
                    'shared_dependencies': 'Shared/Image_Motion/Cache is permanent while referenced'})
    return episode


def run_path(episode, name):
    if not re.fullmatch(r'[a-zA-Z0-9][a-zA-Z0-9_-]{0,95}', name):
        raise ValueError('Invalid run id')
    return inventory.relative_path(episode, 'Work/' + name)


@contextmanager
def locked(episode):
    lock = inventory.relative_path(episode, 'Edit/MediaLifecycle/workspace.lock')
    with lock.open('a') as f:
        fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
        yield


def start(episode, name, owner):
    directory = run_path(episode, name)
    directory.mkdir()  # exclusive; a retry must inspect/resume its own manifest
    for role in ('scratch', 'previews'):
        (directory / role).mkdir()
    save(directory / 'manifest.json', {'version': 1, 'run': name, 'owner': owner,
         'status': 'active', 'created_utc': inventory.now(), 'entries': []})
    return directory


def snapshot(path):
    before = inventory.identity(path)
    digest = inventory.sha256(path)
    if inventory.identity(path) != before:
        raise ValueError(f'Changed file: {path}')
    return {'identity': before, 'sha256': digest}


def unchanged(path, record):
    if snapshot(path) != {k: record[k] for k in ('identity', 'sha256')}:
        raise ValueError(f'Changed file; register a new version: {path}')


def load_run(episode, name, owner):
    p = run_path(episode, name) / 'manifest.json'
    inventory.no_symlinks(p)
    data = json.loads(p.read_text())
    if data['owner'] != owner:
        raise ValueError('Run owner mismatch')
    return p, data


def register(episode, name, owner, value, role, rebuild=(), evidence=(), disposition='pending'):
    path, data = load_run(episode, name, owner)
    if data['status'] != 'active':
        raise ValueError('Register only while the run is active')
    file = inventory.relative_path(episode, value)
    allowed = {'scratch': f'Work/{name}/scratch/', 'preview': f'Work/{name}/previews/',
               'dependency': 'Assets/Generated/', 'evidence': 'Edit/'}
    if role not in allowed or not value.startswith(allowed[role]):
        raise ValueError('Role does not match its storage location')
    if any(e['path'] == value for e in data['entries']):
        raise ValueError('Already registered; use a new version')
    if any(e['path'] == value for e in data.get('qa_batch', {}).get('frames', [])):
        raise ValueError('QA frames are managed by finalize-qa, not generic clean')
    dependencies = []
    for rel in rebuild:
        dep = inventory.relative_path(episode, rel)
        dependencies.append({'path': rel, **snapshot(dep)})
    proofs = []
    for rel in evidence:
        proof = inventory.relative_path(episode, rel)
        proofs.append({'path': rel, **snapshot(proof)})
    if role == 'scratch' and (not dependencies or not proofs):
        raise ValueError('Scratch requires actual reconstruction inputs and evidence')
    if disposition not in ('pending', 'rejected') or (disposition == 'rejected' and role != 'preview'):
        raise ValueError('Only preview may carry a rejected disposition')
    if disposition == 'rejected':
        if not proofs:
            raise ValueError('Rejected preview requires an exact decision receipt')
        decision = json.loads(inventory.relative_path(episode, proofs[0]['path']).read_text())
        if decision.get('decision') != 'rejected' or decision.get('file') != str(file) or decision.get('sha256') != inventory.sha256(file):
            raise ValueError('Decision receipt must name this rejected file/hash')
    data['entries'].append({'path': value, 'role': role, **snapshot(file),
                            'rebuild_from': dependencies, 'evidence': proofs, 'disposition': disposition})
    save(path, data)


def finish(episode, name, owner, status, writer_finished):
    path, data = load_run(episode, name, owner)
    if data['status'] != 'active' or status not in ('complete', 'failed', 'abandoned'):
        raise ValueError('Invalid run transition')
    if not writer_finished:
        raise ValueError('Writer completion must be checked before closing the run')
    data.update(status=status, writer_finished_utc=inventory.now())
    save(path, data)


def reject(episode, name, owner, value, decision_rel):
    path, data = load_run(episode, name, owner)
    if data['status'] != 'complete':
        raise ValueError('Review disposition requires a completed writer')
    entry = next((e for e in data['entries'] if e['path'] == value and e['role'] == 'preview'), None)
    if not entry or entry.get('removed_utc'):
        raise ValueError('Expected a retained preview entry')
    file = inventory.relative_path(episode, value)
    unchanged(file, entry)
    proof = inventory.relative_path(episode, decision_rel)
    record = snapshot(proof)
    decision = json.loads(proof.read_text())
    unchanged(proof, record)
    if decision.get('decision') != 'rejected' or decision.get('file') != str(file) or decision.get('sha256') != entry['sha256']:
        raise ValueError('Decision must name this exact rejected preview/hash')
    entry['evidence'].append({'path': decision_rel, **record})
    entry['disposition'] = 'rejected'
    save(path, data)
    journal(episode, {'action': 'reject_preview', 'path': value,
                      'sha256': entry['sha256'], 'decision': decision_rel})


def journal(episode, event):
    path = inventory.relative_path(episode, 'Edit/MediaLifecycle/locations.jsonl')
    with path.open('a') as f:
        f.write(json.dumps({'utc': inventory.now(), **event}, ensure_ascii=False) + '\n')
        f.flush(); os.fsync(f.fileno())


def fresh_audit(episode, root, policy=None):
    if not episode.is_relative_to(root) or episode == root:
        raise ValueError('Episode must be strictly inside root')
    result = inventory.audit(root, episode, policy)
    if result['errors']:
        raise ValueError('Dependency scan failed: ' + '; '.join(result['errors']))
    return result


def check_unreferenced(audit, rel, preserve_pin=False):
    row = next((r for r in audit['files'] if r['path'] == rel), None)
    if row is None:
        raise ValueError(f'File not covered by fresh inventory: {rel}')
    # Text mentions remain review evidence; source/import/pins/current/writer holds block.
    protections = [p for p in row['protections'] if not (preserve_pin and p.startswith('PINNED:'))]
    if protections:
        raise ValueError(f'Protected file: {rel}: {protections}')
    if row['nlink'] > 1:
        raise ValueError(f'Hardlink requires separate review: {rel}')
    return row


def copy_verified(source, target):
    record = snapshot(source)
    inventory.no_symlinks(target)
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open('xb') as out, source.open('rb') as incoming:
        shutil.copyfileobj(incoming, out, 4 * 1024 * 1024)
        out.flush(); os.fsync(out.fileno())
    if inventory.sha256(target) != record['sha256']:
        raise ValueError('Copy verification failed; source preserved')
    unchanged(source, record)
    return record


def adopt(episode, name, owner, value, role, audit, execute=False, keep_alias=False):
    _, run = load_run(episode, name, owner)
    if run['status'] != 'active' or role not in ('scratch', 'preview'):
        raise ValueError('Only legacy scratch/previews can be adopted into an active run')
    source = inventory.relative_path(episode, value)
    if not value.startswith('Edit/') or source.suffix.lower() not in inventory.MEDIA:
        raise ValueError('Legacy adoption is limited to explicit Edit media')
    check_unreferenced(audit, value, preserve_pin=role == 'preview' and keep_alias)
    if keep_alias and role != 'preview':
        raise ValueError('Compatibility aliases are only for retained previews')
    dest_rel = f'Work/{name}/{"scratch" if role == "scratch" else "previews"}/legacy/{value}'
    target = inventory.relative_path(episode, dest_rel)
    resume = False
    if target.exists():
        log = episode / 'Edit/MediaLifecycle/locations.jsonl'
        inventory.no_symlinks(log)
        events = [json.loads(line) for line in log.read_text().splitlines()] if log.exists() else []
        known = [e for e in events if e.get('action') == 'move' and e.get('from') == value and e.get('to') == dest_rel]
        # Resume only a known prepared copy after observing both actual files.
        resume = bool(known and known[-1].get('state') == 'prepared'
                      and inventory.sha256(source) == known[-1]['sha256'] == inventory.sha256(target))
        if not resume:
            raise ValueError('Destination exists without a matching prepared journal event')
    event = {'action': 'move', 'from': value, 'to': dest_rel, 'role': role,
             'sha256': inventory.sha256(source), 'execute': execute}
    if execute:
        journal(episode, {**event, 'state': 'prepared'})
        record = snapshot(source) if resume else copy_verified(source, target)
        # Recheck dependencies immediately before removing the old directory entry.
        for dep, before in audit['inputs'].items():
            if inventory.identity(Path(dep)) != before:
                raise ValueError(f'Dependency metadata changed; source preserved: {dep}')
        unchanged(source, record)
        source.unlink()
        if keep_alias:
            source.symlink_to(os.path.relpath(target, source.parent))
        journal(episode, {**event, 'state': 'complete', 'legacy_alias': keep_alias})
    return event


def clean(episode, name, owner, audit, execute=False):
    manifest, data = load_run(episode, name, owner)
    if data['status'] != 'complete' or not data.get('writer_finished_utc'):
        raise ValueError('Only completed runs with checked writer completion can be cleaned')
    rows = []
    qa_sources = set()
    for managed in (episode / 'Work').glob('*/manifest.json'):
        inventory.no_symlinks(managed)
        record = snapshot(managed)
        source = json.loads(managed.read_text()).get('qa_batch', {}).get('source', {}).get('path')
        if source: qa_sources.add(source)
        audit['inputs'][str(managed)] = record['identity']
    for entry in data['entries']:
        if entry['path'] in qa_sources:
            continue  # Exact retained reconstruction input for QA; never generic scratch.
        disposable = entry['role'] == 'scratch' or (entry['role'] == 'preview' and entry.get('disposition') == 'rejected')
        if not disposable or entry.get('removed_utc'):
            continue
        rel = entry['path']
        directory = 'scratch' if entry['role'] == 'scratch' else 'previews'
        if not rel.startswith(f'Work/{name}/{directory}/'):
            raise ValueError('Disposable escaped its owned directory')
        check_unreferenced(audit, rel)
        file = inventory.relative_path(episode, rel)
        unchanged(file, entry)
        for dep in entry['rebuild_from'] + entry['evidence']:
            unchanged(inventory.relative_path(episode, dep['path']), dep)
        rows.append(entry)
    # Validate the whole requested set before the first deletion.
    for entry in rows:
        if execute:
            for dep, before in audit['inputs'].items():
                if inventory.identity(Path(dep)) != before:
                    raise ValueError('Dependency metadata changed; remaining scratch preserved')
            file = inventory.relative_path(episode, entry['path'])
            unchanged(file, entry)
            journal(episode, {'action': 'delete_disposable', 'role': entry['role'], 'state': 'prepared',
                             'path': entry['path'], 'sha256': entry['sha256'],
                             'bytes': entry['identity']['bytes']})
            file.unlink()
            entry['removed_utc'] = inventory.now()
            save(manifest, data)
            if str(manifest) in audit['inputs']:
                # Our own receipt update is expected; other inputs keep their
                # original fingerprints and remain guarded before each file.
                audit['inputs'][str(manifest)] = inventory.identity(manifest)
            journal(episode, {'action': 'delete_disposable', 'role': entry['role'], 'state': 'complete',
                             'path': entry['path'], 'sha256': entry['sha256'],
                             'bytes': entry['identity']['bytes']})
    return {'execute': execute, 'files': len(rows),
            'logical_bytes': sum(e['identity']['bytes'] for e in rows),
            'physical_reclaimable_bytes': None}


def promote(episode, source_rel, filename, key, qa_rel):
    if Path(filename).name != filename or not filename or filename in ('.', '..'):
        raise ValueError('Delivery name must be one filename')
    if Path(filename).suffix.lower() not in {'.mp4', '.mov', '.mkv', '.webm', '.srt', '.wav', '.m4a', '.mp3'} or not key:
        raise ValueError('Expected a media/sidecar filename and product/language/format key')
    source = inventory.relative_path(episode, source_rel)
    qa = inventory.relative_path(episode, qa_rel)
    receipt = json.loads(qa.read_text())
    digest = inventory.sha256(source)
    if receipt.get('sha256') != digest or receipt.get('file') != str(source):
        raise ValueError('QA receipt must name this exact source and SHA256')
    # This attests identity, not editorial approval or subjective AV checks.
    current_path = episode / 'Deliverables/current.json'
    inventory.no_symlinks(current_path)
    current = json.loads(current_path.read_text()) if current_path.exists() else {'version': 1, 'items': {}}
    target = inventory.relative_path(episode, 'Deliverables/' + filename)
    if source != target:
        if target.exists():
            raise FileExistsError(target)
        staging = episode / 'Deliverables' / ('.' + filename + '.' + uuid.uuid4().hex + '.staging')
        try:
            copy_verified(source, staging)
            # Atomic publication without replacing an existing file.
            os.link(staging, target)
        finally:
            # Only this call's exclusive UUID staging file; never the source,
            # previous delivery or a directory sweep.
            if staging.exists():
                staging.unlink()
    item = {'path': str(target.relative_to(episode)), 'sha256': digest,
            'qa_receipt': qa_rel, 'qa_status': 'IDENTITY_VERIFIED_SEE_RECEIPT',
            'updated_utc': inventory.now()}
    previous = current['items'].get(key)
    current['items'][key] = item
    save(current_path, current)
    journal(episode, {'action': 'promote', 'key': key, 'previous': previous, 'current': item})
    return item


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--episode', type=Path, required=True)
    sub = p.add_subparsers(dest='command', required=True)
    sub.add_parser('init')
    for name in ('start', 'register', 'finish', 'adopt', 'clean', 'reject', 'register-qa', 'finalize-qa'):
        s = sub.add_parser(name)
        s.add_argument('--run', required=True); s.add_argument('--owner', required=True)
        if name in ('adopt', 'register'):
            s.add_argument('--path', required=True)
            s.add_argument('--role', choices=['scratch', 'preview', 'dependency', 'evidence'], required=True)
        if name == 'reject':
            s.add_argument('--path', required=True)
            s.add_argument('--decision', required=True)
        if name == 'register':
            s.add_argument('--rebuild-from', action='append', default=[])
            s.add_argument('--evidence', action='append', default=[])
            s.add_argument('--disposition', choices=['pending', 'rejected'], default='pending')
        if name == 'finish':
            s.add_argument('--status', choices=['complete', 'failed', 'abandoned'], required=True)
            s.add_argument('--writer-finished', action='store_true')
        if name == 'register-qa':
            s.add_argument('--report', required=True)
            s.add_argument('--legacy', action='store_true', help='Explicit registration of completed legacy QA selection')
            s.add_argument('--recipe', help='Retained reconstruction recipe for a legacy report')
        if name == 'finalize-qa':
            s.add_argument('--review', required=True)
        if name in ('adopt', 'clean', 'finalize-qa'):
            s.add_argument('--root', type=Path, required=True)
            s.add_argument('--policy', type=Path, required=True)
            s.add_argument('--execute', action='store_true')
        if name == 'adopt':
            s.add_argument('--keep-alias', action='store_true')
    s = sub.add_parser('promote')
    s.add_argument('--source', required=True); s.add_argument('--name', required=True)
    s.add_argument('--key', required=True, help='Exact product/language/format identity, e.g. full_en_1080p_mp4')
    s.add_argument('--qa', required=True)
    args = p.parse_args()
    try:
        episode = initialize(args.episode)
        with locked(episode):
            if args.command == 'init': result = {'episode': str(episode), 'layout': 'ready'}
            elif args.command == 'start': result = str(start(episode, args.run, args.owner))
            elif args.command == 'register': result = register(episode, args.run, args.owner, args.path, args.role, args.rebuild_from, args.evidence, args.disposition)
            elif args.command == 'finish': result = finish(episode, args.run, args.owner, args.status, args.writer_finished)
            elif args.command == 'reject': result = reject(episode, args.run, args.owner, args.path, args.decision)
            elif args.command == 'promote': result = promote(episode, args.source, args.name, args.key, args.qa)
            elif args.command == 'register-qa':
                from qa_lifecycle import register_qa
                result = register_qa(episode, args.run, args.owner, args.report, args.legacy, args.recipe)
            else:
                audit = fresh_audit(episode, args.root.resolve(), args.policy.absolute())
                if args.command == 'clean': result = clean(episode, args.run, args.owner, audit, args.execute)
                elif args.command == 'finalize-qa':
                    from qa_lifecycle import finalize_qa
                    result = finalize_qa(episode, args.run, args.owner, args.review, audit, args.execute)
                else: result = adopt(episode, args.run, args.owner, args.path, args.role, audit, args.execute, args.keep_alias)
            print(json.dumps(result, ensure_ascii=False))
        return 0
    except (ValueError, OSError, KeyError, TypeError) as exc:
        print(f'Storage operation refused: {exc}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
