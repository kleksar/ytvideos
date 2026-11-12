"""Prepare the measured draft narration cues and a 48 kHz stereo mix."""
import json
import math
import subprocess
import wave
from pathlib import Path

import numpy as np

EP = Path(__file__).resolve().parents[1]
ROOT = EP.parents[3]
RATE = 48_000
FPS = 24
TOTAL = 31 * RATE
VO = [
    (0.08, 2.30, ['Who ate the last cookie?']),
    (2.46, 4.40, ['That look became a meme.']),
    (6.04, 10.30, ['One bottle flip got', 'the whole room cheering.']),
    (10.62, 13.40, ['Gru had a plan', 'to steal the moon.']),
    (14.75, 17.42, ['Then he saw the last page.']),
    (17.68, 20.58, ['Baby Yoda took', 'one tiny sip.']),
    (23.60, 26.18, ['Tariq just really liked corn.']),
    (26.52, 29.30, ['So his interview', 'became a song.']),
]


def decode(path, channels, *extra):
    result = subprocess.check_output(['ffmpeg','-v','error','-i',str(path),*extra,
        '-ar',str(RATE),'-ac',str(channels),'-f','f32le','-'])
    return np.frombuffer(result,dtype='<f4').reshape((-1,channels)).copy()


def sample(seconds):
    return round(seconds*RATE)


def audible(signal, db_relative=-43, cushion=.03):
    win = sample(.01)
    blocks = signal[:len(signal)//win*win].reshape((-1,win,signal.shape[1]))
    energy = np.sqrt(np.mean(blocks**2,axis=(1,2)))
    valid = np.flatnonzero(energy > energy.max()*10**(db_relative/20))
    if not len(valid):
        raise ValueError('Empty audio event')
    return max(0,valid[0]*win-sample(cushion)), min(len(signal),(valid[-1]+1)*win+sample(cushion))


def fade(signal, in_time=.014, out_time=.026):
    n = min(len(signal)//3,sample(in_time))
    m = min(len(signal)//3,sample(out_time))
    signal[:n] *= np.linspace(0,1,n)[:,None]
    signal[-m:] *= np.linspace(1,0,m)[:,None]
    return signal


def level(signal, rms, peak):
    gain = min(rms/max(1e-8,np.sqrt(np.mean(signal**2))),peak/max(1e-8,abs(signal).max()))
    return signal*gain


def overlay(bus, signal, start):
    i = sample(start)
    j = min(i+len(signal),len(bus))
    bus[i:j] += signal[:j-i]


def clock(seconds):
    ms = round(seconds*1000)
    m,s = divmod(ms//1000,60)
    return f'00:{m:02d}:{s:02d},{ms%1000:03d}'


def main():
    music_source=ROOT/'Shared/Music/2026-11-08/Tracks/Kevin MacLeod - Monkeys Spinning Monkeys.mp3'
    bed=np.zeros((TOTAL,2),dtype=np.float32)
    voice=np.zeros_like(bed)
    effects=np.zeros_like(bed)
    overlay(bed,decode(music_source,2,'-t','31'),.82)
    t=np.arange(TOTAL)/RATE
    envelope = np.full(TOTAL,.33,dtype=np.float32)
    cues=[]
    for i,(start,limit,lines) in enumerate(VO,1):
        filename = '06-v02.aiff' if i == 6 else f'{i:02d}.aiff'
        source=EP/'Source/Voice'/filename
        mono=decode(source,1,'-af','atempo=1.15')
        a,b=audible(mono)
        mono=level(fade(mono[a:b]),.130,.65)
        end=start+len(mono)/RATE
        if end>limit:
            raise ValueError(f'Line {i} runs to {end:.3f}, beyond {limit:.3f}')
        overlay(voice,mono,start)
        attenuation=np.interp(t,[start-.09,start,end,end+.22],[1,.33,.33,1])
        envelope *= attenuation
        cues.append({'index':i,'start_frame':math.floor(start*FPS),
            'end_frame':math.ceil((end+.02)*FPS),'lines':lines,
            'voice_in':round(start,4),'voice_out':round(end,4),'source':source.name})
    for start,end,depth in [(5.58,5.94,.13),(20.20,20.98,.14),(23.54,26.16,.17)]:
        envelope *= np.interp(t,[start-.13,start,end,end+.23],[1,depth,depth,1])
    envelope *= np.interp(t,[0,30.50,30.96,31],[1,1,0,0])
    overlay_fx=[
        ('bottle',5.74,.28,.071),
        ('paper',13.15,.36,.055),
        ('paper',14.63,.36,.058),
        ('sip',20.23,.64,.073),
    ]
    for name,start,length,rms in overlay_fx:
        signal=decode(EP/f'Source/{name}-cc0-preview.mp3',2)
        a,b=audible(signal,-31,.012)
        signal=signal[a:min(b,a+sample(length))]
        overlay(effects,level(fade(signal,.008,.045),rms,.38),start)
    # A soft two-note celesta-like figure gives the trophy its own short payoff.
    for delay,pitch in [(0,587.33),(.116,783.99)]:
        u=np.arange(sample(.34))/RATE
        note=(np.sin(2*np.pi*pitch*u)+.21*np.sin(4*np.pi*pitch*u))*np.exp(-13*u)
        note *= np.minimum(1,u/.014)*.12
        overlay(effects,note[:,None],28.83+delay)
    result=bed*envelope[:,None]+voice+effects
    peak=np.max(np.abs(result))
    if peak>.82:
        result *= .82/peak
    with wave.open(str(EP/'Edit/mix-v02.wav'),'wb') as output:
        output.setparams((2,2,RATE,0,'NONE','not compressed'))
        output.writeframes(np.rint(result*32767).astype('<i2').tobytes())
    (EP/'Edit/cues-v02.json').write_text(json.dumps(cues,indent=2)+'\n')
    srt='\n\n'.join(f"{c['index']}\n{clock(c['start_frame']/FPS)} --> "
                    f"{clock(c['end_frame']/FPS)}\n"+'\n'.join(c['lines']) for c in cues)+'\n'
    (EP/'Edit/meme-time-machine-01-en-draft-v02.srt').write_text(srt)
    print([(c['index'],c['voice_in'],c['voice_out']) for c in cues])


if __name__=='__main__':
    main()
