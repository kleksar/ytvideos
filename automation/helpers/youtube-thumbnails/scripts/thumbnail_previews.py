"""Build local thumbnail QA crops; never modifies source or uploads anything. Requires Pillow."""
import argparse
import base64
import hashlib
import html
import io
import json
import re
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


def load_cards(input_path, main_image):
    data = json.loads(input_path.read_text(encoding='utf-8'))
    if not isinstance(data, dict):
        raise ValueError('Input JSON must be an object')
    allowed = {'title', 'channel', 'duration', 'metadata', 'neighbors'}
    if set(data) - allowed:
        raise ValueError(f'Unknown card fields: {sorted(set(data) - allowed)}')
    neighbors = data.get('neighbors', [])
    if not isinstance(neighbors, list) or len(neighbors) > 6:
        raise ValueError('neighbors must be a list of at most 6 cards')
    base = input_path.resolve().parent
    primary = {k: v for k, v in data.items() if k != 'neighbors'}
    primary['image'] = str(main_image)
    cards = [primary] + neighbors
    sources = []
    for index, card in enumerate(cards):
        if not isinstance(card, dict):
            raise ValueError('Each card must be an object')
        fields = {'image', 'title', 'channel', 'duration', 'metadata'} if index else allowed - {'neighbors'} | {'image'}
        if set(card) - fields:
            raise ValueError(f'Unknown card fields: {sorted(set(card) - fields)}')
        for key in ('title', 'channel', 'image'):
            if not isinstance(card.get(key), str) or not card[key].strip():
                raise ValueError(f'{key} must be a non-empty string')
        if len(card['title']) > 300 or len(card['channel']) > 120:
            raise ValueError('title or channel is too long')
        if 'duration' in card and (not isinstance(card['duration'], str) or not re.fullmatch(r'(?:\d{1,2}:)?[0-5]?\d:[0-5]\d', card['duration'])):
            raise ValueError('duration must use M:SS or H:MM:SS format')
        src = (base / card['image']).resolve()
        if not src.is_file():
            raise ValueError(f'image file not found: {card["image"]}')
        digest = hashlib.sha256(src.read_bytes()).hexdigest()
        with Image.open(src) as raw:
            im = ImageOps.exif_transpose(raw).convert('RGB')
            im.thumbnail((1000, 563), Image.Resampling.LANCZOS)
            buf = io.BytesIO()
            im.save(buf, format='JPEG', quality=88)
        metadata = card.get('metadata', {})
        if not isinstance(metadata, dict):
            raise ValueError('metadata must be an object')
        allowed_meta = {'views', 'published'}
        if set(metadata) - allowed_meta:
            raise ValueError(f'Unknown metadata fields: {sorted(set(metadata) - allowed_meta)}')
        if any(not isinstance(v, str) or not v.strip() for v in metadata.values()):
            raise ValueError('metadata values must be non-empty strings')
        details = ' · '.join(html.escape(metadata[k]) for k in ('views', 'published') if k in metadata)
        duration = html.escape(card['duration']) if 'duration' in card else ''
        sources.append({'src': src, 'sha256': digest, 'image_data': base64.b64encode(buf.getvalue()).decode('ascii'),
                        'width': im.width, 'height': im.height, 'title': card['title'], 'channel': card['channel'],
                        'duration': duration or None, 'details': details})
    return sources


def render_section(cards, theme):
    rendered = []
    for card in cards:
        duration = f'<span class="duration">{card["duration"]}</span>' if card['duration'] else ''
        omitted = ' · duration omitted' if not card['duration'] else ''
        rendered.append(f'''<article><div class="thumb" style="aspect-ratio:{card['width']}/{card['height']}"><img src="data:image/jpeg;base64,{card['image_data']}" alt="">{duration}</div>
<div class="info"><strong>{html.escape(card['title'])}</strong><div class="channel">{html.escape(card['channel'])}</div><div class="meta">{card['details']}</div><div class="prov">LOCAL MOCK · {html.escape(card['src'].name)} · SHA-256 {card['sha256']}{omitted}</div></div></article>''')
    bg, fg, muted = ('#181818', '#f1f1f1', '#aaa') if theme == 'dark' else ('#fff', '#0f0f0f', '#606060')
    return f'''<section class="theme-{theme}" style="background:{bg};color:{fg};--muted:{muted}"><h2>{theme.title()} theme · LOCAL MOCK</h2><div class="grid">{''.join(rendered)}</div></section>'''


