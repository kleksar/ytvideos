"""Check assembled text and explicit protected substrings; no network or writes."""
import argparse
import difflib
import hashlib
import json
from pathlib import Path


def validate(text, manifest, baseline=None):
    errors = []
    if not text.strip():
        errors.append('Description is empty')
    if len(text.encode('utf-8')) > 5000:
        errors.append('Description exceeds 5000 UTF-8 bytes')
    if '<' in text or '>' in text:
        errors.append('Description contains a forbidden angle bracket')
    protected, positions, labels = [], [], set()
    for block in manifest.get('blocks', []):
        label, value = block['label'], block['text']
        expected = block.get('occurrences', 1)
        if label in labels or not value or not isinstance(expected, int) or expected < 1:
            errors.append(f'Invalid/duplicate protected block: {label}')
            continue
        labels.add(label)
        count = text.count(value)
        if count != expected:
            errors.append(f'{label}: expected {expected} exact occurrence(s), found {count}')
        if baseline is not None and baseline.count(value) != expected:
            errors.append(f'{label}: baseline does not match the declared protection')
        positions.append(text.find(value))
        protected.append({'label': label, 'expected': expected, 'actual': count,
                          'sha256': hashlib.sha256(value.encode('utf-8')).hexdigest()})
    if manifest.get('preserve_order') and positions != sorted(positions):
        errors.append('Protected blocks are out of the declared order')
    result = {'valid': not errors, 'errors': errors, 'characters': len(text),
              'utf8_bytes': len(text.encode('utf-8')), 'protected_blocks': protected,
              'limits': 'Mechanical checks only: no factual, timing, URL, media or live-display validation.'}
    if baseline is not None:
        result['changed'] = text != baseline
        result['diff'] = ''.join(difflib.unified_diff(baseline.splitlines(True), text.splitlines(True),
                                                  fromfile='before', tofile='proposed'))
    return result


def read_exact(path):
    return Path(path).read_bytes().decode('utf-8')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('description')
    parser.add_argument('--baseline')
    parser.add_argument('--protected-blocks', help='JSON with blocks and optional preserve_order')
    args = parser.parse_args()
    manifest = json.loads(read_exact(args.protected_blocks)) if args.protected_blocks else {}
    result = validate(read_exact(args.description), manifest,
                      read_exact(args.baseline) if args.baseline else None)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(0 if result['valid'] else 1)


if __name__ == '__main__':
    main()
