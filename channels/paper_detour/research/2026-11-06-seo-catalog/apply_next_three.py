import json
import re
import time
from datetime import datetime, timezone
from pathlib import Path

from google.auth.transport.requests import AuthorizedSession
from google.oauth2.credentials import Credentials

folder = Path(__file__).resolve().parent
channel_id = 'UCMVfdfaNxV3ZkI3_J3Eejzw'
ids = ['LcLKUCjjZ3Q', 'ba2GMSKTB5g', 'UqWIwpbTMik']
titles = [
    'The Dark-Web Market Police Secretly Controlled',
    'How a Car Manual Publisher Ended Up Publishing Dune',
    'The Scholar Who Thought Birds Spent Winter on the Moon',
]
additions = ['#DutchPolice', '#DuneBook', '#MigratoryBirds']
draft = (folder / 'NEXT_THREE_DRAFT.md').read_text()
blocks = re.findall(r'Описание:\n\n(.*?)(?=\n\n## |\Z)', draft, re.S)
assert len(blocks) == 3
descriptions = [block.rstrip('\n') + ' ' + tag for block, tag in zip(blocks, additions)]
baseline = {v['id']: v for v in json.loads((folder / 'next-three-live.json').read_text())['items']}
creds = Credentials.from_authorized_user_file(str(Path.home() / '.local/share/story-youtube/paper-detour/manage-token.json'))
assert set(creds.scopes or []) & {'https://www.googleapis.com/auth/youtube.force-ssl', 'https://www.googleapis.com/auth/youtube'}
session = AuthorizedSession(creds)
base = 'https://www.googleapis.com/youtube/v3/'

def get(endpoint, params):
    response = session.get(base + endpoint, params=params, timeout=30)
    response.raise_for_status()
    return response.json()

channels = get('channels', {'part': 'snippet', 'mine': 'true'})['items']
assert len(channels) == 1 and channels[0]['id'] == channel_id

def read_video(vid):
    items = get('videos', {'part': 'snippet,status', 'id': vid}).get('items', [])
    if len(items) != 1 or items[0]['snippet']['channelId'] != channel_id:
        raise RuntimeError('Video missing or owner mismatch: ' + vid)
    return items[0]

for vid, title, description in zip(ids, titles, descriptions):
    before = read_video(vid)
    receipt_path = folder / (vid + '-seo-20261106-receipt.json')
    if receipt_path.exists():
        receipt = json.loads(receipt_path.read_text())
        if receipt.get('state') == 'applied_verified' and before['snippet'].get('title') == title and before['snippet'].get('description') == description:
            print(vid, 'already_verified_no_write', flush=True)
            continue
        raise RuntimeError(f'{vid}: receipt already exists; inspect before another write')
    old = baseline[vid]
    for field in ('title', 'description'):
        if before['snippet'].get(field) != old['snippet'].get(field):
            raise RuntimeError(f'{vid}: {field} changed since proposal; stopped before write')
    receipt = {'channel_id': channel_id, 'video_id': vid, 'timestamp_utc': datetime.now(timezone.utc).isoformat(), 'before': before, 'requested': {'title': title, 'description': description}, 'state': 'write_outcome_unknown'}
    receipt_path.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + '\n')
    snippet = before['snippet']
    writable = {k: snippet[k] for k in ('categoryId', 'tags', 'defaultLanguage', 'defaultAudioLanguage') if k in snippet}
    writable.update({'title': title, 'description': description})
    response = session.put(base + 'videos', params={'part': 'snippet'}, json={'id': vid, 'snippet': writable}, timeout=30)
    receipt['write_http_status'] = response.status_code
    if not response.ok:
        receipt['write_error'] = response.text[:2000]
        receipt_path.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + '\n')
        raise RuntimeError(f'{vid}: write HTTP {response.status_code}; inspect before retry')
    receipt['write_response'] = response.json()
    after = read_video(vid)
    for _ in range(4):
        if after['snippet'].get('title') == title and after['snippet'].get('description') == description:
            break
        time.sleep(2)
        after = read_video(vid)
    receipt['after'] = after
    receipt['checks'] = {
        'title': after['snippet'].get('title') == title,
        'description_and_hashtags': after['snippet'].get('description') == description,
        'category': after['snippet'].get('categoryId') == snippet.get('categoryId'),
        'tags': after['snippet'].get('tags') == snippet.get('tags'),
        'default_language': after['snippet'].get('defaultLanguage') == snippet.get('defaultLanguage'),
        'audio_language': after['snippet'].get('defaultAudioLanguage') == snippet.get('defaultAudioLanguage'),
        'privacy': after['status'].get('privacyStatus') == before['status'].get('privacyStatus'),
    }
    receipt['state'] = 'applied_verified' if all(receipt['checks'].values()) else 'verification_mismatch'
    receipt_path.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + '\n')
    print(vid, receipt['state'], json.dumps(receipt['checks']), flush=True)
    if receipt['state'] != 'applied_verified':
        raise RuntimeError(f'{vid}: verification mismatch; stopped before next write')
