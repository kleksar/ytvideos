"""Build the five complete music timelines around the accepted excerpt edits."""
from pathlib import Path
import collections
import hashlib
import json
import math
import re
import subprocess
import sys
import wave

import numpy as np

edit = Path(__file__).resolve().parent
batch = edit.parent
repo = batch.parents[1]
sys.path.insert(0, str(repo/'automation'))
from music_montage import accent_signal, candidate_accents, select_rhythm

NAMES = ('mthu','super-funk','bloodstream','bow-bow-bow','paparazzi')
FPS = 30
WIDTH, HEIGHT = 1440, 2560
run = batch/'Work/full-song-v01'
run.mkdir(exist_ok=True)

def read(path):
    return json.loads(Path(path).read_text())

def write(path, data):
    temp = path.with_suffix('.tmp')
    temp.write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n')
    temp.replace(path)

def sha(path):
    with Path(path).open('rb') as f:
        digest = hashlib.sha256()
        for chunk in iter(lambda: f.read(1024*1024),b''):
            digest.update(chunk)
        return digest.hexdigest()

def track(name):
    spec=read(edit/f'{name}-hold-input.json')
    prior=read(edit/f"{name}-review-{spec['new_revision']}-contract.json")
    wav=run/f'{name}.wav'
    if not wav.exists():
        temp=wav.with_suffix('.partial.wav')
        subprocess.run(['ffmpeg','-nostdin','-v','error','-y','-i',prior['source'],'-map','0:a:0',
                        '-ac','2','-ar','44100','-c:a','pcm_s16le',temp],check=True)
        temp.replace(wav)
    with wave.open(str(wav)) as f:
        samples=f.getnframes()
    return spec,prior,wav,samples

def peaks(wav,pulse,offset):
    t,s=accent_signal(wav)
    result={}
    for idx in range(1,len(t)-1):
        if s[idx]>=.035 and s[idx]>=s[idx-1] and s[idx]>s[idx+1]:
            frame=round(t[idx]*FPS)
            row=dict(frame=frame,attack_seconds=round(float(t[idx]),6),strength=round(float(s[idx]),4))
            if frame not in result or row['strength']>result[frame]['strength']:
                result[frame]=row
    if pulse:
        for n,row in candidate_accents(t,s,FPS,[pulse[0],(pulse[1]+offset)%pulse[0]]).items():
            result[n]={**row,'pulse':True}
    return result

def anchor(events,target):
    viable=[row for n,row in events.items() if abs(n-target)<=8]
    if not viable:
        viable=[row for n,row in events.items() if abs(n-target)<=24]
    return max(viable,key=lambda a:min(4,a['strength'])+.35*a.get('pulse',False)-.21*abs(a['frame']-target)) if viable else None

def region(events,left,right,pattern,minlen,maxlen):
    if right-left<1: return []
    local={n-left:{**a,'frame':n-left,'strength':a['strength']+.35*a.get('pulse',False)}
           for n,a in events.items() if left<n<right and a['strength']>=.50}
    bounds=dict(holds=pattern,min=min(minlen,(right-left)/FPS),max=maxlen,opening_max=maxlen)
    try:
        selected=select_rhythm(local,right-left,FPS,bounds)
    except ValueError:
        local={n-left:{**a,'frame':n-left} for n,a in events.items() if left<n<right}
        selected=select_rhythm(local,right-left,FPS,{**bounds,'min':min(.3,(right-left)/FPS),'max':maxlen+.8,'opening_max':maxlen+.8})
    return [events[a['frame']+left] for a in selected]

# Favor the established cadence inside the accepted passage and alternate shorter and longer
# phrases elsewhere. Each complete take has one source only, across all five videos.
CADENCE={
 'mthu':([1.75,2.35,2.0,2.50],.85,3.65),
 'super-funk':([1.65,2.10,1.55,2.35,2.55],.65,3.55),
 'bloodstream':([2.75,3.40,2.40,3.80],1.2,4.65),
 'bow-bow-bow':([2.2,2.95,1.65,2.35,3.35],.85,4.25),
 'paparazzi':([2.7,3.70,3.25,2.45,3.80],1.2,4.7),
}

def keywords(name):
    if name=='bow-bow-bow':
        return ('night','neon','club','party','city','street','dance','dj','concert','urban','bar','crowd','rave','skate')
    if name=='super-funk':
        return ('abstract','ink','liquid','fire','smoke','wave','laser','color','water','macro','city','light','bubble')
    if name=='mthu':
        return ('macro','insect','animal','wildlife','snail','bee','butterfly','forest','bird','leaf','jellyfish','turtle','squirrel','crab')
    if name=='bloodstream':
        return ('aerial','drone','mountain','waterfall','canyon','coast','landscape','river','forest','volcano','cliff','desert')
    return ('calm','sunset','aerial','mountain','landscape','coast','sunrise','fog','lake','snow','countryside','cloud','field')

