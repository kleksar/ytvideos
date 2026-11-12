#!/usr/bin/env python3
"""Render a frame-addressed Paper/Nuviko montage with FFmpeg and word captions."""
from __future__ import annotations
import argparse, concurrent.futures, importlib.util, json, math, subprocess, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
delivery_spec = importlib.util.spec_from_file_location('montage_delivery', HERE / 'delivery.py')
delivery = importlib.util.module_from_spec(delivery_spec); delivery_spec.loader.exec_module(delivery)
spec = importlib.util.spec_from_file_location('semantic_grouping', ROOT / '.agents/skills/ytv-paper-subtitles/scripts/semantic_grouping.py')
grouping = importlib.util.module_from_spec(spec); spec.loader.exec_module(grouping)
DIRECTIONS = {'left_to_right', 'right_to_left', 'top_to_bottom', 'bottom_to_top', 'none'}
ZOOMS = {'in', 'out', 'none'}

def path_from(base, value):
    p=Path(value).expanduser(); return (p if p.is_absolute() else base/p).resolve()

def validate(plan, base):
    if plan.get('channel') not in {'paper','nuviko'}: raise ValueError('channel must be paper or nuviko')
    if plan.get('format') not in {'long','short'}: raise ValueError('format must be long or short')
    if plan.get('fps',30)!=30: raise ValueError('only 30 fps is supported')
    canvas=plan.get('canvas', [2560,1440] if plan['format']=='long' else [1440,2560])
    if not isinstance(canvas,list) or len(canvas)!=2 or any(not isinstance(v,int) or v<64 or v%2 for v in canvas): raise ValueError('canvas must contain two even integer dimensions >= 64')
    if (plan['format']=='long' and canvas[0]<=canvas[1]) or (plan['format']=='short' and canvas[0]>=canvas[1]): raise ValueError('canvas orientation must match format: long landscape, short portrait')
    audio=path_from(base,plan['audio']);
    if not audio.is_file(): raise ValueError(f'audio not found: {audio}')
    scenes=plan.get('scenes');
    if not isinstance(scenes,list) or not scenes: raise ValueError('scenes must be a nonempty list')
    cursor=0; previous=None; previous_zoom=None; result=[]
    for i,s in enumerate(scenes):
        start=s.get('start_frame'); end=s.get('end_frame')
        if not isinstance(start,int) or isinstance(start,bool) or not isinstance(end,int) or start!=cursor or end<=start: raise ValueError(f'scene {i+1}: intervals must be continuous integer frames')
        if plan.get('enforce_scene_duration',True) and not 120<=end-start<=180: raise ValueError(f'scene {i+1}: expected 4–6 seconds at 30fps')
        image=path_from(base,s['image']);
        if not image.is_file(): raise ValueError(f'image not found: {image}')
        if 'direction' not in s or 'zoom' not in s:raise ValueError(f'scene {i+1}: explicit direction and zoom are required')
        direction=s['direction'];zoom=s['zoom']
        camera=s.get('camera')
        if camera: validate_camera(camera, direction, zoom)
        if direction not in DIRECTIONS or zoom not in ZOOMS: raise ValueError(f'scene {i+1}: invalid movement')
        if direction=='none' and zoom=='none': raise ValueError(f'scene {i+1}: no movement selected')
        if direction!='none' and previous==direction: raise ValueError(f'scene {i+1}: neighboring scenes repeat direction {direction}')
        if zoom!='none' and previous_zoom==zoom: raise ValueError(f'scene {i+1}: neighboring scenes repeat zoom {zoom}')
        previous=direction;previous_zoom=zoom;result.append({'image':str(image),'start_frame':start,'end_frame':end,'direction':direction,'zoom':zoom,**({'camera':camera} if camera else {})});cursor=end
    captions=plan.get('subtitles')
    if not isinstance(captions,dict) or captions.get('mode') not in {'words','none'}: raise ValueError('subtitles.mode must be words or explicit none for a technical probe')
    overlays=plan.get('overlays',[])
    for layer in overlays:
        if not path_from(base,layer['path']).is_file():raise ValueError('missing overlay '+layer['path'])
        if not (0<=layer['start_frame']<layer['end_frame']<=cursor):raise ValueError('overlay outside timeline')
    return {'channel':plan['channel'],'format':plan['format'],'subtitle_mode':captions['mode'],'audio':str(audio),'canvas':canvas,'fps':30,'scenes':result,'frames':cursor}

