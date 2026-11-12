"""Delete only the user-authorized Test 01 after its replacement is verified."""
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

from google.auth.transport.requests import AuthorizedSession
from google.oauth2.credentials import Credentials

root = Path(__file__).resolve().parent
sys.path.insert(0, str(root.parents[4]/'automation/youtube'))
from upload import check_channel, private_write

channel = 'UCMVfdfaNxV3ZkI3_J3Eejzw'
old_id = '8PwziOHGxag'
new = json.loads((root/'youtube_receipt.json').read_text())
new_id = new['video_id']
assert new_id != old_id and new['privacy'] == 'private'
assert new['processing_status'] == 'succeeded'
assert json.loads((root/'local_qa.json').read_text())['decode'] == 'PASS'
receipt_path = root/'previous_test_delete_receipt.json'
scope = 'https://www.googleapis.com/auth/youtube.force-ssl'
token = Path('/Users/diplomat/.local/share/story-youtube/paper-detour/manage-token.json')
assert scope in json.loads(token.read_text())['scopes']
credentials = Credentials.from_authorized_user_file(str(token), [scope])
url = 'https://www.googleapis.com/youtube/v3/videos'


def read(session, video_id):
    response = session.get(url, params={'part':'snippet,status,processingDetails','id':video_id}, timeout=60)
    response.raise_for_status()
    return response.json().get('items', [])


def replacement(session):
    items = read(session, new_id)
    assert len(items) == 1
    item = items[0]
    assert item['snippet']['channelId'] == channel
    assert item['status']['privacyStatus'] == 'private'
    assert item['processingDetails']['processingStatus'] == 'succeeded'
    return item


with AuthorizedSession(credentials) as session:
    check_channel(session, channel)
    replacement(session)
    old = read(session, old_id)
    if old:
        assert len(old) == 1 and old[0]['snippet']['channelId'] == channel
        assert old[0]['snippet']['title'] == 'Paper Detour \u2014 Grain Test 01 | 15 seconds | 4K | Private Review'
        if receipt_path.exists():
            raise RuntimeError('Deletion already attempted: reconcile receipt before another mutation.')
        receipt = {'old_video_id':old_id,'replacement_video_id':new_id,'channel_id':channel,
                   'before':old[0], 'attempted_utc':datetime.now(timezone.utc).isoformat(),
                   'status':'attempt_recorded_before_request'}
        private_write(receipt_path,receipt)
        response = session.delete(url, params={'id':old_id}, timeout=60)
        receipt['delete_http_status'] = response.status_code
        private_write(receipt_path,receipt)
        assert response.status_code == 204, 'Delete not accepted; inspect receipt and current state before retry.'
    else:
        receipt = (json.loads(receipt_path.read_text()) if receipt_path.exists() else
                   {'old_video_id':old_id,'replacement_video_id':new_id,'channel_id':channel,
                    'status':'already_absent_before_this_request'})
        assert receipt['old_video_id'] == old_id and receipt['replacement_video_id'] == new_id
    for attempt in range(8):
        if read(session, old_id) == []:
            break
        if attempt < 7:
            time.sleep(3)
    else:
        raise RuntimeError('Delete accepted; old resource still returned. Reconcile reads without another DELETE.')
    replacement(session)
    receipt.update({'old_absent_verified':True,'replacement_preserved_verified':True,
                    'verified_utc':datetime.now(timezone.utc).isoformat()})
    if receipt.get('delete_http_status') == 204:
        receipt['status'] = 'deleted_verified'
    private_write(receipt_path,receipt)
    print(json.dumps({k:v for k,v in receipt.items() if k != 'before'},indent=2))
