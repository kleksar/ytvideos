from pathlib import Path
import json,hashlib
EP=Path(__file__).resolve().parents[3];HERE=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
shot=json.loads((HERE/'shotmap_v02.json').read_text())
mix=EP/'Source/Audio/en_v02/mix_en_v02.wav'
words=json.loads((HERE/'word_times_forced_v01.json').read_text())
words.update(audio_sha256=sha(mix),conform={'source_audio_sha256':words['audio_sha256'],'mapping':'identity speech time; unity voice gain, no cuts, no offset, no second speed change; 48000Hz resample and final fractional-frame padding only','audible_sync':'UNVERIFIED','punctuation_note':'Standalone em dash has a forced-alignment display interval, not an asserted audible word.'})
(HERE/'word_times_mix_v02.json').write_text(json.dumps(words,indent=2)+'\n')
old={6:5,17:19,18:20,35:41,37:44};hosts={1:'host_opening',9:'host_diagnostic',28:'host_memory_obstacle'}
spaces={2,3,4,5,10,13,14,44};recons={22,33,40}
# Explicit subject-based camera decisions, recorded after full-frame source review.
decisions={
1:('in',[.76,.34],'Traveler opening the question; preserve the left explanatory model.'),
2:('right_to_left',[.67,.40],'Follow the craft away from the small Earth while retaining the full boom.'),
3:('in',[.72,.46],'Bring attention from Jupiter to the complete craft.'),
4:('out',[.40,.44],'Open the space around Voyager as Saturn recedes.'),
5:('left_to_right',[.64,.44],'Carry attention from abstract message marks toward the intact dish.'),
6:('in',[.65,.42],'Concentrate on the engineer and unreadable monitor.'),
7:('out',[.5,.45],'Keep both endpoints and the surviving command route visible.'),
8:('in',[.5,.47],'Focus on the two unreadable data channels.'),
9:('out',[.30,.35],'Give the questioning guide and isolated computer concept room.'),
10:('in',[.77,.45],'Very gently draw attention across the enormous empty span to the craft.'),
11:('out',[.55,.46],'Reveal the relation between the solar region and Voyager beyond it.'),
12:('in',[.48,.46],'Concentrate on the wind and field explanation without cropping labels.'),
13:('out',[.68,.44],'Increase surrounding darkness beyond the faint conceptual boundary.'),
14:('in',[.43,.43],'Examine the isolated intact hardware that cannot be reached.'),
15:('right_to_left',[.50,.45],'Follow the outgoing command direction toward Voyager.'),
16:('left_to_right',[.50,.45],'Follow the returning reply toward Earth.'),
17:('in',[.38,.40],'Concentrate on the waiting engineer.'),
18:('out',[.51,.42],'Open from the monitor to the two engineers discussing the problem.'),
19:('in',[.70,.45],'Bring attention to the separate functional computer block.'),
20:('out',[.54,.46],'Reveal both inputs and the outgoing message function.'),
21:('right_to_left',[.50,.45],'Follow the diagnostic command from Earth toward the craft.'),
22:('in',[.69,.35],'Concentrate on the newly decoded abstract screen region.'),
23:('out',[.50,.43],'Expose the complete conceptual memory field.'),
24:('in',[.70,.41],'Bring attention to the changed cells in the comparison.'),
25:('out',[.65,.36],'Show three damaged portions within the whole percentage grid.'),
26:('in',[.65,.36],'Hold attention on the unchanged damaged area.'),
27:('out',[.50,.48],'Reveal the long instruction block and separate intact spaces.'),
28:('in',[.31,.34],'Focus on the guide measuring gaps too small for the whole program.'),
29:('out',[.50,.55],'Present all three conceptual fragments in separate locations.'),
30:('in',[.50,.45],'Bring attention to references that need updating.'),
31:('out',[.50,.52],'Reveal all fragments and their renewed connections.'),
32:('in',[.30,.46],'Give priority to spacecraft status while retaining science as the next step.'),
33:('out',[.38,.35],'Open from the engineer to the still dim monitor, before success.'),
34:('right_to_left',[.50,.45],'Trace the intended status path while retaining the conditional caption.'),
35:('in',[.50,.52],'Concentrate on the hands sending the fix.'),
36:('left_to_right',[.50,.46],'Follow the return leg after showing both directions of the exchange.'),
37:('in',[.66,.39],'Focus on the orderly message region being read.'),
38:('out',[.5,.47],'Reveal the unreadable-to-readable comparison.'),
39:('right_to_left',[.50,.45],'Retain the full route as understandable status reaches Earth.'),
40:('in',[.60,.38],'Bring attention to the engineers returning to scientific information.'),
41:('out',[.56,.45],'Show all four sources joining the returning stream.'),
42:('in',[.65,.36],'Return to the still damaged cells.'),
43:('out',[.50,.52],'Reveal the successful alternative route around the unavailable area.'),
44:('in',[.72,.45],'A barely perceptible approach keeps the small craft present within the final vast space.')}
scenes=[]
for s in shot['scenes']:
 n=int(s['id'][1:]);v2=EP/'Source/Images/v02'
 if n in (17,35):image=v2/(s['id']+'_caption_safe_v01.png')
 elif n in old:image=EP/f'Source/Images/v01/scene_{old[n]:02d}.png'
 elif n in hosts:image=v2/(hosts[n]+'_v01.png')
 elif n in spaces:image=v2/(s['id']+'_space_v01.png')
 elif n in recons:image=v2/(s['id']+'_reconstruction_v01.png')
 else:image=v2/(s['id']+'_diagram_v01.png')
 move,focus,reason=decisions[n]
 if move in ('in','out'):
  direction='none';zoom=move;start={'center':[.5,.5],'scale':1 if move=='in' else 1.025};end={'center':[.5,.5],'scale':1.025 if move=='in' else 1}
 else:
  direction=move;zoom='none';start={'center':[.495 if move=='right_to_left' else .505,.5],'scale':1.025};end={'center':[.505 if move=='right_to_left' else .495,.5],'scale':1.025}
 assert image.is_file(),str(image)
 scenes.append({'id':s['id'],'image':str(image),'start_frame':s['start_frame'],'end_frame':s['end_frame'],'direction':direction,'zoom':zoom,'camera':{'focus':focus,'subject':s['composition'],'reason':reason,'start':start,'end':end}})
plan={'channel':'nuviko','format':'long','fps':30,'canvas':[2560,1440],'source_transfer':'srgb','audio':str(mix),'audio_contract':{'final_audio_sha256':sha(mix),'applied_speed':1.1,'speed_evidence':str(EP/'Source/Audio/en_v02/speed_evidence.md')},'scenes':scenes,'subtitles':{'mode':'words','words':str(HERE/'word_times_mix_v02.json'),'transcript':str(HERE/'transcript_en.txt')}}
existing_path=HERE/'montage_en_v02.json'
if existing_path.exists():
 existing=json.loads(existing_path.read_text())
 for key in ('phrases','keep_together','boundary_exceptions','review'):
  if key in existing['subtitles']:plan['subtitles'][key]=existing['subtitles'][key]
(HERE/'montage_en_v02.json').write_text(json.dumps(plan,indent=2)+'\n')
print('44 scenes, final frame',scenes[-1]['end_frame'])
