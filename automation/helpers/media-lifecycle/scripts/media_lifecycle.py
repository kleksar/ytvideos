#!/usr/bin/env python3
"""Inventory and propose media cleanup. Only new report directories are written."""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import stat
import sys
from urllib.parse import unquote, urlparse

VERSION = 1
MEDIA = {'.mp4', '.mov', '.mkv', '.webm', '.h264', '.pcm', '.aac', '.wav',
         '.mp3', '.m4a', '.png', '.jpg', '.jpeg', '.npy', '.yuv', '.tif'}
TEXT = {'.json', '.jsonl', '.md', '.txt', '.py', '.csv', '.yaml', '.yml', '.srt'}
SKIP = {'.git', '.venv', '__pycache__', 'node_modules', '.agents'}
IDENTITY = ('device', 'inode', 'bytes', 'mtime_ns', 'ctime_ns', 'nlink')


def now():
    return datetime.now(timezone.utc).isoformat()


def identity(path):
    s = path.lstat()
    if not stat.S_ISREG(s.st_mode):
        raise ValueError(f'Not a regular file (symlinks refused): {path}')
    return dict(device=s.st_dev, inode=s.st_ino, bytes=s.st_size,
                mtime_ns=s.st_mtime_ns, ctime_ns=s.st_ctime_ns, nlink=s.st_nlink,
                allocated_bytes=s.st_blocks * 512)


def no_symlinks(path):
    for p in (path, *path.parents):
        if p.is_symlink():
            raise ValueError(f'Symlink component refused: {p}')


def relative_path(base, value):
    p = Path(value)
    if not isinstance(value, str) or not value or p.is_absolute() or '..' in p.parts:
        raise ValueError(f'Expected a confined relative path: {value!r}')
    result = base / p
    no_symlinks(result)
    return result


def sha256(path):
    no_symlinks(path)
    before = identity(path)
    h = hashlib.sha256()
    fd = os.open(path, os.O_RDONLY | getattr(os, 'O_NOFOLLOW', 0))
    with os.fdopen(fd, 'rb') as stream:
        s = os.fstat(stream.fileno())
        if (s.st_dev, s.st_ino) != (before['device'], before['inode']):
            raise ValueError(f'File replaced while opening: {path}')
        for block in iter(lambda: stream.read(4 * 1024 * 1024), b''):
            h.update(block)
    if identity(path) != before:
        raise ValueError(f'File changed while hashing: {path}')
    return h.hexdigest()


def walk_files(base, skipped, errors, packages=None):
    """No symlink traversal, including directory aliases and skill entrypoints."""
    def onerror(exc):
        errors.append(str(exc))
    for directory, dirs, names in os.walk(base, followlinks=False, onerror=onerror):
        parent = Path(directory)
        for name in dirs[:]:
            p = parent / name
            if p.is_symlink():
                skipped.append(str(p)); dirs.remove(name)
            elif name in SKIP or name == 'MediaLifecycle' or name == 'audits':
                dirs.remove(name)
            elif name.endswith('.palmier') and packages is not None:
                packages.add(p); dirs.remove(name)
        for name in names:
            p = parent / name
            if p.is_symlink():
                skipped.append(str(p))
            else:
                yield p


def load_policy(path, episode):
    if path is None:
        return {'version': VERSION, 'candidates': [], 'pins': [], 'current': [],
                'active_work': []}
    no_symlinks(path)
    data = json.loads(path.read_text())
    if data.get('version') != VERSION:
        raise ValueError('Unsupported policy version')
    for item in data.get('candidates', []):
        for field in ('path', 'role', 'status', 'reason', 'evidence', 'rebuild_from'):
            if not item.get(field):
                raise ValueError(f'Candidate lacks {field}: {item}')
        if item['role'] not in {'scratch', 'superseded_export', 'rejected_preview'}:
            raise ValueError(f'Unsupported candidate role: {item["role"]}')
        relative_path(episode, item['path'])
        for field in ('evidence', 'rebuild_from'):
            if not isinstance(item[field], list):
                raise ValueError(f'{field} must be a list')
            for value in item[field]:
                relative_path(episode, value)
    paths = [c['path'] for c in data.get('candidates', [])]
    if len(paths) != len(set(paths)):
        raise ValueError('Duplicate candidate declarations')
    for name in ('pins', 'current', 'active_work'):
        for item in data.get(name, []):
            if not item.get('path') or not item.get('reason'):
                raise ValueError(f'{name} requires path and reason')
            relative_path(episode, item['path'])
            if not isinstance(item.get('evidence', []), list):
                raise ValueError(f'{name} evidence must be a list')
            for value in item.get('evidence', []):
                relative_path(episode, value)
    return data


