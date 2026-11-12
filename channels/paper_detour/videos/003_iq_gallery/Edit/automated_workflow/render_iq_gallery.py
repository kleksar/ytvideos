#!/usr/bin/env python3
"""Render an approved IQ Gallery manifest without editing Palmier.

Contract (paths relative to the manifest):
{
  "output": ".../draft.mp4", "audio": ".../existing_60s.mp4",
  "grain": ".../moving_grain.mov", "transition_frames": 12,
  "scenes": [{
    "frames": 139, "background": "bg.png", "midground": "mg.png",
    "foreground": "fg.png", "overscan_x": 24, "overscan_y": 42,
    "velocity_x": {"background": 6, "midground": -7, "foreground": 10},
    "layer_scale": {"midground": 0.82, "foreground": 0.50},
    "layer_anchor": {"midground": "right_bottom", "foreground": "center"},
    "layer_offset": {"midground": {"x": -55, "y": 0}},
    "entry": {"start": 0.45, "duration": 0.8, "rise": 770},
    "glyphs": [
      {"kind":"name", "char":"KASPAROV", "file":"name.png", "x":60,"y":210,"w":500,"h":130},
      {"kind":"iq", "char":"IQ", "file":"iq.png", "x":56,"y":410,"w":130,"h":100},
      {"kind":"digit", "char":"1", "file":"1.png", "x":270,"y":410,"w":65,"h":100}
    ]
  }]
}
Velocities are total horizontal displacement in 540px-equivalent units over
that scene's nominal duration; all positions/sizes/overscan are in 1080x1920
output pixels. Give the complete name and IQ label each one transparent PNG;
each digit has its own transparent PNG and box. Digit boxes must not touch
even at extreme breathing/rotation. Optionally include scene display_name (str)
and iq_value (integer) to cross-check the declared label/digit strings. A visual
review must verify the PNG artwork actually depicts its declared text.
BG is aspect-fill and center-cropped. MG/FG are aspect-fit and centered on a
transparent canvas, without cropping. The resulting composition must still be
artistically checked: independently fitted layers may not align even if valid.
MG/FG scales are 0.25..1.0; anchors are center or {left,center,right}_
{top,center,bottom}. Both default to 1.0 and center. Offsets are in 1080x1920
output pixels (-500..500), default zero. The estimated alpha bounds and warnings
in the report are not a replacement for checking the actual rendered frames.
Use compatible PNGs; MG/FG and glyphs require alpha. Input files are unaltered. This script does not claim
any image, IQ value, content, scene, or project has been approved.

Usage: python3 render_iq_gallery.py manifest.json --probe
       python3 render_iq_gallery.py manifest.json
--probe validates inputs and prints the resolved manifest/plan, without writes.
A render writes a video and a separate .report.json, without overwriting either.
"""
from __future__ import annotations
import argparse, json, math, os, pathlib, shutil, struct, subprocess, sys, tempfile, zlib

W,H,FPS = 1080,1920,30
ROOT = pathlib.Path(__file__).resolve().parent


def fail(msg):
    raise ValueError(msg)


def cmd(args):
    subprocess.run([str(a) for a in args], check=True)


def probe(path):
    p = subprocess.run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)],
                       capture_output=True,text=True,check=True)
    return json.loads(p.stdout)


_png_cache = {}


def inspect_png(path):
    """Check PNG chunks/CRC, decodability and alpha, cached per input file."""
    if path in _png_cache:
        return _png_cache[path]
    data=path.read_bytes()
    if data[:8] != b"\x89PNG\r\n\x1a\n": fail(f"not a PNG: {path}")
    pos=8; alpha=False; dims=None; ended=False
    while pos+12 <= len(data):
        size=struct.unpack_from('>I',data,pos)[0]
        end=pos+12+size
        if end > len(data): fail(f"truncated PNG chunk: {path}")
        kind=data[pos+4:pos+8]; payload=data[pos+8:pos+8+size]
        crc=struct.unpack_from('>I',data,pos+8+size)[0]
        if zlib.crc32(kind+payload) != crc: fail(f"PNG CRC failure: {path}")
        if pos==8:
            if kind != b'IHDR' or size != 13: fail(f"invalid PNG header: {path}")
            w,h,depth,color,_,_,_=struct.unpack('>IIBBBBB',payload)
            if w<=0 or h<=0: fail(f"invalid PNG dimensions: {path}")
            dims=(w,h); alpha=color in (4,6)
        if kind==b'tRNS': alpha=True
        pos=end
        if kind==b'IEND': ended=True; break
    if not ended or pos!=len(data) or dims is None: fail(f"invalid PNG structure: {path}")
    stream=next((x for x in probe(path)['streams'] if x['codec_type']=='video'),None)
    if not stream or stream.get('codec_name')!='png' or (stream.get('width'),stream.get('height'))!=dims:
        fail(f"PNG decoder/metadata mismatch: {path}")
    decoded=subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(path),'-frames:v','1','-f','null','-'],capture_output=True)
    if decoded.returncode: fail(f"PNG decode failed: {path}")
    _png_cache[path]={'width':dims[0], 'height':dims[1], 'alpha':alpha}
    return _png_cache[path]


