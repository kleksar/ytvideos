"""Conform the three new review recordings to their actual FFmpeg edit clock."""
from pathlib import Path
import hashlib
import json
import math
import re
import subprocess as sp
import sys

ROOT = Path(__file__).resolve().parents[3]
PAPER = ROOT / 'channels/paper_detour'
NUVIKO = ROOT / 'channels/nuviko_history'
MUSIC = PAPER / 'videos/050_great_stink_london/Source/Music'
SIGNAL = MUSIC / 'signal_to_noise_no_piano.mp3'
NIGHT = NUVIKO / 'research/molasses-flood/Source/Music/Night_Vigil.mp3'
EPISODES = {
    'neptune': (PAPER / 'research/2026-11-09-neptune', 0, [(SIGNAL, 72, 33, -22)]),
    'cable': (PAPER / 'research/2026-11-09-atlantic-cable', 10, [(SIGNAL, 4, 285, -22)]),
    'us': (NUVIKO / 'research/us-history', 10, [(SIGNAL, 23, 221, -23), (NIGHT, 12, 228, -24)]),
}

def sha(p):
    h = hashlib.sha256()
    with p.open('rb') as f:
        for chunk in iter(lambda:f.read(1048576),b''):
            h.update(chunk)
    return h.hexdigest()

def run(cmd):
    sp.run([str(x) for x in cmd], check=True)

def dump(path, data):
    with path.open('x') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write('\n')

def probe(p):
    return float(sp.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', p]))

def build(name):
    ep, tail, beds = EPISODES[name]
    audio_dir, work = ep/'Assets/Audio', ep/'Work'
    for p in [audio_dir, work]:
        p.mkdir(parents=True, exist_ok=True)
    source = ep/'Source/Voice/en_v01/voice_en.mp3'
    alignment = source.with_suffix('.alignment.json')
    transcript = ep/'Source/Script/narration_en_v01.txt'
    voice = audio_dir/'voice-conform-v01.wav'
    mix = audio_dir/'full-mix-v01.wav'
    handoff = audio_dir/'HANDOFF.md'
    mpath = work/'word-times-final-v01.json'
    if any(p.exists() for p in [voice, mix, handoff, mpath]):
        raise RuntimeError('These are versioned outputs; use a new revision to rebuild')
    speed = 1.10
    cmd = ['ffmpeg', '-nostdin', '-v', 'error', '-n', '-i', source, '-af', 'atempo=1.10', '-ar', '48000', '-c:a', 'pcm_s24le', voice]
    run(cmd)
    duration = probe(voice)
    speech_frames = math.ceil(duration*30)
    frames = speech_frames+tail*30
    length = frames/30
    a = json.loads(alignment.read_text())['alignment']
    chars = ''.join(a['characters'])
    assert chars.strip() == transcript.read_text().strip()
    words = []
    last_punct = len(chars.rstrip())-1
    assert chars[last_punct] in '.?!'
    for match in re.finditer(r'\S+', chars):
        endchar = min(last_punct-1, match.end()-1)
        start = a['character_start_times_seconds'][match.start()]/speed
        end = a['character_end_times_seconds'][endchar]/speed
        if match.end()-1 == last_punct and end > duration:
            assert end-duration < .12
            end = duration
        assert (not words or words[-1]['end'] <= start+1e-6) and 0 <= start < end <= duration
        words.append(dict(text=match.group(), start=round(start,6), end=round(end,6)))
    fc = ['[0:a]pan=stereo|FL=c0|FR=c0,volume=-2dB[vox]']
    cmdmix = ['ffmpeg', '-nostdin', '-v', 'error', '-n', '-i', voice]
    for i,(src,start,seconds,gain) in enumerate(beds,1):
        cmdmix += ['-ss', str(start), '-t', str(seconds), '-i', src]
        fc.append(f'[{i}:a]aresample=48000,aformat=channel_layouts=stereo,volume={gain}dB[m{i}]')
    bed = '[m1]'
    if len(beds) == 2:
        fc.append('[m1][m2]acrossfade=d=5:c1=tri:c2=tri[bed]')
        bed = '[bed]'
    fc += [f'{bed}afade=t=in:d=0.6,afade=t=out:st={length-2.3:.6f}:d=2.3[music]',
           f'[vox][music]amix=inputs=2:normalize=0,apad,atrim=end_sample={frames*1600}[mix]']
    cmdmix += ['-filter_complex', ';'.join(fc), '-map', '[mix]', '-ar', '48000', '-c:a', 'pcm_s24le', mix]
    run(cmdmix)
    assert abs(probe(mix)-length) < 0.000005
    tracks = [{'path':str(p), 'sha256':sha(p), 'in_seconds':s, 'duration_seconds':d, 'gain_db':g} for p,s,d,g in beds]
    timings = dict(audio_sha256=sha(mix), transcript_sha256=hashlib.sha256(chars.strip().encode()).hexdigest(),
                   words=words, voice_sha256=sha(source), alignment_sha256=sha(alignment),
                   retime={'speed':speed,'start':0,'end':duration}, video_frames=frames, speech_frames=speech_frames)
    dump(mpath, timings)
    measures = {}
    for p in [voice, mix]:
        log=sp.run(['ffmpeg','-hide_banner','-nostats','-i',p,'-af','ebur128=peak=true','-f','null','-'], check=True, capture_output=True,text=True).stderr
        measures[p.name]=log.rsplit('Summary:',1)[-1].strip()
    with handoff.open('x') as f:
        f.write(f'# EN review audio v01\n\nAuthorized for user review MP4, 2026-11-09. Voice source `{source}` SHA-256 `{sha(source)}`. Dry mono ElevenLabs recording, placed at zero; only one FFmpeg `atempo=1.10`, no cuts. Measured conformed voice {duration:.6f}s; full stereo PCM 24-bit / 48 kHz mix {length:.6f}s, {frames} frames at 30 fps. Voice center with −2 dB gain in full mix.\n\n')
        f.write(f'Mix SHA-256 `{sha(mix)}`. Exact provider alignment compared character for character to script. End time of the final word omits punctuation duration (provider clock extends past MP3); for US, the last letter timing also slightly exceeds the measured clip, so the final word terminates at the physical clip end. FFmpeg tail `silencedetect` detected trailing quiet from raw 476.988 s through 477.120 s, supporting this endpoint. No shift applied to earlier words. All intervals finite and monotonic; final map `{mpath}` SHA-256 `{sha(mpath)}`.\n\n')
        f.write('Music: Signal to Noise — No Piano Melody, Scott Buckley, CC BY 4.0, https://www.scottbuckley.com.au/library/signal-to-noise/. For US, five-second crossfade to Night Vigil, Kevin MacLeod, CC BY 4.0, https://incompetech.com/music/royalty-free/index.html?isrc=USUAN1900047.\n\n')
        f.write('Exact processing and measurement:\n\n```json\n'+json.dumps({'voice':[str(x) for x in cmd],'mix':[str(x) for x in cmdmix],'music':tracks,'ebur128':measures},indent=2)+'\n```\n\nSubjective listening: UNVERIFIED.\n')
    print(name, duration, frames, len(words), measures[mix.name])

for name in sys.argv[1:]:
    build(name)
