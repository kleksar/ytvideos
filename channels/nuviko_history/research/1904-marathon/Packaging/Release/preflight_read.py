import json, pathlib, sys, datetime
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import AuthorizedSession
root=pathlib.Path.home()/'.local/share/story-youtube'; expected='UCbyLx6Rf3iWww4bPZJ2oo2A'
def read(session,res,params):
 all=[];p=dict(params,maxResults=50)
 while True:
  r=session.get('https://www.googleapis.com/youtube/v3/'+res,params=p,timeout=30,allow_redirects=False)
  if r.status_code!=200: raise RuntimeError(res+' HTTP '+str(r.status_code))
  data=r.json();all+=data.get('items',[])
  if not data.get('nextPageToken'):return all
  p['pageToken']=data['nextPageToken']
try:
 creds=Credentials.from_authorized_user_file(str(root/'history-endurance-chrome-token.json'))
 with AuthorizedSession(creds) as s:
  ch=read(s,'channels',{'part':'id,snippet,contentDetails','mine':'true'})
  if len(ch)!=1 or ch[0]['id']!=expected: raise RuntimeError('Wrong authorized channel')
  pl=read(s,'playlists',{'part':'id,snippet,status,contentDetails','mine':'true'})
  playlists=[]
  for p in pl:
   it=read(s,'playlistItems',{'part':'snippet,contentDetails','playlistId':p['id']})
   playlists.append({'id':p['id'],'title':p['snippet']['title'],'description':p['snippet'].get('description',''),'privacy':p['status']['privacyStatus'],'members':[{'id':i['contentDetails']['videoId'],'title':i['snippet']['title']} for i in it]})
  up=read(s,'playlistItems',{'part':'contentDetails','playlistId':ch[0]['contentDetails']['relatedPlaylists']['uploads']});ids=[x['contentDetails']['videoId'] for x in up];vid=[]
  for i in range(0,len(ids),50):vid+=read(s,'videos',{'part':'snippet,status,contentDetails','id':','.join(ids[i:i+50])})
  data={'checked_at':datetime.datetime.now().astimezone().isoformat(),'channel_id':expected,'channel_title':ch[0]['snippet']['title'],'playlists':playlists,'videos':[{'id':v['id'],'title':v['snippet']['title'],'publishedAt':v['snippet']['publishedAt'],'privacy':v['status']['privacyStatus'],'publishAt':v['status'].get('publishAt'),'duration':v['contentDetails']['duration']} for v in vid], 'posts':'UNVERIFIED: not covered by YouTube Data API video inventory'}
  out=pathlib.Path(__file__).parent/'preflight_channel_v01.json';out.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n');print('Verified channel',expected,'playlists',len(playlists),'videos',len(vid),'posts unverified; snapshot',out)
except Exception as e:
 print('Read-only preflight failed:', str(e) if isinstance(e,RuntimeError) else type(e).__name__,file=sys.stderr);sys.exit(1)
