#!/usr/bin/env python3
"""Render a review-only Paper accent overlay from prepared PNGs; copy audio unchanged."""
import argparse
import hashlib
import json
import math
import subprocess
from fractions import Fraction
from pathlib import Path


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def probe(path):
    return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-of','json',str(path)]))['streams']


def audio_hash(path):
    return subprocess.check_output(['ffmpeg','-v','error','-i',str(path),'-map','0:a:0','-c','copy','-f','hash','-hash','sha256','-'],text=True).strip()


def keyframes(start, end, transition, fps):
    if any(type(x) is not int for x in (start,end,transition)) or start<0 or transition<1:
        raise ValueError('Frame positions must be integers and transition must be positive')
    keys=[start,start+transition,end-1-transition,end-1]
    if keys[2]-keys[1] < math.ceil(.9*fps):
        raise ValueError('Accent hold must be at least 0.9 seconds; revise the cue')
    return keys


def build_plan(config, prepared, video, root):
    fps=float(Fraction(video['avg_frame_rate']));total=int(video['nb_frames'])
    if Fraction(video['avg_frame_rate'])!=Fraction(video['r_frame_rate']):
        raise ValueError('Variable-rate input requires conform before overlay')
    width,height=video['width'],video['height'];cw,ch=prepared['canvas']
    if width*ch!=height*cw: raise ValueError('Video and prepared canvas aspect ratios differ')
    scale=width/cw
    motion=config['motion'];delta=motion['rise_canvas_fraction']
    if isinstance(delta,bool) or not isinstance(delta,(int,float)) or not math.isfinite(delta) or not 0<delta<=.05:
        raise ValueError('rise_canvas_fraction must be positive and at most 0.05')
    transition=motion['transition_frames'];cues={c['id']:c for c in prepared['cues']}
    pairs={}
    for pair in prepared['pairs']:pairs.setdefault(pair['cue'],[]).append(pair)
    records=[];seen=set()
    for interval in config['intervals']:
        cid=interval['cue'];start,end=interval['start_frame'],interval['end_frame']
        if cid in seen:raise ValueError('Use one interval per prepared cue; split repeated cues explicitly')
        seen.add(cid)
        keys=keyframes(start,end,transition,fps)
        if end>total:raise ValueError('Accent extends beyond video')
        if cid not in cues or cid not in pairs:raise ValueError('Cue missing from prepared manifest')
        cue=cues[cid];positions=[]
        for pair in pairs[cid]:
            comparison=next(x for x in pair['comparisons'] if x['anchor']==pair['anchor'])
            if comparison['checks']['technical']!='PASS':raise ValueError('Prepared geometry is not technically valid')
            positions.append(comparison['layer_top_left_px'])
        if any(p!=positions[0] for p in positions):raise ValueError('Cue crosses differing anchors; resolve explicitly')
        x,y=positions[0];sw,sh=cue['metrics']['size_px'];x,y=round(x*scale),round(y*scale);sw,sh=round(sw*scale),round(sh*scale);dy=height*delta
        box=cue['metrics']['alpha_bbox'];left=x+box[0]*scale;right=x+box[2]*scale;top=y+box[1]*scale-dy;bottom=y+box[3]*scale+dy
        if left<0 or right>width or top<0 or bottom>height:raise ValueError('Accent motion leaves canvas')
        path=(root/cue['png']).resolve()
        if digest(path)!=cue['png_sha256']:raise ValueError('Prepared PNG changed since preflight')
        records.append({'cue':cid,'png':str(path),'sha256':digest(path),'text':cue['lines'],'keys':keys,'x':x,'y':y,'width':sw,'height':sh,'rise_px':dy})
    if not records:raise ValueError('No accent intervals supplied')
    return {'fps':fps,'frames':total,'canvas':[width,height],'cues':records}


def command(video, plan, output):
    cmd=['ffmpeg','-v','error','-n','-i',str(video)];filters=[];fps=plan['fps']
    for i,cue in enumerate(plan['cues'],1):
        cmd+=['-loop','1','-framerate',str(fps),'-i',cue['png']]
        start,hold,exit,last=[f/fps for f in cue['keys']];d=hold-start;y=cue['y'];dy=cue['rise_px']
        filters.append(f'[{i}:v]scale={cue["width"]}:{cue["height"]},format=rgba,fade=t=in:st={start}:d={d}:alpha=1,fade=t=out:st={exit}:d={last-exit}:alpha=1[c{i}]')
        position=f'if(lt(t,{hold}),{y}+{dy}*(1-(t-{start})/{d}),if(gt(t,{exit}),{y}-{dy}*(t-{exit})/{last-exit},{y}))'
        previous='0:v' if i==1 else f'v{i-1}'
        filters.append(f'[{previous}][c{i}]overlay=x={cue["x"]}:y=\'{position}\':enable=\'gte(t,{start})*lt(t,{(cue["keys"][-1]+1)/fps})\'[v{i}]')
    cmd+=['-filter_complex',';'.join(filters),'-map',f'[v{len(plan["cues"])}]','-map','0:a:0','-frames:v',str(plan['frames']),'-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p','-c:a','copy','-movflags','+faststart',str(output)]
    return cmd


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('config',type=Path);parser.add_argument('--output-dir',type=Path,required=True);parser.add_argument('--plan-only',action='store_true');args=parser.parse_args()
    config=json.loads(args.config.read_text());base=args.config.resolve().parent
    video=(base/config['video']).resolve();manifest=(base/config['caption_manifest']).resolve();prepared=json.loads(manifest.read_text());streams=probe(video)
    if not any(s['codec_type']=='audio' for s in streams):raise ValueError('Audio stream required for preservation check')
    v=next(s for s in streams if s['codec_type']=='video');plan=build_plan(config,prepared,v,manifest.parent)
    args.output_dir.mkdir(parents=True,exist_ok=False);out=args.output_dir/'accent_review.mp4';plan.update(status='PLANNED',video=str(video),video_sha256=digest(video),caption_manifest=str(manifest),caption_manifest_sha256=digest(manifest),config_sha256=digest(args.config),script_sha256=digest(__file__),review='Technical checks do not verify scene objects, speech timing, style or independent QA')
    receipt=args.output_dir/'receipt.json';receipt.write_text(json.dumps(plan,indent=2)+'\n')
    if args.plan_only:print(receipt);return
    plan['status']='RENDERING';receipt.write_text(json.dumps(plan,indent=2)+'\n')
    subprocess.run(command(video,plan,out),check=True)
    before,after=audio_hash(video),audio_hash(out);actual=next(s for s in probe(out) if s['codec_type']=='video')
    if before!=after:raise ValueError('Audio packet hash changed; do not accept output')
    if int(actual['nb_frames'])!=plan['frames']:raise ValueError('Output frame count differs')
    subprocess.run(['ffmpeg','-v','error','-i',str(out),'-f','null','-'],check=True)
    plan.update(status='REVIEW_REQUIRED',output=str(out.resolve()),output_sha256=digest(out),audio_packet_hash=after,audio_unchanged=True,decode='PASS');receipt.write_text(json.dumps(plan,indent=2)+'\n');print(out)

if __name__=='__main__':main()
