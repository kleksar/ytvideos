"""Offline layout for explicitly calibrated native recipes; never draw/bake captions."""
from pathlib import Path
import hashlib
import re
from partition import partition_cues

# Native numbers here are measured/accepted recipes, not an assumed px-to-Size conversion.
RECIPES = {
    'paper-short-v09': {
        'channel':'paper_detour', 'format':'short', 'raster':[1440,2560],
        'font':{'family':'Chalkboard SE','style':'Bold'}, 'font_metrics_px':104,
        'native_size':0.121875, 'native_outline':0.04, 'word_gap_ratio':2/3,
        'case':'upper', 'center_x':680, 'center_y':1950.72,
        'max_width':1024, 'neutral':'#F4E8C8', 'active':'#FFD166', 'outline':'#18243A',
        'panel':None, 'evidence':'Paper Flagship v09 native imported Text+; 2026-11-19',
    },
}


def rgba(value):
    if not isinstance(value,str) or not re.fullmatch(r'#[0-9A-Fa-f]{6}([0-9A-Fa-f]{2})?',value):
        raise ValueError('Explicit RGB/RGBA color required')
    value=value[1:]
    return [int(value[i:i+2],16)/255 for i in (0,2,4)]+[int(value[6:8],16)/255 if len(value)==8 else 1]


def native_layout(plan, shots, recipe_id, *, font_loader=None):
    if recipe_id not in RECIPES:
        raise ValueError('No calibrated native recipe; do not substitute another channel')
    recipe=RECIPES[recipe_id]
    style=plan['style']; geometry=style.get('geometry',{})
    if ((style['channel'],style['format']) != (recipe['channel'],recipe['format'])
        or plan['target']['raster'] != recipe['raster'] or style['font_face'] != recipe['font']
        or geometry.get('font_size_px') != recipe['font_metrics_px']):
        raise ValueError('Active channel/format/font/raster differs from native calibration')
    if (style['style'].get('text') != recipe['neutral'] or style['style'].get('highlight') != recipe['active']
        or style['style'].get('outline') != recipe['outline']):
        raise ValueError('Active style colors differ from native calibration')
    path=Path(style['style']['font'])
    if not path.is_file():
        raise ValueError('Required installed font file unavailable; no fallback')
    if font_loader is None:
        from PIL import ImageFont
        font_loader=ImageFont.truetype
    font=font_loader(str(path),recipe['font_metrics_px'],index=style['style'].get('font_index',0))
    normalized=lambda value: re.sub(r'[^a-z0-9]','',value.lower())
    family, face=font.getname()
    if (normalized(family),normalized(face)) != (normalized(recipe['font']['family']), normalized(recipe['font']['style'])):
        raise ValueError('Installed font face does not match the calibrated native recipe')
    sections=partition_cues(plan['cues'],shots)
    width,height=recipe['raster']
    for shot in sections:
        nodes=[]
        for group in shot['sections']:
            words=group['words']
            labels=[w['text'].upper() if recipe['case']=='upper' else w['text'] for w in words]
            lengths=[font.getlength(label) for label in labels]
            gap=font.getlength(' ')*recipe['word_gap_ratio']
            total=sum(lengths)+gap*(len(lengths)-1)
            if total > recipe['max_width']:
                raise ValueError('Reviewed phrase exceeds calibrated one-line safe width; regroup explicitly')
            left=recipe['center_x']-total/2
            for word,label,length in zip(words,labels,lengths):
                active_start=max(shot['start_frame'],group['start_frame'],word['start_frame'])
                active_end=min(shot['end_frame'],group['end_frame'],word['end_frame'])
                nodes.append(dict(name=f"Word{word['index']:05d}",text=label,index=word['index'],
                    x=(left+length/2)/width,y=1-recipe['center_y']/height,
                    first=group['start_frame']-shot['start_frame'],last=group['end_frame']-shot['start_frame'],
                    active_first=active_start-shot['start_frame'] if active_start<active_end else None,
                    active_last=active_end-shot['start_frame'] if active_start<active_end else None))
                left+=length+gap
        shot['nodes']=nodes
    return dict(recipe_id=recipe_id,recipe=recipe,shots=sections,
                font_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                conform_sha256=plan['conform_sha256'],visual='UNVERIFIED',playback='UNVERIFIED')
