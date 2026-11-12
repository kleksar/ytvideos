import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

root = Path(__file__).resolve().parents[1]
edit = root/'Edit'
name, revision = sys.argv[1:]
prefix = f'{name}-review' if revision=='v01' else f'{name}-review-{revision}'
contract = json.loads((edit/f'{prefix}-contract.json').read_text())
file = root/'Deliverables'/f"{contract['title']}-review-{revision}.mp4"
subprocess.run(['ffmpeg','-nostdin','-v','error','-xerror','-i',file,'-map','0:v:0','-map','0:a:0','-f','null','-'],check=True)
probe = json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-show_streams','-show_format','-of','json',file]))
video, audio = probe['streams']
assert (video['width'],video['height'],video['avg_frame_rate'],int(video['nb_read_frames'])) == (1080,1920,'30/1',contract['frames'])
assert (audio['codec_name'],audio['sample_rate'],audio['channels']) == ('aac','44100',2)
log = subprocess.run(['ffmpeg','-nostdin','-i',file,'-vn','-af','ebur128=peak=true','-f','null','-'],capture_output=True,text=True,check=True).stderr
peak = float(re.findall(r'Peak:\s+(-?\d+\.\d+) dBFS',log)[-1])
lufs = float(re.findall(r'I:\s+(-?\d+\.\d+) LUFS',log)[-1])
assert peak<0
frames = sorted({16,contract['frames']-18,*[n+d for n in contract['transition_centres'] for d in [-5,0,5]]})
selection = '+'.join(f'eq(n,{x})' for x in frames)
contact = edit/f'{prefix}-contact.jpg'
subprocess.run(['ffmpeg','-nostdin','-n','-v','error','-i',file,'-vf',f"select='{selection}',scale=120:212,tile=8x3",'-frames:v','1',contact],check=True)
qa = {'file':str(file),'sha256':hashlib.sha256(file.read_bytes()).hexdigest(),'frames':contract['frames'],'size':[1080,1920],'fps':30,'duration':probe['format']['duration'],'full_decode':'PASS','true_peak_dBFS':peak,'integrated_lufs':lufs,'frame_selection':frames,'frame_sampling':'PENDING','continuous_playback':'UNVERIFIED','subjective_audio_listening':'UNVERIFIED','subtitle_timing':'Machine timing with manual adjustments, unverified against continuous audio'}
(edit/f'{prefix}-qa.json').write_text(json.dumps(qa,indent=2)+'\n')
print(file.name,qa['sha256'],peak,lufs)