def beneath(value, prefix):
    return value == prefix.rstrip('/') or value.startswith(prefix.rstrip('/') + '/')


def strings(value):
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for v in value.values():
            yield from strings(v)
    elif isinstance(value, list):
        for v in value:
            yield from strings(v)


def canonical_reference(value, base):
    if '\n' in value or len(value) > 4096 or ('/' not in value and '\\' not in value):
        return ''
    if value.startswith('file://'):
        value = unquote(urlparse(value).path)
    p = Path(value)
    return str((p if p.is_absolute() else base / p).resolve())


def audit(root, episode, policy_path, extra_projects=()):
    policy = load_policy(policy_path, episode)
    skipped, errors, inputs = [], [], {}
    packages = set()
    rows = []
    for p in walk_files(episode, skipped, errors):
        try:
            rows.append({'path': str(p.relative_to(episode)), **identity(p)})
        except (OSError, ValueError) as exc:
            errors.append(str(exc))
    candidates = {c['path']: c for c in policy.get('candidates', [])}
    refs, mentions = defaultdict(list), defaultdict(list)
    target_paths = {str(episode / r['path']): r['path'] for r in rows}
    candidate_paths = {str(episode / p): p for p in candidates}
    # Global text-mention scanning is only needed to protect declared cleanup
    # candidates. Avoid traversing the workspace when there is nothing to
    # compare; in particular, unrelated oversized research logs must not block
    # exact managed QA-frame finalization, which has its own consumer checks.
    if candidate_paths:
        documents = list(walk_files(root, skipped, errors, packages))
    else:
        # Package metadata protects imported files even when the policy has no
        # candidates; consume paths without retaining the whole workspace list.
        for _ in walk_files(root, skipped, errors, packages):
            pass
        documents = []
    packages.update(Path(p).expanduser().absolute() for p in extra_projects)
    aliases = []
    # A legacy alias is not an additional package if its real path is already
    # independently discovered. Never traverse an otherwise unlisted symlink.
    for package in list(packages):
        resolved = package.resolve()
        if package != resolved and resolved in packages:
            aliases.append({'alias': str(package), 'covered_by': str(resolved)})
            packages.remove(package)
    package_details = []
    unresolved = []
    # Imported media are protected even if not used by the visible timeline.
    for package in sorted(packages):
        detail = {'path': str(package), 'metadata_files': 0, 'timelines': 0,
                  'snapshots': 0, 'status': 'READ'}
        try:
            no_symlinks(package)
            media_path = package / 'media.json'
            no_symlinks(media_path)
            before = identity(media_path)
            media = json.loads(media_path.read_text())
            if identity(media_path) != before:
                raise ValueError(f'Package changed during read: {media_path}')
            inputs[str(media_path)] = before
            if not isinstance(media.get('entries'), list):
                raise ValueError(f'Unknown media.json format: {media_path}')
            for entry in media['entries']:
                external = entry.get('source', {}).get('external', {})
                value = external.get('absolutePath')
                if value:
                    target = canonical_reference(value, package)
                    if target in target_paths:
                        refs[target_paths[target]].append(str(media_path))
                    if not Path(target).is_file():
                        unresolved.append({'package': str(package), 'path': target})
            metadata = [package / 'project.json']
            metadata += sorted((package / 'snapshots').glob('*.json'))
            for path in metadata:
                no_symlinks(path)
                before = identity(path)
                data = json.loads(path.read_text())
                if identity(path) != before:
                    raise ValueError(f'Package changed during read: {path}')
                inputs[str(path)] = before
                detail['metadata_files'] += 1
                if path.name == 'project.json':
                    detail['timelines'] = len(data.get('timelines', []))
                else:
                    detail['snapshots'] += 1
                # Some package versions include direct paths in timeline/snapshot data.
                for value in strings(data):
                    target = canonical_reference(value, package)
                    if target in target_paths:
                        refs[target_paths[target]].append(str(path))
        except (OSError, ValueError, TypeError, AttributeError) as exc:
            detail['status'] = 'UNVERIFIED'
            errors.append(f'Package metadata: {exc}')
        package_details.append(detail)
    # Mentions are deliberately separate from actual project imports. No source
    # inference from generic JSON fields such as "file" or "output".
    for p in documents:
        if p.suffix.lower() not in TEXT or '/.agent/archive/' in str(p):
            continue
        if policy_path and p == policy_path:
            continue
        if p.name.startswith(('CLEANUP_', 'cleanup_', 'STORAGE_')):
            continue
        try:
            s = identity(p)
            if s['bytes'] > 8 * 1024 * 1024:
                errors.append(f'Text dependency scan skipped large file: {p}')
                continue
            text = p.read_text(errors='replace')
            hits = set()
            for absolute, rel in candidate_paths.items():
                if absolute in text or rel in text:
                    hits.add(rel)
            if p.suffix == '.json':
                try:
                    for value in strings(json.loads(text)):
                        target = canonical_reference(value, p.parent)
                        if target in candidate_paths:
                            hits.add(candidate_paths[target])
                except (ValueError, OSError):
                    pass  # Non-JSON text mentions remain usable; no dependency inferred.
            for rel in hits:
                mentions[rel].append(str(p))
            if hits:
                inputs[str(p)] = s
        except (OSError, ValueError) as exc:
            errors.append(f'Text reference scan: {exc}')
    if policy_path:
        inputs[str(policy_path)] = identity(policy_path)
    for group in ('pins', 'current', 'active_work'):
        for item in policy.get(group, []):
            for value in item.get('evidence', []):
                path = relative_path(episode, value)
                try:
                    inputs[str(path)] = identity(path)
                except (OSError, ValueError) as exc:
                    errors.append(f'Policy context evidence: {exc}')
    for row in rows:
        p, rel = episode / row['path'], row['path']
        protections = []
        if p.suffix.lower() not in MEDIA or any(x.endswith('.palmier') for x in Path(rel).parts):
            protections.append('PROJECT_OR_RECORD')
        if Path(rel).parts[0] in {'Source', 'Assets', 'Storyboard', 'Research', 'Packaging'}:
            protections.append('PERMANENT_SOURCE_OR_EVIDENCE')
        if refs[rel]:
            protections.append('LEGACY_PACKAGE_IMPORT_OR_SNAPSHOT_REFERENCE')
        for group, code in [('pins', 'PINNED'), ('current', 'CURRENT'), ('active_work', 'ACTIVE_WORK')]:
            for pin in policy.get(group, []):
                if beneath(rel, pin['path']):
                    protections.append(f'{code}: {pin["reason"]}')
        row['project_references'] = sorted(set(refs[rel]))
        row['text_mentions'] = sorted(set(mentions[rel]))
        row['protections'] = protections
        row['classification'] = 'PROTECTED' if protections else 'UNKNOWN'
        if rel in candidates:
            row['declaration'] = candidates[rel]
            row['blockers'] = list(protections)
            if row['text_mentions']:
                row['blockers'].append('TEXT_REFERENCE_REVIEW')
            if candidates[rel]['status'] not in {'review', 'rejected', 'superseded'}:
                row['blockers'].append('CANDIDATE_STATUS_UNRESOLVED')
            for field in ('evidence', 'rebuild_from'):
                for value in candidates[rel][field]:
                    dep = relative_path(episode, value)
                    if not dep.is_file():
                        row['blockers'].append(f'MISSING_{field.upper()}: {value}')
                    else:
                        inputs[str(dep)] = identity(dep)
            if row['nlink'] > 1:
                row['blockers'].append('HARDLINK_REVIEW')
            try:
                row['sha256'] = sha256(p)
                after = identity(p)
                if any(after[k] != row[k] for k in IDENTITY):
                    row['blockers'].append('CHANGED_DURING_AUDIT')
            except (OSError, ValueError) as exc:
                row['blockers'].append(str(exc))
            row['classification'] = 'BLOCKED' if row['blockers'] else 'REVIEW_CANDIDATE'
    present = {r['path'] for r in rows}
    missing_candidates = sorted(set(candidates) - present)
    totals = Counter()
    by_status = defaultdict(lambda: {'files': 0, 'logical_bytes': 0})
    inodes = set()
    for r in rows:
        totals['logical_bytes'] += r['bytes']
        totals['allocated_bytes_sum'] += r['allocated_bytes']
        node = (r['device'], r['inode'])
        if node not in inodes:
            totals['unique_inode_logical_bytes'] += r['bytes']
            totals['unique_inode_allocated_bytes'] += r['allocated_bytes']
        inodes.add(node)
        by_status[r['classification']]['files'] += 1
        by_status[r['classification']]['logical_bytes'] += r['bytes']
    return {'version': VERSION, 'kind': 'audit', 'created_utc': now(),
            'root': str(root), 'episode': str(episode), 'policy': str(policy_path) if policy_path else None,
            'files': rows, 'totals': dict(totals), 'by_classification': dict(by_status),
            'available_volume_bytes': os.statvfs(episode).f_bavail * os.statvfs(episode).f_frsize,
            'physical_reclaimable_bytes': None, 'packages': package_details,
            'covered_package_aliases': aliases,
            'unresolved_imports': unresolved, 'missing_declared_candidates': missing_candidates,
            'skipped_symlinks': sorted(set(skipped)), 'errors': errors, 'inputs': inputs,
            'coverage': 'BOUNDED_NOT_EXHAUSTIVE', 'executable': False,
            'limitations': ['No deletion implementation or permission. No writer absence proof.',
                            'All found imports protected, including retained timelines; unlisted/inaccessible projects and external consumers remain unknown.',
                            'Text scan is heuristic and cannot prove absence of dependencies. Source hashes/QA are evidence, not user acceptance.',
                            'APFS CoW and snapshots prevent inferring physical reclaim from logical or allocated sums.']}


