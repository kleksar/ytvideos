"""Read-only channel and private upload readback. Credentials stay outside project."""
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from google.auth.transport.requests import AuthorizedSession
from google.oauth2.credentials import Credentials

HERE=Path(__file__).resolve().parent
PROJECT=next(p for p in HERE.parents if (p/'automation/youtube/upload.py').is_file())
sys.path.insert(0,str(PROJECT/'automation/youtube'))
from upload import check_channel, SCOPES

channel='UCMVfdfaNxV3ZkI3_J3Eejzw'
creds=Credentials.from_authorized_user_file('/Users/diplomat/.local/share/story-youtube/paper-detour/token.json',SCOPES)
with AuthorizedSession(creds) as session:
    check_channel(session,channel)
    if len(sys.argv)==1:
        print(json.dumps({'channel_id':channel,'authorization_preflight':'PASS','checked_utc':datetime.now(timezone.utc).isoformat()}))
        raise SystemExit(0)
    vid=sys.argv[1]
    assert len(vid)==11
    resource=session.get('https://www.googleapis.com/youtube/v3/videos',params={'part':'snippet,status,processingDetails,contentDetails','id':vid},timeout=60)
    resource.raise_for_status()
    items=resource.json().get('items',[]);assert len(items)==1
    item=items[0];s=item['snippet'];status=item['status']
    meta=json.loads((HERE/'youtube_metadata.json').read_text())
    for k,m in [('title','title'),('description','description'),('categoryId','category_id'),('defaultLanguage','language')]:
        assert s[k]==meta[m],k
    assert s['channelId']==channel and s.get('tags',[])==meta['tags']
    assert status['privacyStatus']=='private' and status['selfDeclaredMadeForKids']==meta['made_for_kids']
    assert status.get('containsSyntheticMedia',False)==meta['contains_synthetic_media']
    local=json.loads((HERE/'render_receipt.json').read_text())
    report={'video_id':vid,'url':f'https://www.youtube.com/watch?v={vid}','channel_id':channel,
        'privacy':status['privacyStatus'],'upload_status':status['uploadStatus'],
        'processing_status':item.get('processingDetails',{}).get('processingStatus'),'metadata_readback':'PASS',
        'checked_utc':datetime.now(timezone.utc).isoformat(),'file':local['file'],'sha256':local['sha256'],
        'preview':True,'user_selection':'PENDING','resource':item,
        'thumbnail':'automatic; not separately approved','playlist':'not requested','tags':[],'hashtags':[],
        'copyright_studio_checks':'UNVERIFIED; API status/restrictions recorded, not Studio review'}
    (HERE/'youtube_receipt.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='resource'},indent=2))
