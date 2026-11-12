#!/usr/bin/env python3
"""Keep the native Palmier H.264 video and replace its AAC with the untouched source stream."""
from pathlib import Path
import hashlib,json,subprocess,time

EP=Path(__file__).resolve().parents[2]
CONTRACT=EP/"Edit/Export/EXPORT_CONTRACT_v01.json"
RECEIPT=EP/"Edit/Export/remux_receipt_v01.json"

def sha(path):
 h=hashlib.sha256()
 with Path(path).open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 return h.hexdigest()
def probe(path,select=None):
 args=['ffprobe','-v','error']
 if select:args += ['-select_streams',select]
 args += ['-show_streams','-show_format','-of','json',str(path)]
 return json.loads(subprocess.run(args,capture_output=True,text=True,check=True).stdout)
def packet_hash(path,select):
 result=subprocess.run(['ffmpeg','-v','error','-i',str(path),'-map',f'0:{select}','-c','copy','-f','hash','-hash','sha256','-'],
                       capture_output=True,text=True,check=True)
 return result.stdout.strip()

c=json.loads(CONTRACT.read_text())
source=EP/'Work/palmier_export_v01.mp4'
audio=EP/'Source/Audio/original_narration.m4a'
output=Path(c['preflight']['output_path'])
if output.exists():raise SystemExit(f'Refusing to overwrite delivery: {output}')
if not source.is_file() or not audio.is_file():raise SystemExit('Export/source audio is missing')
if sha(audio)!=next(d['sha256'] for d in c['edit']['dependencies'] if d['name']=='source_audio'):
 raise SystemExit('Original audio identity changed')
srcv=probe(source,'v:0')['streams'][0];srca=probe(audio,'a:0')['streams'][0]
if (srcv.get('codec_name'),srcv.get('width'),srcv.get('height'),srcv.get('nb_frames'))!=('h264',1920,1080,'16125'):
 raise SystemExit(f'Palmier video differs from contract: {srcv}')
if (srca.get('codec_name'),srca.get('profile'),srca.get('sample_rate'),srca.get('channels'))!=('aac','LC','44100',2):
 raise SystemExit(f'Original audio differs from contract: {srca}')
output.parent.mkdir(parents=True,exist_ok=True)
command=['ffmpeg','-y','-v','error','-i',str(source),'-i',str(audio),'-map','0:v:0','-map','1:a:0',
         '-c:v','copy','-c:a','copy','-movflags','+faststart',str(output)]
subprocess.run(command,check=True)
final=probe(output)
v=next(s for s in final['streams'] if s['codec_type']=='video')
a=next(s for s in final['streams'] if s['codec_type']=='audio')
if (v.get('codec_name'),v.get('width'),v.get('height'),v.get('nb_frames'))!=('h264',1920,1080,'16125'):
 raise SystemExit(f'Final video stream differs from Palmier: {v}')
if (a.get('codec_name'),a.get('profile'),a.get('sample_rate'),a.get('channels'))!=('aac','LC','44100',2):
 raise SystemExit(f'Final audio stream differs from original: {a}')
video_input_hash=packet_hash(source,'v:0');video_final_hash=packet_hash(output,'v:0')
audio_input_hash=packet_hash(audio,'a:0');audio_final_hash=packet_hash(output,'a:0')
if video_input_hash!=video_final_hash:raise SystemExit('Video packet identity changed during remux')
if audio_input_hash!=audio_final_hash:raise SystemExit('Audio packet identity does not match original stream')
receipt={'status':'remuxed_streamcopy_verified','contract':str(CONTRACT),'contractSha256':sha(CONTRACT),
 'palmierVideo':str(source),'palmierVideoSha256':sha(source),'sourceAudio':str(audio),'sourceAudioSha256':sha(audio),
 'final':str(output),'finalSha256':sha(output),'bytes':output.stat().st_size,'ffmpegCommand':command,
 'videoPacketHash':video_final_hash,'sourceAudioPacketHash':audio_input_hash,'finalAudioPacketHash':audio_final_hash,
 'streams':final['streams'],'format':final['format'],'time':time.time(),
 'audioSignal':'source AAC-LC packet stream copied without decode/re-encode; listening remains separate QA'}
RECEIPT.write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'status':receipt['status'],'output':str(output),'sha256':receipt['finalSha256'],
                  'bytes':receipt['bytes'],'videoPacketHash':video_final_hash,'audioPacketHash':audio_final_hash},ensure_ascii=False))
