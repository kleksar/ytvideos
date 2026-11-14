#!/usr/bin/env python3
"""Prepare a hash-bound, review-only WhisperX alignment for a retained recording."""
import argparse
import hashlib
import json
import re
from pathlib import Path


def norm(value):
    return re.sub(r'[^\w]', '', value.casefold(), flags=re.UNICODE)


def build_map(text, audio_hash, aligned):
    tokens = text.split()
    aligned_words = aligned.get('word_segments', [])
    # Some aligners return two spoken words on either side of a contiguous
    # em/en dash. Retain the exact punctuation and describe the missing
    # whitespace explicitly instead of changing the approved transcript.
    mapped = []
    cursor = 0
    for token in tokens:
        parts = re.split(r'(?<=[—–])(?=\w)', token)
        if cursor < len(aligned_words) and norm(token) == norm(aligned_words[cursor].get('word', '')):
            mapped.append((token, aligned_words[cursor], False))
            cursor += 1
        elif (len(parts) > 1 and len(aligned_words[cursor:cursor + len(parts)]) == len(parts)
              and all(norm(part) == norm(item.get('word', ''))
                      for part, item in zip(parts, aligned_words[cursor:cursor + len(parts)]))):
            for index, (part, item) in enumerate(zip(parts, aligned_words[cursor:cursor + len(parts)])):
                mapped.append((part, item, index > 0))
            cursor += len(parts)
        else:
            raise ValueError('Forced alignment tokenization differs from the exact transcript; reconcile explicitly')
    if cursor != len(aligned_words):
        raise ValueError('Forced alignment tokenization differs from the exact transcript; reconcile explicitly')
    result=[]
    for token, item, joined in mapped:
        if 'start' not in item or 'end' not in item:
            raise ValueError(f'Missing timing for {token!r}; manual reconciliation required')
        start,end=item['start'],item['end']
        if not 0 <= start < end or (result and start < result[-1]['end']):
            raise ValueError(f'Invalid or unordered timing for {token!r}')
        display_token = token.translate(str.maketrans('', '', '\"“”„‟«»'))
        if not display_token:
            raise ValueError('Standalone quotation marks require explicit transcript token reconciliation')
        word = {'text':display_token,'start':start,'end':end,'source':'whisperx_forced_alignment','score':item.get('score')}
        if joined:
            word['join_previous'] = True
        result.append(word)
    return {'status':'REVIEW_REQUIRED','audio_sha256':audio_hash,'transcript_sha256':hashlib.sha256(text.encode('utf-8')).hexdigest(),'words':result,'note':'Automatic estimate; audible sync and edit conform unverified.'}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--audio',type=Path,required=True);parser.add_argument('--text',type=Path,required=True)
    parser.add_argument('--language',required=True);parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--raw-output',type=Path,required=True);parser.add_argument('--device',default='cpu')
    args=parser.parse_args()
    if args.output.exists() or args.raw_output.exists() or args.output.resolve()==args.raw_output.resolve():
        raise ValueError('Choose distinct new output paths')
    import whisperx
    text=args.text.read_text(encoding='utf-8').strip();audio=whisperx.load_audio(str(args.audio))
    model,metadata=whisperx.load_align_model(language_code=args.language,device=args.device)
    # WhisperX partitions on spaces. Add an aligner-only boundary after a
    # contiguous dash, without changing the approved text or its hash.
    alignment_text = re.sub(r'(?<=[—–])(?=\w)', ' ', text.replace('\n', ' '))
    result=whisperx.align([{'start':0.0,'end':len(audio)/16000,'text':alignment_text}],model,metadata,audio,args.device,return_char_alignments=False)
    mapped=build_map(text,hashlib.sha256(args.audio.read_bytes()).hexdigest(),result)
    with args.raw_output.open('x',encoding='utf-8') as f: json.dump(result,f,ensure_ascii=False,indent=2)
    with args.output.open('x',encoding='utf-8') as f: json.dump(mapped,f,ensure_ascii=False,indent=2)
    print(f"{len(mapped['words'])} words; REVIEW_REQUIRED")

if __name__=='__main__':main()
