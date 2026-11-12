import json
from pathlib import Path
ep=Path(__file__).resolve().parents[1]
r=json.loads((ep/'Work/render-v02/caption_groups.json').read_text())
scene_rows=json.loads((ep/'Work/shot-map-v01.json').read_text())['scenes']
rows=[dict(id=x['id'],start=x['start_frame'],end=x['end_frame']) for x in scene_rows]
cues=[dict(id=f'C{i+1:02d}',start=x['start_frame'],end=x['end_frame']) for i,x in enumerate(r['display_intervals'])]
sets=[dict(scene=s['id'],cue=c['id'],frame=(max(s['start'],c['start'])+min(s['end'],c['end'])-1)//2) for s in rows for c in cues if max(s['start'],c['start'])<min(s['end'],c['end'])]
frames=sorted({*([478,479,480,481,958,959,960,961]),*(z['frame'] for z in sets)})
mp4=ep/'Deliverables/Brocklesby-Paper-Detour-en-v01.mp4'
identity=json.loads(Path(str(mp4)+'.delivery.json').read_text())['media']
plan=dict(frame_count=1080,fps='30/1',sha256=identity['sha256'],freshness=dict(status='CURRENT',evidence=str(mp4)+'.delivery.json'),required_review_checks=['stream_metadata','full_decode','frame_sampling','motion_framing','cue_timing','word_highlighting','subtitle_continuity','audio_signal','srt'],expected=dict(video=dict(width=1440,height=2560,codec_name='h264',pix_fmt='yuv420p',color_space='bt709'),audio=dict(required=True,codec_name='aac',channels=2,sample_rate=48000)),scenes=rows,cues=cues,extra_frames=frames,scene_seconds=[4,6])
for name,data in [('qa-plan-v01.json',plan),('scene-cue-pairs-v01.json',sets)]:
 (ep/'Edit/QA'/name).write_text(json.dumps(data,indent=2)+'\n')
