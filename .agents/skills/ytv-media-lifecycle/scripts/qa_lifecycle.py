"""Batch accounting and conservative finalization of exact QA frame selections."""
import json
from pathlib import Path

import workspace as w


def edit_path(episode, value):
    path = w.inventory.relative_path(episode, value)
    if not value.startswith('Edit/'):
        raise ValueError('QA records must be retained in Edit')
    return path


def register_qa(episode, name, owner, report_rel, legacy=False, recipe_rel=None):
    """One manifest write and one source hash for the entire selection."""
    manifest, run = w.load_run(episode, name, owner)
    if run.get('qa_batch'):
        raise ValueError('QA batch already registered; use a new run')
    if run['status'] != 'active' and not (legacy and run['status'] == 'complete'):
        raise ValueError('Expected active QA run or explicit completed legacy run')
    report_path = edit_path(episode, report_rel)
    report_record = w.snapshot(report_path)
    report = json.loads(report_path.read_text())
    recipe_record = None
    recipe = report.get('frame_recipe', {})
    if recipe_rel:
        if not legacy: raise ValueError('External recipe is only for legacy registration')
        recipe_path = edit_path(episode, recipe_rel)
        recipe_record = {'path': recipe_rel, **w.snapshot(recipe_path)}
        recipe = json.loads(recipe_path.read_text())
    if not recipe.get('argv') or not recipe.get('ffmpeg_version'):
        raise ValueError('Missing reconstruction command/tool version; legacy report needs a new evidenced report')
    required = report.get('plan', {}).get('required_review_checks', recipe.get('required_review_checks'))
    if (not isinstance(required, list) or not all(isinstance(k, str) and k for k in required) or
            not {'stream_metadata', 'full_decode', 'frame_sampling'}.issubset(required)):
        raise ValueError('Freeze applicable required_review_checks in the QA plan or legacy recipe')
    media = Path(report['media'])
    media_rel = str(media.relative_to(episode))
    media = w.inventory.relative_path(episode, media_rel)
    source = w.snapshot(media)
    if source['sha256'] != report['sha256']:
        raise ValueError('QA source changed')
    frames, seen = [], set()
    for item in report.get('frame_map', []):
        # Historical report paths may contain ..; normalize then recheck confinement/symlinks.
        raw = report_path.parent / item['path']
        w.inventory.no_symlinks(raw)
        file = raw.resolve()
        rel = str(file.relative_to(episode))
        if not any(rel.startswith(f'Work/{name}/{part}/') for part in ('scratch', 'previews')):
            raise ValueError('QA frame escaped owned run')
        if file.suffix.lower() != '.png' or rel in seen or type(item['index']) is not int:
            raise ValueError('Invalid or duplicate QA frame')
        seen.add(rel)
        frames.append({'path': rel, 'index': item['index'], **w.snapshot(file)})
    if not frames or sorted(f['index'] for f in frames) != report['requested_frame_indices']:
        raise ValueError('Incomplete QA frame map')
    if media_rel in seen or media.suffix.lower() not in {'.mp4', '.mov', '.mkv', '.webm'}:
        raise ValueError('QA reconstruction input must be a retained video, outside frame candidates')
    if seen.intersection(e['path'] for e in run['entries']):
        raise ValueError('Frame already has a different storage role')
    w.unchanged(report_path, report_record)
    if w.inventory.identity(media) != source['identity']:
        raise ValueError('Source changed during registration')
    run['qa_batch'] = {'report': {'path': report_rel, **report_record},
                       'source': {'path': media_rel, **source}, 'frames': frames,
                       'recipe_record': recipe_record,
                       'required_review_checks': required,
                       'legacy': legacy, 'registered_utc': w.inventory.now()}
    w.save(manifest, run)
    return {'registered_frames': len(frames), 'source_sha256': source['sha256']}


