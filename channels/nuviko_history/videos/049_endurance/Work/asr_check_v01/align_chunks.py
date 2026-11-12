"""Chunked forced-alignment diagnostic; not accepted timing and no audio changes."""
from pathlib import Path
import json,re,hashlib
import whisperx
root=Path(__file__).resolve().parents[2]
audio=root/'Source/Voice/voice_en_v01/voice_en.mp3'
provider=json.loads((root/'Source/Captions/word_times_en_v01.json').read_text())['words']
# Conservative, overlapping 20-second nominal windows anchored to the provider estimate.
# Input words are assigned once; overlaps give the aligner room to handle segment boundaries.
chunks=[]
for sec in range(0,560,20):
 words=[x for x in provider if sec<=x['start']<sec+20]
 if words:
  chunks.append({'start':max(0,sec-1.2),'end':min(559.84,sec+21.2),'text':' '.join(x['text'] for x in words)})
model,meta=whisperx.load_align_model(language_code='en',device='cpu')
y=whisperx.load_audio(str(audio));aligned=whisperx.align(chunks,model,meta,y,'cpu',return_char_alignments=False)
out=Path(__file__).with_name('whisperx_chunks_raw_v01.json')
with out.open('x') as f:json.dump({'status':'REVIEW_REQUIRED','audio_sha256':hashlib.sha256(audio.read_bytes()).hexdigest(),'chunks':chunks,'result':aligned,'note':'Independent estimates from overlapping chunks. Map not conformed; verify words and audio.'},f,ensure_ascii=False,indent=2)
print('saved',out,'words',len(aligned.get('word_segments',[])))
