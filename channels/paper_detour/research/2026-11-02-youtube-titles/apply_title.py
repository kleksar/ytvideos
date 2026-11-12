"""Apply one internally accepted title correction from this catalog's AUDIT.json."""
import argparse
import json
import re
import time
from datetime import datetime, timezone
from pathlib import Path
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import AuthorizedSession

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
BASE='https://www.googleapis.com/youtube/v3/'
MUTABLE=('title','description','tags','categoryId','defaultLanguage','defaultAudioLanguage')

def main():
    parser=argparse.ArgumentParser();parser.add_argument('video_id');args=parser.parse_args()
    assert args.video_id!='0RaC4t7yn5o','Protected active title/thumbnail experiment.'
    dest=HERE/('TITLE_'+args.video_id+'_RECEIPT.json')
    if dest.exists():raise SystemExit('Receipt exists. Read and reconcile; no automatic repeated write.')
    audit=json.loads((HERE/'AUDIT.json').read_text())
    row=next(v for v in audit['videos'] if v['id']==args.video_id)
    assert row['decision']=='revise' and row['content_status']=='grounded'
    assert (HERE/row['consultation']).exists()
    old=row['before'];new=row['selected_title']
    assert new and len(new)<=100 and '<' not in new and '>' not in new
    assert re.findall(r'(?<!\S)#[^\s#]+',old)==re.findall(r'(?<!\S)#[^\s#]+',new)
    cfg=json.loads((ROOT/'stories/automation/channels.json').read_text())['paper_detour']
    credentials=Credentials.from_authorized_user_file(cfg['playlist_token_file'])
    assert 'https://www.googleapis.com/auth/youtube.force-ssl' in credentials.scopes
    session=AuthorizedSession(credentials)
    def get(kind,**params):
        r=session.get(BASE+kind,params=params,headers={'Cache-Control':'no-cache'},timeout=40);r.raise_for_status();return r.json()
    mine=get('channels',part='id',mine='true')['items']
    assert len(mine)==1 and mine[0]['id']==cfg['channel_id']==audit['channel_id']
    def read():
        values=get('videos',part='snippet,status,contentDetails,localizations',id=args.video_id)['items']
        assert len(values)==1 and values[0]['snippet']['channelId']==cfg['channel_id']
        return values[0]
    before=read()
    assert before['snippet']['title']==old,'Concurrent title change. Reconcile this video before mutation.'
    assert before['status']['privacyStatus']=='public'
    snippet={k:before['snippet'][k] for k in MUTABLE if k in before['snippet']}
    snippet['title']=new
    record={'video_id':args.video_id,'channel_id':cfg['channel_id'],'before':before,'request':{'method':'PUT','resource':'videos','part':'snippet','body':{'id':args.video_id,'snippet':snippet}},'started_at':datetime.now(timezone.utc).isoformat(),'state':'outcome_unknown'}
    def save():dest.write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
    with dest.open('x') as stream:stream.write(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
    # One write only. Any error retains a receipt for read-only reconciliation.
    response=session.put(BASE+'videos',params={'part':'snippet'},json=record['request']['body'],timeout=40)
    record.update(http_status=response.status_code,response=response.json());save();response.raise_for_status()
    record['state']='applied_unverified';save()
    for attempt in range(5):
        after=read();record.update(after=after,read_attempts=attempt+1);save()
        actual={k:after['snippet'][k] for k in MUTABLE if k in after['snippet']}
        if actual==snippet and after['status']==before['status'] and after['contentDetails']==before['contentDetails']:
            record.update(state='saved_verified',verified_at=datetime.now(timezone.utc).isoformat(),localizations_changed=before.get('localizations')!=after.get('localizations'))
            save();print(json.dumps({'id':args.video_id,'title':new,'state':record['state'],'localizations_changed':record['localizations_changed']},ensure_ascii=False));return
        if attempt<4:time.sleep(2)
    raise SystemExit('Read-back did not reconcile; do not repeat the mutation.')

if __name__=='__main__':main()
