"""Direct timed-SRT to editable Text+ candidate using the existing native adapter."""
from fractions import Fraction
import hashlib
import json
import copy
import subprocess
from pathlib import Path

from command import candidate_token, script_call, sha
from layout import native_layout
from mcp import ResolveMCP
from srt_plan import format_srt, plan_srt


def adapt_baseline(template, width, height):
    """Scale a clearly labelled generic baseline on its 16:9/9:16 aspect."""
    result=copy.deepcopy(template); recipe=result['recipe']; style=result['style']
    if recipe.get('baseline') is not True:
        return result
    old_w,old_h=recipe['raster']
    if abs(width*old_h-height*old_w)>max(width,height)*0.01:
        raise ValueError('Generic baseline requires a 16:9 or 9:16 raster')
    scale=height/old_h
    recipe['raster']=[width,height]
    for field in ('font_metrics_px','center_y'):
        recipe[field]=round(recipe[field]*scale, 6)
    recipe['font_metrics_px']=round(recipe['font_metrics_px'])
    recipe['center_x']=width/2
    recipe['max_width']=round(width*0.8)
    geom=style['geometry']
    geom.update(reference_width=width,reference_height=height,font_size_px=recipe['font_metrics_px'],
                max_visible_width_px=recipe['max_width'],center_x_ratio=.5,center_y_ratio=recipe['center_y']/height)
    recipe['profile_geometry']=dict(geom)
    return result