def scale_of(url):
    if any(k in url for k in ('macro','close-up','leaf','insect','liquid','bubble','spark','dew')): return 'close'
    if any(k in url for k in ('aerial','landscape','drone','panoramic','timelapse')): return 'wide'
    return 'medium'

def subject_of(url):
    return next((k for k in ('butterfly','waterfall','mountain','forest','nightclub','street','sunset','coast','ocean','fog','river','ink','fire','lake','snow','dance','liquid','crowd') if k in url),url.split('/')[-2].split('-')[0])

def pick(name,needed,stock,used,previous,source_cursor):
    options=[]
    for row in stock:
        if row['id'] in used or row['duration']<needed+.08: continue
        own=name in row['groups']
        relevance=sum(k in row['page'] for k in keywords(name))
        if not own and (relevance<2 or name in ('bow-bow-bow','mthu')): continue
        scale=scale_of(row['page'])
        subject=subject_of(row['page'])
        if row['id'] in source_cursor: continue
        width,height=row['dimensions']
        recent=previous[-4:]
        score=(3.2*own + .28*min(relevance,4) + .45*(height>=width)
               + .36*(not recent or recent[-1].get('scale')!=scale)
               - .55*sum(x.get('subject')==subject for x in recent))
        # Short shots use the short takes first, preserving options for long holds.
        score-=.10*max(0,row['duration']-needed)
        score+=int(hashlib.blake2s(f"{name}:{len(previous)}:{row['id']}".encode(),digest_size=2).hexdigest(),16)/65535*.55
        options.append((score,row['id'],row,scale,subject))
    if not options:
        raise ValueError(f'{name}: no unused {needed:.2f}s matching take at slot {len(previous)+1}')
    _,sid,row,scale,subject=max(options)
    used.add(sid)
    headroom=row['duration']-needed-.08
    offset=round(min(.6,max(0,headroom*.3)),3)
    return dict(id=sid,path=row['path'],source_in=offset,max_seconds=row['duration']-offset,
                pre_crop='',scale=scale,subject=subject,sha256=row['sha256'],source_page=row['page'])

def words_for(name,spec,prior,total_frames):
    asr=edit/f'{name}-full-song-asr.json'
    isolated=edit/f'{name}-full-song-isolated-asr.json'
    segments=read(isolated if isolated.exists() else asr)
    trusted=read(spec['caption_source_words'])['words']
    left=prior['offset']
    right=left+prior['frames']/FPS
    outside=[]
    for seg in segments:
        for item in seg['words']:
            if not re.search(r'[^\W\d_]',item['text']) or item['end_seconds']<=item['start_seconds']: continue
            item=dict(item)
            item['text']=re.sub(r'(.)\1{7,}',r'\1'*4,item['text'],flags=re.I)
            item.pop('p',None)
            if item['end_seconds']<=left+.02 or item['start_seconds']>=right-.01:
                outside.append(item)
    accepted=[w for w in trusted if w['start_seconds']<right and w['end_seconds']>left]
    if accepted:
        outside=[w for w in outside if not (w['start_seconds']<accepted[-1]['end_seconds'] and w['end_seconds']>accepted[0]['start_seconds'])]
    sequence=sorted(outside+accepted,key=lambda w:w['start_seconds'])
    words=[]
    prev_frame=-1
    for entry in sequence:
        row=dict(entry)
        start=max(0,row['start_seconds'])
        frame=math.ceil(start*FPS-1e-9)
        if frame<=prev_frame:
            frame=prev_frame+1
            start=frame/FPS
        if frame>=total_frames: continue
        end=min(total_frames/FPS,max(row['end_seconds'],(frame+1)/FPS))
        row.update(start_seconds=start,end_seconds=end)
        words.append(row)
        prev_frame=frame
    if not words: raise ValueError('No vocal caption timings')
    return dict(words=words,method='Local ASR with retained reviewed word timing across the approved passage',
                analysis=str(isolated if isolated.exists() else asr),approved_source_words=spec['caption_source_words'])