_alpha_bbox_cache = {}


def alpha_bbox(path):
    """Return source nonzero-alpha bounds as [left, top, right, bottom], exclusive."""
    if path in _alpha_bbox_cache: return _alpha_bbox_cache[path]
    meta=inspect_png(path); width=meta['width']; height=meta['height']
    p=subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(path),'-vf','format=rgba,alphaextract',
                      '-frames:v','1','-f','rawvideo','-pix_fmt','gray','-'],capture_output=True)
    if p.returncode or len(p.stdout)!=width*height: fail(f'cannot decode alpha plane: {path}')
    left=width; right=0; top=height; bottom=0
    for y in range(height):
        row=p.stdout[y*width:(y+1)*width]
        if not row.strip(b'\x00'): continue
        first=width-len(row.lstrip(b'\x00')); last=len(row.rstrip(b'\x00'))
        left=min(left,first); right=max(right,last); top=min(top,y); bottom=y+1
    if bottom==0: fail(f'layer is fully transparent: {path}')
    _alpha_bbox_cache[path]=[left,top,right,bottom]
    return _alpha_bbox_cache[path]


def estimated_layer_bounds(source,scale,anchor,offset,velocity,overscan_x,overscan_y,frames,extra,width,height,factor):
    """Estimate transformed nonzero alpha bounds; ffmpeg rounding can differ."""
    meta=inspect_png(source); x0,y0,x1,y1=alpha_bbox(source)
    sw=round(width+2*overscan_x*factor); sh=round(height+2*overscan_y*factor)
    ox=(sw-width)/2; oy=(sh-height)/2
    mw=max(1,round(sw*scale)); mh=max(1,round(sh*scale))
    ratio=min(mw/meta['width'],mh/meta['height'])
    fw=round(meta['width']*ratio); fh=round(meta['height']*ratio)
    ax,ay=('center','center') if anchor=='center' else anchor.split('_')
    px={'left':0,'center':(sw-fw)/2,'right':sw-fw}[ax]
    py={'top':0,'center':(sh-fh)/2,'bottom':sh-fh}[ay]
    move=velocity*2*factor*(frames+extra-1)/frames
    left=-ox+offset['x']*factor+px+x0*fw/meta['width']
    right=-ox+offset['x']*factor+px+x1*fw/meta['width']
    top=-oy+offset['y']*factor+py+y0*fh/meta['height']
    bottom=-oy+offset['y']*factor+py+y1*fh/meta['height']
    bounds=[left+min(0,move),top,right+max(0,move),bottom]
    return {'source_alpha_bbox': [x0,y0,x1,y1],
            'estimated_motion_bbox_px':[round(v,2) for v in bounds],
            'possibly_clipped':bounds[0]<0 or bounds[1]<0 or bounds[2]>width or bounds[3]>height,
            'note':'Approximate nonzero-alpha bounds including scene motion and transition, before transition slide; compare actual frames. Subpixel/filter rounding and faint alpha can affect the result.'}


def audio_packets(path):
    p = subprocess.run(['ffprobe','-v','error','-select_streams','a:0','-show_packets',
                        '-show_entries','packet=data_hash','-show_data_hash','sha256','-of','json',str(path)],
                       capture_output=True,text=True,check=True)
    return json.loads(p.stdout)['packets']


def real(base, value, what):
    if not isinstance(value,str) or not value.strip(): fail(f'{what}: expected nonempty path')
    p = pathlib.Path(value).expanduser()
    p = (base/p).resolve() if not p.is_absolute() else p.resolve()
    if not p.is_file(): fail(f'{what}: missing file: {p}')
    return p