def validate_camera(camera,direction,zoom):
    for name in ('start','end'):
        key=camera[name]; z=key['scale'];c=key['center']
        if not isinstance(z,(int,float)) or not math.isfinite(z) or not 1<=z<=1.3:raise ValueError('camera scale must be 1..1.3')
        if len(c)!=2 or any(not isinstance(v,(int,float)) or not math.isfinite(v) or not 0<=v<=1 for v in c):raise ValueError('camera center must be two normalized coordinates')
    a,b=camera['start'],camera['end'];minimum=min(a['scale'],b['scale'])
    # Conservative bounds guarantee coverage for the entire linear path.
    for key in (a,b):
        if any(c-.5/minimum < -1e-8 or c+.5/minimum > 1+1e-8 for c in key['center']):raise ValueError('camera path exposes an image edge')
    dz=b['scale']-a['scale'];ax,ay=a['center'];bx,by=b['center']
    dx=(.5-bx)*b['scale']-(.5-ax)*a['scale'];dy=(.5-by)*b['scale']-(.5-ay)*a['scale']
    if direction=='left_to_right' and dx<=0 or direction=='right_to_left' and dx>=0:raise ValueError('camera endpoints contradict visible movement direction')
    if direction=='top_to_bottom' and dy<=0 or direction=='bottom_to_top' and dy>=0:raise ValueError('camera endpoints contradict visible movement direction')
    if direction=='none' and (abs(dx)>1e-8 or abs(dy)>1e-8):raise ValueError('camera endpoints contradict no movement')
    if zoom=='in' and dz<=0 or zoom=='out' and dz>=0 or zoom=='none' and abs(dz)>1e-8:raise ValueError('camera endpoints contradict zoom')
    if not camera.get('subject') or not camera.get('reason'):raise ValueError('camera requires subject and reason')
    focus=camera.get('focus')
    if not isinstance(focus,list) or len(focus)!=2 or any(not isinstance(v,(int,float)) or not math.isfinite(v) or not 0<=v<=1 for v in focus):raise ValueError('camera focus must contain normalized x/y')
    for key in (a,b):
        if any(not 0.02<=((f-c)*key['scale']+.5)<=.98 for f,c in zip(focus,key['center'])):raise ValueError('camera crops the focus point')

def camera_filter(width,height,n,camera):
    if n<2:raise ValueError('scene needs at least 2 frames')
    a,b=camera['start'],camera['end']
    def lerp(x,y):return f'({x:.10f}+({y-x:.10f})*on/{n-1})'
    z=lerp(a['scale'],b['scale']);cx=lerp(a['center'][0],b['center'][0]);cy=lerp(a['center'][1],b['center'][1])
    left=f'(W/2-W*{cx}*{z})';top=f'(H/2-H*{cy}*{z})'
    return (f"scale={width}:{height}:force_original_aspect_ratio=increase:flags=lanczos,crop={width}:{height},"
            f"perspective=sense=destination:x0='{left}':y0='{top}':x1='{left}+W*{z}':y1='{top}':"
            f"x2='{left}':y2='{top}+H*{z}':x3='{left}+W*{z}':y3='{top}+H*{z}':"
            f"interpolation=cubic:eval=frame,setsar=1,format=yuv420p")