def main():
    only=set(sys.argv[1:])
    manifest=read(batch/'Source/Footage/full-song-stock/manifest.json')
    stock=[x for x in manifest if 'path' in x]
    prior_ids={str(clip['source_id']).removeprefix('pexels:') for item in read(edit/'FRAGMENTS.json')['exports'] for clip in item['video']}
    used=set(prior_ids)
    for name in NAMES:
        path=edit/f'{name}-full-song-v01-contract.json'
        if path.exists() and (not only or name not in only):
            used.update(str(c['id']) for c in read(path)['clips'])
    for name in NAMES:
        path=edit/f'{name}-full-song-v01-contract.json'
        if only and name not in only: continue
        if path.exists(): continue
        spec,prior,wav,samples=track(name)
        frames=math.ceil(samples*FPS/44100)
        events=peaks(wav,spec.get('pulse'),prior['offset'])
        origin=round(prior['offset']*FPS)
        anchors={n:a for n,a in events.items() if a['strength']>=.32}
        start_mark=anchor(anchors,origin)
        end_mark=anchor(anchors,origin+prior['frames'])
        start=start_mark['frame'] if start_mark else 0
        end=end_mark['frame'] if end_mark else frames
        approved=[]
        for old in prior['accents']:
            n=origin+old['frame']
            local=[row for k,row in events.items() if abs(k-n)<=1]
            if local:
                mark=min(local,key=lambda a:(abs(a['frame']-n),-a['strength']))
            else:
                mark={**old,'frame':n,'attack_seconds':round(old['attack_seconds']+prior['offset'],6)}
            approved.append(mark)
        assert start<approved[0]['frame'] and approved[-1]['frame']<end
        pattern,lower,upper=CADENCE[name]
        for factor in (1,1.13,1.27,1.42,1.56):
            try:
                before=region(events,0,start,[v*factor for v in pattern],lower,upper*factor)
                after=region(events,end,frames,[v*factor for v in pattern],lower,upper*factor)
            except ValueError as exc:
                print(name,exc,flush=True)
                continue
            cuts=[*before,*([start_mark] if start_mark else []),*approved,*([end_mark] if end_mark else []),*after]
            marks=[0,*[m['frame'] for m in cuts],frames]
            first_index=len(before)+int(start_mark is not None)
            last_index=first_index+len(prior['clips'])
            trial=used.copy()
            clips=[]
            try:
                for i,(a,b) in enumerate(zip(marks,marks[1:])):
                    seconds=(b-a+(1 if i else 0)+(2 if b<frames else 0))/FPS
                    if first_index<=i<last_index:
                        old=dict(prior['clips'][i-first_index])
                        if i==first_index:
                            old['source_in']=max(0,round(old['source_in']+(a-origin)/FPS,6))
                        old['approved_excerpt']=True
                        clips.append(old)
                    else:
                        clips.append(pick(name,seconds,stock,trial,clips,prior_ids))
            except ValueError as e:
                print(str(e),flush=True)
                continue
            used=trial
            break
        else:
            raise RuntimeError(f'{name}: stock pool is too short')
        words=words_for(name,spec,prior,frames)
        prefix=edit/f'{name}-full-song-v01'
        word_path=prefix.with_name(prefix.name+'-words.json')
        write(word_path,words)
        output=batch/'Deliverables'/f"{prior['title']}-full-v01.mp4"
        old_caption=read(Path(prior['mask']).with_name(Path(prior['mask']).name.replace('-mask.mov','-caption-plan.json')))
        write(path,dict(title=prior['title'],name=name,source=prior['source'],source_sha256=sha(prior['source']),
            wav=str(wav),pcm_sha256=sha(wav),samples=samples,sample_rate=44100,offset=0,fps=FPS,
            frames=frames,dimensions=[WIDTH,HEIGHT],output=str(output),clips=clips,
            transition_centres=marks[1:-1],accents=cuts,caption_beats=list(events.values()),
            transition_seconds=.1,words=str(word_path),font_size=old_caption['font_size_px'],
            motion_seed=old_caption['line_motion']['seed'],tilt_every=old_caption['line_motion']['tilt_every'],
            approved_review=prior['output'],approved_excerpt_source_seconds=[prior['offset'],prior['offset']+prior['frames']/FPS],
            video={'codec':'h264','profile':'high','pixel_format':'yuv420p','color_space':'bt709','range':'tv','rate_control':'libx264 CRF 18, superfast','fps':'30/1'},
            audio={'codec':'aac','sample_rate':44100,'channels':2,'bitrate':256000,'source_decoded_in_samples':0,'source_decoded_out_samples':samples}))
        print(name,round(samples/44100,3),len(clips),len(words['words']),flush=True)

if __name__=='__main__':
    main()
