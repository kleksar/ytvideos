import hashlib
import json
import sys
from pathlib import Path

root = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(root / 'automation' / 'elevenlabs'))
import tts

episode = Path(__file__).resolve().parents[1]
audio = episode / 'Source' / 'Audio' / 'v01'
script = (audio / 'narration.txt').read_text().strip()
ending = 'What would you do if you had...'
assert script.endswith(ending)
request = ending + ' ' + script[:-len(ending)].strip()
(audio / 'request_text.txt').write_text(request + '\n')
out = audio / 'voice_raw.mp3'
receipt = audio / 'request.json'
if receipt.exists() or out.exists():
    raise SystemExit('Existing request or audio: inspect before any retry.')
keys = tts.configured_keys()
if not keys:
    raise SystemExit('No ElevenLabs key accessible; no synthesis request sent.')
record = {'voice_id': 'zfc8CJQpe8Kqyl0vvCzo', 'model': 'eleven_v4', 'speed': 1.1,
          'text_sha256': hashlib.sha256(request.encode()).hexdigest(), 'status': 'request_started'}
tts.save_new(receipt, (json.dumps(record, indent=2) + '\n').encode())
try:
    tts.synthesize_with_failover(request, out, api_keys=keys, voice_id=record['voice_id'],
                                 model=record['model'], stability=1.0, similarity=0.0, speed=1.1)
except tts.TTSError as exc:
    print('Synthesis stopped:', exc, file=sys.stderr)
    raise SystemExit(1)
record['status'] = 'completed'
record['audio_sha256'] = hashlib.sha256(out.read_bytes()).hexdigest()
receipt.write_text(json.dumps(record, indent=2) + '\n')
print('Voice generated; receipt recorded.')