def motion_filter(width,height,n,direction,zoom):
    sw=round(width*1.10/2)*2; sh=round(height*1.10/2)*2; cx=(sw-width)//2;cy=(sh-height)//2
    if n<2: raise ValueError('scene needs at least 2 frames')
    e={'out':f'{2*width/1920:.8f}+{24*width/1920:.8f}*on/{n-1}','in':f'{26*width/1920:.8f}-{24*width/1920:.8f}*on/{n-1}','none':'0'}[zoom]
    ex=21.708*width/1920; ey=21.708*height/1080
    x={'right_to_left':f'(-{ex:.8f}+{2*ex:.8f}*on/{n-1})','left_to_right':f'({ex:.8f}-{2*ex:.8f}*on/{n-1})'}.get(direction,'0')
    y={'bottom_to_top':f'(-{ey:.8f}+{2*ey:.8f}*on/{n-1})','top_to_bottom':f'({ey:.8f}-{2*ey:.8f}*on/{n-1})'}.get(direction,'0')
    q=f'({e})*H/W'
    return (f"scale={sw}:{sh}:force_original_aspect_ratio=increase:flags=lanczos,crop={sw}:{sh},"
            f"perspective=x0='-({e})+({x})':y0='-({q})+({y})':x1='W+({e})+({x})':y1='-({q})+({y})':"
            f"x2='-({e})+({x})':y2='H+({q})+({y})':x3='W+({e})+({x})':y3='H+({q})+({y})':"
            f"interpolation=cubic:eval=frame,crop={width}:{height}:{cx}:{cy},setsar=1,format=yuv420p")

def quote(p): return "'"+str(p).replace("'", "'\\''")+"'"
def run(cmd): subprocess.run(cmd,check=True,stdin=subprocess.DEVNULL)
def scene_render(i,s,work,canvas,encoder,bitrate):
    p=work/f'scene_{i:05d}.mp4';n=s['end_frame']-s['start_frame']
    vf=camera_filter(*canvas,n,s['camera']) if s.get('camera') else motion_filter(*canvas,n,s['direction'],s['zoom'])
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-n','-loop','1','-framerate','30','-i',s['image'],'-vf',vf,'-frames:v',str(n),'-an','-c:v',encoder,'-b:v',bitrate,'-pix_fmt','yuv420p',str(p)]
    delivery.write_json(work/f'scene_{i:05d}.command.json',cmd)
    run(cmd)
    return p

