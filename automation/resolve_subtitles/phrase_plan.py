"""Explicit approved display intervals; no guessed speech alignment or style fallback."""
import json
import math
import re
from pathlib import Path

RECIPE = 'georgia-white-608x1080-native-v1'
STYLE = {'font': 'Georgia', 'face': 'Bold', 'size': 0.10338345864661655,
         'center': [0.5, 0.195634920634921], 'raster': [608, 1080],
         'color': [1, 1, 1, 1]}


def phrase_layout(request):
    data = request['native_titles']
    recipes = {RECIPE: STYLE, 'svin-white-608x1080-owner-smaller-v1': dict(STYLE, size=0.0878759398496244)}
    expected_style = recipes.get(data.get('recipe_id'))
    if expected_style is None or request['target']['raster'] != expected_style['raster']:
        raise ValueError('No calibrated independent-title recipe for this target; no fallback')
    if data.get('style') != expected_style:
        raise ValueError('Exact approved native style required; no profile substitution')
    evidence = data.get('display_evidence', {})
    if not evidence.get('source') or evidence.get('kind') != 'approved_display_intervals':
        raise ValueError('Reviewed whole-phrase display timing provenance required')
    rows = data['display_clips']
    if not rows:
        raise ValueError('No display phrases')
    result = []
    previous = request['target']['origin_frame']
    for row in rows:
        a, b = row['start_frame'], row['end_frame']
        if type(a) is not int or type(b) is not int or a != previous or b <= a:
            raise ValueError('Exact contiguous full phrase intervals required')
        text = row['text']
        if not isinstance(text, str) or not text.strip() or any(ord(c) < 32 for c in text):
            raise ValueError('Explicit nonempty single-line phrase text required')
        panel = row['panel']
        values = [*panel['center'], panel['width'], panel['height'], *panel['color']]
        if len(panel['center']) != 2 or len(panel['color']) != 4 or any(type(v) not in (int, float) or not math.isfinite(v) for v in values):
            raise ValueError('Finite panel geometry required')
        if (panel['color'] != [32/255, 37/255, 43/255, 0.8]
            or abs(panel['height'] - 69/1080) > 1e-9
            or abs(panel['center'][1] - 0.19212962962962965) > 1e-9
            or abs(panel['center'][0] - 0.5) > 0.002
            or not 0 < panel['width'] <= 0.9):
            raise ValueError('Panel differs from calibrated recipe')
        if row.get('width_review') != 'native_verified':
            raise ValueError('Whole phrase width must be inspected natively; no shrink-to-fit fallback')
        result.append(dict(start_frame=a, end_frame=b, text=text, style=dict(expected_style, panel=panel)))
        previous = b
    if previous != request['target']['end_frame']:
        raise ValueError('Display phrases must cover the exact target range')
    return result


def write_comps(layout, folder):
    """Sanitized native Text+ graph; no source media or machine-private cache paths."""
    folder = Path(folder)
    folder.mkdir(parents=True, exist_ok=True)
    template = Path(__file__).with_name('phrase_template.comp').read_text()
    paths = []
    for index, row in enumerate(layout):
        panel = row['style']['panel']
        substitutions = {'__END__': str(row['end_frame']-row['start_frame']-1),
                         '__TEXT__': json.dumps(row['text'], ensure_ascii=False),
                         '__SIZE__': repr(row['style']['size']),
                         '__PANEL_X__': repr(panel['center'][0]), '__PANEL_WIDTH__': repr(panel['width'])}
        value = re.sub(r'__(?:END|TEXT|SIZE|PANEL_X|PANEL_WIDTH)__',
                       lambda match: substitutions[match.group()], template)
        path = folder / f'phrase-{index:04}.comp'
        path.write_text(value)
        paths.append(str(path.resolve()))
    return paths
