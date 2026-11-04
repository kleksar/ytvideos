#!/usr/bin/env python3
"""Prepare a review-only word map using two alignments and measured quiet spans."""
import argparse, difflib, hashlib, json, re, subprocess
from pathlib import Path


def normalize(text):
    return re.sub(r'[^\w]', '', text.casefold(), flags=re.UNICODE)


def reconcile(provider, observed, silences):
    match = difflib.SequenceMatcher(None, [normalize(w['text']) for w in provider],
                                    [normalize(w['word']) for w in observed], autojunk=False)
    indexes = {block.a + i: block.b + i for block in match.get_matching_blocks() for i in range(block.size)}
    result, flags = [], []
    for i, original in enumerate(provider):
        word = {'text': original['text'], 'start': original['start_seconds'], 'end': original['end_seconds'], 'source': 'provider'}
        if i not in indexes:
            flags.append({'index': i, 'word': word['text'], 'reason': 'unmatched_asr_tokenization'})
        else:
            alt = observed[indexes[i]]
            crossing = [s for s in silences if alt['start'] < s[0] and alt['end'] > s[1]]
            delta = abs(alt['start'] - word['start'])
            if crossing:
                flags.append({'index': i, 'word': word['text'], 'reason': 'asr_word_spans_silence', 'asr_start': alt['start'], 'asr_end': alt['end'], 'silence': crossing, 'provider_start': word['start']})
            elif delta > .15:
                flags.append({'index': i, 'word': word['text'], 'reason': 'alignment_disagreement', 'difference_seconds': round(delta, 3)})
        if word['end'] < word['start'] or (result and word['start'] < result[-1]['start']):
            raise ValueError('Provider word timing is invalid or unordered')
        result.append(word)
    return result, flags


def main():
    ap = argparse.ArgumentParser();ap.add_argument('--audio', type=Path, required=True);ap.add_argument('--provider', type=Path, required=True);ap.add_argument('--asr', type=Path, required=True);ap.add_argument('--output', type=Path, required=True);args=ap.parse_args()
    provider=json.loads(args.provider.read_text())['words'];asr=json.loads(args.asr.read_text());observed=[w for s in asr['segments'] for w in s['words']]
    proc=subprocess.run(['ffmpeg','-hide_banner','-nostats','-i',str(args.audio),'-af','silencedetect=noise=-35dB:d=0.12','-f','null','-'],capture_output=True,text=True,check=True)
    quiet=[];start=None
    for line in proc.stderr.splitlines():
        m=re.search(r'silence_start: ([0-9.]+)',line)
        if m: start=float(m.group(1))
        m=re.search(r'silence_end: ([0-9.]+)',line)
        if m and start is not None: quiet.append([start,float(m.group(1))]);start=None
    words,flags=reconcile(provider,observed,quiet)
    result={'status':'REVIEW_REQUIRED','audio_sha256':hashlib.sha256(args.audio.read_bytes()).hexdigest(),'provider_sha256':hashlib.sha256(args.provider.read_bytes()).hexdigest(),'asr_sha256':hashlib.sha256(args.asr.read_bytes()).hexdigest(),'silence_settings':'-35 dB, minimum 0.12 s','silences':quiet,'words':words,'flags':flags,'warning':'Provider timing is an unverified estimate; quiet is not speech identification. Review all flagged words and audible sync.'}
    args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(f'{len(words)} words, {len(flags)} flags; REVIEW_REQUIRED')
if __name__=='__main__':main()