def install_srt(srt_path, template_path, output, *, channel=None, exact_fps=None, dimensions=None, baseline=False):
    """Create or recheck an owned candidate in the already active project.

    Requires exclusive access to Resolve. Never modifies the supplied SRT.
    """
    source=Path(srt_path).resolve(); template_file=Path(template_path).resolve() if template_path else None
    out=Path(output).resolve()
    if source.is_relative_to(out) or template_file and template_file.is_relative_to(out):
        raise ValueError('Source SRT and template must be outside the output directory')
    if baseline and template_file is not None:
        raise ValueError('Choose baseline or explicit template, not both')
    if template_file is None and not channel and not baseline:
        raise ValueError('Channel, explicit native template or generic baseline required')
    original=source.read_bytes(); source_hash=hashlib.sha256(original).hexdigest()
    text=original.decode('utf-8-sig')
    client=ResolveMCP(timeout=75)
    try:
        observed=script_call(client,'discover_current(resolve)')
        raw_width,raw_height=observed['width_observed'],observed['height_observed']
        missing=raw_width in ('','None','0') or raw_height in ('','None','0')
        if missing:
            if not dimensions or len(dimensions)!=2:
                raise ValueError('Timeline dimensions unavailable; supply explicit dimensions')
            width,height=dimensions
        else:
            width,height=int(raw_width),int(raw_height)
            if dimensions and list(dimensions)!=[width,height]:
                raise ValueError('Explicit dimensions conflict with Resolve readback')
        if type(width) is not int or type(height) is not int or width<=0 or height<=0 or width==height:
            raise ValueError('Timeline dimensions unavailable or orientation ambiguous')
        if baseline:
            template_file=Path(__file__).with_name('templates')/('generic-landscape.json' if width>height else 'generic-portrait.json')
        elif template_file is None:
            matches=[]
            for path in Path(__file__).with_name('templates').glob('*.json'):
                item=json.loads(path.read_text(encoding='utf-8'))
                if item['style']['channel']==channel and item['recipe']['raster']==[width,height]:
                    matches.append(path)
            if len(matches)!=1:
                raise ValueError('No unique channel template for observed timeline dimensions; supply --template')
            template_file=matches[0].resolve()
        if template_file.is_relative_to(out):
            raise ValueError('Template must be outside the output directory')
        template=json.loads(template_file.read_text(encoding='utf-8'))
        if set(template) != {'recipe_id','recipe','style'}:
            raise ValueError('Template requires recipe_id, recipe and style')
        if channel and template['style']['channel']!=channel and not baseline:
            raise ValueError('Template belongs to a different channel')
        if baseline:
            template=adapt_baseline(template,width,height)
        fps_text=observed['fps_observed']
        if exact_fps is None:
            fps=Fraction(fps_text)
            if fps.denominator != 1:
                raise ValueError('Fractional frame rate requires explicit exact_fps')
        else:
            fps=Fraction(exact_fps)
            if fps<=1 or abs(float(fps)-float(fps_text)) > .005:
                raise ValueError('Exact fps conflicts with Resolve readback')
        target=dict(project_id=observed['project_id'],timeline_id=observed['timeline_id'],
                    origin_frame=observed['origin_frame'],end_frame=observed['end_frame'],
                    raster=[width,height],fps=str(fps))
        native_target=dict(target,native_fps_values=[fps_text],explicit_missing_raster=missing)
        before=script_call(client,'snapshot(resolve, '+repr(native_target)+')')
        plan=plan_srt(text,target); plan['source_srt_sha256']=source_hash
        plan['conform_sha256']=source_hash; plan['style']=template['style']
        shots=[dict(id='synthetic-carrier',carrier_id='synthetic-carrier',
                    start_frame=plan['cues'][0]['start_frame'],end_frame=plan['cues'][-1]['end_frame'])]
        layout=native_layout(plan,shots,template['recipe_id'],template=template['recipe'],neutral_only=True)
        layout['orientation']='landscape' if width>height else 'portrait'
        token=candidate_token({'plan':plan,'layout':layout,'replace_tracks':[]},before)
        name='Native branded candidate '+token[-16:]
        out.mkdir(parents=True,exist_ok=True)
        (out/'plan.json').write_text(json.dumps(plan,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
        (out/'display.srt').write_text(format_srt(plan),encoding='utf-8')
        (out/'native-layout.json').write_text(json.dumps(layout,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
        # This tiny neutral file is only a Fusion composition carrier; Text+ and
        # panel remain separate editable nodes, never baked into this media.
        carrier=out/('technical-carrier-'+token[-16:]+'.mp4')
        frames=shots[0]['end_frame']-shots[0]['start_frame']
        if not carrier.exists():
            subprocess.run(['ffmpeg','-v','error','-n','-f','lavfi','-i',
                'color=c=black:s=16x16:r='+str(fps),'-frames:v',str(frames),
                '-c:v','libx264','-pix_fmt','yuv420p',str(carrier)],check=True)
        probe=subprocess.run(['ffprobe','-v','error','-count_frames','-select_streams','v:0',
            '-show_entries','stream=nb_read_frames,r_frame_rate,width,height','-of','json',str(carrier)],
            check=True,capture_output=True,text=True)
        streams=json.loads(probe.stdout)['streams']
        if len(streams)!=1 or int(streams[0]['nb_read_frames'])!=frames or Fraction(streams[0]['r_frame_rate'])!=fps or (streams[0]['width'],streams[0]['height'])!=(16,16):
            raise ValueError('Technical carrier does not match planned frames and fps')
        comps=out/('native-comps-'+token[-16:]); comps.mkdir(exist_ok=True)
        paths=[str(comps/f'section-{i:04d}.comp') for i in range(len(shots))]
        receipt_file=out/'native-receipt.json'
        receipt_file.write_text(json.dumps(dict(status='IN_PROGRESS',candidate_name=name,token=token)))
        expression='install_branded(resolve, '+', '.join(repr(v) for v in
            (native_target,before,layout,None,None,paths,name,token,[],str(carrier)))+')'
        try:
            receipt=script_call(client,expression,branded=True)
        except Exception as exc:
            receipt_file.write_text(json.dumps(dict(status='UNKNOWN',candidate_name=name,token=token,
                error=str(exc),next='Inspect candidate and source before retrying.'),indent=2))
            raise
        if receipt.get('status') not in ('CREATED','UNCHANGED') or receipt.get('native_cues') != 0:
            raise RuntimeError('Native candidate readback did not confirm success')
        if sha(source)!=source_hash:
            raise RuntimeError('SRT source changed during native authoring')
        receipt.update(source_srt_sha256=source_hash,template_sha256=sha(template_file),
                       orientation=layout['orientation'],generic_baseline=baseline,technical_carrier_sha256=sha(carrier),render=False,published=False,
                       visual='UNVERIFIED',playback='UNVERIFIED')
        receipt_file.write_text(json.dumps(receipt,indent=2)+'\n')
        return receipt
    finally:
        client.close()
