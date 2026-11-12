import datetime,json,sys
from pathlib import Path
from google.auth.transport.requests import AuthorizedSession
from google.oauth2.credentials import Credentials
sys.path.insert(0,str(Path('automation/youtube').resolve()))
from add_to_playlist import read_items
from upload import check_channel
channel='UCMVfdfaNxV3ZkI3_J3Eejzw'
base='https://www.googleapis.com/youtube/v3/'
creds=Credentials.from_authorized_user_file(sys.argv[1],['https://www.googleapis.com/auth/youtube.force-ssl'])
with AuthorizedSession(creds) as session:
 check_channel(session,channel)
 r=session.get(base+'channels',params={'part':'id,contentDetails','mine':'true'},timeout=30)
 if r.status_code!=200: raise SystemExit('channel contents HTTP '+str(r.status_code))
 uploads=r.json()['items'][0]['contentDetails']['relatedPlaylists']['uploads']
 playlists=read_items(session,'playlists',{'part':'id,snippet,status,contentDetails','mine':'true'})
 chosen=[p for p in playlists if p['id']=='PLEIDCTZ8y2k8' and p['snippet']['channelId']==channel]
 items=read_items(session,'playlistItems',{'part':'snippet,contentDetails','playlistId':chosen[0]['id']}) if len(chosen)==1 else []
 latest=session.get(base+'playlistItems',params={'part':'snippet,contentDetails','playlistId':uploads,'maxResults':50},timeout=30)
 if latest.status_code!=200: raise SystemExit('upload inventory HTTP '+str(latest.status_code))
 ids=[i['contentDetails']['videoId'] for i in latest.json().get('items',[])]
 r=session.get(base+'videos',params={'part':'snippet,status,contentDetails','id':','.join(ids)},timeout=30)
 if r.status_code!=200: raise SystemExit('calendar HTTP '+str(r.status_code))
 data=dict(channel=channel,utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),playlists=playlists,selected_members=items,videos=[dict(id=x['id'],title=x['snippet']['title'],publishedAt=x['snippet']['publishedAt'],status=x['status']['privacyStatus'],publishAt=x['status'].get('publishAt'),duration=x['contentDetails']['duration']) for x in r.json()['items']],posts='Not provided by Data API; separate coverage')
 Path(sys.argv[2]).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
 print('Verified channel; playlists:',len(playlists),'matching playlist:',len(chosen),'current members:',len(items),'calendar videos:',len(data['videos']))