def build_card_html(cards, theme, grayscale):
    themes = ('light', 'dark') if theme == 'both' else (theme,)
    sections = ''.join(render_section(cards, t) for t in themes)
    fg = '''body{margin:0}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,360px));gap:24px}article{min-width:0}.thumb{position:relative;background:#777;overflow:hidden;border-radius:10px}.thumb img{width:100%;height:100%;display:block;''' + ('filter:grayscale(1);' if grayscale else '') + '''}.duration{position:absolute;right:6px;bottom:6px;background:#111d;color:#fff;padding:3px 5px;border-radius:3px;font-weight:bold}.info{padding-top:9px}strong{font-size:16px;line-height:1.35;display:block}.channel,.meta,.prov{margin-top:5px;color:var(--muted)}.prov{font-size:10px;overflow-wrap:anywhere}section{padding:24px;margin-bottom:24px;font:14px Arial,sans-serif}'''
    return f'<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>Local thumbnail QA mock</title><style>{fg}</style><body><p>Illustrative local QA layout; not YouTube UI</p>{sections}</body></html>'


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('image', type=Path)
    p.add_argument('--out', type=Path, required=True)
    p.add_argument('--widths', type=int, nargs='+', default=[360, 180])
    p.add_argument('--crops', nargs='*', default=['2:3'])
    p.add_argument('--regions', type=Path, help='JSON: regions [{label, box:[left,top,right,bottom]}], normalized 0..1')
    p.add_argument('--card-json', type=Path, help='JSON with required title/channel, optional duration/metadata {views,published}, and up to 6 neighbors [{image,title,channel,duration,metadata}]. Neighbor image paths are relative to this JSON.')
    p.add_argument('--theme', choices=['both', 'light', 'dark'], default='both', help='Local mock color theme')
    p.add_argument('--grayscale', action='store_true', help='Apply grayscale diagnostic filter to mock thumbnails')
    a = p.parse_args()
    if any(w <= 0 for w in a.widths):
        p.error('Widths must be positive')
    source = a.image.resolve()
    if not source.is_file():
        p.error(f'Image file not found: {source}')
    with Image.open(source) as raw:
        im = ImageOps.exif_transpose(raw).convert('RGB')
    try:
        regions_data = json.loads(a.regions.read_text(encoding='utf-8')) if a.regions else {}
        regions = regions_data.get('regions', [])
        if not isinstance(regions, list):
            raise ValueError('regions must be a list')
    except (OSError, json.JSONDecodeError, AttributeError, ValueError) as exc:
        p.error(f'Invalid regions input: {exc}')
    for r in regions:
        try:
            left, top, right, bottom = r['box']
        except (KeyError, TypeError, ValueError):
            p.error('Each region requires box [left,top,right,bottom]')
        if not isinstance(r.get('label'), str) or not r['label'].strip():
            p.error('Each region requires a non-empty label')
        if any(isinstance(v, bool) or not isinstance(v, (int, float)) for v in (left, top, right, bottom)):
            p.error('Region coordinates must be numbers')
        if not (0 <= left < right <= 1 and 0 <= top < bottom <= 1):
            p.error('Region coordinates must be normalized, ordered and inside the source')
    try:
        cards = load_cards(a.card_json, source) if a.card_json else []
    except (ValueError, OSError, json.JSONDecodeError) as exc:
        p.error(str(exc))
    variants = [('full', (0, 0, *im.size))]
    try:
        variants += [(r.replace(':', 'x'), center_box(im.size, ratio(r))) for r in a.crops]
    except argparse.ArgumentTypeError as exc:
        p.error(str(exc))
    output_targets = [(a.out.resolve() / 'manifest.json').resolve()]
    for label, box in variants:
        cw, ch = box[2]-box[0], box[3]-box[1]
        for width in a.widths:
            output_targets.append((a.out.resolve() / f'qa_{label}_{width}x{round(width*ch/cw)}.jpg').resolve())
    if a.card_json:
        output_targets.append((a.out.resolve() / 'qa_cards.html').resolve())
    input_paths = [source]
    if a.card_json:
        input_paths += [a.card_json.resolve()] + [c['src'].resolve() for c in cards]
    if a.regions:
        input_paths.append(a.regions.resolve())
    collisions = set(output_targets) & set(input_paths)
    if collisions:
        p.error(f'Refusing to overwrite input: {sorted(map(str, collisions))}')
    a.out.mkdir(parents=True, exist_ok=True)
    if a.card_json:
        (a.out / 'qa_cards.html').write_text(build_card_html(cards, a.theme, a.grayscale), encoding='utf-8')
    report = {'source': str(source), 'sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
              'source_pixels': list(im.size), 'previews': [],
              'limits': 'Local simulation only. Region containment uses supplied bounds, not OCR or face detection. Visual readability, actual device and YouTube display require separate observation.'}
    for label, box in variants:
        cw, ch = box[2]-box[0], box[3]-box[1]
        checks = []
        for r in regions:
            left, top, right, bottom = [v*im.size[i % 2] for i,v in enumerate(r['box'])]
            margins = [left-box[0], top-box[1], box[2]-right, box[3]-bottom]
            checks.append({'label':r['label'], 'contained':min(margins)>=0,
                           'margins_source_px':margins})
        for width in a.widths:
            height = round(width*ch/cw)
            dest = a.out / f'qa_{label}_{width}x{height}.jpg'
            # Crop and resample for inspection; never stretch a source into another ratio.
            im.resize((width,height),Image.Resampling.LANCZOS,box=box).save(dest,quality=95,subsampling=0)
            report['previews'].append({'path':str(dest), 'pixels':[width,height],
                                       'crop_box_source_px':list(box), 'regions':checks})
    if a.card_json:
        report['card_mock'] = {
            'path': str((a.out / 'qa_cards.html').resolve()), 'theme': a.theme, 'grayscale': a.grayscale,
            'json_path': str(a.card_json.resolve()), 'json_sha256': hashlib.sha256(a.card_json.read_bytes()).hexdigest(),
            'assets': [{'path': str(c['src']), 'sha256': c['sha256'], 'title': c['title'],
                        'channel': c['channel'], 'duration': c['duration']} for c in cards]}
    (a.out/'manifest.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'previews':len(report['previews']), 'source_pixels':im.size,
                      'all_declared_regions_contained':all(c['contained'] for v in report['previews'] for c in v['regions']) if regions else None}))


if __name__ == '__main__':
    main()
