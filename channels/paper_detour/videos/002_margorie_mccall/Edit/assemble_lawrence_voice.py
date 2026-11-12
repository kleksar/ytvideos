#!/usr/bin/env python3
"""Assemble the seven generated V7 English voice segments without truncation."""
from pathlib import Path
import hashlib, json, struct, subprocess, wave
from array import array
root=Path('/Users/diplomat/ytvideos/channels/paper_detour/videos/002_margorie_mccall/Source/Voice')
text_path=root/'script_en.txt'
script=text_path.read_text().strip()
parts=root/'segments_v7_lawrence'
rate=44100
gap_seconds=0.22
gap_samples=round(gap_seconds*rate)
combined=array('h')
chars=[]; starts=[]; ends=[]; report=[]; corrections=[]
for n in range(1,8):
    folder=parts/f'{n:02d}'
    text=(folder/'text.txt').read_text().strip()
    response=json.loads((folder/'voice_en.alignment.json').read_text())['alignment']
    if ''.join(response['characters']) != text: raise ValueError(f'{n}: text does not match alignment')
    pcm=subprocess.run(['ffmpeg','-v','error','-i',str(folder/'voice_en.mp3'),'-f','s16le','-ac','1','-ar',str(rate),'-'],check=True,stdout=subprocess.PIPE).stdout
    audio=array('h'); audio.frombytes(pcm)
    duration=len(audio)/rate
    if n>1:
        old_end=len(combined)/rate
        combined.extend([0]*gap_samples)
        for k in range(2):
            chars.append('\n'); starts.append(old_end+k*gap_seconds/2); ends.append(old_end+(k+1)*gap_seconds/2)
    offset=len(combined)/rate
    for char,start,end in zip(response['characters'],response['character_start_times_seconds'],response['character_end_times_seconds']):
        if end>duration+0.001:
            corrections.append({'segment':n,'character':char,'source_end':end,'decoded_end':duration})
            end=min(end,duration)
        start=min(start,duration)
        chars.append(char); starts.append(round(offset+start,6)); ends.append(round(offset+end,6))
    combined.extend(audio)
    last=audio[-min(len(audio),round(0.05*rate)):]
    rms=(sum(x*x for x in last)/len(last))**0.5/32768 if last else 0
    report.append({'segment':n,'start_seconds':round(offset,6),'duration_seconds':round(duration,6),'end_rms_50ms':rms,'audio':str(folder/'voice_en.mp3'),'alignment':str(folder/'voice_en.alignment.json'),'text':str(folder/'text.txt')})
if ''.join(chars)!=script: raise ValueError('Combined text does not match script')
out=root/'voice_en_lawrence_1x.wav'
if out.exists(): raise FileExistsError(out)
with wave.open(str(out),'wb') as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(rate); w.writeframes(combined.tobytes())
(root/'voice_en_lawrence.alignment.json').write_text(json.dumps({'alignment':{'characters':chars,'character_start_times_seconds':starts,'character_end_times_seconds':ends}},ensure_ascii=False,indent=2)+'\n')
(root/'segments_lawrence_timeline.json').write_text(json.dumps({'sample_rate':rate,'duration_seconds_1x':len(combined)/rate,'gap_seconds':gap_seconds,'alignment_clips_at_decoded_end':corrections,'segments':report},ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'duration_seconds_1x':len(combined)/rate,'duration_seconds_110':len(combined)/rate/1.1,'duration_seconds_1155':len(combined)/rate/1.155,'alignment_clips_at_decoded_end':corrections,'segments':report},ensure_ascii=False,indent=2))
