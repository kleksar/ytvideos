"""Offline layout for explicitly calibrated native recipes; never draw/bake captions."""
from pathlib import Path
import hashlib
import re
import math
from partition import partition_cues

# Native numbers here are measured/accepted recipes, not an assumed px-to-Size conversion.
RECIPES = {
    'paper-short-v09': {
        'channel':'paper_detour', 'format':'short', 'raster':[1440,2560],
        'font':{'family':'Chalkboard SE','style':'Bold'}, 'font_metrics_px':104,
        'native_size':0.121875, 'native_outline':0.04, 'word_gap_ratio':2/3,
        'case':'upper', 'center_x':680, 'center_y':1950.72,
        'max_width':1024, 'neutral':'#F4E8C8', 'active':'#FFD166', 'outline':'#18243A',
        'profile_geometry':{'reference_width':1440,'reference_height':2560,'font_size_px':104,
                            'max_visible_width_px':1024,'center_x_ratio':0.4722222222222222,'center_y_ratio':0.762},
        'profile_style':{'background':None,'outline_width':3,'pad_x':20,'pad_y':12,'font_index':2},
        'panel':None, 'evidence':'Paper Flagship v09 native imported Text+; 2026-11-19',
    },
    'nuviko-history-long-native-v1': {
        'channel':'nuviko_history','format':'long','raster':[2560,1440],
        'font':{'family':'Georgia','style':'Bold'},'font_metrics_px':84,
        'native_size':0.046875,'native_outline':0,'word_gap_ratio':1,
        'case':'preserve','center_x':1280,'center_y':1255,
        'max_width':1286,'neutral':'#F3E9D5','active':'#FFD166','outline':'#20252B',
        'profile_geometry':{'reference_width':2560,'reference_height':1440,'font_size_px':84,
                            'max_visible_width_px':1344,'center_x_ratio':0.5,'baseline_y_ratio':0.8944444444444445,
                            'bottom_y_ratio':0.925},
        'profile_style':{'background':'#20252BCC','outline_width':0,'pad_x':29,'pad_y':17,'font_index':0},
        'panel':{'color':'#20252BCC','pad_x':29,'top':1193,'height':135},
        'evidence':'Canonical long/nuviko profile; native Georgia 84px caps/descenders calibration 2026-11-19',
    },
}


def rgba(value):
    if not isinstance(value,str) or not re.fullmatch(r'#[0-9A-Fa-f]{6}([0-9A-Fa-f]{2})?',value):
        raise ValueError('Explicit RGB/RGBA color required')
    value=value[1:]
    return [int(value[i:i+2],16)/255 for i in (0,2,4)]+[int(value[6:8],16)/255 if len(value)==8 else 1]


def native_layout(plan, shots, recipe_id, *, font_loader=None, display_cut_anchors=None):
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
    if geometry != recipe['profile_geometry']:
        raise ValueError('Active profile geometry differs from native calibration')
    profile_style=style['style']
    if any(key not in profile_style or type(profile_style[key]) is not type(expected)
           or profile_style[key] != expected for key,expected in recipe['profile_style'].items()):
        raise ValueError('Active panel, outline, padding or font index differs from native calibration')
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
    sections=partition_cues(plan['cues'],shots,display_cut_anchors)
    width,height=recipe['raster']
    for shot in sections:
        nodes=[];panels=[]
        for group in shot['sections']:
            words=group['words']
            labels=[w['text'].upper() if recipe['case']=='upper' else w['text'] for w in words]
            lengths=[font.getlength(label) for label in labels]
            gap=font.getlength(' ')*recipe['word_gap_ratio']
            total=sum(lengths)+gap*(len(lengths)-1)
            if total > recipe['max_width']:
                raise ValueError('Reviewed phrase exceeds calibrated one-line safe width; regroup explicitly')
            left=recipe['center_x']-total/2
            if recipe['panel']:
                panel=recipe['panel'];box_width=math.ceil(total+2*panel['pad_x'])
                box_left=round(recipe['center_x']-box_width/2)
                panels.append(dict(name='Panel'+str(words[0]['index']),
                    x=(box_left+box_width/2)/width,y=1-(panel['top']+panel['height']/2)/height,
                    width=box_width/width,height=panel['height']/height,
                    first=group['start_frame']-shot['start_frame'],last=group['end_frame']-shot['start_frame']))
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
        shot['panels']=panels
    return dict(recipe_id=recipe_id,recipe=recipe,shots=sections,
                font_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                conform_sha256=plan['conform_sha256'],visual='UNVERIFIED',playback='UNVERIFIED')