def number(obj, key, what, low=None, high=None):
    v = obj.get(key)
    if isinstance(v,bool) or not isinstance(v,(int,float)) or not math.isfinite(v): fail(f'{what}.{key}: must be finite number')
    if low is not None and v < low or high is not None and v > high: fail(f'{what}.{key}: outside [{low}, {high}]')
    return float(v)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('manifest', type=pathlib.Path)
    ap.add_argument('--probe', action='store_true', help='validate and print plan without rendering')
    ap.add_argument('--test-mode', action='store_true', help=argparse.SUPPRESS)
    ap.add_argument('--test-full-size', action='store_true', help=argparse.SUPPRESS)
    a = ap.parse_args()
    for tool in ['ffmpeg','ffprobe']:
        if not shutil.which(tool): fail(f'missing {tool}')
    manifest_path = a.manifest.expanduser().resolve()
    m = json.loads(manifest_path.read_text())
    if not isinstance(m,dict): fail('manifest must be an object')
    base = manifest_path.parent
    if a.test_full_size and not a.test_mode: fail('--test-full-size requires --test-mode')
    width,height = (270,480) if a.test_mode and not a.test_full_size else (W,H)
    factor = width/W
    scenes=m.get('scenes')
    if not isinstance(scenes,list) or len(scenes) < 2: fail('at least two scenes are required')
    if a.test_mode and len(scenes) != 2: fail('test mode expects 2 scenes')
    transition=m.get('transition_frames',12)
    if type(transition) is not int or not 1 <= transition <= 30: fail('transition_frames must be an integer 1..30')
    audio=real(base,m.get('audio'),'audio'); grain=real(base,m.get('grain'),'grain')
    out_value=m.get('output')
    if not isinstance(out_value,str) or not out_value: fail('output path required')
    output=pathlib.Path(out_value).expanduser()
    output=(base/output).resolve() if not output.is_absolute() else output.resolve()
    if output.suffix.lower() != '.mp4': fail('output must end in .mp4')
    if not output.parent.is_dir(): fail(f'output parent does not exist: {output.parent}')
    report=pathlib.Path(str(output)+'.report.json')
    if output.exists() or report.exists(): fail('refusing to overwrite output or report')
    info=probe(audio)
    streams=[s for s in info['streams'] if s['codec_type']=='audio']
    if not streams: fail('audio source has no audio stream')
    audio_stream=streams[0]
    if audio_stream.get('codec_name') != 'aac': fail('MP4 stream-copy requires AAC audio')
    aud_duration=float(audio_stream.get('duration') or info.get('format',{}).get('duration') or 0)
    gr_info=probe(grain)
    grain_stream=next((s for s in gr_info['streams'] if s['codec_type']=='video'),None)
    if not grain_stream: fail('grain has no video stream')
    direction_rules_version=m.get('direction_rules_version')
    if direction_rules_version not in (None,1): fail('direction_rules_version must be 1 when supplied')
    profile_input=m.get('title_motion',{})
    if not isinstance(profile_input,dict): fail('title_motion must be an object')
    title_motion={
        'cycle_seconds':number(profile_input,'cycle_seconds','title_motion',3,16) if 'cycle_seconds' in profile_input else 6.0,
        'scale_amplitude':number(profile_input,'scale_amplitude','title_motion',0,0.05) if 'scale_amplitude' in profile_input else 0.03,
        'rotation_amplitude_degrees':number(profile_input,'rotation_amplitude_degrees','title_motion',0,2) if 'rotation_amplitude_degrees' in profile_input else round(math.degrees(0.0209),4),
        'x_oscillation_px_1080':number(profile_input,'x_oscillation_px_1080','title_motion',0,8) if 'x_oscillation_px_1080' in profile_input else 2.0,
        'y_oscillation_px_1080':number(profile_input,'y_oscillation_px_1080','title_motion',0,8) if 'y_oscillation_px_1080' in profile_input else 3.0,
        'entry_scale_from':number(profile_input,'entry_scale_from','title_motion',0.9,1.0) if 'entry_scale_from' in profile_input else 0.992,
        'entry_settle_frames':profile_input.get('entry_settle_frames',6),
        'group_scale_amplitude':number(profile_input,'group_scale_amplitude','title_motion',0,0.02) if 'group_scale_amplitude' in profile_input else 0.005,
        'group_rotation_amplitude_degrees':number(profile_input,'group_rotation_amplitude_degrees','title_motion',0,1) if 'group_rotation_amplitude_degrees' in profile_input else 0.25,
    }
    if type(title_motion['entry_settle_frames']) is not int or not 0 <= title_motion['entry_settle_frames'] <= 30:
        fail('title_motion.entry_settle_frames must be an integer from 0 to 30')
    total=0
    all_paths={audio,grain}
    resolved=[]
    previous_direction=None
    for i,s in enumerate(scenes):
        tag=f'scenes[{i}]'
        if not isinstance(s,dict): fail(f'{tag}: must be object')
        frames=s.get('frames')
        if type(frames) is not int or frames <= transition+30: fail(f'{tag}.frames must exceed transition + 30')
        total+=frames
        ox=number(s,'overscan_x',tag,1,500); oy=number(s,'overscan_y',tag,1,500)
        vel=s.get('velocity_x')
        if not isinstance(vel,dict): fail(f'{tag}.velocity_x must be object')
        v={k:number(vel,k,tag+'.velocity_x',-100,100) for k in ('background','midground','foreground')}
        anchor_side=s.get('foreground_anchor_side')
        direction=s.get('motion_direction')
        exception=s.get('direction_exception_reason')
        if direction_rules_version==1:
            if anchor_side not in ('left','right'): fail(f'{tag}: foreground_anchor_side must be left or right')
            if direction not in ('left_to_right','right_to_left'): fail(f'{tag}: explicit motion_direction required')
            if exception is not None and (not isinstance(exception,str) or not exception.strip()): fail(f'{tag}: empty direction exception')
            expected={'left':'right_to_left','right':'left_to_right'}[anchor_side]
            if direction!=expected and not exception: fail(f'{tag}: direction conflicts with its foreground anchor')
            signs={1 if value>0 else -1 if value<0 else 0 for value in v.values()}
            expected_sign=1 if direction=='left_to_right' else -1
            if signs!={expected_sign}: fail(f'{tag}: all three layers must share the declared motion direction')
            if previous_direction==direction and not exception: fail(f'{tag}: repeated direction needs a documented continuity reason')
            previous_direction=direction
        # Velocities specified in the same 540 px units as the measured pilot.
        if any(abs(d*2)*(frames + (transition if i<len(scenes)-1 else 0))/frames > ox for d in v.values()): fail(f'{tag}: velocity requires more horizontal overscan, including transition')
        if len(set(v.values()))<2: fail(f'{tag}: layers need different speeds')
        scale_input=s.get('layer_scale',{})
        anchor_input=s.get('layer_anchor',{})
        offset_input=s.get('layer_offset',{})
        if not all(isinstance(a,dict) for a in (scale_input,anchor_input,offset_input)): fail(f'{tag}: layer_scale, layer_anchor and layer_offset must be objects')
        if any(set(a)-{'midground','foreground'} for a in (scale_input,anchor_input,offset_input)): fail(f'{tag}: transforms support only midground and foreground')
        offsets={}
        for key in ('midground','foreground'):
            item=offset_input.get(key,{})
            if not isinstance(item,dict) or set(item)-{'x','y'}: fail(f'{tag}.layer_offset.{key}: expected x/y object')
            offsets[key]={axis:(number(item,axis,tag+'.layer_offset.'+key,-500,500) if axis in item else 0.0) for axis in ('x','y')}
        scales={k:(number(scale_input,k,tag+'.layer_scale',0.25,1.0) if k in scale_input else 1.0) for k in ('midground','foreground')}
        valid_anchors={'center'} | {x+'_'+y for x in ('left','center','right') for y in ('top','center','bottom')}
        anchors={k:anchor_input.get(k,'center') for k in ('midground','foreground')}
        if any(not isinstance(a,str) or a not in valid_anchors for a in anchors.values()): fail(f'{tag}: invalid layer anchor')
        layers={k:real(base,s.get(k),f'{tag}.{k}') for k in ('background','midground','foreground')}
        dims={}
        for k,p in layers.items():
            all_paths.add(p)
            meta=inspect_png(p)
            dims[k]=[meta['width'],meta['height']]
            if k!='background' and not meta['alpha']:
                fail(f'{tag}.{k}: alpha channel required')
        bounds={k:estimated_layer_bounds(layers[k],scales[k],anchors[k],offsets[k],v[k],ox,oy,frames,transition if i<len(scenes)-1 else 0,width,height,factor) for k in ('midground','foreground')}
        en=s.get('entry',{})
        start=number(en,'start',tag+'.entry',0,4)
        dur=number(en,'duration',tag+'.entry',0.1,2)
        rise=number(en,'rise',tag+'.entry',0,1500)
        if start+dur+(0.5 if a.test_mode else 2) > frames/FPS: fail(f'{tag}: entry must leave enough time for reading')
        glyphs=s.get('glyphs')
        if not isinstance(glyphs,list) or not glyphs: fail(f'{tag}.glyphs: individual glyphs required')
        gs=[]
        for j,g in enumerate(glyphs):
            gt=f'{tag}.glyphs[{j}]'
            if not isinstance(g,dict) or g.get('kind') not in ('name','iq','digit'): fail(f'{gt}: invalid kind')
            label=g.get('char')
            if not isinstance(label,str) or not label or label != label.strip(): fail(f'{gt}: nonempty text without leading/trailing spaces required')
            if g['kind']=='name' and (len(label)>100 or not any(c.isalpha() for c in label) or not all((c.isalpha() and c.isupper()) or c in " .-'’" for c in label)):
                fail(f'{gt}: name must use uppercase letters, spaces or name punctuation')
            if g['kind']=='iq' and label != 'IQ': fail(f'{gt}: IQ label must be IQ')
            if g['kind']=='digit' and (len(label)!=1 or label not in '0123456789'): fail(f'{gt}: one decimal digit per PNG required')
            p=real(base,g.get('file'),gt+'.file'); all_paths.add(p)
            meta=inspect_png(p)
            if not meta['alpha']: fail(f'{gt}: alpha PNG required')
            x=number(g,'x',gt,0,W); y=number(g,'y',gt,0,H)
            w=number(g,'w',gt,12,W); h=number(g,'h',gt,12,H)
            if x+w>W or y+h>H: fail(f'{gt}: final box exceeds frame')
            gs.append(dict(kind=g['kind'],char=g['char'],path=p,x=x,y=y,w=w,h=h,source_dimensions=[meta['width'],meta['height']]))
        if sum(g['kind']=='name' for g in gs)!=1 or sum(g['kind']=='iq' for g in gs)!=1:
            fail(f'{tag}: exactly one name group and one IQ group required')
        ds=sorted((g for g in gs if g['kind']=='digit'),key=lambda g:g['x'])
        if not ds: fail(f'{tag}: at least one digit required')
        name=next(g['char'] for g in gs if g['kind']=='name')
        if 'display_name' in s and s['display_name'] != name: fail(f'{tag}: display_name differs from name group')
        if 'iq_value' in s:
            n=s['iq_value']
            if type(n) is not int or n<0 or str(n) != ''.join(d['char'] for d in ds):
                fail(f'{tag}: iq_value differs from displayed digit sequence')
        for x,y in zip(ds,ds[1:]):
            # Cover 3% scale, 1.2-degree rotation and +/-2 px position on each side.
            margin=0.03*(x['w']+y['w'])/2 + 0.021*(x['h']+y['h'])/2 + 5
            if y['x']-x['x']-x['w'] < margin: fail(f'{tag}: digit boxes too close; need gap >= {margin:.1f}px')
        text_group=None
        if 'text_group' in s:
            g=s['text_group']
            if not isinstance(g,dict) or g.get('kind')!='group': fail(f'{tag}.text_group must be a group object')
            p=real(base,g.get('file'),tag+'.text_group.file'); all_paths.add(p)
            meta=inspect_png(p)
            if not meta['alpha']: fail(f'{tag}.text_group: alpha PNG required')
            gx=number(g,'x',tag+'.text_group',0,W); gy=number(g,'y',tag+'.text_group',0,H)
            gw=number(g,'w',tag+'.text_group',12,W); gh=number(g,'h',tag+'.text_group',12,H)
            if gx+gw>W or gy+gh>H: fail(f'{tag}.text_group: final box exceeds frame')
            if 'display_name' in s and s.get('display_name') not in str(g.get('char','')):
                fail(f'{tag}.text_group: declared name missing from group label')
            if 'iq_value' in s and f"IQ {s['iq_value']}" not in str(g.get('char','')):
                fail(f'{tag}.text_group: declared IQ score missing from group label')
            text_group=dict(path=p,x=gx,y=gy,w=gw,h=gh,source_dimensions=[meta['width'],meta['height']])
        overlay_specs=s.get('occlusion_overlays',[])
        if not isinstance(overlay_specs,list): fail(f'{tag}.occlusion_overlays must be a list')
        occlusion_overlays=[]
        seen_overlay_names=set()
        for j,o in enumerate(overlay_specs):
            ot=f'{tag}.occlusion_overlays[{j}]'
            if not isinstance(o,dict): fail(f'{ot} must be an object')
            name=o.get('name')
            if not isinstance(name,str) or not name or any(not (c.isalnum() or c in '_-') for c in name):
                fail(f'{ot}.name must contain only letters, digits, underscore or hyphen')
            if name in seen_overlay_names: fail(f'{tag}: duplicate occlusion overlay name {name}')
            seen_overlay_names.add(name)
            transform_layer=o.get('transform_layer','midground')
            if transform_layer not in ('midground','foreground'):
                fail(f'{ot}.transform_layer must be midground or foreground')
            p=real(base,o.get('file'),ot+'.file'); all_paths.add(p)
            meta=inspect_png(p)
            if not meta['alpha']: fail(f'{ot}: alpha PNG required')
            if [meta['width'],meta['height']] != dims[transform_layer]:
                fail(f'{ot}: source dimensions must match its {transform_layer} transform layer')
            occlusion_overlays.append(dict(name=name,path=p,transform_layer=transform_layer,
                                           source_dimensions=[meta['width'],meta['height']]))
        resolved.append(dict(frames=frames,ox=ox,oy=oy,vel=v,layers=layers,glyphs=gs,text_group=text_group,
                             occlusion_overlays=occlusion_overlays,start=start,dur=dur,rise=rise,dims=dims,
                             scales=scales,anchors=anchors,offsets=offsets,bounds=bounds,
                             foreground_anchor_side=anchor_side,motion_direction=direction,
                             direction_exception_reason=exception))
    expected = 2*60 if a.test_mode else m.get('expected_frames',total)
    if type(expected) is not int or expected <= 0: fail('expected_frames must be a positive integer')
    if total != expected: fail(f'scene frame total must equal {expected}, got {total}')
    if aud_duration+0.0001 < total/FPS: fail(f'audio is too short: {aud_duration:.3f}s')
    if output in all_paths or report in all_paths: fail('output collides with an input')
    group_mode=all(s['text_group'] is not None for s in resolved)
    plan={'manifest':str(manifest_path),'output':str(output),'report':str(report),'format':f'{width}x{height} {FPS}fps','frames':total,'audio':str(audio),'grain':str(grain),'grain_dimensions':[grain_stream['width'],grain_stream['height']],'audio_duration':aud_duration,'transition_frames':transition,'title_motion':{**title_motion,'animation_mode':'one shared composite group for name and IQ score' if group_mode else 'legacy individual glyphs','entry':'shared quintic smootherstep position/scale and same-time alpha fade; settle before gentle enveloped breathing'},'scenes':[{'frames':s['frames'],'source_dimensions':s['dims'],'foreground_anchor_side':s['foreground_anchor_side'],'motion_direction':s['motion_direction'],'direction_exception_reason':s['direction_exception_reason'],'velocity_x':s['vel'],'layer_scale':s['scales'],'layer_anchor':s['anchors'],'layer_offset':s['offsets'],'estimated_layer_bounds':s['bounds'],'glyph_count':len(s['glyphs']),'text_group':None if s['text_group'] is None else {'path':str(s['text_group']['path']),'box':[s['text_group']['x'],s['text_group']['y'],s['text_group']['w'],s['text_group']['h']]},'glyph_sources':[{'kind':g['kind'],'char':g['char'],'path':str(g['path']),'dimensions':g['source_dimensions']} for g in s['glyphs']],'layers':{k:str(v) for k,v in s['layers'].items()}} for s in resolved]}
    for scene_plan,scene in zip(plan['scenes'],resolved):
        scene_plan['occlusion_overlays']=[{'name':o['name'],'transform_layer':o['transform_layer'],
                                           'path':str(o['path']),'source_dimensions':o['source_dimensions']}
                                          for o in scene['occlusion_overlays']]
    if a.probe:
        print(json.dumps(plan,ensure_ascii=False,indent=2)); return
    render(resolved, audio, grain, output, report, plan, transition, width,height, factor, total,title_motion)


