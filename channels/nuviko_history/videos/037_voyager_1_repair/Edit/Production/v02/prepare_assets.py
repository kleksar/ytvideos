from pathlib import Path
import json,hashlib,re,subprocess,math
EP=Path(__file__).resolve().parents[3]; OUT=EP/'Edit/Production/v02'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
voice=EP/'Source/Voice/en_v01_nuviko/voice_en.mp3'; transcript=(EP/'Source/Script/narration_en_v01.md').read_text().strip().removeprefix('# ').strip();(OUT/'transcript_en.txt').write_text(transcript+'\n')
alignment_path=EP/'Source/Voice/en_v01_nuviko/voice_en.alignment.json';raw=json.loads(alignment_path.read_text());a=raw['alignment'];starts=a['character_start_times_seconds'];durations=a['character_end_times_seconds'];chars=a['characters'];s=''.join(chars)
assert s.strip().removeprefix('# ').strip()==transcript
# Saved provider-history adapter labelled durations as end times. Do not mutate it.
diffs=[abs(starts[i]+durations[i]-starts[i+1]) for i in range(len(starts)-1)]
assert max(diffs)<.005,max(diffs)
ends=[x+y for x,y in zip(starts,durations)]; words=[]
for m in re.finditer(r'\S+',s):
 token=m[0]
 if token=='#':continue
 if token=='—':
  words[-1]['text']+=' —';continue
 indices=[i for i in range(m.start(),m.end()) if chars[i].isalnum()]
 if not indices:raise ValueError(token)
 words.append({'text':token,'start':starts[indices[0]],'end':ends[indices[-1]],'source':'provider_history_durations_converted'})
# Caption-only punctuation is attached to its preceding spoken word, preserving literal whitespace-normalized text.
assert ' '.join(x['text'] for x in words)==' '.join(transcript.split())
record={'status':'REVIEW_REQUIRED','audio_sha256':sha(voice),'transcript_sha256':hashlib.sha256(transcript.encode()).hexdigest(),'words':words,'source_alignment_sha256':sha(alignment_path),'conform':'Voice already synthesized at speed 1.1; no second speed/offset. Source start maps to final start 0.0. Final mix identity will be bound after mix preparation.','normalization':'Raw history JSON end-time array contains per-character durations: all nonfinal starts+durations match next start within 5ms. Converted to absolute ends in this derived map only. Markdown heading marker is nonspoken (zero duration); standalone em dash attached to preceding spoken word; trailing punctuation timing excluded from last word.'}
(OUT/'word_times_provider_v01.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
(OUT/'alignment_adapter_evidence.json').write_text(json.dumps({'raw':str(alignment_path),'raw_sha256':sha(alignment_path),'max_duration_to_next_start_error_seconds':max(diffs),'raw_chars':len(chars),'spoken_word_entries':len(words),'last_spoken_word_end':words[-1]['end'],'last_punctuation_end':ends[-1],'audio_source_sha256':sha(voice),'audible_sync':'UNVERIFIED'},indent=2)+'\n')
print(EP,len(words),'last word',words[-1])
