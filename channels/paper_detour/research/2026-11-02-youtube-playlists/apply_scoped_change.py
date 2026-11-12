"""Receipt-bearing executor for this accepted plan only; not a generic uploader."""
import argparse
import json
import time
from datetime import datetime, timezone
from pathlib import Path
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import AuthorizedSession

ROOT=Path(__file__).resolve().parents[3]
HERE=Path(__file__).resolve().parent
BASE='https://www.googleapis.com/youtube/v3/'
cfg=json.loads((ROOT/'stories/automation/channels.json').read_text())['paper_detour']
credentials=Credentials.from_authorized_user_file(cfg['playlist_token_file'])
assert 'https://www.googleapis.com/auth/youtube.force-ssl' in credentials.scopes
session=AuthorizedSession(credentials)
plan=json.loads((HERE/'PLAN.json').read_text())

def get(kind,**params):
    response=session.get(BASE+kind,params=params,headers={'Cache-Control':'no-cache'},timeout=40)
    response.raise_for_status()
    return response.json()

def pages(kind,**params):
    items=[]
    while True:
        data=get(kind,**params); items.extend(data.get('items',[]))
        if not data.get('nextPageToken'): return items
        params['pageToken']=data['nextPageToken']

def playlist(pid):
    values=get('playlists',part='snippet,status,contentDetails',id=pid)['items']
    assert len(values)==1 and values[0]['snippet']['channelId']==cfg['channel_id']
    return values[0]

def members(pid):
    return pages('playlistItems',part='snippet,contentDetails,status',playlistId=pid,maxResults=50)

def ids(items): return [item['contentDetails']['videoId'] for item in items]

def now(): return datetime.now(timezone.utc).isoformat()

def main():
    parser=argparse.ArgumentParser(); parser.add_argument('operation',choices=['digital_metadata','digital_add','digital_add_manual','iq_create','iq_add'])
    args=parser.parse_args(); receipt=HERE/(args.operation+'_receipt.json')
    if receipt.exists(): raise SystemExit('Receipt exists: reconcile it read-only; no automatic repeat.')
    mine=get('channels',part='id',mine='true')['items']
    assert len(mine)==1 and mine[0]['id']==cfg['channel_id']==plan['channel_id']
    record={'operation':args.operation,'channel_id':cfg['channel_id'],'started_at':now(),'state':'preflight'}
    kind='playlistItems'; method='POST'; part='snippet'; before=None
    if args.operation=='digital_metadata':
        pid='PLCAXo3w7Gths'; before=playlist(pid)
        assert before['status']['privacyStatus']=='public'
        assert before['snippet']['title']=='Digital Life & Attention'
        description=next(p['description'] for p in plan['playlist_architecture'] if p.get('id')==pid)
        snippet={k:before['snippet'][k] for k in ('title','description','defaultLanguage') if k in before['snippet']}
        snippet.update(description=description,defaultLanguage='en')
        body={'id':pid,'snippet':snippet}; kind='playlists'; method='PUT'
        def valid():
            value=playlist(pid)
            ok=all(value['snippet'].get(k)==v for k,v in snippet.items()) and value['status']==before['status']
            return ok,value
    elif args.operation=='iq_create':
        target=next(p for p in plan['playlist_architecture'] if p.get('key')=='new_iq')
        before=pages('playlists',part='snippet,status',mine='true',maxResults=50)
        assert not any(p['snippet']['title'].casefold()==target['title'].casefold() for p in before)
        body={'snippet':{'title':target['title'],'description':target['description'],'defaultLanguage':'en'},'status':{'privacyStatus':'private'}}
        kind='playlists'; part='snippet,status'
        def valid():
            values=get('playlists',part='snippet,status,contentDetails',id=record['response']['id'])['items']
            if not values: return False,values
            assert len(values)==1 and values[0]['snippet']['channelId']==cfg['channel_id']
            value=values[0]
            ok=all(value['snippet'].get(k)==v for k,v in body['snippet'].items()) and value['status']['privacyStatus']=='private'
            return ok,value
    else:
        if args.operation in ('digital_add','digital_add_manual'):
            if args.operation=='digital_add_manual':
                old=json.loads((HERE/'digital_add_receipt.json').read_text())
                assert old['state']=='rejected_no_membership_observed'
                assert (HERE/'STUDIO_SORTING.md').exists()
            pid='PLCAXo3w7Gths'; vid='WQw7ny9svrk'; expected=['-KW8jgSoEz0']
        else:
            creation=json.loads((HERE/'iq_create_receipt.json').read_text())
            assert creation['state']=='saved_verified'
            pid=creation['response']['id']; vid='xYS2XBeR_Jc'; expected=[]
        owner=playlist(pid); before=members(pid)
        video=get('videos',part='snippet,status',id=vid)['items']
        assert len(video)==1 and video[0]['snippet']['channelId']==cfg['channel_id']
        assert video[0]['status']['privacyStatus']=='public'
        assert ids(before)==expected and vid not in ids(before)
        body={'snippet':{'playlistId':pid,'position':len(before),'resourceId':{'kind':'youtube#video','videoId':vid}}}
        record.update(playlist_before=owner,video_before=video[0])
        def valid():
            value=members(pid)
            return ids(value)==expected+[vid] and len(set(ids(value)))==len(value),value
    record.update(before=before,request={'method':method,'resource':kind,'part':part,'body':body},state='outcome_unknown')
    def save(): receipt.write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
    save()
    # A single mutation; exceptions deliberately retain outcome_unknown.
    response=session.request(method,BASE+kind,params={'part':part},json=body,timeout=40)
    record['http_status']=response.status_code; record['response']=response.json();save()
    response.raise_for_status()
    record['state']='applied_unverified';save()
    for attempt in range(5):
        ok,observed=valid();record.update(after=observed,read_attempts=attempt+1);save()
        if ok:
            record.update(state='saved_verified',verified_at=now());save()
            print(json.dumps({'operation':args.operation,'state':record['state'],'id':record['response'].get('id'),'receipt':str(receipt)}));return
        if attempt<4: time.sleep(2)
    raise SystemExit('Read-back not reconciled; no mutation retry.')

if __name__=='__main__': main()
