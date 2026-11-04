"""Build local thumbnail QA crops; never modifies source or uploads anything. Requires Pillow."""
import argparse
import hashlib
import json
from pathlib import Path
from PIL import Image, ImageOps


def ratio(value):
    try:
        a, b = map(int, value.split(':'))
    except ValueError as exc:
        raise argparse.ArgumentTypeError('Use a positive integer ratio, e.g. 2:3') from exc
    if a <= 0 or b <= 0:
        raise argparse.ArgumentTypeError('Ratio values must be positive')
    return a / b


def center_box(size, target):
    w, h = size
    cw, ch = min(w, h * target), min(h, w / target)
    return ((w-cw)/2, (h-ch)/2, (w+cw)/2, (h+ch)/2)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('image', type=Path)
    p.add_argument('--out', type=Path, required=True)
    p.add_argument('--widths', type=int, nargs='+', default=[360, 180])
    p.add_argument('--crops', nargs='*', default=['2:3'])
    p.add_argument('--regions', type=Path, help='JSON: regions [{label, box:[left,top,right,bottom]}], normalized 0..1')
    a = p.parse_args()
    if any(w <= 0 for w in a.widths):
        p.error('Widths must be positive')
    source = a.image.resolve()
    a.out.mkdir(parents=True, exist_ok=True)
    if a.out.resolve() == source.parent and source.name.startswith('qa_'):
        p.error('Use a separate output directory')
    with Image.open(source) as raw:
        im = ImageOps.exif_transpose(raw).convert('RGB')
    regions = json.loads(a.regions.read_text())['regions'] if a.regions else []
    for r in regions:
        l, t, rr, b = r['box']
        if not (0 <= l < rr <= 1 and 0 <= t < b <= 1):
            p.error('Region coordinates must be normalized, ordered and inside the source')
    report = {'source': str(source), 'sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
              'source_pixels': list(im.size), 'previews': [],
              'limits': 'Local simulation only. Region containment uses supplied bounds, not OCR or face detection. Visual readability, actual device and YouTube display require separate observation.'}
    variants = [('full', (0, 0, *im.size))]
    try:
        variants += [(r.replace(':', 'x'), center_box(im.size, ratio(r))) for r in a.crops]
    except argparse.ArgumentTypeError as exc:
        p.error(str(exc))
    for label, box in variants:
        cw, ch = box[2]-box[0], box[3]-box[1]
        checks = []
        for r in regions:
            l,t,rr,b = [v*im.size[i % 2] for i,v in enumerate(r['box'])]
            margins = [l-box[0], t-box[1], box[2]-rr, box[3]-b]
            checks.append({'label':r['label'], 'contained':min(margins)>=0,
                           'margins_source_px':margins})
        for width in a.widths:
            height = round(width*ch/cw)
            dest = a.out / f'qa_{label}_{width}x{height}.jpg'
            if dest.resolve() == source:
                p.error('Refusing to overwrite source')
            # Crop and resample for inspection; never stretch a source into another ratio.
            im.resize((width,height),Image.Resampling.LANCZOS,box=box).save(dest,quality=95,subsampling=0)
            report['previews'].append({'path':str(dest), 'pixels':[width,height],
                                       'crop_box_source_px':list(box), 'regions':checks})
    (a.out/'manifest.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'previews':len(report['previews']), 'source_pixels':im.size,
                      'all_declared_regions_contained':all(c['contained'] for v in report['previews'] for c in v['regions']) if regions else None}))


if __name__ == '__main__':
    main()
