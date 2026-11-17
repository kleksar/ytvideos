#!/usr/bin/env python3
"""Validate preserved reference evidence without network or image dependencies."""
import hashlib
import json
from pathlib import Path
import struct


def verify(root):
    root = Path(root)
    rows = json.loads((root / 'source_passport.json').read_text())
    indexed = {r['frame_file']: r for r in rows}
    assert len(rows) == len(indexed) == 11, 'expected 11 distinct source frames'
    assert {p.relative_to(root).as_posix() for p in (root / 'originals').glob('*.png')} == set(indexed)
    profiles = {'Mind': {12, 23, 43, 62, 105, 178}, 'Everyone': {16, 28, 46, 82, 190}}
    for profile, times in profiles.items():
        assert {r['seek_seconds'] for r in rows if r['profile'] == profile} == times
    for name, row in indexed.items():
        raw = (root / name).read_bytes()
        assert hashlib.sha256(raw).hexdigest() == row['frame_sha256'], name + ': hash mismatch'
        assert raw[:8] == b'\x89PNG\r\n\x1a\n'
        assert struct.unpack('>II', raw[16:24]) == (1920, 1080), name + ': dimensions'
        assert len(row['source_mp4_sha256']) == 64
        assert 'NOT imagegen original' in row['origin']
    for crop in json.loads((root / 'crop_manifest.json').read_text()):
        assert 'originals/' + crop['source'] in indexed
        assert (root / 'collages' / (crop['sheet'] + '.jpg')).is_file()
        if crop['crop_box']:
            x0, y0, x1, y1 = crop['crop_box']
            assert 0 <= x0 < x1 <= 1920 and 0 <= y0 < y1 <= 1080
    lock = json.loads((root / 'reference-lock.example.json').read_text())
    assert lock['status'] == 'example_not_episode_approval'
    assert lock['character_profile'] == 'mind-stick'
    for ref in lock['references']:
        assert ref['sha256'] == indexed[ref['file']]['frame_sha256']
    print('PASS: 11 source frames, passport hashes, dimensions, crop map and example lock')


if __name__ == '__main__':
    verify(Path(__file__).resolve().parent)