def caption_sequence(plan,base,work,canvas,total):
    sub=plan['subtitles']; profile=json.loads((HERE/'profiles'/f"{plan['channel']}.json").read_text())
    if sub.get('style') or any(key in sub for key in ('width','y')):
        raise ValueError('Subtitle style and geometry are defined by the shared format profile')
    words,_=delivery.validate_words(plan,base,total)
    caption_end=sub.get('end_frame',total)
    if not isinstance(caption_end,int) or isinstance(caption_end,bool) or not 1<=caption_end<=total:
        raise ValueError('subtitles.end_frame must be an exclusive frame within the timeline')
    width,height=canvas
    _,geometry_path=delivery.profile_paths(plan['channel'],plan['format'])
    geometry=json.loads(geometry_path.read_text())
    reference=geometry['reference_height']
    factor=min(width/geometry['reference_width'],height/reference)
    fs=max(8,round(geometry['font_size_px']*factor))
    pad_x=round(profile['pad_x']*factor);pad_y=round(profile['pad_y']*factor);stroke=round(profile['outline_width']*factor)
    visible_width=geometry['max_visible_width_px']*factor
    center_x=width*geometry['center_x_ratio']
    if center_x-visible_width/2 < 0 or center_x+visible_width/2 > width:raise ValueError('Subtitle safe area is outside the canvas')
    font=ImageFont.truetype(profile['font'],fs,index=profile['font_index']);safe=visible_width-2*(pad_x+stroke)
    if sub.get('phrases'): groups=grouping.plan_phrases(words,sub['phrases'],font,safe,keep_together=sub.get('keep_together',()),combine_sentences=plan['format']=='long',boundary_exceptions=sub.get('boundary_exceptions',()))
    else:
        max_words=3 if plan['channel']=='paper' and plan['format']=='short' else None
        try:groups=grouping.group_words(words,font,safe,keep_together=sub.get('keep_together',()),max_words=max_words,combine_sentences=plan['format']=='long')
        except ValueError:
            if plan['format']!='short' or max_words is not None:raise
            groups=grouping.group_words(words,font,safe,max_words=len(words))
    if plan['channel']=='paper' and plan['format']=='short' and any(len(g)>3 for g in groups):
        raise ValueError('Paper Shorts require explicit reviewed phrases of at most 3 words; supply subtitles.phrases')
    ascent,descent=font.getmetrics(); extra=4 if plan['format']=='short' else max(1,round(4*factor))
    band_h=ascent+descent+2*pad_y+2*stroke+extra
    if plan['format']=='short':top=round(height*geometry['center_y_ratio']-band_h/2)
    else:
        top=round(height*geometry['baseline_y_ratio'])-(pad_y+stroke+ascent)
        band_h=min(band_h,round(height*geometry['bottom_y_ratio'])-top)
        if band_h < pad_y+ascent+descent+2*stroke:raise ValueError('Subtitle font does not fit above the shared bottom boundary')
    if top<0 or top+band_h>height:raise ValueError('subtitle band is outside canvas')
    directory=work/'caption_states';directory.mkdir()
    events=[]
    for gi,g in enumerate(groups):
        text=' '.join(w['text'] for w in g);line=font.getlength(text);boxw=math.ceil(line+2*pad_x+2*stroke);x=round(center_x-boxw/2)
        def state(active):
            name=directory/f'{gi:05d}_{active if active is not None else "neutral"}.png'
            if name.exists():return name
            im=Image.new('RGBA',(width,band_h));draw=ImageDraw.Draw(im)
            if profile['background']:draw.rectangle((x,0,x+boxw-1,band_h-1),fill=profile['background'])
            pen=center_x-line/2; baseline=pad_y+stroke+ascent
            for j,word in enumerate(g):
                draw.text((round(pen),baseline),word['text'],font=font,anchor='ls',fill=profile['highlight'] if j==active else profile['text'],stroke_width=stroke,stroke_fill=profile['outline'] if stroke else None)
                pen+=font.getlength(word['text'])+font.getlength(' ')
            bounds=im.getbbox(); left=center_x-visible_width/2; right=center_x+visible_width/2
            if bounds and (bounds[0] < math.ceil(left) or bounds[2] > math.floor(right)):
                raise ValueError('Subtitle pixels exceed the shared maximum visible width')
            if plan['format']=='long' and bounds and top+bounds[3]>round(height*geometry['bottom_y_ratio']):
                raise ValueError('Long subtitle pixels exceed the shared bottom boundary')
            im.save(name,compress_level=1);return name
        if gi==0:events.append((0,state(None)))
        for wi,w in enumerate(g):events.append((min(total-1,max(0,math.ceil(float(w['start'])*30-1e-7))),state(wi)))
    ordered=sorted(dict(events).items());ffcat=work/'captions.ffconcat';lines=['ffconcat version 1.0']
    if caption_end < total:
        blank=directory/'transparent.png'
        Image.new('RGBA',(width,band_h),(0,0,0,0)).save(blank,compress_level=1)
        ordered.append((caption_end,blank))
        ordered.sort(key=lambda event:event[0])
    for i,(frame,p) in enumerate(ordered):
        end=ordered[i+1][0] if i+1<len(ordered) else total
        if end>frame:lines.extend(['file '+quote(p),'option framerate 30',f'duration {(end-frame)/30:.12f}'])
    lines.extend(['file '+quote(ordered[-1][1]),'option framerate 30']);ffcat.write_text('\n'.join(lines)+'\n')
    report={'status':'REVIEW_REQUIRED','groups':groups,'profile':profile,'geometry_profile':str(geometry_path),'shared_geometry':geometry,'shared_short_geometry':geometry if plan['format']=='short' else None,'channel':plan['channel'],'format':plan['format'],'canvas':list(canvas),'reference_height':reference,'scale':factor,'resolved_font_size_px':fs,'max_visible_width_px':visible_width,'center_x_px':center_x,'baseline':top+pad_y+stroke+ascent}
    report['grouping_source']='explicit_plan' if sub.get('phrases') else 'automatic_draft'
    report['algorithm']=grouping.VERSION
    report['boundary_exceptions']=sub.get('boundary_exceptions',[])
    report['boundary_warnings']=grouping.boundary_warnings(groups)
    report['caption_end_frame']=caption_end
    report['display_intervals']=[{'start_frame':0 if i==0 else math.ceil(g[0]['start']*30-1e-7),'end_frame':math.ceil(groups[i+1][0]['start']*30-1e-7) if i+1<len(groups) else caption_end} for i,g in enumerate(groups)]
    report['word_events']=[{'frame':frame,'path':str(path)} for frame,path in ordered]
    delivery.write_json(work/'caption_groups.json',report)
    resolved={key:report[key] for key in ('resolved_font_size_px','max_visible_width_px','center_x_px','baseline','algorithm','display_intervals','boundary_warnings')}
    contract=delivery.subtitle_contract(plan,base,canvas,total,groups,resolved)
    delivery.write_json(work/'subtitle_contract.json',contract)
    delivery.write_json(work/'subtitle_review.json',delivery.review_template(contract))
    return ffcat,top

