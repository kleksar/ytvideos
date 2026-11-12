"""One authorized description write, guarded by accepted bytes and a durable receipt."""
import argparse, hashlib, importlib.util, json, time
from datetime import datetime, timezone
from pathlib import Path
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import AuthorizedSession
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
OUT=HERE/'rollout_20261102'
BASE='https://www.googleapis.com/youtube/v3/'
MUTABLE=('title','description','tags','categoryId','defaultLanguage','defaultAudioLanguage')
def main():
    p=argparse.ArgumentParser();p.add_argument('video_id');a=p.parse_args()
    dest=OUT/(a.video_id+'.receipt.json')
    assert not dest.exists(),'Existing receipt: reconcile with read-only calls; never repeat blindly.'
    accepted=json.loads((OUT/'ACCEPTANCE.json').read_text())
    decision=next(x for x in accepted['videos'] if x['id']==a.video_id)
    raw=(ROOT/decision['path']).read_bytes()
    assert hashlib.sha256(raw).hexdigest()==decision['sha256'],'Accepted text changed.'
    proposed=raw.decode('utf-8')
    baseline=(HERE/'texts'/f'{a.video_id}.before.txt').read_bytes().decode('utf-8')
    manifest=json.loads((HERE/'texts'/f'{a.video_id}.protected.json').read_text())
    spec=importlib.util.spec_from_file_location('validator',ROOT/'.agents/skills/ytv-youtube-descriptions/scripts/validate_description.py')
    validator=importlib.util.module_from_spec(spec);spec.loader.exec_module(validator)
    cfg=json.loads((ROOT/'stories/automation/channels.json').read_text())['paper_detour']
    credentials=Credentials.from_authorized_user_file(cfg['playlist_token_file'])
    assert 'https://www.googleapis.com/auth/youtube.force-ssl' in credentials.scopes
    session=AuthorizedSession(credentials)
    def get(kind,**params):
        r=session.get(BASE+kind,params=params,headers={'Cache-Control':'no-cache'},timeout=40);r.raise_for_status();return r.json()
    mine=get('channels',part='id',mine='true')['items']
    assert len(mine)==1 and mine[0]['id']==cfg['channel_id']=='UCMVfdfaNxV3ZkI3_J3Eejzw'
    def read():
        items=get('videos',part='snippet,status,contentDetails,localizations',id=a.video_id)['items']
        assert len(items)==1 and items[0]['snippet']['channelId']==cfg['channel_id']
        return items[0]
    before=read()
    assert before['snippet']['description']==baseline,'Concurrent description change: stop and reconcile.'
    assert before['status']['privacyStatus']=='public'
    validation=validator.validate(proposed,manifest,before['snippet']['description'])
    assert validation['valid'],validation['errors']
    if a.video_id=='0RaC4t7yn5o':
        state=(OUT/'RADIO_AB_BEFORE.txt').read_text()
        assert 'Тестирование…' in state and 'How People Got Computer Programs From the Radio' in state
    snippet={k:before['snippet'][k] for k in MUTABLE if k in before['snippet']};snippet['description']=proposed
    record={'video_id':a.video_id,'channel_id':cfg['channel_id'],'acceptance':decision,'before':before,'validation':validation,'request':{'method':'PUT','resource':'videos','part':'snippet','body':{'id':a.video_id,'snippet':snippet}},'started_at':datetime.now(timezone.utc).isoformat(),'state':'outcome_unknown'}
    def save():dest.write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
    with dest.open('x') as f:f.write(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
    response=session.put(BASE+'videos',params={'part':'snippet'},json=record['request']['body'],timeout=40)
    record.update(http_status=response.status_code,response=response.json());save();response.raise_for_status()
    record['state']='applied_unverified';save()
    for attempt in range(5):
        after=read();record.update(after=after,read_attempts=attempt+1);save()
        actual={k:after['snippet'][k] for k in MUTABLE if k in after['snippet']}
        if actual==snippet and all(after[k]==before[k] for k in ('status','contentDetails')) and after['snippet'].get('thumbnails')==before['snippet'].get('thumbnails'):
            record.update(state='saved_verified',verified_at=datetime.now(timezone.utc).isoformat(),localizations_changed=before.get('localizations')!=after.get('localizations'))
            save();print(json.dumps({'id':a.video_id,'state':record['state'],'protected_blocks':len(validation['protected_blocks']),'localizations_changed':record['localizations_changed']}));return
        if attempt<4:time.sleep(2)
    raise SystemExit('Read-back mismatch: no repeated mutation.')
if __name__=='__main__':main()
