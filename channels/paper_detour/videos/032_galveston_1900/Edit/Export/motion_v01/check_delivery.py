import hashlib
import json
import struct
import subprocess
from fractions import Fraction
from pathlib import Path

import numpy as np

EP = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
CONTRACT = json.loads((OUT / 'EXPORT_CONTRACT_v01.json').read_text())
NATIVE = Path(CONTRACT['encoding']['requested_arguments']['outputPath'])
FINAL = EP / 'Work/galveston-export-motion-v01/previews/032_galveston_en_motion_v01.mp4'
VOICE = Path(CONTRACT['required_delivery']['audio_contract']['source_path'])
COMMANDS = []


def run(args):
    COMMANDS.append(args)
    return subprocess.check_output(args)


def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for b in iter(lambda: f.read(4 * 1024 * 1024), b''):
            h.update(b)
    return h.hexdigest()


probe = json.loads(run(['ffprobe', '-v', 'error', '-show_streams', '-show_format', '-of', 'json', str(FINAL)]))
(OUT / 'final_ffprobe.json').write_text(json.dumps(probe, indent=2))
v = next(x for x in probe['streams'] if x['codec_type'] == 'video')
a = next(x for x in probe['streams'] if x['codec_type'] == 'audio')
packet_data = json.loads(run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_packets', '-show_entries', 'packet=pts,dts,duration,flags', '-of', 'json', str(FINAL)]))
(OUT / 'video_packet_timing.json').write_text(json.dumps(packet_data, indent=2))
packets = packet_data['packets']
step = Fraction(1, 30) / Fraction(v['time_base'])
pts = sorted(int(p['pts']) for p in packets)
cfr = len(pts) == 17233 and step.denominator == 1 and pts == [i * int(step) for i in range(17233)] and all(int(p['duration']) == step for p in packets)
keys = sorted(int(p['pts']) for p in packets if 'K' in p['flags'])
gops = [int((y - x) / step) for x, y in zip(keys, keys[1:])]
stream_hashes = {}
for label, path in [('native', NATIVE), ('final', FINAL)]:
    stream_hashes[label] = run(['ffmpeg', '-v', 'error', '-i', str(path), '-map', '0:v:0', '-c:v', 'copy', '-f', 'hash', '-hash', 'sha256', '-']).decode().strip()

atoms = []
with FINAL.open('rb') as f:
    size = FINAL.stat().st_size
    offset = 0
    while offset + 8 <= size:
        f.seek(offset)
        length, kind = struct.unpack('>I4s', f.read(8))
        if length == 1:
            length = struct.unpack('>Q', f.read(8))[0]
        elif length == 0:
            length = size - offset
        if length < 8:
            raise ValueError('Invalid MP4 atom length')
        atoms.append({'type': kind.decode('ascii', 'replace'), 'offset': offset, 'size': length})
        offset += length

# Decode the current delivery and its sole accepted complete-mix source through
# pipes. No PCM or downmix audio file is created. Compare aligned sample signals.
af = ['ffmpeg', '-v', 'error', '-i', str(FINAL), '-map', '0:a:0', '-af', 'atrim=duration=574.4333333333333', '-ar', '48000', '-ac', '2', '-f', 'f32le', '-']
rf = ['ffmpeg', '-v', 'error', '-i', str(VOICE), '-af', 'atrim=duration=574.4,aresample=48000,apad,atrim=duration=574.4333333333333', '-ar', '48000', '-ac', '1', '-f', 'f32le', '-']
COMMANDS.extend([af, rf])
ap = subprocess.Popen(af, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
rp = subprocess.Popen(rf, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
count = 0
sum_ref2 = sum_out2 = dot = error2 = 0.0
max_lr = peak = 0.0
while True:
    rb = rp.stdout.read(48000 * 4)
    if not rb:
        break
    ref = np.frombuffer(rb, dtype='<f4').astype(np.float64)
    ob = ap.stdout.read(len(ref) * 8)
    out = np.frombuffer(ob, dtype='<f4').reshape(-1, 2).astype(np.float64)
    if len(ref) != len(out):
        raise ValueError('Decoded mix length differs')
    mono = (out[:, 0] + out[:, 1]) * .5
    max_lr = max(max_lr, float(np.max(np.abs(out[:, 0] - out[:, 1]))))
    peak = max(peak, float(np.max(np.abs(out))))
    sum_ref2 += float(np.dot(ref, ref))
    sum_out2 += float(np.dot(mono, mono))
    dot += float(np.dot(ref, mono))
    error2 += float(np.dot(mono - ref, mono - ref))
    count += len(ref)
remaining = ap.stdout.read()
assert not remaining, 'Unexpected decoded audio tail'
assert ap.wait() == rp.wait() == 0
audio_signal = {'sample_count_per_channel': count, 'zero_lag_correlation': dot / (sum_ref2 * sum_out2) ** .5, 'linear_gain_vs_reference': dot / sum_ref2, 'snr_db': float(10 * np.log10(sum_ref2 / error2)), 'max_L_R_difference': max_lr, 'sample_peak': peak, 'fold_down': '0.5L+0.5R compared with source; identical L/R do not cancel', 'subjective_listening': 'UNVERIFIED'}
required = {'width': 2560, 'height': 1440, 'codec_name': 'h264', 'pix_fmt': 'yuv420p', 'color_range': 'tv', 'color_space': 'bt709', 'color_transfer': 'bt709', 'color_primaries': 'bt709', 'field_order': 'progressive'}
metadata_ok = all(v.get(k) == value for k, value in required.items()) and a['codec_name'] == 'aac' and a['profile'] == 'LC' and a['sample_rate'] == '48000' and a['channels'] == 2
result = {'file': str(FINAL), 'sha256': sha(FINAL), 'contract_path': str(OUT / 'EXPORT_CONTRACT_v01.json'), 'contract_sha256': sha(OUT / 'EXPORT_CONTRACT_v01.json'), 'required_stream_properties': 'PASS' if metadata_ok else 'FAIL', 'actual_video': v, 'actual_audio': a, 'CFR_30_exact_packet_pts': cfr, 'video_payload_identity': stream_hashes, 'video_copied_without_reencoding': stream_hashes['native'] == stream_hashes['final'], 'GOP_min_max': [min(gops), max(gops)] if gops else None, 'GOP_note': 'Preference only; native engine managed', 'MP4_top_level_atoms': atoms, 'fast_start': next(x['offset'] for x in atoms if x['type'] == 'moov') < next(x['offset'] for x in atoms if x['type'] == 'mdat'), 'edit_lists': 'AAC priming/timing edit lists may be retained; preserving sync takes precedence over preference for no edit lists', 'audio_signal': audio_signal, 'native_sha256': sha(NATIVE), 'source_voice_sha256': sha(VOICE), 'commands': COMMANDS, 'verdict_scope': 'Stream, packet cadence, payload identity and objective audio correspondence only; no visual, subjective or editorial acceptance awarded'}
(OUT / 'delivery_checks.json').write_text(json.dumps(result, indent=2))
print(json.dumps({k: result[k] for k in ['required_stream_properties', 'CFR_30_exact_packet_pts', 'video_copied_without_reencoding', 'fast_start', 'GOP_min_max', 'audio_signal']}))
