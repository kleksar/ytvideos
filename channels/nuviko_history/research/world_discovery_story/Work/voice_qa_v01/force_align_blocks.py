import json, hashlib, re, time
from pathlib import Path
import whisperx
base=Path('channels/nuviko_history/research/world_discovery_story')
work=base/'Work/voice_qa_v01'
audio_file=base/'Source/Voice/voice_en.mp3'
text_file=base/'Source/Voice/narration-en-v01.txt'
source=text_file.read_text().strip()
blocks=source.split('\n\n')
bounds=json.loads((work/'block_boundaries-provider.json').read_text())['blocks']
assert len(blocks)==len(bounds)==89
print('load audio and model',flush=True)
audio=whisperx.load_audio(str(audio_file)); model,metadata=whisperx.load_align_model(language_code='en',device='cpu')
segments=[]
for b,v in zip(blocks,bounds):
 segments.append({'start':max(0,v['start']-0.8),'end':min(len(audio)/16000,v['last_word_end']+0.45),'text':b})
print('align',len(segments),'overlapping sentence windows',flush=True)
result=whisperx.align(segments,model,metadata,audio,'cpu',return_char_alignments=False,print_progress=True)
out=work/'forced_blocks_raw.json'
with out.open('x') as f: json.dump({'audio_sha256':hashlib.sha256(audio_file.read_bytes()).hexdigest(),'text_sha256':hashlib.sha256(source.encode()).hexdigest(),'window_padding':'0.8 s before and 0.45 s after provider boundaries; overlapping audio, unique text','result':result},f,ensure_ascii=False)
print('done raw',len(result.get('word_segments',[])),flush=True)