def render(scenes,audio,grain,output,report,plan,transition,width,height,factor,total,title_motion):
    # Output and all intermediate files live on the output filesystem. os.link
    # publishes the verified file atomically and fails if the target appeared.
    with tempfile.TemporaryDirectory(prefix='.iq_gallery_',dir=output.parent) as td:
        td=pathlib.Path(td); clips=[]
        for i,s in enumerate(scenes):
            frames=s['frames']+(transition if i<len(scenes)-1 else 0)
            duration=frames/FPS
            paths=[s['layers'][k] for k in ('background','midground','foreground')]
            if s['text_group'] is not None:
                paths.append(s['text_group']['path'])
            else:
                paths += [g['path'] for g in s['glyphs']]
            occlusion_input_start=len(paths)
            paths += [o['path'] for o in s['occlusion_overlays']]
            args=['ffmpeg','-hide_banner','-loglevel','error','-filter_complex_threads','1']
            for p in paths: args+=['-loop','1','-framerate',str(FPS),'-i',str(p)]
            f=[]
            def add(x): f.append(x)
            ox=s['ox']*factor; oy=s['oy']*factor
            sw=int(round(width+2*ox)); sh=int(round(height+2*oy))
            ox=(sw-width)/2; oy=(sh-height)/2
            tnom=s['frames']/FPS
            v=lambda k:s['vel'][k]*2*factor
            add(f"[0:v]scale={sw}:{sh}:force_original_aspect_ratio=increase,crop={sw}:{sh},crop={width}:{height}:x='{ox}-{v('background')}*t/{tnom}':y={oy},setsar=1,format=rgba[bg]")
            last='bg'
            start=s['start']; dur=s['dur']; rise=s['rise']*factor
            ease=f"pow(clip((t-{start})/{dur},0,1),2)*(3-2*clip((t-{start})/{dur},0,1))"
            if s['text_group'] is not None:
                g=s['text_group']; w=max(2,round(g['w']*factor)); h=max(2,round(g['h']*factor))
                pw=math.ceil((w*1.01+16)/2)*2; ph=math.ceil((h*1.01+16)/2)*2
                rw=math.ceil((pw+ph*0.01+4)/2)*2; rh=math.ceil((ph+pw*0.01+4)/2)*2
                x=g['x']*factor-(rw-w)/2; y=g['y']*factor-(rh-h)/2
                cycle=title_motion['cycle_seconds']
                u=f'clip((t-{start})/{dur},0,1)'
                ease=f'({u}*{u}*{u}*({u}*({u}*6-15)+10))'
                hold_start=start+dur+title_motion['entry_settle_frames']/FPS
                p=f'mod(max(t-{hold_start},0)/{cycle},1)'
                p_in=f'clip(({p})/0.08,0,1)'; p_out=f'clip((({p})-0.92)/0.08,0,1)'
                smoother=lambda q:f'(({q})*({q})*({q})*(({q})*(({q})*6-15)+10))'
                envelope=f'{smoother(p_in)}*(1-{smoother(p_out)})'
                motion=f'sin(2*PI*({p}))*({envelope})'
                entry_from=title_motion['entry_scale_from']
                scale_expr=f'({entry_from}+(1-{entry_from})*({ease})+{title_motion["group_scale_amplitude"]}*({motion}))'
                angle=math.radians(title_motion['group_rotation_amplitude_degrees'])
                rotation_expr=f'({angle}*({motion}))'
                add(f"[3:v]scale=w='trunc({w}*{scale_expr}/2)*2':h='trunc({h}*{scale_expr}/2)*2':eval=frame,format=rgba,pad={pw}:{ph}:(ow-iw)/2:(oh-ih)/2:color=0x00000000,rotate=a='{rotation_expr}':ow={rw}:oh={rh}:c=none,fade=t=in:st={start}:d={dur}:alpha=1[title]")
                add(f"[{last}][title]overlay=x='{x}':y='{y}+{rise}*(1-({ease}))':format=auto[textgroup]")
                last='textgroup'
            else:
                for j,g in enumerate(s['glyphs']):
                    phase=0.0 if g['kind'] in ('name','iq') else (j*0.65) % (2*math.pi)
                    w=max(2,round(g['w']*factor)); h=max(2,round(g['h']*factor))
                    pw=math.ceil((w*1.04+4)/2)*2; ph=math.ceil((h*1.04+4)/2)*2
                    rw=math.ceil((pw+ph*0.025+4)/2)*2; rh=math.ceil((ph+pw*0.025+4)/2)*2
                    x=g['x']*factor-(rw-w)/2; y=g['y']*factor-(rh-h)/2
                    cycle=title_motion['cycle_seconds']; amplitude=title_motion['scale_amplitude']
                    rotation=math.radians(title_motion['rotation_amplitude_degrees'])
                    x_motion=title_motion['x_oscillation_px_1080']*factor
                    y_motion=title_motion['y_oscillation_px_1080']*factor
                    add(f"[{j+3}:v]scale=w='trunc({w}*(1+{amplitude}*sin(2*PI*t/{cycle}+{phase}))/2)*2':h='trunc({h}*(1+{amplitude}*sin(2*PI*t/{cycle}+{phase}))/2)*2':eval=frame,format=rgba,pad={pw}:{ph}:(ow-iw)/2:(oh-ih)/2:color=0x00000000,rotate=a='{rotation}*sin(2*PI*t/{cycle}+{phase})':ow={rw}:oh={rh}:c=none,fade=t=in:st={start}:d={dur}:alpha=1[g{j}]")
                    add(f"[{last}][g{j}]overlay=x='{x}+{x_motion}*sin(2*PI*t/{cycle}+{phase})':y='{y}+{rise}*(1-({ease}))+{y_motion}*sin(2*PI*t/{cycle}+{phase})':format=auto[text{j}]")
                    last=f'text{j}'
            for idx,k in [(1,'midground'),(2,'foreground')]:
                maxw=max(1,round(sw*s['scales'][k])); maxh=max(1,round(sh*s['scales'][k]))
                anchor=s['anchors'][k]
                ax,ay=('center','center') if anchor=='center' else anchor.split('_')
                px={'left':'0','center':'(ow-iw)/2','right':'ow-iw'}[ax]
                py={'top':'0','center':'(oh-ih)/2','bottom':'oh-ih'}[ay]
                add(f"[{idx}:v]scale={maxw}:{maxh}:force_original_aspect_ratio=decrease,format=rgba,pad={sw}:{sh}:x='{px}':y='{py}':color=0x00000000,setsar=1[{k}]")
                dx=s['offsets'][k]['x']*factor; dy=s['offsets'][k]['y']*factor
                add(f"[{last}][{k}]overlay=x='{-ox}+{dx}+{v(k)}*t/{tnom}':y={-oy+dy}:format=auto[with{k}]")
                last=f'with{k}'
            for j,o in enumerate(s['occlusion_overlays']):
                idx=occlusion_input_start+j
                k=o['transform_layer']
                label=f'occlusion_{i}_{j}'
                maxw=max(1,round(sw*s['scales'][k])); maxh=max(1,round(sh*s['scales'][k]))
                anchor=s['anchors'][k]
                ax,ay=('center','center') if anchor=='center' else anchor.split('_')
                px={'left':'0','center':'(ow-iw)/2','right':'ow-iw'}[ax]
                py={'top':'0','center':'(oh-ih)/2','bottom':'oh-ih'}[ay]
                add(f"[{idx}:v]scale={maxw}:{maxh}:force_original_aspect_ratio=decrease,format=rgba,pad={sw}:{sh}:x='{px}':y='{py}':color=0x00000000,setsar=1[{label}]")
                dx=s['offsets'][k]['x']*factor; dy=s['offsets'][k]['y']*factor
                add(f"[{last}][{label}]overlay=x='{-ox}+{dx}+{v(k)}*t/{tnom}':y={-oy+dy}:format=auto[with{label}]")
                last=f'with{label}'
            add(f'[{last}]format=yuv420p,setsar=1,settb=AVTB,setpts=PTS-STARTPTS[scene]')
            clip=td/f'scene_{i:02d}.mp4'
            args+=['-filter_complex',';'.join(f),'-map','[scene]','-an','-frames:v',str(frames),'-c:v','libx264','-preset','veryfast','-crf','14','-pix_fmt','yuv420p','-n',str(clip)]
            print(f'Rendering scene {i+1}/{len(scenes)}',file=sys.stderr,flush=True)
            cmd(args); clips.append(clip)
        args=['ffmpeg','-hide_banner','-loglevel','error','-filter_complex_threads','1']
        for clip in clips: args+=['-i',str(clip)]
        args+=['-stream_loop','-1','-i',str(grain),'-i',str(audio)]
        f=[]; last='0:v'; offset=0
        for i in range(1,len(clips)):
            offset+=scenes[i-1]['frames']
            out=f'xf{i}'
            f.append(f'[{last}][{i}:v]xfade=transition=slideleft:duration={transition/FPS:.9f}:offset={offset/FPS:.9f}[{out}]')
            last=out
        f.append(f'[{last}]trim=end_frame={total},setpts=PTS-STARTPTS[combined]')
        f.append(f'[{len(clips)}:v]scale={width}:{height},format=rgba,colorchannelmixer=aa=0.4[grain]')
        f.append('[combined][grain]overlay=0:0:format=auto:shortest=1,format=yuv420p[v]')
        tmp=td/'verified.mp4'
        args+=['-filter_complex',';'.join(f),'-map','[v]','-map',f'{len(clips)+1}:a:0','-t',str(total/FPS),'-c:v','libx264','-preset','medium','-crf','18','-pix_fmt','yuv420p','-c:a','copy','-movflags','+faststart','-n',str(tmp)]
        print('Compositing transitions, continuous grain and copied audio',file=sys.stderr,flush=True)
        cmd(args)
        cmd(['ffmpeg','-v','error','-xerror','-i',str(tmp),'-f','null','-'])
        actual=probe(tmp); vs=next(s for s in actual['streams'] if s['codec_type']=='video')
        au=next(s for s in actual['streams'] if s['codec_type']=='audio')
        if (vs['width'],vs['height'],int(vs['nb_frames'])) != (width,height,total): fail('rendered video dimensions or frame count incorrect')
        if au.get('codec_name')!='aac': fail('output audio was not AAC')
        if float(au.get('duration',0)) < total/FPS - 0.025: fail('output audio unexpectedly short')
        src_packets=audio_packets(audio); out_packets=audio_packets(tmp)
        if not out_packets or src_packets[:len(out_packets)] != out_packets: fail('audio packets do not match source prefix')
        record=dict(plan=plan,actual=actual,validation={'complete_decode':True,'audio':'source packet hashes match the output prefix; stream copy; no subjective listening','visual_review':'not performed by renderer','input_compatibility':'PNG CRC/decode and alpha checked; different source dimensions normalized; spatial composition, contact and hidden areas require independent visual review','intermediate':'H.264 CRF 14, final H.264 CRF 18'})
        report_tmp=td/'report.json'; report_tmp.write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
        # No clobber: each publication is atomic. If report publication races,
        # preserve the video and report clearly rather than deleting a user file.
        os.link(tmp,output)
        try: os.link(report_tmp,report)
        except FileExistsError: fail(f'video saved but report path already exists: {report}')
        print(json.dumps({'output':str(output),'report':str(report),'frames':total},indent=2))


if __name__ == '__main__':
    try: main()
    except (ValueError,KeyError,FileNotFoundError,subprocess.CalledProcessError,json.JSONDecodeError) as e:
        print(f'error: {e}',file=sys.stderr); sys.exit(1)
