import json, sys
from pathlib import Path
E=Path('/Users/diplomat/ytvideos/new_channel/videos/032_galveston_1900')
sys.path.insert(0,str(E/'Edit/ChurchDemo_v01'))
from palmier_client import call
P='25533909'; T='6545DD44'; C='63CEB173'
target=E/'Assets/Generated/ship-camera-v01/ship_camera_g08.mp4'
record=E/'Work/subtitles-final-v01/ship-camera/apply_receipt.json'
assert not record.exists()
before=call('get_timeline',{'projectId':P,'timelineId':T},'ship_target_before_swap')
clip=next(c for t in before['tracks'] for c in t['clips'] if c['id']==C)
assert clip['mediaRef']=='B1682F49' and clip['frames']==[738,858]
snap=call('manage_snapshots',{'projectId':P,'timelineId':T,'action':'save','name':'Before ship camera-only correction'},'ship_swap_snapshot')
asset=call('import_media',{'projectId':P,'source':{'path':str(target)},'name':'R007 camera only G08'},'ship_import')
print('IMPORTED',json.dumps(asset),flush=True)
record.write_text(json.dumps({'phase':'imported','snapshot':snap,'asset':asset},indent=2))
ref=asset['mediaRef']
media=call('get_media',{'projectId':P,'ids':[ref]},'ship_import_check')
record.write_text(json.dumps({'phase':'swapping','snapshot':snap,'asset':asset,'media':media},indent=2))
result=call('swap_clip_media',{'projectId':P,'timelineId':T,'clipId':C,'mediaRef':ref},'ship_swap')
after=call('get_timeline',{'projectId':P,'timelineId':T},'ship_target_after_swap')
changed=next(c for t in after['tracks'] for c in t['clips'] if c['id']==C)
assert changed['mediaRef']==ref and changed['frames']==[738,858] and changed.get('trimEndFrame')==2
record.write_text(json.dumps({'phase':'verified','snapshot':snap,'asset':asset,'media':media,'swap':result,'clip':changed,'source_static_image':str(E/'Source/Images/paper_v01/scene_007_v01.png'),'method':'static image, camera and G08 only; no depth/parallax','visual_trajectory_samples':[0,30,60,90,119]},indent=2))
print('VERIFIED',json.dumps(changed),flush=True)
