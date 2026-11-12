import json
from pathlib import Path

episode = Path('/Users/diplomat/ytvideos/new_channel/videos/032_galveston_1900')
work = episode / 'Work/subtitles-final-v01/ship-camera'
scene = json.loads((episode / 'Edit/ImageMotion/19fd8c3ec5f28ece170b/run.json').read_text())['scenes'][6]
job = {key: scene[key] for key in ('width', 'height', 'frames', 'fps', 'grain')}
job.update(input=str(work / 'static_clean.mp4'), output=str(work / 'ship_camera_g08.mp4'),
           camera=scene['baked_camera'], seed=int(scene['image_hash'][:16], 16) ^ scene['grain']['seed'],
           receipt=str(work / 'finish_receipt.json'), log=str(work / 'finish.log'))
(work / 'finish_job.json').write_text(json.dumps(job, indent=2))
