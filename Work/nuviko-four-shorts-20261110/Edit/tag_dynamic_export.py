"""Preserve encoded streams while correcting missing BT.709 video tags."""
import json
import os
from pathlib import Path
import subprocess
import sys

edit = Path(__file__).resolve().parent
name = sys.argv[1]
variant = 'hold' if '--hold' in sys.argv[2:] else 'sync' if '--sync' in sys.argv[2:] else 'unique' if '--unique' in sys.argv[2:] else 'dynamic'
revision = json.loads((edit/f'{name}-{variant}-input.json').read_text())['new_revision']
contract_path = edit/f'{name}-review-{revision}-contract.json'
contract = json.loads(contract_path.read_text())
dest = Path(contract['output'])
scratch = edit.parent/'Work'/f'{dest.stem}-tagged.mp4'

def color(path):
    data = subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_streams','-of','json',path])
    v = json.loads(data)['streams'][0]
    return [v.get(k) for k in ('color_space','color_primaries','color_transfer')]

if color(dest) != ['bt709']*3:
    cmd = ['ffmpeg','-nostdin','-n','-v','error','-i',str(dest),'-map','0:v:0','-map','0:a:0','-c','copy',
           '-bsf:v','h264_metadata=colour_primaries=1:transfer_characteristics=1:matrix_coefficients=1:video_full_range_flag=0',
           '-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709',
           '-movflags','+faststart+write_colr',str(scratch)]
    subprocess.run(cmd,check=True)
    assert color(scratch) == ['bt709']*3
    os.replace(scratch,dest)
    contract['colour_metadata_mux_argv'] = cmd
    contract_path.write_text(json.dumps(contract,indent=2,ensure_ascii=False)+'\n')
