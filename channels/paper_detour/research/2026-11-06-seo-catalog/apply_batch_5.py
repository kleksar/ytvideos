import json
import time
from datetime import datetime, timezone
from pathlib import Path

from google.auth.transport.requests import AuthorizedSession
from google.oauth2.credentials import Credentials

root = Path(__file__).resolve().parent
channel_id = 'UCMVfdfaNxV3ZkI3_J3Eejzw'
items = {
    'lotfSkfgvuM': ('#HomeComputing', '001_radio_game/Shorts/01_radio_signal'),
    'gc19EQoi-L0': ('#MSXGames', '001_radio_game/Shorts/02_decoder'),
    'Yz1Fn3GRsrw': ('#ThirdWheel', '008_boyfriend_brought_friend'),
}
baseline = {v['id']: v for v in json.loads((root / 'batch5-live.json').read_text())['items']}
credentials = Credentials.from_authorized_user_file(str(Path.home() / '.local/share/story-youtube/paper-detour/manage-token.json'))
assert set(credentials.scopes or []) & {'https://www.googleapis.com/auth/youtube.force-ssl', 'https://www.googleapis.com/auth/youtube'}
session = AuthorizedSession(credentials)
api = 'https://www.googleapis.com/youtube/v3/'

def fetch(endpoint, params):
    response = session.get(api + endpoint, params=params, timeout=30)
    response.raise_for_status()
    return response.json()

channels = fetch('channels', {'part': 'snippet', 'mine': 'true'}).get('items', [])
assert len(channels) == 1 and channels[0]['id'] == channel_id

def read_video(video_id):
    found = fetch('videos', {'part': 'snippet,status', 'id': video_id}).get('items', [])
    if len(found) != 1 or found[0]['snippet']['channelId'] != channel_id:
        raise RuntimeError('missing video or owner mismatch: ' + video_id)
    return found[0]

for video_id, (new_hashtags, episode) in items.items():
    path = root / (video_id + '-batch5-20261106-receipt.json')
    if path.exists():
        raise RuntimeError('receipt already exists; reconcile before any repeat: ' + video_id)
    before = read_video(video_id)
    old = baseline[video_id]
    if any(before['snippet'].get(k) != old['snippet'].get(k) for k in ('title', 'description')):
        raise RuntimeError('title or description changed since proposal: ' + video_id)
    original = before['snippet']
    description = original['description'] + ' ' + new_hashtags
    assert len(description.encode('utf-8')) <= 5000 and '<' not in description and '>' not in description
    requested = {'title': original['title'], 'description': description}
    receipt = {'video_id': video_id, 'channel_id': channel_id, 'timestamp_utc': datetime.now(timezone.utc).isoformat(), 'before': before, 'requested': requested, 'state': 'write_outcome_unknown'}
    path.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + '\n')
    snippet = {k: original[k] for k in ('categoryId', 'tags', 'defaultLanguage', 'defaultAudioLanguage') if k in original}
    snippet.update(requested)
    response = session.put(api + 'videos', params={'part': 'snippet'}, json={'id': video_id, 'snippet': snippet}, timeout=30)
    receipt['write_http_status'] = response.status_code
    if not response.ok:
        receipt['write_error'] = response.text[:2000]
        path.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + '\n')
        raise RuntimeError('update failed; do not retry blindly: ' + video_id)
    receipt['write_response'] = response.json()
    for attempt in range(5):
        after = read_video(video_id)
        if all(after['snippet'].get(k) == v for k, v in requested.items()):
            break
        if attempt < 4:
            time.sleep(2)
    receipt['after'] = after
    receipt['checks'] = {
        'title': after['snippet'].get('title') == requested['title'],
        'description_and_hashtags': after['snippet'].get('description') == description,
        'category': after['snippet'].get('categoryId') == original.get('categoryId'),
        'tags': after['snippet'].get('tags') == original.get('tags'),
        'language': after['snippet'].get('defaultLanguage') == original.get('defaultLanguage'),
        'audio_language': after['snippet'].get('defaultAudioLanguage') == original.get('defaultAudioLanguage'),
        'privacy': after['status'].get('privacyStatus') == before['status'].get('privacyStatus'),
    }
    receipt['state'] = 'applied_verified' if all(receipt['checks'].values()) else 'verification_mismatch'
    path.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + '\n')
    print(video_id, receipt['state'], json.dumps(receipt['checks']), flush=True)
    if receipt['state'] != 'applied_verified':
        raise RuntimeError('verification mismatch: ' + video_id)
    episode_dir = root.parents[1] / 'videos' / episode / 'Packaging' / 'Metadata'
    episode_dir.mkdir(parents=True, exist_ok=True)
    (episode_dir / 'seo-batch5-20261106-receipt.json').write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + '\n')
