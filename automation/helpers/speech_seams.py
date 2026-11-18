"""Conservative, read-only natural-speech-gap audit; never edits audio.

Input WAV must be an unpadded narration stem, not a final music/SFX mix.
Boundaries JSON: [{"id":"...", "left_word_end":1.2,"right_word_start":1.3,
"cut":1.25}]. Word times must be verified against the exact source.
"""
import argparse
import hashlib
import json
import math
from pathlib import Path
import wave


def audit(samples, rate, boundaries, threshold_dbfs=-50, minimum_ms=100, timing_reason=''):
    if (not math.isfinite(rate) or rate <= 0 or not -120 <= threshold_dbfs < 0
            or not math.isfinite(minimum_ms) or minimum_ms <= 0):
        raise ValueError('Invalid rate/threshold; target gap must be finite and positive')
    if minimum_ms != 100 and not timing_reason.strip():
        raise ValueError('Non-default gap requires a timing reason, not automatic approval')
    if not samples or any(not math.isfinite(x) for x in samples):
        raise ValueError('Empty or non-finite audio')
    limit = 10 ** (threshold_dbfs / 20)
    required = math.ceil(rate * minimum_ms / 1000)
    result = []
    for item in boundaries:
        row = dict(item, status='REVIEW', reasons=[], minimum_ms=minimum_ms,
                   timing_reason=timing_reason)
        try:
            left, right, cut = (float(item[k]) for k in
                                ('left_word_end', 'right_word_start', 'cut'))
            if not all(math.isfinite(x) for x in (left,right,cut)) or not 0 <= left <= cut <= right <= len(samples)/rate:
                raise ValueError()
        except (KeyError, ValueError, TypeError):
            row['reasons'] = ['missing_or_invalid_verified_word_boundaries']
            result.append(row)
            continue
        a,b,c = math.ceil(left*rate), math.floor(right*rate), round(cut*rate)
        # Every channel is represented by its absolute maximum, not a mono sum.
        lo=hi=min(c,b)
        while lo>a and abs(samples[lo-1]) <= limit: lo-=1
        while hi<b and abs(samples[hi]) <= limit: hi+=1
        row.update(natural_quiet_start=lo/rate, natural_quiet_end=hi/rate,
                   natural_quiet_ms=(hi-lo)*1000/rate)
        if hi-lo < required:
            row['reasons'].append('below_requested_natural_gap_at_cut')
        else:
            row['status']='MEASURED_CANDIDATE'
        # Energy cannot establish phoneme completeness or prove natural provenance.
        row['requires']=['source_provenance','word_boundary_review','listening_in_final_mix']
        result.append(row)
    return result


def read_pcm(path):
    with wave.open(str(path),'rb') as f:
        n, width, rate = f.getnchannels(), f.getsampwidth(), f.getframerate()
        if width not in (2,3,4) or f.getcomptype()!='NONE':
            raise ValueError('Use signed PCM 16/24/32-bit WAV')
        data=f.readframes(f.getnframes())
    scale=2**(width*8-1)
    values=[abs(int.from_bytes(data[i:i+width],'little',signed=True))/scale
            for i in range(0,len(data),width)]
    return [max(values[i:i+n]) for i in range(0,len(values),n)],rate


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('voice_wav',type=Path); p.add_argument('boundaries',type=Path)
    p.add_argument('--threshold-dbfs',type=float,required=True)
    p.add_argument('--minimum-ms', type=float, default=100,
                   help='Diagnostic target (default 100ms); not an audio edit')
    p.add_argument('--timing-reason', default='',
                   help='Required for a non-default target; explain scene rhythm/meaning')
    args=p.parse_args()
    samples,rate=read_pcm(args.voice_wav)
    rows=audit(samples,rate,json.loads(args.boundaries.read_text()),args.threshold_dbfs,
               args.minimum_ms, args.timing_reason)
    print(json.dumps({'voice_sha256':hashlib.sha256(args.voice_wav.read_bytes()).hexdigest(),
                     'threshold_dbfs':args.threshold_dbfs,'sample_rate':rate,
                     'minimum_ms':args.minimum_ms,'timing_reason':args.timing_reason,'audio_modified':False,'seams':rows},indent=2))
    return 2 if any(x['status']=='REVIEW' for x in rows) else 0

if __name__=='__main__':
    raise SystemExit(main())
