import hashlib
import json
import re
from pathlib import Path

base = Path(__file__).resolve().parents[2]
text = (base / 'Source/Voice/narration_en_v01.txt').read_text().strip()
source = json.loads((base / 'Source/Voice/word_times_source_v01.json').read_text())
tokens = text.split()
words = source['words']
if len(tokens) != len(words):
    raise ValueError('Token count mismatch')
def canonical(s):
    return re.sub(r'[^\w\u2019\']', '', s).casefold()
for token, word in zip(tokens, words):
    if canonical(token) != canonical(word['text']):
        raise ValueError(f"Token mismatch: {token} != {word['text']}")
result = {
    'status': 'REVIEW_REQUIRED',
    'audio_sha256': hashlib.sha256((base / 'Work/audio-v01/mix_draft.wav').read_bytes()).hexdigest(),
    'transcript_sha256': hashlib.sha256(text.encode()).hexdigest(),
    'source': 'ElevenLabs character alignment; source / 1.10 + 0.30 seconds; draft mix',
    'words': [{'text': token, 'start': round(.3 + w['start_seconds'] / 1.1, 4),
               'end': round(.3 + w['end_seconds'] / 1.1, 4)} for token, w in zip(tokens, words)],
}
for i, word in enumerate(result['words']):
    if word['end'] <= word['start'] or (i and word['start'] < result['words'][i-1]['end']):
        raise ValueError(f'Invalid interval {i}: {word}')
out = base / 'Work/audio-v01/word_times_draft.json'
with out.open('x') as f:
    json.dump(result, f, indent=2, ensure_ascii=False)
print(f"Wrote {len(words)} words to {out}; listening and final-mix validation remain open.")
