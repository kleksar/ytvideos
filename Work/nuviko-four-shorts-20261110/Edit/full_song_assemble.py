"""Assemble saved video parts with durations on the exact 30 fps timeline."""
from pathlib import Path
import json, subprocess, sys
from full_song_plan import edit, run, read, write, FPS

name=sys.argv[1]
plan=read(edit/f'{name}-full-song-v01-contract.json')
folder=run/name
output=Path(plan['output'])
clips=plan['clips']
bounds=[0,*plan['transition_centres'],plan['frames']]
parts=sorted(folder.glob('part-[0-9][0-9][0-9].mp4'))
sections=[(i,min(i+9,len(clips))) for i in range(0,len(clips),9)]
assert len(parts)==len(sections)
concat=folder/'exact-sections.ffconcat'
entries=[]
for slot,(part,(start,end)) in enumerate(zip(parts,sections)):
    if slot in plan.get('replacement_sections',[]):
        part=part.with_name(part.stem+'-replacement.mp4')
        assert part.is_file()
    a=bounds[start]-int(start>0)
    b=bounds[end]-int(end<len(clips))
    entries.append(f"file '{part.name}'\nduration {(b-a)/FPS:.9f}\n")
concat.write_text('ffconcat version 1.0\n'+''.join(entries))
tmp=folder/'verified-assembly.mp4'
assert not tmp.exists()
audio_source = plan['source'] if plan['audio'].get('packet_copy') else plan['wav']
audio_args = ['-c:a','copy','-bsf:a','aac_adtstoasc'] if plan['audio'].get('packet_copy') else ['-c:a','aac','-b:a','256k','-ar','44100']
cmd=['ffmpeg','-nostdin','-n','-v','error','-f','concat','-safe','0','-i',str(concat),'-i',audio_source,
     '-map','0:v:0','-map','1:a:0','-c:v','copy',*audio_args,
     '-bsf:v','h264_metadata=colour_primaries=1:transfer_characteristics=1:matrix_coefficients=1:video_full_range_flag=0',
     '-colorspace','bt709','-color_primaries','bt709','-color_trc','bt709',
     '-movflags','+faststart+write_colr','-video_track_timescale','30000',str(tmp)]
write(folder/'exact-assemble-command.json',cmd)
subprocess.run(cmd,check=True)
raw=subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_packets','-show_entries','packet=pts','-of','json',tmp])
pts=sorted(int(p['pts']) for p in json.loads(raw)['packets'])
assert pts==list(range(0,plan['frames']*1000,1000)),next(((i,n) for i,n in enumerate(pts) if i*1000!=n),None)
tmp.replace(output)
print(name,'verified exact frame PTS',len(pts),flush=True)
