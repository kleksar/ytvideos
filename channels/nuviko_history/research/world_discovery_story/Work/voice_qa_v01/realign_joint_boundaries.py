from pathlib import Path
import json,hashlib
import whisperx
base=Path("channels/nuviko_history/research/world_discovery_story")
work=base/"Work/voice_qa_v01"
audio_path=base/"Source/Voice/voice_en.mp3"
raw=json.loads((work/"forced_blocks_raw.json").read_text())
segs=raw["result"]["segments"]
pairs=[(8,9),(23,24),(38,39)]
audio=whisperx.load_audio(str(audio_path))
model,meta=whisperx.load_align_model(language_code="en",device="cpu")
merged=[{"start":max(0,segs[a]["start"]-0.8),"end":min(len(audio)/16000,segs[b]["end"]+0.6),"text":segs[a]["text"]+" "+segs[b]["text"]} for a,b in pairs]
result=whisperx.align(merged,model,meta,audio,"cpu",return_char_alignments=False,print_progress=True)
out={"audio_sha256":hashlib.sha256(audio_path.read_bytes()).hexdigest(),"input_text_sha256":raw["text_sha256"],"method":"joint alignment of each adjacent sentence pair in one audio window; automated only","raw_segment_pairs_1based":[[a+1,b+1] for a,b in pairs],"result":result}
(work/"joint_boundaries_3pairs_DRAFT.json").write_text(json.dumps(out,indent=2,ensure_ascii=False))
print("saved",len(result["segments"]))
