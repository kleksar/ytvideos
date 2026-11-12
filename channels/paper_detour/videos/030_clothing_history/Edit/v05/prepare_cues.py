from pathlib import Path
from PIL import Image,ImageOps
import json,shutil
p=Path('/Users/diplomat/ytvideos/channels/paper_detour/videos/030_clothing_history');g=p/'Source/Graphics/v05'
base=Path('/Users/diplomat/.codex/generated_images/01a1981d-a870-7112-8979-ccd0e34cc760')
shutil.copy2(base/'exec-bf831d6b-7f02-4181-8bdb-32720fdae79e.png',g/'C04b_raw.png');shutil.copy2(base/'exec-ec71d15e-b531-4adf-a35d-565eff06d8dd.png',g/'C05b_raw.png')
museum=p/'Source/Images/v05/44_future_museum.png';shutil.copy2(base/'exec-d0fab31c-492c-45c8-8bd5-37e89e29d1be.png',museum)
shots=json.loads((p/'Storyboard/SHOTLIST_v05.json').read_text())
for sh in shots:
 if sh['id'] not in ['V35','V36']:continue
 sh['path']=str(museum);sh['source_scene']='S44';im=Image.open(museum).convert('RGB');w,h=im.size;z=sh['zoom'];cw,ch=w/z,h/z
 im=im.crop((round((w-cw)/2),round((h-ch)/2),round((w+cw)/2),round((h+ch)/2)))
 ImageOps.fit(im,(1920,1080),method=Image.Resampling.LANCZOS).save(sh['framed_path'])
(p/'Storyboard/SHOTLIST_v05.json').write_text(json.dumps(shots,ensure_ascii=False,indent=2))
rows=[('C01',['WHERE ARE THEIR','CLOTHES?'],'V01','primary',1.68,4.32,'Where are their clothes?'),('C02',['ONE SMALL CLUE'],'V08','primary',34.48,37.55,'Here’s a tiny sandal, woven from esparto grass.'),('C03',['YOUR PICK?'],'V22','primary',103.44,104.9,'Which would you choose?'),('C04',['DRESSED TO','IMPRESS'],'V25','alternate',115.71,119.15,"You wouldn't exactly blend into the background wearing either of these."),('C05',['FUTURE','ARTIFACTS'],'V35','primary',163.6,169.1,"Picture a museum in the future. Behind the glass: our sneakers, a jacket, someone's favorite T-shirt."),('C06',['WHAT WILL','THEY FIND?'],'V39','primary',186.0,190.0,'What will they find after us?')]
cues=[];pairs=[];cue_sheet=[]
for cid,lines,scene,anchor,start,end,trigger in rows:
 file=g/(cid+('b' if cid in ['C04','C05'] else '')+'_raw.png')
 cues.append({'id':cid,'lines':lines,'backend':{'type':'existingPNG','path':str(file),'face':{'mode':'creamOrange'},'reference':str(Path('/Users/diplomat/ytvideos/channels/paper_detour/videos/001_radio_game/Source/Images/accent_typography_v2/A_MESSAGE.png')),'status':'Author visually checked exact wording, paper texture and reference shape; no independent review'},'provenance':{'method':'built-in imagegen','record':str(p/'Storyboard/DECISIONS_v05.md')},'timing':{'status':'measured alignment; audible sync UNVERIFIED','startFrame':round(start*30),'endFrame':round(end*30)}})
 pairs.append({'scene':scene,'cue':cid,'anchor':anchor})
 cue_sheet.append({'id':cid,'lines':lines,'scene':scene,'anchor':anchor,'startFrame':round(start*30),'endFrame':round(end*30),'spoken_trigger_end':trigger,'source':'Lawrence v05 character/word alignment; end includes readability hold, final includes tail','listening':'UNVERIFIED','motion':'4-frame enter/fade, constant optical scale, 4-frame exit/fade; final remains through last frame','decision_record':'Storyboard/DECISIONS_v05.md'})
manifest={'version':1,'canvas':[1920,1080],'face_height_px':76,'min_face_height_px':70,'anchors':{'primary':{'center':[0.5,0.12],'max_width_px':1560,'max_height_px':240},'alternate':{'center':[0.23,0.2],'max_width_px':720,'max_height_px':240}},'scenes':[{'id':s['id'],'path':s['framed_path']} for s in shots],'cues':cues,'pairs':pairs}
(g/'caption_input.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2));(p/'Storyboard/CUE_SHEET_v05.json').write_text(json.dumps(cue_sheet,ensure_ascii=False,indent=2))
