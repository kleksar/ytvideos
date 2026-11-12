#!/usr/bin/env python3
"""Generate centered, aspect-aware Palmier keyframes for a specific 1.05x CSV.

Does not connect to Palmier. Creates new files only; never overwrites output.
"""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

from PIL import Image

EDIT = Path(__file__).resolve().parent
VALIDATOR = EDIT / 'palmier_recut_105_provisional.py'
spec = importlib.util.spec_from_file_location('recut_validator', VALIDATOR)
recut = importlib.util.module_from_spec(spec)
spec.loader.exec_module(recut)


def digest(path):
    return recut.sha256(path)


def key(w, h, zoom):
    """Cover canvas preserving aspect ratio; place center at (0.5, 0.5).

    width, height and top-left coordinates are normalized to canvas axes.
    Rounding is done after geometry and checked again for uncovered canvas.
    """
    aspect_relative = (w * recut.HEIGHT) / (h * recut.WIDTH)
    cover_w = max(1.0, aspect_relative)
    cover_h = max(1.0, 1.0 / aspect_relative)
    width, height = round(cover_w * zoom, 8), round(cover_h * zoom, 8)
    x, y = round((1.0 - width) / 2.0, 8), round((1.0 - height) / 2.0, 8)
    recut.check(x <= 0 and y <= 0 and x + width >= 1 and y + height >= 1, 'Keyframe fails canvas coverage')
    recut.check(abs((x + width / 2) - .5) < 1e-7 and abs((y + height / 2) - .5) < 1e-7, 'Keyframe fails centering')
    return width, height, x, y


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--map', required=True, help='Absolute CSV path of the final 1.05x map')
    ap.add_argument('--output', required=True, help='New keyframes JSON path; metadata is written beside it')
    ap.add_argument('--min-zoom', type=float, default=1.01, help='Relative to aspect-preserving cover size; default 1.01')
    ap.add_argument('--max-zoom', type=float, default=1.035, help='Relative to aspect-preserving cover size; default 1.035')
    a = ap.parse_args()
    recut.check(1.0 <= a.min_zoom < a.max_zoom <= 1.04, 'Zoom must satisfy 1.0 <= min < max <= 1.04')
    path = Path(a.map)
    out = Path(a.output)
    recut.check(path.is_absolute() and path.is_file(), 'Map must be an existing absolute file')
    recut.check(out.is_absolute() and out.suffix.lower() == '.json', 'Output must be an absolute .json path')
    meta = out.with_name(out.stem + '.metadata.json')
    recut.check(out.parent.is_dir() and not out.exists() and not meta.exists(), 'Output parent must exist and output/metadata must be new')
    map_hash = digest(path)
    rows = recut.read_map(path)
    hashes = {p: digest(p) for p in sorted({r['image_path'] for r in rows})}
    sizes = {}
    for p in hashes:
        with Image.open(p) as im:
            im.verify()
        with Image.open(p) as im:
            recut.check(im.getexif().get(274, 1) == 1, f'Non-default EXIF orientation requires manual review: {p}')
            sizes[p] = im.size
        recut.check(all(v > 0 for v in sizes[p]), f'Invalid image dimensions: {p}')
    animations, metadata_rows = {}, []
    for r in rows:
        shot = r['shot']; duration = r['duration_frames']; w, h = sizes[r['image_path']]
        first, last = (a.min_zoom, a.max_zoom) if shot % 2 else (a.max_zoom, a.min_zoom)
        s1, h1, x1, y1 = key(w, h, first)
        s2, h2, x2, y2 = key(w, h, last)
        animations[str(shot)] = {
            'scale': [[0, s1, h1, 'smooth'], [duration-1, s2, h2, 'smooth']],
            'position': [[0, x1, y1, 'smooth'], [duration-1, x2, y2, 'smooth']],
        }
        # Fraction of the image removed in the worst crop direction at the larger zoom.
        max_width, max_height, _, _ = key(w,h,a.max_zoom)
        crop = max(1.0 - 1.0 / max_width, 1.0 - 1.0 / max_height)
        metadata_rows.append({'clip':shot, 'image_path':r['image_path'], 'image_dimensions':[w,h], 'duration_frames':duration,
                              'crop_fraction_max_axis':round(crop,6), 'review_crop':crop>0.20})
    recut.check(digest(path) == map_hash and all(digest(p) == v for p,v in hashes.items()), 'Map or image changed while generating')
    payload = (json.dumps(animations, ensure_ascii=False, indent=2) + '\n').encode('utf-8')
    manifest = {'map':str(path.resolve()), 'map_sha256':map_hash, 'keyframes_sha256':hashlib.sha256(payload).hexdigest(),
                'canvas':[recut.WIDTH,recut.HEIGHT], 'fps':recut.FPS, 'frame_range':[recut.START,recut.TOTAL],
                'clip_count':len(rows), 'unique_images':len(hashes), 'image_sha256':hashes,
                'provisional_clips':[r['shot'] for r in rows if r['status'] == 'provisional'],
                'zoom_relative_to_cover':[a.min_zoom,a.max_zoom], 'shots':metadata_rows,
                'warning':'Geometry follows documented MCP scale and top-left position coordinates; renderer output, clip edges, and sync must be checked visually on a copy. Review clips with significant crop. Rebuild if map or media changes.'}
    # Exclusive create avoids replacing existing work; on failure do not delete a pre-existing file.
    created_output = False
    try:
        with out.open('xb') as f:
            created_output = True
            f.write(payload)
        recut.read_keyframes(out, rows)
        with meta.open('x', encoding='utf-8') as f:
            json.dump(manifest, f, ensure_ascii=False, indent=2); f.write('\n')
    except Exception:
        if created_output and out.exists():
            out.unlink()
        raise
    print(json.dumps({'keyframes':str(out), 'metadata':str(meta), 'map_sha256':map_hash, 'keyframes_sha256':manifest['keyframes_sha256'], 'clips':len(rows), 'provisional':len(manifest['provisional_clips']), 'crop_review_clips':sum(x['review_crop'] for x in metadata_rows)},ensure_ascii=False))

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f'STOP: {e}', file=sys.stderr)
        sys.exit(1)
