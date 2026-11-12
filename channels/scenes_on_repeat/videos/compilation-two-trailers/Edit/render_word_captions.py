import argparse, hashlib, importlib.util, json, math, subprocess, sys
from pathlib import Path
from PIL import Image

EP=Path('/Users/diplomat/ytvideos/channels/scenes_on_repeat/videos/compilation-two-trailers')
ROOT=Path('/Users/diplomat/ytvideos')
OTHER=Path('/Users/diplomat/.codex/worktrees/ad59/ytvideos/channels/scenes_on_repeat/videos')
E=OTHER/'edge-of-tomorrow-2014/Edit/trailer-v03'
H=OTHER/'home-alone-1990/Edit/trailer-v02'
WORK=EP/'Work/v01'
SRC=EP/'Deliverables/movie-trailers-compilation-v02.mp4'
OUT=EP/'Deliverables/movie-trailers-compilation-v03.mp4'
sys.path[:0]=[str(ROOT/'channels/scenes_on_repeat/automation/pipeline')]
from long_captions import prepare

def digest(p):
    h=hashlib.sha256()
    with open(p,'rb') as f:
        for b in iter(lambda:f.read(4*1024*1024),b''): h.update(b)
    return h.hexdigest()

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--font',default='/System/Library/Fonts/Avenir Next.ttc');parser.add_argument('--font-index',type=int,default=0);parser.add_argument('--prepare-only',action='store_true');args=parser.parse_args()
    if digest(SRC)!='14cc2b9e0987f9028060682c4975d0259508d5cc7f7d299231d6f59d1116a4c4': raise ValueError('Accepted v02 source changed')
    for folder in [E,H]:
        h=json.loads((folder/'compilation-handoff.json').read_text())
        if digest(folder/h['timeline'])!=h['timeline_sha256']: raise ValueError('Edit handoff changed')
    eh=json.loads((E/'compilation-handoff.json').read_text());hh=json.loads((H/'compilation-handoff.json').read_text())
    if digest(E/eh['dialogue']['path'])!=eh['dialogue']['sha256'] or digest(H/hh['word_map'])!=hh['word_map_sha256']: raise ValueError('Word map identity changed')
    e=json.loads((E/'dialogue.json').read_text())['words']
    home=json.loads((H/'dialogue-final.json').read_text())['word_groups']
    hw=[{'text':v['text'],'start':v['start']+51,'end':v['end']+51} for g in home for v in g]
    caption_dir=EP/'Work/v03/captions'; caption_dir.mkdir(parents=True,exist_ok=True)
    plan=prepare([{'end':48,'words':e},{'end':99,'words':hw}],caption_dir,fps=24,width=1280,height=720,font_path=args.font,font_index=args.font_index,font_size=42)
    words=[w for g in plan['groups'] for w in g['words']]
    assert [w['text'] for w in words]==[w['text'] for w in e]+[w['text'] for w in hw]
    print(f"Prepared {len(words)} words in {len(plan['groups'])} groups; warnings: {plan['boundary_warnings']}",flush=True)
    if args.prepare_only:return
    if OUT.exists(): raise RuntimeError('Output already exists')
    (EP/'Edit/export-contract-v03.json').write_text(json.dumps({'source_v02':str(SRC),'source_sha256':digest(SRC),'purpose':'Local user review, subtitle style revision','canvas':[1280,720],'fps':'24/1','frames':2448,'audio':'AAC stream copy from v02, no change','subtitle_plan':str(caption_dir/'caption-map.json'),'subtitle_plan_sha256':digest(caption_dir/'caption-map.json'),'font':args.font,'font_index':args.font_index,'red':'#FF302A','output':str(OUT)},indent=2)+'\n')
    band=plan['band_height']; blank=Image.new('RGBA',(1280,band)).tobytes();cache={}
    for g in plan['groups']:
        for st in g['states']:cache[st['path']]=Image.open(st['path']).convert('RGBA').tobytes()
    cmd=['ffmpeg','-v','error','-n','-f','concat','-safe','0','-i',str(WORK/'list.txt'),'-i',str(SRC),'-f','rawvideo','-pixel_format','rgba','-video_size',f'1280x{band}','-framerate','24','-i','pipe:0','-filter_complex',f'[0:v]setpts=N/(24*TB)[base];[base][2:v]overlay=0:560:shortest=1:format=auto,format=yuv420p[v]','-map','[v]','-map','1:a:0','-frames:v','2448','-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p','-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709','-c:a','copy','-movflags','+faststart',str(OUT)]
    (EP/'Edit/render-command-v03.json').write_text(json.dumps(cmd,indent=2)+'\n')
    with open(EP/'Work/v03/render.log','wb') as log:
        proc=subprocess.Popen(cmd,stdin=subprocess.PIPE,stdout=subprocess.DEVNULL,stderr=log)
        try:
            for frame in range(2448):
                active=next((g for g in plan['groups'] if g['start_frame']<=frame<g['end_frame']),None)
                states=[s for s in active['states'] if s['frame']<=frame] if active else []
                proc.stdin.write(cache[states[-1]['path']] if states else blank)
        finally:proc.stdin.close()
        status=proc.wait()
    if status:raise RuntimeError((EP/'Work/v03/render.log').read_text())
    print('RENDERED',OUT,digest(OUT),flush=True)
if __name__=='__main__':main()
