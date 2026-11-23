"""Direct timed-SRT to editable Text+ candidate using the existing native adapter."""
from fractions import Fraction
import hashlib
import json
from pathlib import Path

from command import candidate_token, script_call, sha
from layout import native_layout
from mcp import ResolveMCP
from srt_plan import choose_carriers, format_srt, plan_srt


def install_srt(srt_path, template_path, output, *, channel=None, exact_fps=None, dimensions=None):
    """Create or recheck an owned candidate in the already active project.

    Requires exclusive access to Resolve. Never modifies the supplied SRT.
    """
    source=Path(srt_path).resolve(); template_file=Path(template_path).resolve() if template_path else None
    out=Path(output).resolve()
    if source.is_relative_to(out) or template_file and template_file.is_relative_to(out):
        raise ValueError('Source SRT and template must be outside the output directory')
    if template_file is None and not channel:
        raise ValueError('Channel or explicit native template required')
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
        if template_file is None:
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
        if channel and template['style']['channel']!=channel:
            raise ValueError('Template belongs to a different channel')
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
        shots=choose_carriers(before,plan['cues'])
        layout=native_layout(plan,shots,template['recipe_id'],template=template['recipe'],neutral_only=True)
        layout['orientation']='landscape' if width>height else 'portrait'
        token=candidate_token({'plan':plan,'layout':layout,'replace_tracks':[]},before)
        name='Native branded candidate '+token[-16:]
        out.mkdir(parents=True,exist_ok=True)
        (out/'plan.json').write_text(json.dumps(plan,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
        (out/'display.srt').write_text(format_srt(plan),encoding='utf-8')
        (out/'native-layout.json').write_text(json.dumps(layout,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
        comps=out/('native-comps-'+token[-16:]); comps.mkdir(exist_ok=True)
        paths=[str(comps/f'section-{i:04d}.comp') for i in range(len(shots))]
        receipt_file=out/'native-receipt.json'
        receipt_file.write_text(json.dumps(dict(status='IN_PROGRESS',candidate_name=name,token=token)))
        expression='install_branded(resolve, '+', '.join(repr(v) for v in
            (native_target,before,layout,None,None,paths,name,token,[]))+')'
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
                       orientation=layout['orientation'],render=False,published=False,
                       visual='UNVERIFIED',playback='UNVERIFIED')
        receipt_file.write_text(json.dumps(receipt,indent=2)+'\n')
        return receipt
    finally:
        client.close()