def plan(audit_path):
    no_symlinks(audit_path)
    source = json.loads(audit_path.read_text())
    if source.get('version') != VERSION or source.get('kind') != 'audit':
        raise ValueError('Expected a version 1 audit')
    episode = Path(source['episode'])
    no_symlinks(episode)
    stale = []
    for path, before in source['inputs'].items():
        try:
            no_symlinks(Path(path))
            if identity(Path(path)) != before:
                stale.append(path)
        except (OSError, ValueError):
            stale.append(path)
    entries = []
    for row in source['files']:
        if 'declaration' not in row:
            continue
        item = dict(row)
        blockers = list(row.get('blockers', []))
        try:
            path = relative_path(episode, row['path'])
            current = identity(path)
            if any(current[k] != row[k] for k in IDENTITY) or sha256(path) != row.get('sha256'):
                blockers.append('STALE_FILE_IDENTITY')
        except (OSError, ValueError) as exc:
            blockers.append(f'FILE_RECHECK_FAILED: {exc}')
        if stale:
            blockers.append('STALE_AUDIT_INPUTS')
        if source['errors']:
            blockers.append('INCOMPLETE_DEPENDENCY_SCAN')
        item['blockers'] = blockers
        item['classification'] = 'BLOCKED' if blockers else 'REVIEW_CANDIDATE'
        item['required_before_any_future_removal'] = [
            'Fresh dependency scan including retained project histories and all known consumers',
            'Writer/import/render completion verified; absent locks do not prove inactivity',
            'Resolve text mentions, pins and source/rebuild dependencies',
            'Applicable retention/authorization and changed-file check at action time']
        entries.append(item)
    return {'version': VERSION, 'kind': 'plan', 'created_utc': now(),
            'audit': str(audit_path), 'audit_sha256': sha256(audit_path),
            'episode': str(episode), 'executable': False, 'deletion_implemented': False,
            'stale_inputs': stale, 'entries': entries,
            'review_candidate_logical_bytes': sum(r['bytes'] for r in entries if r['classification'] == 'REVIEW_CANDIDATE'),
            'blocked_logical_bytes': sum(r['bytes'] for r in entries if r['classification'] == 'BLOCKED'),
            'physical_reclaimable_bytes': None,
            'missing_declared_candidates': source['missing_declared_candidates'],
            'limitations': source['limitations'], 'errors': source['errors']}


