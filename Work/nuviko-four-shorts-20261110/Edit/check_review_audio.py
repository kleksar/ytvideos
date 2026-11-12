import json
import subprocess
import sys
from pathlib import Path

import numpy as np

root = Path(__file__).resolve().parents[1]
edit = root / 'Edit'

def pcm(path):
    data = subprocess.check_output(['ffmpeg','-nostdin','-v','error','-i',str(path),'-map','0:a:0','-ar','8000','-ac','1','-f','f32le','-'])
    return np.frombuffer(data, dtype='<f4')

for name in sys.argv[1:]:
    qa = edit/f'{name}-review-qa.json'
    result = json.loads(qa.read_text())
    output = pcm(result['file'])
    source = pcm(edit/f'{name}-review-excerpt.wav')
    n = min(len(source), len(output))
    a, b = output[1600:n-2000], source[1600:n-2000]
    if n<3600:
        raise ValueError(f'Short audio unexpectedly missing for {name}')
    match = float(np.corrcoef(a,b)[0,1])
    peak = float(np.max(np.abs(output)))
    result['audio_signal']={'decoded_excerpt_correlation':round(match,6),'mono_peak_amplitude':round(peak,5),'compared_without_fades':True}
    qa.write_text(json.dumps(result,indent=2)+'\n')
    print(name, result['audio_signal'])
