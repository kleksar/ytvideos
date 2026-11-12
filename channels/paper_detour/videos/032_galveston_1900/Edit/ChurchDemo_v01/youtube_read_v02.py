import json,sys
from pathlib import Path
sys.path.insert(0,'/Users/diplomat/ytvideos/automation/youtube')
from add_to_playlist import read_items
from google.auth.transport.requests import AuthorizedSession
from google.oauth2.credentials import Credentials
E=Path('/Users/diplomat/ytvideos/channels/paper_detour/videos/032_galveston_1900');D=E/'Packaging/Metadata';D.mkdir(parents=True,exist_ok=True)
C='UCMVfdfaNxV3ZkI3_J3Eejzw';P='PLEIDCTZ8y2k8'
# Registry ID is read below; never infer a playlist ID from a title or shortened URL.
registry=Path('/Users/diplomat/ytvideos/channels/paper_detour/docs/YOUTUBE_PLAYLISTS.md').read_text()
import re
ids=re.findall(r'PL[A-Za-z0-9_-]{10,}',registry);print('registry_playlist_ids',ids)
# Use exact ID from registry table.
m=re.search(r'\| \[Real Stories & Discoveries[^\n]*?`(PL[A-Za-z0-9_-]{10,})`',registry)
if m:P=m.group(1)
else:raise RuntimeError('Read exact Real Stories registry ID before request')
credentials=Credentials.from_authorized_user_file('/Users/diplomat/.local/share/story-youtube/paper-detour/manage-token.json')
with AuthorizedSession(credentials) as s:
    channels=read_items(s,'channels',{'part':'id,snippet,contentDetails','mine':'true'});assert len(channels)==1 and channels[0]['id']==C
    playlist=read_items(s,'playlists',{'part':'id,snippet,status','id':P});assert len(playlist)==1 and playlist[0]['snippet']['channelId']==C
    items=read_items(s,'playlistItems',{'part':'id,snippet,contentDetails','playlistId':P})
    uploads=read_items(s,'playlistItems',{'part':'id,snippet,contentDetails','playlistId':channels[0]['contentDetails']['relatedPlaylists']['uploads']})
    receipt={'channel_id':C,'playlist':playlist,'playlist_items':items,'uploads':[{'id':x['contentDetails']['videoId'],'title':x['snippet']['title']} for x in uploads]}
    if len(sys.argv)>1:
        receipt['video']=read_items(s,'videos',{'part':'id,snippet,status,contentDetails,processingDetails,fileDetails','id':sys.argv[1]})
        receipt['captions']=read_items(s,'captions',{'part':'id,snippet','videoId':sys.argv[1]})
    (D/('youtube_read_after_v02.json' if len(sys.argv)>1 else 'youtube_preflight_v02.json')).write_text(json.dumps(receipt,indent=2,ensure_ascii=False))
    print(json.dumps({'channel':C,'playlist':P,'playlist_privacy':playlist[0]['status']['privacyStatus'],'items':len(items),'galveston_matches':[x for x in receipt['uploads'] if 'galveston' in x['title'].lower()]}))
