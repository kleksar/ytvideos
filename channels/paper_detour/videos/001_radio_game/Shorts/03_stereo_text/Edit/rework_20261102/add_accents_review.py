import json,subprocess,hashlib
from pathlib import Path
p=Path('/Users/diplomat/ytvideos/channels/paper_detour/videos/001_radio_game/Shorts/03_stereo_text');base=p/'Work/rework_20261102/full_review_forced/full_REVIEW.mp4';root=p/'Assets/Generated/accents-v03';manifest=json.loads((root/'manifest.json').read_text());out=p/'Work/rework_20261102/full_review_accents_v01';out.mkdir(parents=True,exist_ok=True)
windows=[(12,78),(390,456),(621,690),(951,1023),(1143,1224)]
cmd=['ffmpeg','-v','error','-y','-i',str(base)];filters=[];receipts=[]
for i,(cue,pair,(start,end)) in enumerate(zip(manifest['cues'],manifest['pairs'],windows),1):
 path=root/cue['png'];cmd+=['-loop','1','-framerate','30','-i',str(path)]
 placement=next(x for x in pair['comparisons'] if x['anchor']==pair['anchor']);x,y=placement['layer_top_left_px'];w,h=cue['metrics']['size_px'];filters.append(f'[{i}:v]scale={round(w/2)}:{round(h/2)},format=rgba,fade=t=in:st={start/30}:d={4/30}:alpha=1,fade=t=out:st={(end-4)/30}:d={4/30}:alpha=1[c{i}]')
 prev='0:v' if i==1 else f'v{i-1}';filters.append(f'[{prev}][c{i}]overlay={round(x/2)}:{round(y/2)}:enable=\'gte(t,{start/30})*lt(t,{end/30})\'[v{i}]')
 receipts.append({'cue':cue['id'],'text':cue['lines'],'start_frame':start,'end_frame':end,'anchor':pair['anchor'],'placement_1080':[x,y],'file':str(path),'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
output=out/'short03_accents_REVIEW.mp4';cmd+=['-filter_complex',';'.join(filters),'-map','[v5]','-map','0:a:0','-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p','-c:a','copy','-t','40.9','-movflags','+faststart',str(output)]
subprocess.run(cmd,check=True);(out/'render_receipt.json').write_text(json.dumps({'status':'REVIEW_REQUIRED','base':str(base),'base_sha256':hashlib.sha256(base.read_bytes()).hexdigest(),'output':str(output),'output_sha256':hashlib.sha256(output.read_bytes()).hexdigest(),'cues':receipts,'audio':'copied without re-encoding from continuous review base; original source unchanged'},indent=2));print(output)
