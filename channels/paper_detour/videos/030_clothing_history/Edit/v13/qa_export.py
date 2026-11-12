"""Technical and sample QA of the actual new MP4, never a full-playback claim."""
import hashlib
import json
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[2]
RUN = Path(json.loads((ROOT / 'Edit/v13/TARGET_RUN.json').read_text())['run'])
QA = ROOT / 'Edit/v13/QA'
QA.mkdir(exist_ok=True)
film = ROOT / 'Deliverables/PAPER_DETOUR_030_CLOTHING_HISTORY_EN_v13.mp4'
native = ROOT / 'Edit/v13/Palmier_export.mp4'
shots = json.loads((ROOT / 'Storyboard/SHOTLIST_v13.json').read_text())
cues = json.loads((ROOT / 'Storyboard/CUE_SHEET_v13.json').read_text())
timeline = json.loads((ROOT / 'Edit/v13/timeline_final.json').read_text())
probe = json.loads(subprocess.check_output(['ffprobe', '-v', 'error', '-show_streams', '-show_format', '-of', 'json', str(film)]))
(QA / 'ffprobe.json').write_text(json.dumps(probe, indent=2) + '\n')
v = next(x for x in probe['streams'] if x['codec_type'] == 'video')
a = next(x for x in probe['streams'] if x['codec_type'] == 'audio')
assert (v['width'], v['height'], v['r_frame_rate'], v['nb_frames']) == (1920, 1080, '30/1', '5700')
assert float(probe['format']['duration']) == 190
assert (a['sample_rate'], a['channels']) == ('48000', 2)
assert len(shots) == 39 and len(cues) == 33
assert not any('grain' in t['name'].lower() or 'ripple' in t['name'].lower() for t in timeline['tracks'])
frames = set()
for s in shots:
    frames.update([s['startFrame'] + 2, (s['startFrame'] + s['endFrame']) // 2, s['endFrame'] - 3])
for c in cues:
    frames.update([c['startFrame'] + 1, c['startFrame'] + 4, (c['startFrame'] + c['endFrame']) // 2, c['endFrame'] - 5, c['endFrame'] - 1])
frames = sorted(frames)
def balanced(terms):
    if len(terms) == 1:
        return terms[0]
    mid = len(terms) // 2
    return '(' + balanced(terms[:mid]) + '+' + balanced(terms[mid:]) + ')'
raw = QA / 'ExportFrames'
raw.mkdir(exist_ok=True)
expression = balanced([f'eq(n\\,{f})' for f in frames])
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-xerror', '-i', str(film), '-vf', 'select=' + expression,
                '-fps_mode', 'vfr', '-q:v', '3', '-an', str(raw / '%03d.jpg')], check=True)
files = sorted(raw.glob('*.jpg'))
assert len(files) == len(frames)
fmap = {str(f): str(p) for f, p in zip(frames, files)}
(QA / 'frame_map.json').write_text(json.dumps(fmap, indent=2) + '\n')
def cell(sheet, f, x, y, label, width=480, height=270):
    with Image.open(fmap[str(f)]) as im:
        sheet.paste(im.resize((width, height)), (x, y))
    ImageDraw.Draw(sheet).text((x + 5, y + height + 3), label, fill='black')
for start in range(0, 39, 13):
    group = shots[start:start + 13]
    sheet = Image.new('RGB', (1440, len(group) * 294), '#ddd9cc')
    for row, s in enumerate(group):
        samples = [s['startFrame'] + 2, (s['startFrame'] + s['endFrame']) // 2, s['endFrame'] - 3]
        for col, frame in enumerate(samples):
            cell(sheet, frame, col * 480, row * 294, s['id'] + ' f' + str(frame))
    sheet.save(QA / f'EXPORTED_SCENES_{start // 13 + 1}.jpg')
for start in range(0, 34, 9):
    group = cues[start:start + 9]
    sheet = Image.new('RGB', (1536, len(group) * 240), '#ddd9cc')
    for row, c in enumerate(group):
        samples = [c['startFrame'] + 1, c['startFrame'] + 4, c['endFrame'] - 5, c['endFrame'] - 1]
        for col, frame in enumerate(samples):
            cell(sheet, frame, col * 384, row * 240, c['id'] + ' f' + str(frame), 384, 216)
    sheet.save(QA / f'EXPORTED_CUES_{start // 9 + 1}.jpg')
subprocess.run(['ffmpeg', '-v', 'error', '-xerror', '-i', str(film), '-vn', '-f', 'null', '-'], check=True)
def payload_hash(path, selector):
    return subprocess.check_output(['ffmpeg', '-v', 'error', '-i', str(path), '-map', selector, '-c', 'copy', '-f', 'hash', '-hash', 'sha256', '-']).decode().strip()
video = payload_hash(film, '0:v:0')
assert video == payload_hash(native, '0:v:0')
audio = payload_hash(film, '0:a:0')
assert audio == payload_hash(ROOT / 'Source/Audio/v06/accepted_v05_mix.m4a', '0:a:0')
srt = ROOT / 'Deliverables/PAPER_DETOUR_030_CLOTHING_HISTORY_EN_v13.srt'
assert srt.read_bytes() == (ROOT / 'Edit/v05/Accepted_delivery_v05.srt').read_bytes()
report = {'file': str(film), 'sha256': hashlib.sha256(film.read_bytes()).hexdigest(),
          'duration': 190, 'scenes': 39, 'paper_accents': 33, 'grain': 'ABSENT',
          'scene_motion': '39 depth-parallax clips with gentle-aligned camera keys',
          'native_video_payload': video, 'unchanged_accepted_audio_payload': audio,
          'audio_actual_bitrate': int(a['bit_rate']), 'full_video_audio_decode': 'PASS',
          'actual_export_frames_sampled': len(frames), 'srt_identical': True,
          'visual_sample_review': 'PENDING', 'full_1x_with_sound': 'UNVERIFIED',
          'independent_review': 'NOT_PERFORMED'}
(QA / 'REPORT.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({k: report[k] for k in ['duration', 'scenes', 'paper_accents', 'grain', 'actual_export_frames_sampled']}))
