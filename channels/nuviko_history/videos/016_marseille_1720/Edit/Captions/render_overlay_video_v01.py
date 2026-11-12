#!/usr/bin/env python3
"""Encode the exact source-time word states as one transparent 30fps ProRes layer."""
from pathlib import Path
import hashlib, json, subprocess
from PIL import Image

EP=Path(__file__).resolve().parents[2]
WORDS=EP/"Edit/Captions/word_states_manifest_source_v01.json"
OUT=EP/"Assets/Generated/subtitle_overlay_v01.mov"
RUN=EP/"Edit/Captions/subtitle_overlay_video_v01.json"
WORK=EP/"Work/subtitle_overlay_video_v01"
FPS=30; TOTAL=16125; CANVAS=(1920,1080)

def digest(p:Path)->str:
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
    return h.hexdigest()

data=json.loads(WORDS.read_text())
if data.get('status')!='SOURCE_TIME_DRAFT_REVIEW_REQUIRED' or data.get('audibleSync')!='UNVERIFIED':
    raise SystemExit('Unexpected subtitle readiness status')
if data.get('fps')!=FPS or data.get('canvas')!=list(CANVAS) or data.get('totalFrames')!=TOTAL:
    raise SystemExit('Subtitle overlay geometry/frame contract mismatch')
states=data['timeline']; cursor=states[0]['startFrame']
if cursor<0:raise SystemExit('Invalid first subtitle state')
for s in states:
    if s['startFrame']!=cursor or s['endFrame']<=s['startFrame']:
        raise SystemExit('Word-state intervals contain a gap, overlap or zero span')
    p=Path(s['image'])
    if not p.is_file() or digest(p)!=s['sha256']:
        raise SystemExit(f"Word-state image identity changed: {s['image_id']}")
    with Image.open(p) as im:
        if im.size!=CANVAS or im.mode!='RGBA':raise SystemExit(f"Word-state canvas mismatch: {s['image_id']}")
    cursor=s['endFrame']
if cursor!=TOTAL:raise SystemExit(f'Subtitle coverage ends at {cursor}, expected {TOTAL}')

WORK.mkdir(parents=True,exist_ok=True);OUT.parent.mkdir(parents=True,exist_ok=True)
blank=WORK/'transparent_blank.png'
if not blank.exists():Image.new('RGBA',CANVAS,(0,0,0,0)).save(blank)
parts=[];cursor=0
for s in states:
    a,b=s['startFrame'],s['endFrame']
    if a>cursor:parts.append((blank,cursor,a))
    parts.append((Path(s['image']),a,b));cursor=b
if cursor<TOTAL:parts.append((Path(states[-1]['image']),cursor,TOTAL))
concat=WORK/'sequence.ffconcat'
lines=['ffconcat version 1.0']
for path,a,b in parts:
    if b<=a:raise SystemExit('Empty concat interval')
    resolved=str(path.resolve())
    if "'" in resolved:raise SystemExit('Unexpected quote in media path')
    lines.extend([f"file '{resolved}'",f'duration {(b-a)/FPS:.9f}'])
lines.append(f"file '{parts[-1][0].resolve()}'")
concat.write_text('\n'.join(lines)+'\n')
command=['ffmpeg','-y','-v','error','-f','concat','-safe','0','-i',str(concat),
         '-vf',f'fps={FPS},format=yuva444p12le,setpts=N/({FPS}*TB)',
         '-frames:v',str(TOTAL),'-an','-c:v','prores_ks','-profile:v','4',
         '-pix_fmt','yuva444p12le','-vendor','apl0','-movflags','+faststart',str(OUT)]
if OUT.exists():raise SystemExit(f'Output already exists; inspect before overwrite: {OUT}')
subprocess.run(command,check=True)
probe=json.loads(subprocess.run(['ffprobe','-v','error','-select_streams','v:0','-show_entries',
    'stream=codec_name,pix_fmt,width,height,avg_frame_rate,duration,nb_frames','-of','json',str(OUT)],
    capture_output=True,text=True,check=True).stdout)['streams'][0]
if (probe.get('codec_name'),probe.get('pix_fmt'),probe.get('width'),probe.get('height'),
    probe.get('avg_frame_rate'),probe.get('nb_frames'))!=('prores','yuva444p12le',1920,1080,'30/1',str(TOTAL)):
    raise SystemExit(f'Overlay video export differs from contract: {probe}')
receipt={'version':'subtitle-overlay-v01','status':'rendered_alpha_layer',
         'sourceWordStateManifest':str(WORDS),'sourceWordStateSha256':digest(WORDS),
         'fps':FPS,'totalFrames':TOTAL,'durationSeconds':TOTAL/FPS,'canvas':list(CANVAS),
         'wordStates':len(states),'uniqueImages':data['uniqueImageCount'],
         'codec':probe['codec_name'],'pixelFormat':probe['pix_fmt'],'video':str(OUT),
         'videoSha256':digest(OUT),'bytes':OUT.stat().st_size,'ffmpegCommand':command,
         'audibleSync':'UNVERIFIED','frameCoverage':'PASS; source-time alignment estimate, no holes'}
RUN.write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'status':receipt['status'],'video':str(OUT),'sha256':receipt['videoSha256'],
                  'bytes':receipt['bytes'],'frames':TOTAL,'fps':FPS,'codec':probe['codec_name'],
                  'pix_fmt':probe['pix_fmt'],'wordStates':len(states)},ensure_ascii=False))
