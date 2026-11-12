"""Verify the exact complete MP4, decoded audio alignment and caption intervals."""
from pathlib import Path
import json
import math
import subprocess
import sys
import wave

import numpy as np
from PIL import Image, ImageDraw

from full_song_plan import batch, edit, run, read, write, sha, FPS, accent_signal

name=sys.argv[1]
prefix=edit/f'{name}-full-song-v01'
contract=read(prefix.with_name(prefix.name+'-contract.json'))
output=Path(contract['output'])
folder=run/name
frames=contract['frames']
samples=contract['samples']
width,height=contract['dimensions']
def capture(*args):
    return subprocess.check_output([str(a) for a in args])

def qa_audio():
    with wave.open(contract['wav'],'rb') as reference:
        expected=np.frombuffer(reference.readframes(samples),'<i2').reshape(-1,2)
    raw=capture('ffmpeg','-nostdin','-v','error','-xerror','-i',output,'-vn','-c:a','pcm_s16le','-f','s16le','-')
    actual=np.frombuffer(raw,'<i2').reshape(-1,2)
    assert samples<=len(actual)<samples+1024, (samples,len(actual))
    identical_pcm = bool(contract['audio'].get('packet_copy'))
    if identical_pcm:
        assert np.array_equal(expected,actual), 'Copied AAC did not decode to the original PCM'
    stats=[]
    for start in np.linspace(0,samples-44100,9,dtype=int):
        original=expected[start:start+44100].astype('f4')
        rendered=actual[start:start+44100].astype('f4')
        norm=np.linalg.norm(original)*np.linalg.norm(rendered)
        if norm>1e-6:
            similarity=float((original*rendered).sum()/norm)
            assert similarity>.96, (name,start,similarity)
            stats.append(round(similarity,5))
    assert len(stats)>=7
    return {'reference_samples_per_channel':samples,'decoded_samples_per_channel':len(actual),
            'correlation_at_start_middle_and_end':stats,'reference_pcm_sha256':contract['pcm_sha256'],
            'source_pcm_sample_identity':identical_pcm}

