import hashlib, json, subprocess
from pathlib import Path

root = Path('/Users/diplomat/ytvideos')
batch = root / 'Work/nuviko-four-shorts-20261110'
src = root / 'Work/nuviko-videos-short-batch-20261110'
out = batch / 'Deliverables/Epic-Inspiration-review-v01.mp4'
if out.exists():
    raise SystemExit('Output exists; do not overwrite')
cuts = [0, 91, 185, 281, 376, 480]
shots = [src / f'pexels-{n}.mp4' for n in [30320376,35179742,35188969,36086839,37362542]]
audio = batch / 'Source/epic-excerpt-60s.wav'
graph = []
for i, (start, end) in enumerate(zip(cuts, cuts[1:])):
    frames = end-start
    phase = f'(1-cos(PI*on/{frames-1}))/2'
    z = f'1+0.1052631579*{phase}' if i % 2 == 0 else f'1.1052631579-0.1052631579*{phase}'
    graph.append(f"[{i}:v]fps=30,trim=start=1:end={1+frames/30:.8f},setpts=PTS-STARTPTS,scale=1140:2026:force_original_aspect_ratio=increase:flags=bicubic,crop=1140:2026,zoompan=z='{z}':x='(iw-iw/zoom)/2':y='(ih-ih/zoom)/2':d=1:s=1080x1920:fps=30,setsar=1,setpts=PTS-STARTPTS[v{i}]")
graph.append(''.join(f'[v{i}]' for i in range(len(shots))) + f'concat=n={len(shots)}:v=1:a=0,eq=contrast=1.25:saturation=1.5,format=yuv420p,split[base][high]')
graph.append("[high]lutyuv=y='max(0,val-190)*3':u=128:v=128,gblur=sigma=12[glow]")
glow = '+'.join(f'pow((1+cos(PI*min(abs(T*30-{n})/3.75,1)))/2,2)' for n in cuts[1:-1])
blur = '+'.join(f'((1+cos(PI*min(abs(T*30-{n})/7.5,1)))/2)' for n in cuts[1:-1])
graph.append(f"[base][glow]blend=c0_expr='min(235,A+B*0.35*({glow}))':c1_expr='A':c2_expr='A',split[clean][blur_source]")
graph.append('[blur_source]gblur=sigma=5[blurred]')
graph.append(f"[clean][blurred]blend=all_expr='A+(B-A)*0.25*({blur})',format=yuv420p[video]")
graph.append(f'[{len(shots)}:a]atrim=duration=16,asetpts=PTS-STARTPTS,afade=t=in:st=0:d=0.04,afade=t=out:st=15.8:d=0.2[audio]')
graph_path = batch/'Edit/epic-v01.ffgraph'
graph_path.write_text(';\n'.join(graph)+'\n')
def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''): h.update(block)
    return h.hexdigest()
argv=['ffmpeg','-nostdin','-n','-hide_banner','-loglevel','error','-filter_complex_threads','2']
for p in shots: argv += ['-i',str(p)]
argv += ['-i',str(audio),'-filter_complex_script',str(graph_path),'-map','[video]','-map','[audio]','-r','30','-fps_mode','cfr','-c:v','libx264','-preset','veryfast','-crf','19','-pix_fmt','yuv420p','-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709','-c:a','aac','-b:a','192k','-ar','44100','-ac','2','-movflags','+faststart',str(out)]
contract={'status':'READY_TO_RENDER','purpose':'private local review; no upload','track':'Epic Inspiration — AShamaluevMusic','music_source':'official artist free download','music_publication_rights':'unverified for embedded channel publication; separate review required','excerpt_seconds_in_full_track':[60,76],'fps':30,'frames':480,'size':[1080,1920],'cuts':cuts,'shots':[{'path':str(p),'sha256':sha(p),'source_offset_seconds':1} for p in shots],'audio':{'path':str(audio),'sha256':sha(audio)},'graph_sha256':sha(graph_path),'command':argv,'subtitles':'none: user request','output':str(out),'qa':'pending'}
(batch/'Edit/epic-v01-contract.json').write_text(json.dumps(contract,indent=2,ensure_ascii=False)+'\n')
(batch/'Edit/epic-v01-cut-map.json').write_text(json.dumps({'fps':30,'cut_frames':cuts[1:-1]},indent=2)+'\n')
subprocess.run(argv,check=True)
