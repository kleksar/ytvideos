from pathlib import Path
import json, datetime
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import AuthorizedSession
ROOT=Path('/Users/diplomat/ytvideos')
OUT=ROOT/'new_channel/research/2026-11-02-expanded-metadata'
CONFIG=json.loads((ROOT/'stories/automation/channels.json').read_text())['paper_detour']
CHANNEL=CONFIG['channel_id']
BASE='https://www.googleapis.com/youtube/v3/'
def session():
    c=Credentials.from_authorized_user_file(CONFIG['playlist_token_file'])
    assert set(c.scopes or []) & {'https://www.googleapis.com/auth/youtube.force-ssl','https://www.googleapis.com/auth/youtube'},'No management scope'
    return AuthorizedSession(c)
def get(s,path,**params):
    r=s.get(BASE+path,params=params,timeout=45)
    if r.status_code!=200:raise RuntimeError('API read HTTP '+str(r.status_code))
    return r.json()
def pages(s,path,**params):
    out=[]
    while True:
        d=get(s,path,**params);out.extend(d.get('items',[]))
        if not d.get('nextPageToken'):return out
        params['pageToken']=d['nextPageToken']
def inventory():
    with session() as s:
        channels=get(s,'channels',part='id,snippet,contentDetails,status',mine='true')['items']
        assert len(channels)==1 and channels[0]['id']==CHANNEL
        uploadsid=channels[0]['contentDetails']['relatedPlaylists']['uploads']
        uploads=pages(s,'playlistItems',part='snippet,contentDetails',playlistId=uploadsid,maxResults=50)
        ids=[i['contentDetails']['videoId'] for i in uploads]
        videos=[]
        for j in range(0,len(ids),50):videos.extend(get(s,'videos',part='snippet,status,contentDetails,processingDetails,statistics',id=','.join(ids[j:j+50]))['items'])
        playlists=pages(s,'playlists',part='snippet,status,contentDetails',mine='true',maxResults=50)
        members={p['id']:pages(s,'playlistItems',part='snippet,contentDetails,status',playlistId=p['id'],maxResults=50) for p in playlists}
        result={'captured_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'channel':channels[0],'uploads':uploads,'videos':videos,'playlists':playlists,'members':members}
        (OUT/'BEFORE.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
        print(json.dumps({'channel':CHANNEL,'videos':[{'id':v['id'],'title':v['snippet']['title'],'duration':v['contentDetails']['duration'],'privacy':v['status']['privacyStatus'],'category':v['snippet'].get('categoryId')} for v in videos]},ensure_ascii=False,indent=2))
if __name__=='__main__':inventory()
