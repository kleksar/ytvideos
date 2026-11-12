import datetime,json,sys,urllib.parse
from pathlib import Path
from google.auth.transport.requests import AuthorizedSession
from google.oauth2.credentials import Credentials
import requests
sys.path.insert(0,str(Path('automation/youtube').resolve()))
from schedule import read,verify_serving_caption
channel='UCMVfdfaNxV3ZkI3_J3Eejzw'
video='azhQEhV6ywg'
ep=Path(sys.argv[2])
md=ep/'Packaging/Metadata'
phase=sys.argv[3]
with AuthorizedSession(Credentials.from_authorized_user_file(sys.argv[1],['https://www.googleapis.com/auth/youtube.force-ssl'])) as session:
 result=read(session,channel,video)
 sn=result['snippet'];st=result['status']
 target=json.loads((md/'upload-metadata-v01.json').read_text())
 for k,m in [('title','title'),('description','description'),('categoryId','category_id'),('defaultLanguage','language'),('defaultAudioLanguage','audio_language')]:
  assert sn[k]==target[m],k
 assert sorted(sn['tags'])==sorted(target['tags'])
 assert st['privacyStatus']==phase and not st.get('publishAt') and st['uploadStatus']=='processed'
 assert st.get('selfDeclaredMadeForKids') is False and st.get('containsSyntheticMedia',False) is False
 cap=json.loads((md/'caption-upload-20261108.json').read_text())
 caption=verify_serving_caption(session,channel,video,'en',ep/'Deliverables/Brocklesby-en-v01.srt',cap['receipt'])
 assert result['processingDetails']['processingStatus']=='succeeded'
 thumbs=sn['thumbnails']
 thumb=thumbs.get('maxres') or thumbs.get('standard') or thumbs['high']
 url=thumb['url']
 parsed=urllib.parse.urlparse(url)
 if parsed.scheme=='https' and parsed.hostname and parsed.hostname.endswith('.ytimg.com'):
  try:
   response=requests.get(url,headers={'Cache-Control':'no-cache'},timeout=15)
   if response.status_code==200 and response.headers.get('Content-Type','').startswith('image/'):
    (ep/'Work'/('yt-thumbnail-'+phase+'.jpg')).write_bytes(response.content)
  except requests.RequestException: pass
 data=dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),video=result,caption=caption,thumb_url_verified=bool((ep/'Work'/('yt-thumbnail-'+phase+'.jpg')).exists()))
 (md/('yt-readback-'+phase+'-20261108.json')).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
 print('Saved exact metadata, privacy='+phase+', processing=succeeded, caption=serving, thumbnail image fetched='+str(data['thumb_url_verified']))
