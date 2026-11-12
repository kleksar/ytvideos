#!/usr/bin/env python3
"""Build a new trial mix with one non-looped recorded sound per specified cue.
Usage: python3 make_short02_single_sfx.py cue_file.json unique_output_basename
Cue file: {"events":[{"visual_frame":N,"source":"book-page-02.wav",
                      "source_trim_s":0.10,"start_frame":N-1,
                      "duration_frames":18,"gain_db":-27}]}
Event placement is provisional until checked against the actual composited frames
and listened to alongside the voice.  Never use a previous compressed MP4 as base.
"""
import json, math, pathlib, subprocess, sys
import numpy as np

ROOT=pathlib.Path('/Users/diplomat/ytvideos/channels/paper_detour/videos/001_radio_game')
OUT=ROOT/'Shorts/02_decoder/Source/Audio/Director_trial_20261031'
SOURCE=ROOT/'Source/Audio/paper_motion_cc0_20261030'
BASE=OUT/'preview_mix_36p6_no_sfx_stereo.wav'
RATE=44100
FPS=30
TOTAL=round(36.6*RATE)
if len(sys.argv)!=3: raise SystemExit(__doc__)
config=pathlib.Path(sys.argv[1]); prefix=sys.argv[2]
if not prefix or pathlib.Path(prefix).name!=prefix:raise ValueError('invalid prefix')
outpaths=[OUT/(prefix+'_mix.wav'),OUT/(prefix+'_sfx.wav'),OUT/(prefix+'_receipt.json')]
if any(p.exists() for p in outpaths):raise FileExistsError('Refuse overwrite')
def load(path):
 raw=subprocess.run(['ffmpeg','-v','error','-i',str(path),'-f','f32le','-ac','2','-ar',str(RATE),'-'],stdout=subprocess.PIPE,check=True).stdout
 return np.frombuffer(raw,dtype='<f4').reshape(-1,2).copy()
def encode(path,data):
 subprocess.run(['ffmpeg','-v','error','-f','f32le','-ar',str(RATE),'-ac','2','-i','-','-c:a','pcm_s24le','-n',str(path)],input=data.astype('<f4').tobytes(),check=True)
base=load(BASE)
if len(base)!=TOTAL:raise ValueError('Unexpected base length')
raw=json.loads(config.read_text());events=raw['events']
if not events:raise ValueError('At least one event required')
effects=np.zeros_like(base);sources={};receipt=[]
for event in events:
 name=event['source']
 if name not in ('book-page-01.wav','book-page-02.wav'):raise ValueError('unsupported SFX source')
 if name not in sources:sources[name]=load(SOURCE/name)
 start=int(event['start_frame']);frames=int(event.get('duration_frames',18));trim=float(event.get('source_trim_s',0.10));gain=float(event.get('gain_db',-27));visual=int(event['visual_frame'])
 if not 0<=start<1098 or frames<1 or not -60<=gain<=0:raise ValueError('invalid event')
 a=round(start*RATE/FPS);count=min(round(frames*RATE/FPS),TOTAL-a);offset=round(trim*RATE);seg=sources[name][offset:offset+count].copy()
 if len(seg)<count:raise ValueError('event exceeds source duration')
 # One original gesture, a 1-frame fade-in and 5-frame fade-out as used in long film.
 fi=min(len(seg),round(RATE/FPS));fo=min(len(seg),round(5*RATE/FPS))
 seg[:fi]*=np.linspace(0,1,fi,dtype=np.float32)[:,None]
 seg[-fo:]*=np.linspace(1,0,fo,dtype=np.float32)[:,None]
 effects[a:a+count]+=seg*(10**(gain/20))
 receipt.append({'label':event.get('label',''),'source':str(SOURCE/name),'source_trim_s':trim,'timeline_start_frame':start,'timeline_end_frame_exclusive':start+frames,'visual_frame_expected':visual,'gain_db':gain,'fade_in_frames':1,'fade_out_frames':5})
mix=base+effects;peak=float(np.max(np.abs(mix)))
if peak>=1:raise ValueError('Mix exceeds digital full scale')
encode(outpaths[0],mix);encode(outpaths[1],effects)
info={'base':str(BASE),'fps':FPS,'sample_rate':RATE,'duration_s':36.6,'method':'one non-looped source gesture per event; voice and background music unchanged; no normalization','events':receipt,'sample_peak_dbfs':round(20*math.log10(max(peak,1e-12)),2),'listening_performed':False,'timing_warning':'Estimated visual and source onset; validate composited movement and actual listening.'}
outpaths[2].write_text(json.dumps(info,indent=2)+'\n')
print(json.dumps({'mix':str(outpaths[0]),'sfx':str(outpaths[1]),'receipt':str(outpaths[2]),'events':len(receipt),'sample_peak_dbfs':info['sample_peak_dbfs']}))