def finalize_qa(episode, name, owner, review_rel, audit, execute=False):
    manifest, run = w.load_run(episode, name, owner)
    if run['status'] != 'complete' or not run.get('writer_finished_utc'):
        raise ValueError('QA writer must be finished before finalization')
    batch = run['qa_batch']
    report_path = edit_path(episode, batch['report']['path'])
    review_path = edit_path(episode, review_rel)
    review_record = w.snapshot(review_path)
    review = json.loads(review_path.read_text())
    for record in (batch['report'], batch['source']):
        w.unchanged(w.inventory.relative_path(episode, record['path']), record)
    recipe_records = [batch['recipe_record']] if batch.get('recipe_record') else []
    for record in recipe_records:
        w.unchanged(edit_path(episode, record['path']), record)
    report = json.loads(report_path.read_text())
    required = review.get('required_checks', [])
    checks = review.get('checks', {})
    if (review.get('version') != 1 or review.get('run') != name or
            review.get('file') != str(episode / batch['source']['path']) or
            review.get('sha256') != batch['source']['sha256'] or
            review.get('report_sha256') != batch['report']['sha256'] or
            review.get('verdict') != 'PASS' or review.get('freshness') != 'CURRENT' or
            not isinstance(required, list) or not required or
            not {'stream_metadata', 'full_decode', 'frame_sampling'}.issubset(required) or
            not set(batch['required_review_checks']).issubset(required) or
            any(checks.get(k) != 'PASS' for k in required) or
            any(v == 'FAIL' for v in checks.values()) or
            not review.get('reviewer') or review.get('writer_finished') is not True or
            review.get('reconstruction_verified') is not True or
            report['technical_status'] != 'PASS' or report['failures'] or report['policy_failures'] or
            report['reported_freshness'].get('status') != 'CURRENT' or
            report['checks'].get('full_decode') != 'PASS' or
            report['checks'].get('frame_extraction') != 'PASS'):
        raise ValueError('QA acceptance/freshness/required coverage is unresolved')
    if set(review.get('inspected_frame_indices', [])) != set(report['requested_frame_indices']):
        raise ValueError('Actual review must cover the full requested selection')
    # Keep real evidence, not only an assertion. It includes edit binding and reconstruction proof.
    evidence = review.get('evidence', [])
    if not evidence or not review.get('retain_indices'):
        raise ValueError('Retained evidence and selected real frames are required')
    proofs = [{'path': rel, **w.snapshot(edit_path(episode, rel))} for rel in evidence]
    proofs.append({'path': review_rel, **review_record})
    selected = set(review['retain_indices'])
    if not selected.issubset(f['index'] for f in batch['frames']):
        raise ValueError('Unknown retained frame index')
    inputs = {str(episode / r['path']): r['identity']
              for r in [batch['report'], batch['source'], *recipe_records, *proofs]}
    inputs.update(audit['inputs'])
    # Other managed consumers are protected even when they are not Palmier imports.
    candidates = {f['path'] for f in batch['frames']}
    consumer_holds = set()
    for other in (episode / 'Work').glob('*/manifest.json'):
        if other == manifest:
            continue
        w.inventory.no_symlinks(other)
        rec = w.snapshot(other)
        data = json.loads(other.read_text())
        def strings(value):
            if isinstance(value, str):
                yield value
            elif isinstance(value, dict):
                for v in value.values(): yield from strings(v)
            elif isinstance(value, list):
                for v in value: yield from strings(v)
        mentions = set(strings(data))
        consumer_holds.update(rel for rel in candidates if rel in mentions or str(episode / rel) in mentions)
        inputs[str(other)] = rec['identity']
    previous = batch.get('finalization')
    binding = {'review': {'path': review_rel, **review_record}, 'evidence': proofs}
    if previous and previous['binding'] != binding:
        raise ValueError('Finalization evidence changed; cannot resume')
    archive = edit_path(episode, f'Edit/QA-Retention/{name}')
    retained = []
    if previous:
        for record in previous['retained']:
            w.unchanged(episode / record['path'], record)
        retained = previous['retained']
    # Validate all before removing anything. Missing files are allowed only with our durable prepare event.
    log = episode / 'Edit/MediaLifecycle/locations.jsonl'
    w.inventory.no_symlinks(log)
    prepared = set()
    if log.exists():
        with log.open() as stream:
            for line in stream:
                event = json.loads(line)
                if (event.get('action') == 'delete_qa_frame' and event.get('run') == name
                        and event.get('state') == 'prepared'):
                    prepared.add((event.get('path'), event.get('sha256')))
    covered = {row['path']: row for row in audit['files']}
    rows, kept = [], []
    for frame in batch['frames']:
        file = w.inventory.relative_path(episode, frame['path'])
        if frame.get('removed_utc'):
            if file.exists(): raise ValueError('Removed QA path was recreated')
            continue
        if not file.exists() and previous and (frame['path'], frame['sha256']) in prepared:
            rows.append(frame)
            continue
        w.unchanged(file, frame)
        try:
            row = covered.get(frame['path'])
            w.check_unreferenced({'files': [row] if row else []}, frame['path'])
            if frame['path'] in consumer_holds:
                raise ValueError('Referenced by another managed run')
        except ValueError as error:
            kept.append({'path': frame['path'], 'reason': str(error)})
            continue
        rows.append(frame)
    result = {'execute': execute, 'files': len(rows),
              'logical_bytes': sum(f['identity']['bytes'] for f in rows),
              'kept': kept,
              'physical_reclaimable_bytes': None}
    if not execute:
        return result
    if not previous:
        if archive.exists(): raise ValueError('Unowned retention directory exists')
        archive.mkdir(parents=True)
        for frame in batch['frames']:
            if frame['index'] in selected:
                dest = archive / f"{frame['index']:09d}.png"
                w.copy_verified(episode / frame['path'], dest)
                retained.append({'path': str(dest.relative_to(episode)), **w.snapshot(dest)})
        # Durable preparation precedes the first unlink. Records/maps stay at their original Edit paths.
        batch['finalization'] = {'binding': binding, 'retained': retained, 'state': 'prepared'}
        w.save(manifest, run)
    inputs[str(manifest)] = w.inventory.identity(manifest)
    for record in retained:
        inputs[str(episode / record['path'])] = record['identity']
    # The lifecycle journal is an audit input, but this operation appends to it
    # after every unlink. Verify its scanned identity once before removal, then
    # exclude our own expected journal writes from per-file dependency checks.
    journal_identity = inputs.pop(str(log), None)
    if journal_identity is not None and w.inventory.identity(log) != journal_identity:
        raise ValueError('Lifecycle journal changed before QA frame removal')
    try:
        for frame in rows:
            for dep, before in inputs.items():
                if w.inventory.identity(Path(dep)) != before:
                    raise ValueError('Dependency/evidence metadata changed; remaining frames preserved')
            file = w.inventory.relative_path(episode, frame['path'])
            event = {'action': 'delete_qa_frame', 'run': name, 'path': frame['path'],
                     'sha256': frame['sha256'], 'bytes': frame['identity']['bytes']}
            if file.exists():
                w.unchanged(file, frame)
                w.journal(episode, {**event, 'state': 'prepared'})
                file.unlink()
            frame['removed_utc'] = w.inventory.now()
            w.journal(episode, {**event, 'state': 'complete'})
        batch['finalization']['state'] = 'complete'
        batch['finalization']['result'] = result
    finally:
        w.save(manifest, run)
    return result