def write_report(data, output):
    no_symlinks(output)
    if any(p.suffix == '.palmier' for p in (output, *output.parents)):
        raise ValueError('Reports cannot be written inside a retained native project package')
    episode = Path(data['episode'])
    if output.is_relative_to(episode):
        rel = output.relative_to(episode)
        if rel.parts and rel.parts[0] in {'Source', 'Assets', 'Storyboard', 'Packaging', 'Research'}:
            raise ValueError('Report output cannot be inside permanent source/evidence')
    output.mkdir(parents=True, exist_ok=False)
    (output / f'{data["kind"]}.json').write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
    lines = [f'# Media lifecycle {data["kind"]}', '', f'Episode: `{data["episode"]}`',
             f'UTC: {data["created_utc"]}', '', '**Read-only. Nothing deleted. This is not an executable deletion plan.**', '']
    if data['kind'] == 'audit':
        lines += ['| Classification | Files | Logical GiB |', '|---|---:|---:|']
        for status, values in sorted(data['by_classification'].items()):
            lines.append(f'| {status} | {values["files"]} | {values["logical_bytes"]/1024**3:.3f} |')
        lines += ['', f'Logical bytes: {data["totals"].get("logical_bytes", 0)}.',
                  f'Filesystem-reported allocated sum: {data["totals"].get("allocated_bytes_sum", 0)}.',
                  f'Project packages read: {len(data["packages"])}; skipped symlinks: {len(data["skipped_symlinks"])}.',
                  f'Unresolved import entries: {len(data["unresolved_imports"])}.', '']
        rows = [r for r in data['files'] if 'declaration' in r]
    else:
        lines += [f'Review candidates: {data["review_candidate_logical_bytes"]/1024**3:.3f} GiB logical.',
                  f'Blocked declarations: {data["blocked_logical_bytes"]/1024**3:.3f} GiB logical.',
                  f'Stale dependency inputs: {len(data["stale_inputs"])}.', '']
        rows = data['entries']
    lines += ['| Declared path | MiB | Status | Blockers |', '|---|---:|---|---|']
    for row in rows:
        blockers = '; '.join(row.get('blockers', [])) or 'Future dependency/writer review still required'
        lines.append(f'| `{row["path"]}` | {row["bytes"]/1024**2:.1f} | {row["classification"]} | {blockers.replace(chr(124), "/")} |')
    lines += ['', 'Physical reclaim: **unknown**. Logical groups are not guaranteed disk savings.', '']
    lines += [f'- {value}' for value in data['limitations']]
    if data['errors']:
        lines += ['', 'Read/coverage errors:'] + [f'- {e}' for e in data['errors']]
    (output / f'{data["kind"]}.md').write_text('\n'.join(lines) + '\n')


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    a = sub.add_parser('audit', help='Read sources and write a new inventory report')
    a.add_argument('--root', type=Path, required=True)
    a.add_argument('--episode', type=Path, required=True)
    a.add_argument('--policy', type=Path)
    a.add_argument('--output-dir', type=Path, required=True)
    p = sub.add_parser('plan', help='Recheck a saved audit and write a non-executable plan')
    p.add_argument('--audit', type=Path, required=True)
    p.add_argument('--output-dir', type=Path, required=True)
    opts = parser.parse_args(argv)
    try:
        output = opts.output_dir.expanduser().absolute()
        no_symlinks(output)
        output = output.resolve()
        if output.exists():
            raise ValueError(f'Output exists; choose a new report directory: {output}')
        if opts.command == 'audit':
            root, episode = opts.root.expanduser().resolve(), opts.episode.expanduser().resolve()
            if not episode.is_dir() or not episode.is_relative_to(root) or episode == root:
                raise ValueError('Episode must be a directory strictly inside the explicit project root')
            policy_path = opts.policy.expanduser().absolute() if opts.policy else None
            data = audit(root, episode, policy_path)
        else:
            data = plan(opts.audit.expanduser().absolute())
        write_report(data, output)
        print(json.dumps({'status': 'REPORT_WRITTEN', 'kind': data['kind'], 'output': str(output),
                          'executable': False, 'media_deleted': 0, 'coverage_errors': len(data['errors'])}))
        return 0
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f'Cannot build lifecycle report: {exc}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
