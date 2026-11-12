import hashlib, importlib.util, json, os, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path('/Users/diplomat/ytvideos')
EP = ROOT/'channels/scenes_on_repeat/videos/compilation-two-trailers'
WORK = EP/'Work/v01'
OTHER = Path('/Users/diplomat/.codex/worktrees/ad59/ytvideos/channels/scenes_on_repeat/videos')
E = OTHER/'edge-of-tomorrow-2014/Edit/trailer-v03'
H = OTHER/'home-alone-1990/Edit/trailer-v02'
OUT = EP/'Deliverables/movie-trailers-compilation-v01.mp4'
FPS=24

def sha(p):
    h=hashlib.sha256()
    with open(p,'rb') as f:
        for b in iter(lambda:f.read(4*1024*1024),b''): h.update(b)
    return h.hexdigest()

def run(args):
    subprocess.run([str(x) for x in args], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)

def module(path, name):
    spec=importlib.util.spec_from_file_location(name,path)
    m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

def ass_time(t):
    cs=round(t*100); return f'{cs//360000}:{cs//6000%60:02}:{cs//100%60:02}.{cs%100:02}'

def main():
    WORK.mkdir(parents=True,exist_ok=True)
    if OUT.exists(): raise RuntimeError('Output already exists')
    eh=json.loads((E/'compilation-handoff.json').read_text()); hh=json.loads((H/'compilation-handoff.json').read_text())
    for handoff,base in [(eh,E),(hh,H)]:
        for path,expect in [(Path(handoff['source']['path']),handoff['source']['sha256']), (base/handoff['timeline'],handoff['timeline_sha256'])]:
            if sha(path)!=expect: raise RuntimeError(f'Hash mismatch: {path}')
    edge=json.loads((E/'frozen-edit.json').read_text()); home=json.loads((H/'frozen-edit.json').read_text())
    edge_source=Path(eh['source']['path']); home_source=Path(hh['source']['path'])
    for h in [eh,hh]:
        p=Path(h['music']['path']).expanduser()
        if sha(p)!=h['music']['sha256']: raise RuntimeError(f'Music hash mismatch: {p}')
    sys.path[:0]=[str(ROOT/'channels/scenes_on_repeat/automation/pipeline'),str(ROOT/'automation/ffmpeg_montage')]
    ebuild=module(E/'build.py','edge_build'); hbuild=module(H/'build.py','home_build')
    from caption_groups import resolve_groups
    edialogue=json.loads((E/'dialogue.json').read_text())
    egroups=resolve_groups(edialogue['words'],edialogue['lines'])
    ebuild.SCRATCH=WORK
    edge_pcm=ebuild.audio(edge['runs'],egroups)
    home_speech=json.loads((H/'dialogue-source.json').read_text())
    hshots,hruns,hgroups=hbuild.timeline(home,home_speech)
    # The builders use a common scratch filename; preserve the first complete mix.
    edge_pcm.rename(WORK/'edge-mix.f32le')
    home_pcm,_=hbuild.audio_mix(home_source,2,Path(hh['music']['path']).expanduser(),2.4,hruns,hgroups,1152,WORK)
    home_pcm.rename(WORK/'home-mix.f32le')
    shots=[]
    for s in edge['shots']:
        shots.append((edge_source,s['in'],s['end_frame']-s['start_frame']))
    for s in hshots:
        shots.append((home_source,s['in'],s['end_frame']-s['start_frame']))
    assert sum(x[2] for x in shots[:len(edge['shots'])])==1152
    assert sum(x[2] for x in shots[len(edge['shots']):])==1152
    contract={'purpose':'User review; two accepted trailer edits assembled horizontally','edits':[{'handoff':str(E/'compilation-handoff.json'),'sha256':sha(E/'compilation-handoff.json')},{'handoff':str(H/'compilation-handoff.json'),'sha256':sha(H/'compilation-handoff.json')}], 'frames':2448,'fps':'24/1','canvas':[1280,720], 'card_frames':72,'duration_seconds':102,'video':'H.264 yuv420p CRF 18, BT.709, source picture fit within 16:9','audio':'Original per-trailer reconstructed mixes, AAC stereo 48 kHz 256k, silent poster cards','subtitle':'English cue maps rebuilt for 16:9, separate SRT and burned captions','output':str(OUT),'status':'READY_TO_RENDER'}
    (EP/'Edit/export-contract-v01.json').write_text(json.dumps(contract,indent=2)+'\n')
    print('Building source-based shots',len(shots),flush=True)
    def render(item):
        i,(source,start,frames)=item; out=WORK/f'shot-{i:03}.mp4'
        run(['ffmpeg','-v','error','-n','-ss',f'{start:.9f}','-i',source,'-an','-vf','fps=24,scale=1280:720:force_original_aspect_ratio=decrease:force_divisible_by=2,pad=1280:720:(ow-iw)/2:(oh-ih)/2:color=black,setsar=1','-frames:v',str(frames),'-c:v','libx264','-preset','ultrafast','-crf','17','-pix_fmt','yuv420p',out]); return out
    with ThreadPoolExecutor(max_workers=3) as pool: files=list(pool.map(render,enumerate(shots)))
    font='/System/Library/Fonts/Supplemental/Arial Bold.ttf'
    for i,(poster,title,year) in enumerate([(Path(eh['poster']['path']),'EDGE OF TOMORROW','2014'),((H/hh['poster']['path']).resolve(),'HOME ALONE','1990')]):
        expected=[eh['poster']['sha256'],hh['poster']['sha256']][i]
        if sha(poster)!=expected: raise RuntimeError('Poster identity mismatch')
        image=Image.new('RGB',(1280,720),'#101621'); draw=ImageDraw.Draw(image)
        pic=Image.open(poster).convert('RGB'); pic.thumbnail((310,535)); image.paste(pic,(120+(310-pic.width)//2,(720-pic.height)//2))
        draw.text((505,270),title,font=ImageFont.truetype(font,47),fill='#f9efd6',stroke_width=0)
        draw.text((508,345),year,font=ImageFont.truetype(font,31),fill='#e6ae58')
        draw.text((508,412),'SCENES ON REPEAT',font=ImageFont.truetype(font,22),fill='#aeb9c5')
        p=WORK/f'card-{i}.png'; image.save(p)
        run(['ffmpeg','-v','error','-n','-loop','1','-framerate','24','-i',p,'-frames:v','72','-c:v','libx264','-preset','ultrafast','-crf','17','-pix_fmt','yuv420p',WORK/f'card-{i}.mp4'])
    ne=len(edge['shots']); ordered=files[:ne]+[WORK/'card-0.mp4']+files[ne:]+[WORK/'card-1.mp4']
    (WORK/'list.txt').write_text(''.join(f"file '{p.as_posix()}'\n" for p in ordered))
    cues=[]
    for g in egroups: cues.append((g[0]['start'],g[-1]['end']+.08,' '.join(w['text'] for w in g)))
    for g in hgroups: cues.append((51+g[0]['start'],51+g[-1]['end']+.08,' '.join(w['text'] for w in g)))
    header='[Script Info]\nScriptType: v4.00+\nPlayResX: 1280\nPlayResY: 720\n[V4+ Styles]\nFormat: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding\nStyle: Default,Arial,36,&H00EAF2F9,&H00FFFFFF,&H0010151B,&H80000000,-1,0,0,0,100,100,0,0,1,2,1,2,100,100,40,1\n[Events]\nFormat: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text\n'
    (WORK/'captions.ass').write_text(header+''.join(f'Dialogue: 0,{ass_time(a)},{ass_time(b)},Default,,0,0,0,,{text}\n' for a,b,text in cues))
    def srt_time(t):
        m=round(t*1000);return f'{m//3600000:02}:{m//60000%60:02}:{m//1000%60:02},{m%1000:03}'
    (EP/'Deliverables/movie-trailers-compilation-v01.en.srt').write_text('\n'.join(f'{i}\n{srt_time(a)} --> {srt_time(b)}\n{text}\n' for i,(a,b,text) in enumerate(cues,1)))
    print('Encoding final compilation',flush=True)
    cmd=['ffmpeg','-v','error','-n','-f','concat','-safe','0','-i',WORK/'list.txt','-f','f32le','-ar','48000','-ac','2','-i',WORK/'edge-mix.f32le','-f','f32le','-ar','48000','-ac','2','-i',WORK/'home-mix.f32le','-filter_complex',f"[0:v]ass={WORK/'captions.ass'}[v];anullsrc=r=48000:cl=stereo:d=3[s0];anullsrc=r=48000:cl=stereo:d=3[s1];[1:a][s0][2:a][s1]concat=n=4:v=0:a=1[a]",'-map','[v]','-map','[a]','-frames:v','2448','-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p','-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709','-c:a','aac','-b:a','256k','-movflags','+faststart',OUT]
    (EP/'Edit/render-command.json').write_text(json.dumps([str(x) for x in cmd],indent=2)+'\n')
    run(cmd)
    print('DONE',OUT,sha(OUT),flush=True)

if __name__=='__main__': main()
