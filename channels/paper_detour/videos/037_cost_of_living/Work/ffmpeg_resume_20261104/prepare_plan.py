import json, pathlib, math
p=pathlib.Path(__file__).resolve().parents[1].parent
w=pathlib.Path(__file__).resolve().parent
old=json.loads((p/'Edit/Timeline/timing_map_v01.json').read_text())
N=10320
scenes=[]; start=0; prior=None
for i,s in enumerate(old['scenes']):
 remaining=72-i
 if remaining==0: end=N
 else:
  target=round(s['end_frame']/1.1)
  lo=max(start+120,N-remaining*180); hi=min(start+180,N-remaining*120)
  end=max(lo,min(hi,target))
 motion=s['motion']
 if motion==prior:
  motion={'push-in':'pan-right','pull-out':'pan-left','pan-right':'push-in','pan-left':'pull-out'}[motion]
 motionmap={'push-in':('none','in'),'pull-out':('none','out'),'pan-right':('left_to_right','none'),'pan-left':('right_to_left','none')}
 dr,zoom=motionmap[motion]
 image=p/'Source/Images/paper_v01'/s['filename']
 if not image.exists(): raise Exception(str(image))
 scenes.append({'image':str(image),'start_frame':start,'end_frame':end,'direction':dr,'zoom':zoom})
 start=end; prior=motion
plan={'channel':'paper','format':'long','audio':str(w/'voice_110.wav'),'audio_contract':{'final_audio_sha256':'3c4129bc2fc7d4e7d7f4a21f8eff796693dbc779bddc083f45aec4a558eb5744','applied_speed':1.1,'speed_evidence':str(w/'STATUS.md')},'scenes':scenes,'subtitles':{'mode':'words','words':str(w/'word_times_provisional.json'),'transcript':str(p/'Source/Voice/en_v01_lawrence/voice_text_en.txt')}}
(w/'plan_draft.json').write_text(json.dumps(plan,indent=2)+'\n')
print('scenes',len(scenes),'frame durations',min(s['end_frame']-s['start_frame'] for s in scenes),max(s['end_frame']-s['start_frame'] for s in scenes),'total',start)
