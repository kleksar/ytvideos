from pathlib import Path
import json,hashlib,re
work=Path(__file__).resolve().parent
base=work.parents[1]
original=json.loads((work/"scene_boundaries_forced_DRAFT.json").read_text())
joint=json.loads((work/"joint_boundaries_3pairs_DRAFT.json").read_text())
assert original["audio_sha256"]==joint["audio_sha256"]==hashlib.sha256((base/"Source/Voice/voice_en.mp3").read_bytes()).hexdigest()
assert original["text_sha256"]==joint["input_text_sha256"]
spans=original["blocks"]
pairs=joint["raw_segment_pairs_1based"]; sentences=joint["result"]["segments"]
assert len(sentences)==2*len(pairs)
normalize=lambda s:re.sub(r"[^\w]","",s.casefold())
for one,two in zip(sentences[::2],sentences[1::2]):
 left=[i for i,x in enumerate(spans) if normalize(one["text"]) in normalize(x["text"])]
 right=[i for i,x in enumerate(spans) if normalize(two["text"]) in normalize(x["text"])]
 assert len(left)==len(right)==1 and right[0]==left[0]+1
 a,b=left[0],right[0]
 assert one["words"][-1]["end"]<=two["words"][0]["start"]
 spans[a]["speech_end"]=one["words"][-1]["end"]
 spans[b]["speech_start"]=two["words"][0]["start"]
cuts=[0.0]+[round((a["speech_end"]+b["speech_start"])/2,3) for a,b in zip(spans,spans[1:])]+[483.76]
for i,x in enumerate(spans):
 x["cut_in"],x["cut_out"]=cuts[i:i+2]
 x["duration"]=round(cuts[i+1]-cuts[i],3)
 x["status"]="REVIEW_OVERLAP" if i and spans[i-1]["speech_end"]>x["speech_start"] else ("RETIME" if not 4<=x["duration"]<=6 else "DRAFT")
out={**original,"method":"forced block alignment with three pairwise joint realignments, midpoint scene cuts; automatic draft only","blocks":spans}
(work/"scene_boundaries_joint_DRAFT.json").write_text(json.dumps(out,ensure_ascii=False,indent=2)+"\n")
print("scene_count",len(spans),"retime",sum(x["status"]=="RETIME" for x in spans),"overlap",sum(x["status"]=="REVIEW_OVERLAP" for x in spans))
