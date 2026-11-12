"""Measured local checks; these do not claim full audiovisual viewing."""
import hashlib
import argparse
import json
import subprocess
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('preset', nargs='?', type=Path, default=Path(__file__).resolve().parent/'preset.json')
preset_path = parser.parse_args().preset.resolve()
root = preset_path.parent
p = json.loads(preset_path.read_text())
video = root/p['output']
w,h = p['width'],p['height']
size = w*h*3//2
probe = json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames',
                    '-show_streams','-show_format','-of','json',str(video)]))
vs = next(s for s in probe['streams'] if s['codec_type']=='video')
assert (vs['width'],vs['height'],vs['nb_read_frames'],vs['avg_frame_rate']) == (w,h,'450','30/1')
assert all(vs[k]=='bt709' for k in ('color_space','color_transfer','color_primaries'))
assert vs['color_range']=='tv'
subprocess.run(['ffmpeg','-v','error','-i',str(video),'-f','null','-'],check=True)
frames = [80,243,400]
expression = '+'.join(f'eq(n\\,{n})' for n in frames)
raw = subprocess.check_output(['ffmpeg','-v','error','-i',str(video),'-map','0:v:0',
          '-vf',f'select={expression}','-fps_mode','passthrough','-pix_fmt','yuv420p',
          '-f','rawvideo','pipe:1'])
assert len(raw)==size*len(frames)
results=[]
sheet=Image.new('RGB',(1200,720));draw=ImageDraw.Draw(sheet)
for j,n in enumerate(frames):
    clean=np.fromfile(root/f'sample_{n:03}_clean.yuv',dtype=np.uint8)
    grain=np.fromfile(root/f'sample_{n:03}_grain.yuv',dtype=np.uint8)
    encoded=np.frombuffer(raw[j*size:(j+1)*size],dtype=np.uint8)
    y=clean[:w*h].reshape(h,w).astype(np.float32)
    injected=grain[:w*h].reshape(h,w).astype(np.float32)-y
    residual=encoded[:w*h].reshape(h,w).astype(np.float32)-y
    # Projection on known random input noise, avoiding high-contrast edges.
    flat=(np.abs(np.diff(y,axis=1,prepend=y[:,:1]))<2)&(np.abs(np.diff(y,axis=0,prepend=y[:1]))<2)&(y>=64)&(y<=208)
    gain=float(np.sum(residual[flat]*injected[flat])/np.sum(injected[flat]**2))
    assert np.array_equal(clean[w*h:],grain[w*h:])
    assert np.mean(injected**2)>0.1
    results.append({'frame':n,'pre_encode_luma_rms':float(np.sqrt(np.mean(injected**2))),
                    'chroma_unchanged_before_encode':True,
                    'local_encode_noise_projection_gain_flat_midtones':gain})
    png=subprocess.check_output(['ffmpeg','-v','error','-f','rawvideo','-pixel_format','yuv420p',
        '-video_size',f'{w}x{h}','-i','pipe:0','-frames:v','1','-f','image2pipe','-vcodec','png','pipe:1'],input=raw[j*size:(j+1)*size])
    file=root/f'encoded_{n:03}.png';file.write_bytes(png)
    im=Image.open(file).convert('RGB');im.thumbnail((400,225));sheet.paste(im,(400*j,30))
    crop=Image.open(file).convert('RGB').crop((1600,650,2000,1050));sheet.paste(crop,(400*j,285))
    draw.text((400*j+10,8),f'frame {n}, encoded | below: UHD 1:1',fill='white')
sheet.save(root/'local_qa_samples.jpg',quality=95)
source=(root/p['source']).resolve()
common=['ffmpeg','-v','error']
source_audio=subprocess.check_output(common+['-ss',str(p['start_frame']/p['fps']),'-i',str(source),
     '-t','15','-map','0:a:0','-c','copy','-f','adts','pipe:1'])
test_audio=subprocess.check_output(common+['-i',str(video),'-map','0:a:0','-c','copy','-f','adts','pipe:1'])
audio_equal=source_audio==test_audio
assert audio_equal
report={'decode':'PASS','probe':probe,'samples':results,
        'audio_packets_match_same_source_trim':audio_equal,
        'audio_adts_sha256':hashlib.sha256(test_audio).hexdigest(),
        'limitations':'Sampled visual review and local metrics only; no independent review or complete AV playback claimed.'}
(root/'local_qa.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'frames':vs['nb_read_frames'],'duration':vs['duration'],
        'bitrate':vs.get('bit_rate'),'samples':results,'audio_equal':audio_equal},indent=2))
