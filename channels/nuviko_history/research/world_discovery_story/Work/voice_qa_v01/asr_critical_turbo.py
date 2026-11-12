from pathlib import Path
import json,subprocess,hashlib
from faster_whisper import WhisperModel
root=Path(__file__).resolve().parents[2]; out=Path(__file__).parent/'turbo_windows_v01';out.mkdir(exist_ok=True)
source=root/'Source/Voice/voice_en.mp3'
model='/Users/diplomat/.cache/huggingface/hub/models--mobiuslabsgmbh--faster-whisper-large-v3-turbo/snapshots/0a363e9161cbc7ed1431c9597a8ceaf0c4f78fcf'
windows=[('maori',15,10),('al_idrisi',232,12),('taino',316,12),('elcano',382,12)]
m=WhisperModel(model,device='cpu',compute_type='int8',cpu_threads=4,local_files_only=True)
result=[]
for name,start,duration in windows:
 path=out/(name+'.wav')
 subprocess.run(['ffmpeg','-v','error','-y','-ss',str(start),'-t',str(duration),'-i',str(source),'-ac','1','-ar','16000',str(path)],check=True)
 segs,info=m.transcribe(str(path),beam_size=5,language='en',vad_filter=False,word_timestamps=True,condition_on_previous_text=False)
 segs=list(segs); item={'id':name,'source_offset':start,'duration':duration,'text':' '.join(x.text.strip() for x in segs),'words':[{'word':w.word,'start':round(start+w.start,3),'end':round(start+w.end,3),'probability':w.probability} for x in segs for w in (x.words or [])]};result.append(item);print(name,item['text'],flush=True)
(out/'recognition_DRAFT.json').write_text(json.dumps({'audio_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'model':'faster-whisper-large-v3-turbo local CPU int8','status':'ASR diagnostic, not listening or pronunciation verification','windows':result},ensure_ascii=False,indent=2)+'\n')
