"""Offline plan or one bounded batch of independent native Text+ phrase clips."""
import argparse
import json
from pathlib import Path

from command import candidate_token, sha, target_native, unpack, validate_voice
from mcp import ResolveMCP
from phrase_plan import phrase_layout, write_comps


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('request', type=Path)
    parser.add_argument('--output', type=Path, required=True)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument('--batch-start', type=int)
    mode.add_argument('--finalize', action='store_true')
    parser.add_argument('--batch-size', type=int, default=5)
    parser.add_argument('--exclusive-session', action='store_true')
    args = parser.parse_args(argv)
    active = args.batch_start is not None or args.finalize
    if active and not args.exclusive_session:
        parser.error('Explicit exclusive native slot required')
    if not 1 <= args.batch_size <= 5 or (args.batch_start is not None and args.batch_start < 0):
        parser.error('Batch start must be nonnegative and size 1..5')
    request = json.loads(args.request.read_text())
    layout = phrase_layout(request)
    data = request['native_titles']
    tracks = data.get('replace_tracks')
    if not isinstance(tracks, list) or any(type(t) is not int or t < 1 for t in tracks) or len(set(tracks)) != len(tracks):
        raise ValueError('Explicit old-caption replacement video track list required')
    source = request['native_snapshot']
    for track in tracks:
        if track > len(source['picture']):
            raise ValueError('Replacement track absent from inspected source')
    # No raw comp file from an outside source is executed: exact known template only.
    template_sha = sha(Path(__file__).with_name('phrase_template.comp'))
    engine_sha = sha(Path(__file__).with_name('phrase_native.py'))
    identity = {'layout': layout, 'replace_tracks': tracks, 'template': template_sha,
                'engine': engine_sha, 'display_evidence': data['display_evidence']}
    token = candidate_token(identity, source).replace('ytv-native-cc-v1:', 'ytv-phrase-titles-v1:')
    name = 'Native phrase titles ' + token[-16:]
    args.output.mkdir(parents=True, exist_ok=True)
    paths = write_comps(layout, args.output / ('comps-' + token[-16:]))
    manifest = dict(token=token, candidate_name=name, layout=layout,
                    comps=[{'path': p, 'sha256': sha(p)} for p in paths],
                    style='CALIBRATED_RECIPE_ONLY', playback='UNVERIFIED', inspector='UNVERIFIED')
    (args.output/'phrase-plan.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2))
    if not active:
        print('PLAN ONLY: no app connection or native change')
        return 0
    target = target_native(request['target'])
    review = data.get('native_review', {})
    if args.finalize:
        if review.get('token') != token or not review.get('candidate_id') or not review.get('source') or not all(review.get(k) is True for k in ('visual', 'playback', 'independent_edit_move_restore', 'style')):
            raise ValueError('Exact candidate native review required before obsolete carrier removal')
    client = ResolveMCP(timeout=75)
    receipt_path = args.output/'phrase-receipt.json'
    try:
        code = '\n'.join(Path(__file__).with_name(name).read_text() for name in ('native.py', 'branded_native.py', 'phrase_native.py'))
        before = unpack(client.run(code+'\nresult = snapshot(resolve, '+repr(target)+')'))
        hashes = validate_voice(request, before)
        replace_ids = {t: [row[0] for row in before['picture'][t-1]] for t in tracks}
        arguments = (target, before, layout, paths, name, token, replace_ids)
        if args.finalize:
            observed = unpack(client.run(code + '\np = resolve.GetProjectManager().GetCurrentProject()\nresult = {"ids": [p.GetTimelineByIndex(i).GetUniqueId() for i in range(1, p.GetTimelineCount()+1) if p.GetTimelineByIndex(i).GetName() == ' + repr(name) + ']}\n'))
            if observed.get('ids') != [review['candidate_id']]:
                raise ValueError('Reviewed candidate identity changed')
        if args.finalize:
            expression = 'finalize_phrase_candidate(resolve, ' + ', '.join(repr(x) for x in arguments) + ')'
        else:
            arguments += (data['insertion_timecode'], args.batch_start, args.batch_size)
            expression = 'install_phrase_batch(resolve, ' + ', '.join(repr(x) for x in arguments) + ')'
        receipt_path.write_text(json.dumps(dict(status='IN_PROGRESS', token=token, candidate_name=name)))
        try:
            receipt = unpack(client.run(code+'\nresult = '+expression+'\n'))
            if any(sha(p) != digest for p, digest in hashes.items()):
                raise RuntimeError('Final narration source changed during authoring')
        except Exception as exc:
            receipt_path.write_text(json.dumps(dict(status='UNKNOWN', token=token, candidate_name=name,
                error=str(exc), next='Inspect owned candidate before retrying. Never recreate unknown state.'), indent=2))
            raise
        receipt.update(native_review=review if args.finalize else None, token=token, source_hashes=hashes, render=False, published=False,
                       inspector='UNVERIFIED', playback='UNVERIFIED', visual='UNVERIFIED')
        receipt_path.write_text(json.dumps(receipt, ensure_ascii=False, indent=2))
        print(json.dumps(receipt, ensure_ascii=False))
    finally:
        client.close()
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
