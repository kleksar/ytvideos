#!/usr/bin/env python3
"""Create one owned unlisted playlist with an exclusive before-write receipt.

An unknown result always requires manual reconciliation, never blind retry.
"""
import argparse
import json
import re
import sys
import time
from pathlib import Path
from add_to_playlist import read_items
from schedule import API, SCOPE, ScheduleError, reserve, mark_done


def create(session, channel, title, state):
    if not re.fullmatch(r'UC[A-Za-z0-9_-]{22}', channel or ''):
        raise ScheduleError('Invalid channel ID')
    if not title or len(title) > 150 or title != title.strip():
        raise ScheduleError('Invalid title')
    state = Path(state)
    if state.exists():
        raise ScheduleError('Receipt exists; reconcile manually before retry')
    channels = read_items(session, 'channels', {'part': 'id', 'mine': 'true'})
    if len(channels) != 1 or channels[0].get('id') != channel:
        raise ScheduleError('Authorized channel does not match')

    def matches():
        lists = read_items(session, 'playlists', {'part': 'id,snippet,status', 'mine': 'true'})
        return [p for p in lists if p.get('snippet', {}).get('title', '').casefold() == title.casefold()]

    if matches():
        raise ScheduleError('Playlist with this title already exists; inspect and reuse manually')
    reserve(state, {'state': 'outcome_unknown', 'action': 'create_playlist', 'channel_id': channel,
                    'title': title, 'privacy': 'unlisted'})
    if matches():
        raise ScheduleError('Matching playlist appeared; inspect receipt and channel before retry')
    body = {'snippet': {'title': title}, 'status': {'privacyStatus': 'unlisted'}}
    try:
        response = session.post(API + 'playlists', params={'part': 'snippet,status'},
                                json=body, timeout=60, allow_redirects=False)
    except Exception:
        raise ScheduleError('Creation outcome unknown; inspect channel before any retry') from None
    if response.status_code not in (200, 201):
        raise ScheduleError('Creation HTTP %s; inspect channel before any retry' % response.status_code)
    try:
        playlist_id = response.json()['id']
    except Exception:
        raise ScheduleError('Creation response incomplete; inspect channel before any retry') from None
    if not isinstance(playlist_id, str) or not playlist_id:
        raise ScheduleError('Creation response incomplete; inspect channel before any retry')
    # Save the returned ID even if subsequent readback is delayed or fails.
    # This is still an unknown outcome until ownership and privacy are read back.
    mark_done(state, {'state': 'outcome_unknown', 'action': 'create_playlist',
                      'channel_id': channel, 'playlist_id': playlist_id,
                      'title': title, 'privacy': 'unlisted'})
    for attempt in range(5):
        all_matching = matches()
        if all_matching:
            break
        if attempt < 4:
            time.sleep(2)
    found = [p for p in all_matching if p.get('id') == playlist_id]
    if len(all_matching) != 1 or len(found) != 1 or found[0].get('snippet', {}).get('channelId') != channel or found[0].get('status', {}).get('privacyStatus') != 'unlisted':
        raise ScheduleError('Playlist ownership or unlisted status not confirmed; inspect manually')
    result = {'state': 'confirmed', 'action': 'create_playlist', 'channel_id': channel,
              'playlist_id': playlist_id, 'title': title, 'privacy': 'unlisted'}
    mark_done(state, result)
    return result


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--token', required=True)
    p.add_argument('--channel-id', required=True)
    p.add_argument('--title', required=True)
    p.add_argument('--state', required=True)
    a = p.parse_args()
    try:
        from google.oauth2.credentials import Credentials
        from google.auth.transport.requests import AuthorizedSession
        creds = Credentials.from_authorized_user_file(a.token, [SCOPE])
        # Disable AuthorizedSession's automatic 401 replay of the POST.
        # before_request can still refresh expired credentials before sending.
        with AuthorizedSession(creds, max_refresh_attempts=0) as session:
            result = create(session, a.channel_id, a.title, a.state)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except Exception as exc:
        print('Error:', str(exc) if isinstance(exc, (ScheduleError, RuntimeError)) else type(exc).__name__, file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
