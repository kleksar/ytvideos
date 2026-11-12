import json, datetime
from pathlib import Path
from api_inventory import session,get,pages,CHANNEL,BASE,ROOT
D=ROOT/'new_channel/videos/031_jascon4_okene/Packaging/Metadata'
V='zA0kogtqoUs';P='PLEIDCTZ8y2k8';receipt=D/'YOUTUBE_PLAYLIST_RECEIPT_20261102.json'
with session() as s:
 c=get(s,'channels',part='id',mine='true')['items'];assert len(c)==1 and c[0]['id']==CHANNEL
 video=get(s,'videos',part='snippet,status,processingDetails,contentDetails',id=V)['items'][0]
 assert video['snippet']['channelId']==CHANNEL and video['status']['privacyStatus']=='private'
 p=get(s,'playlists',part='snippet,status',id=P)['items'][0];assert p['snippet']['channelId']==CHANNEL
 before=pages(s,'playlistItems',part='snippet,contentDetails',playlistId=P,maxResults=50)
 existing=[x for x in before if x['contentDetails']['videoId']==V]
 state={'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'channel_id':CHANNEL,'video_id':V,'playlist_id':P,'playlist_before':p,'before_items':before,'sorting_mode':'Manual verified in Studio this turn','phase':'no_write_yet'}
 if not existing:
  assert not receipt.exists(),'Existing mutation receipt requires reconciliation'
  body={'snippet':{'playlistId':P,'position':len(before),'resourceId':{'kind':'youtube#video','videoId':V}}}
  state.update(phase='inserting_outcome_unknown',request=body);receipt.write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n')
  response=s.post(BASE+'playlistItems',params={'part':'snippet'},json=body,timeout=45)
  state.update(http_status=response.status_code)
  receipt.write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n')
  assert response.status_code in (200,201),'Reconcile before retry'
  state['insert_response']=response.json()
 after=pages(s,'playlistItems',part='snippet,contentDetails',playlistId=P,maxResults=50)
 matched=[x for x in after if x['contentDetails']['videoId']==V];assert len(matched)==1
 assert [x['contentDetails']['videoId'] for x in after]==[x['contentDetails']['videoId'] for x in before if x['contentDetails']['videoId']!=V]+[V]
 pafter=get(s,'playlists',part='snippet,status',id=P)['items'][0]
 assert pafter['status']==p['status']
 assert get(s,'videos',part='status',id=V)['items'][0]['status']['privacyStatus']=='private'
 state.update(phase='saved_verified',after_items=after,playlist_after=pafter,playlist_item_id=matched[0]['id'],position=matched[0]['snippet']['position'],privacy='private',previous_order_preserved=True)
 receipt.write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps({k:state[k] for k in ['video_id','playlist_id','phase','position','privacy','previous_order_preserved']}))