def final_command(plan,base,prepared,work,out,subtitle,encoder,video_bitrate,audio):
    video=work/'picture.mp4';frames=prepared['frames'];sub=plan['subtitles']
    audio_codec=audio['codec_name'];audio_channels=int(audio['channels'])
    audio_bitrate='256k' if audio_channels >= 2 else '192k'
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-n','-i',str(video)]; filters=[]; source='0:v';index=1
    if subtitle:
        path,y=subtitle
        if sub['mode']=='words' or path.suffix=='.ffconcat':cmd+=['-f','concat','-safe','0']
        cmd+=['-i',str(path)];filters.append(f'[{index}:v]fps=30,format=rgba[subs]');filters.append(f'[{source}][subs]overlay=0:{y}:eof_action=pass:format=auto[vsub]');source='vsub';index+=1
    for j,layer in enumerate(plan.get('overlays',[])):
        path=path_from(base,layer['path'])
        if path.suffix.lower() in {'.png','.jpg','.jpeg','.webp'}:cmd+=['-loop','1','-framerate','30']
        cmd+=['-i',str(path)];start=layer['start_frame'];end=layer['end_frame'];x=int(layer.get('x',0));y=int(layer.get('y',0))
        filters.append(f'[{index}:v]setpts=PTS-STARTPTS+{start}/(30*TB)[ov{j}]');filters.append(f'[{source}][ov{j}]overlay={x}:{y}:enable=\'gte(n,{start})*lt(n,{end})\':eof_action=pass:format=auto[v{j}]');source=f'v{j}';index+=1
    audioindex=index;cmd+=['-i',prepared['audio']]
    # Explicit opt-in for sRGB-authored scenes and caption graphics. Restore RGB
    # before an explicit matrix/range conversion and the sRGB -> Rec.709 transfer.
    color=''
    if plan.get('source_transfer')=='srgb':
        color='format=rgb24,scale=in_range=pc:out_range=tv:out_color_matrix=bt709,format=yuv444p,colorspace=ispace=bt709:itrc=srgb:iprimaries=bt709:irange=tv:all=bt709:range=tv:format=yuv420p,'
    elif plan.get('source_transfer') is not None:
        raise ValueError('source_transfer must be srgb when supplied')
    filters.append(f'[{source}]{color}setsar=1,format=yuv420p[vout]')
    cmd+=['-filter_complex',';'.join(filters),'-map','[vout]','-map',f'{audioindex}:a:0','-c:v',encoder,'-b:v',video_bitrate,'-pix_fmt','yuv420p','-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709','-color_range','tv','-c:a',('copy' if audio_codec=='aac' else 'aac'),*([] if audio_codec=='aac' else ['-b:a',audio_bitrate]),'-t',f'{frames/30:.12f}','-movflags','+faststart',str(out)]
    return cmd

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('manifest',type=Path);ap.add_argument('--output',type=Path,required=True);ap.add_argument('--work-dir',type=Path,required=True);ap.add_argument('--jobs',type=int,default=2);ap.add_argument('--encoder',default='h264_videotoolbox');ap.add_argument('--bitrate',default='20M');ap.add_argument('--plan-only',action='store_true');ap.add_argument('--prepare-subtitles',action='store_true',help='Prepare the same subtitle states and contract as the full renderer, without encoding video');ap.add_argument('--export-contract',type=Path,help='READY_TO_RENDER passport required for encoding');ap.add_argument('--check-settings',action='store_true',help='Validate passport against actual command without encoding');args=ap.parse_args()
    manifest=args.manifest.resolve(); base=manifest.parent;plan=json.loads(manifest.read_text()); prepared=validate(plan,base)
    if sum((args.plan_only,args.prepare_subtitles,args.check_settings))>1:raise ValueError('Choose one preparation mode')
    if args.jobs<1:raise ValueError('jobs must be positive')
    out=args.output.resolve();work=args.work_dir.resolve()
    if out.exists() or work.exists():raise ValueError('output or work directory exists; choose new paths')
    work.mkdir(parents=True);out.parent.mkdir(parents=True,exist_ok=True)
    (work/'input_manifest.json').write_text(json.dumps(plan,indent=2,ensure_ascii=False)+'\n')
    prepared['manifest_path']=str(manifest)
    prepared['source_transfer']=plan.get('source_transfer')
    (work/'plan.json').write_text(json.dumps(prepared,indent=2,ensure_ascii=False)+'\n')
    if args.plan_only: print(f'PLAN {work / "plan.json"}');return
    canvas=prepared['canvas'];frames=prepared['frames'];sub=plan['subtitles'];subtitle=None
    inputs=delivery.render_inputs(manifest,plan,base)
    if sub['mode']=='words':subtitle=caption_sequence(plan,base,work,canvas,frames)
    elif args.prepare_subtitles:raise ValueError('Subtitle preparation requires subtitles.mode=words')
    if args.prepare_subtitles:print(f'SUBTITLES {work / "subtitle_contract.json"}');return
    contract=json.loads((work/'subtitle_contract.json').read_text()) if sub['mode']=='words' else None
    review=json.loads(path_from(base,sub['review']).read_text()) if sub.get('review') else None
    if review is not None and review.get('subtitle_contract_sha256')!=delivery.fingerprint(contract):
        raise ValueError('Pre-render subtitle review is stale')
    audio_info=json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','a:0','-show_entries','stream=codec_name,profile,channels,sample_rate,bit_rate,duration:format=duration','-of','json',prepared['audio']]))
    audio_stream=audio_info.get('streams',[])
    if not audio_stream:raise ValueError('audio input has no audio stream')
    audio_duration=float(audio_stream[0].get('duration') or audio_info['format']['duration'])
    if audio_duration + 0.04 < frames/30:raise ValueError('audio is shorter than the timeline; supply the full accepted mix')
    if not args.export_contract:raise ValueError('--export-contract is required before encoding; provide the accepted passport')
    passport_path=args.export_contract.resolve()
    cmd=final_command(plan,base,prepared,work,out,subtitle,args.encoder,args.bitrate,audio_stream[0])
    passport=json.loads(passport_path.read_text())
    settings=delivery.check_export_settings(passport,cmd,prepared,audio_stream[0],manifest,out)
    delivery.write_json(work/'render_command.json',cmd)
    delivery.write_json(work/'settings_check.json',{'status':'PASS','settings':settings})
    engine=contract['engine'] if contract else [delivery.file_record(HERE/'montage.py'),delivery.file_record(HERE/'delivery.py')]
    provenance=delivery.freeze_render(work,passport_path,work/'render_command.json',engine,prepared,audio_stream[0],manifest,out)
    delivery.write_json(work/'render_provenance.json',provenance)
    if args.check_settings:print(f'SETTINGS_PASS {work / "settings_check.json"}');return
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.jobs) as pool:
        futures=[pool.submit(scene_render,i,s,work,canvas,args.encoder,args.bitrate) for i,s in enumerate(prepared['scenes'])]
        clips=[f.result() for f in futures]
    listing=work/'scenes.ffconcat';listing.write_text('ffconcat version 1.0\n'+''.join('file '+quote(p)+'\n' for p in clips));video=work/'picture.mp4'
    run(['ffmpeg','-hide_banner','-loglevel','error','-n','-f','concat','-safe','0','-i',str(listing),'-c','copy',str(video)])
    for p in clips:p.unlink()
    run(cmd)
    if sub['mode']=='words':
        # Detect writers changing accepted inputs or the running engine during render.
        for record in inputs + contract['profiles'] + contract['engine']:
            delivery.check_record(record)
        delivery.write_receipt(out,plan['channel'],contract,inputs,review,provenance)
    print(f'RENDERED {out}',flush=True)

if __name__=='__main__':
    try:main()
    except (ValueError,TypeError,KeyError,OSError,subprocess.CalledProcessError,json.JSONDecodeError) as e: print(f'ERROR: {e}',file=sys.stderr);sys.exit(2)