def qa_caption():
    caption=read(prefix.with_name(prefix.name+'-caption-plan.json'))
    word_map=read(contract['words'])
    assert len(caption['groups'])==len(word_map['words'])
    assert caption['hold_gap_lt_ms']==500 and caption['frames']==frames
    expected=np.zeros(frames,dtype=bool)
    hold_frames=[]
    silence_frames=[]
    for i,g in enumerate(caption['groups']):
        start,end=g['start_frame'],g['end_frame_exclusive']
        assert 0<=start<end<=frames and not expected[start:end].any()
        expected[start:end]=True
        if i<len(caption['groups'])-1:
            next_start=caption['groups'][i+1]['start_frame']
            gap=round(1000*(word_map['words'][i+1]['start_seconds']-word_map['words'][i]['end_seconds']),6)
            natural=g['natural_end_frame_exclusive']
            assert end==(next_start if 0<=gap<500 else natural)
            if end>natural:
                hold_frames.append((end+natural-1)//2)
            if end<next_start:
                silence_frames.append((end+next_start-1)//2)
    data=capture('ffmpeg','-nostdin','-v','error','-threads','2','-i',folder/'mask.mov','-vf',
                 'format=gbrp,extractplanes=g,scale=112:48','-pix_fmt','gray','-f','rawvideo','-')
    active=np.frombuffer(data,'u1').reshape(frames,112*48).max(axis=1)>20
    assert np.array_equal(active,expected),np.flatnonzero(active!=expected)[:12].tolist()
    return {'words':len(caption['groups']),'decoded_mask_frames':frames,'held_gaps':len(hold_frames),
            'long_gaps':len(silence_frames)},hold_frames,silence_frames

def sheets(hold_frames,silence_frames):
    cuts=contract['transition_centres']
    bounds=[0,*cuts,frames]
    positions={(a+b)//2 for a,b in zip(bounds,bounds[1:])}
    examples=[cuts[i] for i in np.linspace(0,len(cuts)-1,min(15,len(cuts)),dtype=int)]
    around={f+d for f in examples for d in (-2,0,3) if 0<=f+d<frames}
    def examples_from(values):
        return [values[i] for i in np.linspace(0,len(values)-1,min(len(values),6),dtype=int)] if values else []
    details=around|set(examples_from(hold_frames))|set(examples_from(silence_frames))|{0,frames-1}
    targets=sorted(positions|details)
    terms=[f'eq(n,{f})' for f in targets]
    select='+'.join('('+'+'.join(terms[i:i+10])+')' for i in range(0,len(terms),10))
    w,h=126,224
    raw=capture('ffmpeg','-nostdin','-v','error','-xerror','-threads','2','-i',output,'-an','-vf',
                f"select='{select}',scale={w}:{h}:flags=lanczos",'-fps_mode','passthrough','-pix_fmt','rgb24','-f','rawvideo','-')
    pictures=dict(zip(targets,np.frombuffer(raw,'u1').reshape(len(targets),h,w,3)))
    result={}
    for label,group in [('shots',positions),('timing',details)]:
        cols=9
        sheet=Image.new('RGB',(cols*w,(h+16)*math.ceil(len(group)/cols)),'#202020')
        pen=ImageDraw.Draw(sheet)
        for i,frame in enumerate(sorted(group)):
            x,y=(i%cols)*w,(i//cols)*(h+16)
            sheet.paste(Image.fromarray(pictures[frame]),(x,y))
            tag=' beat' if frame in cuts else ' held' if frame in hold_frames else ' gap' if frame in silence_frames else ''
            pen.text((x+4,y+h+1),f'{frame/FPS:.2f}{tag}',fill='white')
        path=prefix.with_name(prefix.name+f'-{label}.jpg')
        sheet.save(path,quality=87)
        result[label]=str(path)
    return result

def main():
    probe=json.loads(capture('ffprobe','-v','error','-show_streams','-show_format','-of','json',output))
    v,a=probe['streams']
    assert (v['width'],v['height'],v['codec_name'],v['pix_fmt'])==(width,height,'h264','yuv420p')
    assert v['r_frame_rate']=='30/1' and int(v['nb_frames'])==frames
    assert all(v.get(key)=='bt709' for key in ('color_space','color_primaries','color_transfer'))
    assert v['color_range']=='tv'
    assert (a['codec_name'],a['sample_rate'],a['channels'])==('aac','44100',2)
    assert abs(float(a['duration'])-samples/44100)<.001
    packets=json.loads(capture('ffprobe','-v','error','-select_streams','v:0','-show_packets','-show_entries','packet=pts','-of','json',output))
    assert v['time_base']=='1/30000'
    pts=sorted(int(p['pts']) for p in packets['packets'])
    assert pts==list(range(0,frames*1000,1000)),next(((i,n) for i,n in enumerate(pts) if i*1000!=n),None)
    audio=qa_audio()
    caption,held,silence=qa_caption()
    signal,strength=accent_signal(output)
    measured=[]
    for cut in contract['accents']:
        timing=float(cut['attack_seconds'])
        frame=cut['frame']
        assert abs(frame/FPS-timing)<.036
        j=int(np.argmin(np.abs(signal-timing)))
        measured.append(dict(frame=frame,source_attack_seconds=timing,
                             export_sample_seconds=round(float(signal[j]),6),
                             export_attack_strength=round(float(strength[j]),4)))
    samples_paths=sheets(held,silence)
    result=dict(file=str(output),sha256=sha(output),frames=frames,fps=FPS,dimensions=[width,height],
                duration_seconds=frames/FPS,audio_duration_seconds=samples/44100,
                full_decode='PASS',constant_frame_cadence='PASS',audio=audio,captions=caption,
                measured_accents=measured,visual_samples=samples_paths,visual_inspection='PENDING',
                subjective_playback='UNVERIFIED')
    write(prefix.with_name(prefix.name+'-qa.json'),result)
    print(name,frames,caption,'audio',min(audio['correlation_at_start_middle_and_end']),flush=True)

if __name__=='__main__':
    main()
