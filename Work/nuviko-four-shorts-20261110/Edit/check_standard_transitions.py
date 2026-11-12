import hashlib
import json
import subprocess
import sys
from pathlib import Path

root = Path(__file__).resolve().parents[1]
edit = root/'Edit'
repo = root.parents[1]
name, revision = sys.argv[1:]
prefix = f'{name}-review-{revision}'
contract = json.loads((edit/f'{prefix}-contract.json').read_text())
path = root/'Deliverables'/f"{contract['title']}-review-{revision}.mp4"

def output(*args):
    return subprocess.check_output([str(arg) for arg in args], cwd=repo)

def audio_hash(file):
    return output('ffmpeg','-v','error','-i',file,'-map','0:a:0','-c','copy','-f','hash','-hash','sha256','-').decode().strip()

probe = json.loads(output('ffprobe','-v','error','-count_frames','-show_streams','-show_format','-of','json',path))
v,a = probe['streams']
assert (v['width'],v['height'],v['avg_frame_rate'],int(v['nb_read_frames'])) == (1080,1920,'30/1',contract['frames'])
assert (a['codec_name'],a['channels'],a['sample_rate']) == ('aac',2,'44100')
assert len(contract['clips']) == len(contract['transition_centres']) + 1
assert audio_hash(path) == audio_hash(contract['previous_review']), 'AAC packets changed'
subprocess.run(['ffmpeg','-nostdin','-v','error','-xerror','-i',path,'-map','0:v:0','-map','0:a:0','-f','null','-'],check=True)
centres = contract['transition_centres']
map_file = edit/f'{prefix}-cut-map.json'
beat_file = edit/f'{prefix}-final-beats.json'
map_file.write_text(json.dumps({'fps':30,'cut_frames':centres},indent=2)+'\n')
output('python3','automation/music_beats.py',path,'--fps','30','--cut-map',map_file,'--output',beat_file)
beats = json.loads(beat_file.read_text())
matched = {item['nearest_cut_frame']:item['distance_frames'] for item in beats['cut_audit']['matched']}
indices = [c+d for c in centres for d in (-7,-3,0,3,7)]
expr = '+'.join(f'eq(n,{frame})' for frame in indices)
contact = edit/f'{prefix}-transitions.jpg'
output('ffmpeg','-nostdin','-n','-v','error','-i',path,'-vf',f"select='{expr}',scale=108:192,tile=5x{len(centres)}",'-frames:v','1',contact)
receipt = {'file':str(path),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
           'frames':contract['frames'],'fps':30,'size':[1080,1920],'duration':probe['format']['duration'],
           'full_decode':'PASS','audio_packets':audio_hash(path),'audio_packet_identity':'PASS',
           'transition_effects':contract['transition_effects'],'transition_centres':centres,
           'transition_samples':indices,'transition_samples_inspection':'PENDING',
           'beat_distances_frames':[matched.get(c) for c in centres],
           'continuous_playback':'UNVERIFIED','subjective_audio_listening':'UNVERIFIED',
           'subtitles':'existing timed captions retained; partial coverage' if name=='super-funk' else 'existing timed captions retained'}
(edit/f'{prefix}-qa.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(path.name, receipt['sha256'], receipt['beat_distances_frames'], flush=True)
