import json,sys
from pathlib import Path
import whisperx
w=Path(__file__).parent
name=sys.argv[1]
audio=w/'separated'/'htdemucs'/('notion-rise-excerpt' if name=='notion' else 'atlantis-excerpt-draft')/'vocals.wav'
lyrics=('Rise oh back when I was younger was told by other youngsters that my end will be torture beneath the earth cause I dont see what' if name=='notion' else 'And in my head tell me why this has to end oh no oh no I cant save us my Atlantis we')
model,meta=whisperx.load_align_model(language_code='en',device='cpu',model_dir='/Users/diplomat/.cache/torch/hub/checkpoints')
segments=([{'start':0,'end':6.99,'text':'Rise oh back when I was younger was told by other youngsters'},
           {'start':6.99,'end':12.94,'text':'that my end will be torture beneath the earth'},
           {'start':12.94,'end':14.99,'text':'cause I dont see what'}] if name=='notion' else
          [{'start':0,'end':5.55,'text':'And in my head tell me why this has to end oh no'},
           {'start':6.4,'end':9.7,'text':'oh no'},
           {'start':9.7,'end':14.99,'text':'I cant save us my Atlantis we'}])
result=whisperx.align(segments,model,meta,str(audio),'cpu',return_char_alignments=False)
(w/f'{name}-vocal-ctc-segmented.json').write_text(json.dumps(result,indent=2)); print(json.dumps(result['word_segments']))
