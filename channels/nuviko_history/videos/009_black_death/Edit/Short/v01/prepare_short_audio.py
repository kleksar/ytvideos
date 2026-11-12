import json, pathlib, subprocess, sys
base=pathlib.Path('/Users/diplomat/ytvideos/channels/nuviko_history/videos/009_black_death')
source=base/'Source/Recovered/word_alignment_from_youtube_captions_v01.json'
outdir=base/'Source/Short/v01'
audio_in=base/'Source/Recovered/black_death_original_audio.m4a'
audio_out=outdir/'black_death_short_mix_v01.wav'
alignment=json.load(open(source))
assert alignment['status']=='PROVISIONAL_REQUIRES_AUDIBLE_ALIGNMENT_REVIEW'
segments=[(232.85,239.292),(285.77,298.094),(302.21,318.294)]
filters=[]
for i,(a,b) in enumerate(segments):
    filters.append(f'[0:a]atrim=start={a:.2f}:end={b:.2f},asetpts=PTS-STARTPTS[s{i}]')
filters.append(f'{"".join(f"[s{i}]" for i in range(len(segments)))}concat=n={len(segments)}:v=0:a=1[out]')
cmd=['ffmpeg','-nostdin','-y','-v','warning','-i',str(audio_in),'-filter_complex',';'.join(filters),'-map','[out]','-c:a','pcm_s24le','-ar','44100','-ac','2',str(audio_out)]
subprocess.run(cmd,check=True)
# Conform each source timed word to the concatenated output timeline, retaining only complete words.
words=[]; offset=0.0
for a,b in segments:
    selected=[w for w in alignment['words'] if w['start']>=a-1e-7 and w['end']<=b+1e-7]
    if not selected:
        raise SystemExit(f'no aligned words in {a}-{b}')
    for w in selected:
        words.append({'text':w['text'],'start':round(offset+w['start']-a,3),'end':round(offset+w['end']-a,3),'source_start':w['start'],'source_end':w['end'],'timing_source':w['timing_source']})
    offset += b-a
payload={'status':'PROVISIONAL_REQUIRES_AUDIBLE_ALIGNMENT_REVIEW','source_audio':str(audio_in),'source_audio_sha256':alignment['source_audio_sha256'],'source_alignment':str(source),'source_alignment_status':alignment['status'],'source_vtt_sha256':alignment['source_vtt_sha256'],'edit_audio':str(audio_out),'segments':[{'source_in':a,'source_out':b,'output_in':round(sum(y-x for x,y in segments[:i]),3),'duration':round(b-a,3)} for i,(a,b) in enumerate(segments)],'expected_duration_seconds':round(offset,3),'words':words}
json.dump(payload,open(outdir/'word_times_v01.json','w'),ensure_ascii=False,indent=2)
text=' '.join(w['text'] for w in words)
pathlib.Path(outdir/'retained_transcript_v01.txt').write_text(text+'\n')
print(json.dumps({'audio':str(audio_out),'expected_duration':round(offset,3),'words':len(words),'first':words[0],'last':words[-1]},ensure_ascii=False,indent=2))
