"""Read back the exact private replacement upload; never changes YouTube."""
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from google.auth.transport.requests import AuthorizedSession
from google.oauth2.credentials import Credentials

root = Path(__file__).resolve().parent
sys.path.insert(0, str(root.parents[4]/'automation/youtube'))
from upload import check_channel, private_write, SCOPES

video_id = sys.argv[1]
channel = 'UCMVfdfaNxV3ZkI3_J3Eejzw'
assert len(video_id) == 11 and video_id != '8PwziOHGxag'
meta = json.loads((root/'youtube_metadata.json').read_text())
creds = Credentials.from_authorized_user_file('/Users/diplomat/.local/share/story-youtube/paper-detour/token.json', SCOPES)
with AuthorizedSession(creds) as session:
    check_channel(session, channel)
    response = session.get('https://www.googleapis.com/youtube/v3/videos',
                           params={'part':'snippet,status,processingDetails','id':video_id},timeout=60)
    response.raise_for_status()
    items = response.json().get('items', [])
    assert len(items) == 1
    item = items[0]
    snippet,status = item['snippet'],item['status']
    assert snippet['channelId'] == channel
    for api_key,meta_key in [('title','title'),('description','description'),('categoryId','category_id'),
                             ('defaultLanguage','language'),('defaultAudioLanguage','audio_language')]:
        assert snippet[api_key] == meta[meta_key], api_key
    assert snippet.get('tags',[]) == meta['tags']
    assert status['privacyStatus'] == 'private'
    assert status['selfDeclaredMadeForKids'] == meta['made_for_kids']
    assert status.get('containsSyntheticMedia',False) == meta['contains_synthetic_media']
    report={'video_id':video_id,'url':f'https://www.youtube.com/watch?v={video_id}',
            'channel_id':channel,'privacy':status['privacyStatus'],
            'upload_status':status['uploadStatus'],
            'processing_status':item.get('processingDetails',{}).get('processingStatus'),
            'metadata_readback':'PASS','checked_utc':datetime.now(timezone.utc).isoformat(),
            'resource':item,'user_review':'PENDING',
            'source_file':'PD030_GRAIN_02_VISIBLE_15S_2160P.mp4',
            'preview':True,'hashtags':[],'tags':[],'thumbnail':'automatic; not separately approved',
            'playlist':'not requested','production_defaults_changed':False}
    private_write(root/'youtube_receipt.json',report)
    print(json.dumps({k:v for k,v in report.items() if k!='resource'},indent=2))
