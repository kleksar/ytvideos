from pathlib import Path
import json,sys,hashlib,importlib.util
from urllib.parse import quote
sys.path.insert(0,'/Users/diplomat/ytvideos/automation/youtube')
from add_to_playlist import read_items
from google.auth.transport.requests import AuthorizedSession
from google.oauth2.credentials import Credentials
E=Path('/Users/diplomat/ytvideos/channels/paper_detour/videos/032_galveston_1900');D=E/'Packaging/Metadata';r=json.loads((D/'youtube_read_after_v02.json').read_text());m=json.loads((D/'metadata_final_v02.json').read_text());v=r['video'][0];C='UCMVfdfaNxV3ZkI3_J3Eejzw';assert v['snippet']['channelId']==C and v['status']['privacyStatus']=='private';assert v['processingDetails']['processingStatus']=='succeeded';sn=v['snippet'];checks={}
for local,remote in [('title','title'),('description','description'),('category_id','categoryId'),('language','defaultLanguage'),('audio_language','defaultAudioLanguage'),('tags','tags')]:
 actual=sn.get(remote);expected=m[local];checks[local]=(sorted(actual)==sorted(expected) if local=='tags' else actual==expected)
 assert checks[local],local
assert v['status'].get('selfDeclaredMadeForKids',v['status'].get('madeForKids')) is False
synthetic=v['status'].get('containsSyntheticMedia','NOT_RETURNED')
tracks=[x for x in r['captions'] if x.get('snippet',{}).get('language')=='en' and x.get('snippet',{}).get('trackKind','').lower()!='asr'];assert len(tracks)==1;track=tracks[0];assert track['snippet']['status']=='serving' and track['snippet']['isDraft'] is False
vid=v['id'];matches=[x for x in r['playlist_items'] if x['contentDetails']['videoId']==vid];assert len(matches)==1 and r['playlist'][0]['status']['privacyStatus']=='public'
b=json.loads((D/'youtube_before_playlist_v02.json').read_text());before=[x['contentDetails']['videoId'] for x in b['playlist_items']];after=[x['contentDetails']['videoId'] for x in r['playlist_items']];assert after==before+[vid]
credentials=Credentials.from_authorized_user_file('/Users/diplomat/.local/share/story-youtube/paper-detour/manage-token.json')
with AuthorizedSession(credentials) as s:
 ch=read_items(s,'channels',{'part':'id','mine':'true'});assert len(ch)==1 and ch[0]['id']==C
 caps=read_items(s,'captions',{'part':'id,snippet','videoId':vid});assert any(x['id']==track['id'] and x['snippet']['videoId']==vid for x in caps)
 res=s.get('https://www.googleapis.com/youtube/v3/captions/'+quote(track['id'],safe=''),params={'tfmt':'srt'},timeout=60,allow_redirects=False);assert res.status_code==200,('caption_download',res.status_code)
 raw=res.content;(D/'youtube_manual_en_download_v02.srt').write_bytes(raw)
spec=importlib.util.spec_from_file_location('srt_owner','/Users/diplomat/ytvideos/.agents/skills/ytv-srt/scripts/srt_tool.py');owner=importlib.util.module_from_spec(spec);spec.loader.exec_module(owner)
local=owner.parse_srt((E/'Deliverables/032_galveston_en_v02.srt').read_text());remote=owner.parse_srt(raw.decode('utf-8-sig'));assert len(local)==len(remote)
maxdelta=0.
for a,b in zip(local,remote):
 assert owner.canonical(a['text'])==owner.canonical(b['text'])
 for k in ['start_seconds','end_seconds']:maxdelta=max(maxdelta,float(abs(a[k]-b[k])))
assert maxdelta<=.001,maxdelta
receipt={'video_id':vid,'url':'https://www.youtube.com/watch?v='+vid,'channel_id':C,'privacy':'private','processing':'succeeded','metadata_fields':checks,'made_for_kids':False,'contains_synthetic_media_readback':synthetic,'playlist_id':'PLEIDCTZ8y2k8','playlist_privacy':'public','playlist_position':matches[0]['snippet']['position'],'old_order_preserved':True,'caption_id':track['id'],'caption_status':'serving','caption_language':'en','caption_manual_count':1,'caption_download_cue_count':len(remote),'caption_max_time_difference_seconds':maxdelta,'caption_text_matches':True,'thumbnail_visual_check':'PENDING_SEPARATE_LIVE_UI','player_chapter_rendering':'UNVERIFIED_SEPARATE_FROM_DESCRIPTION_READBACK','subjective_listening':'UNVERIFIED'};(D/'release_api_verification_v02.json').write_text(json.dumps(receipt,indent=2));print(json.dumps(receipt,indent=2))
