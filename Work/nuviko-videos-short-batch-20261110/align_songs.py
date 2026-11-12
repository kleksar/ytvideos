import json, sys
from pathlib import Path
import torch, whisper
from whisper.timing import find_alignment
from whisper.tokenizer import get_tokenizer
w=Path(__file__).parent
name=sys.argv[1]
audio=w/('notion-rise-excerpt.wav' if name=='notion' else 'atlantis-excerpt-draft.wav')
lyrics=('Rise oh back when I was younger was told by other youngsters that my end will be torture beneath the earth cause I dont see what' if name=='notion' else 'And in my head tell me why this has to end oh no oh no I cant save us my Atlantis we')
device='mps' if torch.backends.mps.is_available() else 'cpu'
model=whisper.load_model('medium',device=device)
data=whisper.load_audio(str(audio)); mel=whisper.log_mel_spectrogram(whisper.pad_or_trim(data),model.dims.n_mels).to(device)
tok=get_tokenizer(model.is_multilingual,language='en',task='transcribe')
with torch.no_grad():
 result=find_alignment(model,tok,tok.encode(' '+lyrics),mel,min(len(data)//160,3000))
out=[{'text':x.word.strip(),'start_seconds':round(x.start,3),'end_seconds':round(x.end,3),'probability':round(x.probability,3)} for x in result]
(w/f'{name}-forced-alignment.json').write_text(json.dumps(out,indent=2)); print(json.dumps(out))
