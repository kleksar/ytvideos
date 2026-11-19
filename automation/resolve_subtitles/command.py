"""One command: offline plan, or exact-target native CC candidate via official MCP."""
import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path

from planning import plan_subtitles
from mcp import ResolveMCP


def sha(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda: stream.read(1024*1024), b''):
            h.update(block)
    return h.hexdigest()


def unpack(response):
    value = response.get('structuredContent')
    if value is None:
        texts = [x['text'] for x in response.get('content', []) if x.get('type') == 'text']
        if len(texts) != 1:
            raise RuntimeError('Unknown official run_script result envelope')
        value = json.loads(texts[0])
    if isinstance(value, dict) and isinstance(value.get('result'), dict):
        value = value['result']
    if not isinstance(value, dict):
        raise RuntimeError('Native result must be a structured object')
    return value


def script_call(client, expression):
    source = Path(__file__).with_name('native.py').read_text()
    return unpack(client.run(source+'\nresult = '+expression+'\n'))


def target_native(target):
    result = dict(target)
    fps = Fraction(target['fps'])
    # No rounded 29.97 alias for 30000/1001: runtime must report exact rate.
    result['native_fps_values'] = [str(fps)]
    if fps.denominator == 1:
        result['native_fps_values'].append(str(float(fps)))
    return result


def validate_voice(request, snapshot):
    """Bind alignments to exact enabled TimelineItems and immutable source files.

    First native adapter intentionally accepts untrimmed unity-rate narration.
    Planner supports retimes, but that is not proof of native speed readback.
    """
    seen = {item['id']:item for item in snapshot['voice']}
    if len(seen) != len(snapshot['voice']):
        raise ValueError('Ambiguous native audio item identity')
    expected = request.get('native_snapshot')
    if expected != snapshot:
        raise ValueError('Exact saved native_snapshot required; inspect first and align that narration')
    hashes = {}
    for placement in request['placements']:
        item = seen.get(placement['id'])
        if not item or not item['enabled']:
            raise ValueError('Narration placement missing or disabled')
        if Fraction(str(placement['speed'])) != 1 or Fraction(str(placement['source_in'])) != 0 or item['left'] != 0:
            raise ValueError('Native trim/speed verification not supported yet; planner output alone is insufficient')
        if (item['start'],item['end']) != (placement['timeline_start'],placement['timeline_end']):
            raise ValueError('On-timeline narration placement changed')
        if not item['path']:
            raise ValueError('Narration source unavailable')
        digest = sha(item['path'])
        if digest != placement['source_sha256']:
            raise ValueError('Final narration source hash differs from alignment')
        hashes[item['path']] = digest
    return hashes


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('request', type=Path)
    parser.add_argument('--output', type=Path, required=True)
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--inspect', action='store_true', help='Read exact current native target; no edits')
    group.add_argument('--apply-native-cc', action='store_true', help='Create isolated editable CC candidate; does not install branded screen captions')
    parser.add_argument('--exclusive-session', action='store_true', help='Coordinator has granted sole access to this Resolve instance')
    args = parser.parse_args(argv)
    request = json.loads(args.request.read_text())
    args.output.mkdir(parents=True, exist_ok=True)
    if (args.inspect or args.apply_native_cc) and not args.exclusive_session:
        parser.error('Native operations require an explicitly granted exclusive session')
    plan = None if args.inspect else plan_subtitles(request)
    if plan:
        (args.output/'plan.json').write_text(json.dumps(plan, indent=2, ensure_ascii=False)+'\n')
        (args.output/'captions.en.srt').write_text(plan['srt'])
    if not (args.inspect or args.apply_native_cc):
        print('PLAN ONLY: native authoring/playback/style are UNVERIFIED')
        return 0
    target = target_native(request['target'] if args.inspect else plan['target'])
    client = ResolveMCP(timeout=75)
    try:
        (args.output/'mcp-capabilities.json').write_text(json.dumps(client.tools, indent=2))
        before = script_call(client, 'snapshot(resolve, '+repr(target)+')')
        if args.inspect:
            (args.output/'native-snapshot.json').write_text(json.dumps(before, indent=2))
            print('READBACK ONLY: align final source audio and preserve this exact native_snapshot')
            return 0
        (args.output/'position-api.json').write_text(json.dumps(client.position_api(), indent=2))
        hashes = validate_voice(request, before)
        payload = json.dumps({'plan':plan,'native_snapshot':before}, sort_keys=True, ensure_ascii=False)
        token = 'ytv-native-cc-v1:'+hashlib.sha256(payload.encode()).hexdigest()
        name = 'Native CC candidate '+token[-16:]
        expected = [(c['spoken_start_frame'], c['spoken_end_frame'], c['text']) for c in plan['cues']]
        srt = str((args.output/'captions.en.srt').resolve())
        expression = 'install(resolve, '+', '.join(repr(v) for v in (target,before,expected,srt,name,token))+')'
        receipt = script_call(client, expression)
        if receipt.get('status') not in ('CREATED','UNCHANGED') or receipt.get('native_cues') != len(expected):
            raise RuntimeError('Native installation did not return verified cue readback')
        if any(sha(path) != digest for path,digest in hashes.items()):
            raise RuntimeError('Narration source changed during authoring; candidate requires review')
        receipt.update(source_hashes=hashes, conform_sha256=plan['conform_sha256'],
                       render=False, published=False, visual='UNVERIFIED', playback='UNVERIFIED',
                       branded_style='NOT_APPLIED', source_timeline_preserved=True)
        (args.output/'native-receipt.json').write_text(json.dumps(receipt, indent=2)+'\n')
        print(json.dumps(receipt, ensure_ascii=False))
    finally:
        client.close()
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
