"""Read-only YouTube catalog capture. No YouTube mutations."""
import json
from pathlib import Path
from datetime import datetime, timezone
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import AuthorizedSession

root = Path('/Users/diplomat/ytvideos')
out = root / 'new_channel/research/2026-11-02-catalog-renewal'
config = json.loads((root / 'stories/automation/channels.json').read_text())['paper_detour']
creds = Credentials.from_authorized_user_file(config['token_file'])
scopes = list(creds.scopes or [])
if not any(s.endswith(('/youtube.readonly', '/youtube', '/youtube.force-ssl')) for s in scopes):
    raise SystemExit('Required existing read permission absent')
session = AuthorizedSession(creds)
def get(resource, **params):
    response = session.get('https://www.googleapis.com/youtube/v3/' + resource, params=params, timeout=45)
    if response.status_code != 200:
        raise SystemExit(f'YouTube read failed: HTTP {response.status_code}')
    return response.json()
started = datetime.now(timezone.utc).isoformat()
channel = get('channels', part='snippet,contentDetails', mine='true')
items = channel.get('items', [])
if len(items) != 1 or items[0]['id'] != config['channel_id']:
    raise SystemExit('Authorized channel mismatch')
uploads = items[0]['contentDetails']['relatedPlaylists']['uploads']
entries = []
page = None
while True:
    params = dict(part='snippet,contentDetails', playlistId=uploads, maxResults=50)
    if page:
        params['pageToken'] = page
    data = get('playlistItems', **params)
    entries.extend(data.get('items', []))
    page = data.get('nextPageToken')
    if not page:
        break
ids = list(dict.fromkeys(e['contentDetails']['videoId'] for e in entries))
videos = []
for start in range(0, len(ids), 50):
    videos.extend(get('videos', part='snippet,status,contentDetails,statistics', id=','.join(ids[start:start+50]), maxResults=50).get('items', []))
if any(v['snippet']['channelId'] != config['channel_id'] for v in videos):
    raise SystemExit('Video ownership mismatch')
result = dict(captured_start_utc=started, captured_end_utc=datetime.now(timezone.utc).isoformat(), source='YouTube Data API v3; cumulative counters', scopes=scopes, channel=channel, uploads=entries, videos=videos, missing_video_ids=sorted(set(ids)-{v['id'] for v in videos}), format_classification='not provided by Data API; corroborate Studio/records', report_timezone='not applicable to cumulative snapshot', retention='not collected')
(out / 'inventory.json').write_text(json.dumps(result, ensure_ascii=False, indent=2))
print('Verified channel:', items[0]['id'], items[0]['snippet']['title'])
print('Capture UTC:', result['captured_end_utc'])
print('Uploads:', len(entries), 'returned videos:', len(videos))
for v in sorted(videos, key=lambda v:v['snippet']['publishedAt']):
    print(json.dumps(dict(id=v['id'], publishedAt=v['snippet']['publishedAt'], privacy=v['status']['privacyStatus'], views=v.get('statistics',{}).get('viewCount'), duration=v['contentDetails']['duration'], title=v['snippet']['title']), ensure_ascii=False))
