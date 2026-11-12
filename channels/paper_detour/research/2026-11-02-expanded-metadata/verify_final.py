import json,datetime
from pathlib import Path
from api_inventory import session,get,pages,ROOT,CHANNEL
D=ROOT/'new_channel/research/2026-11-02-expanded-metadata';before=json.loads((D/'BEFORE.json').read_text());plan=json.loads((D/'PLAN.json').read_text())
with session() as s:
 ch=get(s,'channels',part='id,contentDetails',mine='true')['items'];assert len(ch)==1 and ch[0]['id']==CHANNEL
 uploads=pages(s,'playlistItems',part='snippet,contentDetails',playlistId=ch[0]['contentDetails']['relatedPlaylists']['uploads'],maxResults=50)
 ids=[x['contentDetails']['videoId'] for x in uploads];videos=[]
 for i in range(0,len(ids),50):videos+=get(s,'videos',part='snippet,status,processingDetails,contentDetails',id=','.join(ids[i:i+50]))['items']
 playlists=pages(s,'playlists',part='snippet,status,contentDetails',mine='true',maxResults=50)
 members={p['id']:pages(s,'playlistItems',part='snippet,contentDetails,status',playlistId=p['id'],maxResults=50) for p in playlists}
 snapshot={'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'channel_id':CHANNEL,'videos':videos,'playlists':playlists,'members':members,'uploads':uploads}
 (D/'AFTER.json').write_text(json.dumps(snapshot,ensure_ascii=False,indent=2)+'\n')
 live={v['id']:v for v in videos};base={v['id']:v for v in before['videos']}
 for row in plan['rows']:
  v=live[row['video_id']];assert v['snippet']['title']==row['title'];assert v['snippet']['description']==row['description'];assert v['status']==base[row['video_id']]['status']
 for exc in plan['excluded']:
  v=live[exc['id']];b=base[exc['id']]
  for key in ['title','description','tags','categoryId','defaultLanguage','defaultAudioLanguage']:
   assert v['snippet'].get(key)==b['snippet'].get(key)
  assert v['status']==b['status']
  def thumbnail_identity(sn):
   return {k:{**x,'url':x['url'].split('?')[0]} for k,x in sn.get('thumbnails',{}).items()}
  assert thumbnail_identity(v['snippet'])==thumbnail_identity(b['snippet'])
 V='zA0kogtqoUs';jas=live[V];m=ROOT/'new_channel/videos/031_jascon4_okene/Packaging/Metadata';expected=json.loads((m/'YOUTUBE_UPLOAD_METADATA_v14_v02.json').read_text())
 assert jas['snippet']['title']==expected['title'];assert jas['snippet']['description']==expected['description'].rstrip()
 assert set(jas['snippet']['tags'])==set(expected['tags']);assert jas['snippet']['defaultLanguage']=='en';assert jas['snippet']['defaultAudioLanguage']=='en';assert jas['snippet']['categoryId']=='24'
 assert jas['status']['privacyStatus']=='private' and 'publishAt' not in jas['status']
 assert jas['processingDetails']['processingStatus']=='succeeded' and jas['status']['uploadStatus']=='processed';assert jas['contentDetails']['hasCustomThumbnail']
 for p in playlists:
  old=next(x for x in before['playlists'] if x['id']==p['id']);assert p['snippet']==old['snippet'] and p['status']==old['status']
  b=[x['contentDetails']['videoId'] for x in before['members'][p['id']]];a=[x['contentDetails']['videoId'] for x in members[p['id']]]
  assert a==b+([V] if p['id']=='PLEIDCTZ8y2k8' else [])
 summary={'new_upload':{'id':V,'privacy':'private','processing':'succeeded','exact_title':True,'exact_description':'matches except YouTube strips final newline','separate_tags':'12set matches; YouTube sorted their order','languages':'en/en','cover':'APIcustomthumbnail true; Studio upload/save/reload and Shorts image visually inspected','playlist':'PLEIDCTZ8y2k8','playlist_position':5},'other_editorial_videos':len(plan['rows']),'metadata_updated':sum(bool(json.loads((D/'receipts'/f"{r['video_id']}.json").read_text())['requested_changes']) for r in plan['rows']),'already_complete_unchanged':sum(not bool(json.loads((D/'receipts'/f"{r['video_id']}.json").read_text())['requested_changes']) for r in plan['rows']),'technical_exclusions_unchanged':len(plan['excluded']),'old_privacy_and_playlists_preserved':True,'before_count':len(before['videos']),'after_count':len(videos),'playlist_count':len(playlists),'api_validation':'PASS','radio_test':'active with same3titles before and after in fresh Studio; see AX and screenshot','localized_fields':'Unrequested localized descriptions changed on some rows; origin unverified, no localizations part written or reverted. Full per-row before/after receipts retained.'}
 (D/'VALIDATION.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n');(m/'YOUTUBE_READBACK_FINAL_20261102.json').write_text(json.dumps(jas,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps(summary,ensure_ascii=False,indent=2))
