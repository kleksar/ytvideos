#!/usr/bin/env python3
"""Publish the user-requested 014 Russian video after all checks; never retry unknown writes."""
import argparse,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[4]/'automation'/'youtube'))
import schedule,upload_caption_ru as upload_caption
from google.auth.transport.requests import AuthorizedSession
from google.oauth2.credentials import Credentials
CHANNEL='UCY0Wa9sdQrvFgbv7B-AXCyg'
PLAYLIST='PLcuh6srN6l_c'

def main():
 p=argparse.ArgumentParser();p.add_argument('--video-id',required=True);p.add_argument('--token',required=True);p.add_argument('--upload-receipt',required=True);p.add_argument('--state',required=True);a=p.parse_args()
 session=AuthorizedSession(Credentials.from_authorized_user_file(a.token,[schedule.SCOPE]))
 schedule.verify_upload_receipt(a.upload_receipt,CHANNEL,a.video_id)
 v=schedule.read(session,CHANNEL,a.video_id);st=v.get('status',{})
 if st.get('privacyStatus')!='private' or st.get('publishAt') or v.get('processingDetails',{}).get('processingStatus')!='succeeded':raise RuntimeError('Video is not unscheduled, private and fully processed')
 for k in ('embeddable','license','publicStatsViewable'):
  if k not in st:raise RuntimeError('Cannot preserve status settings')
 tracks=upload_caption.english_manual(upload_caption.captions(session,a.video_id))
 if len(tracks)!=1 or tracks[0].get('snippet',{}).get('status')!='serving' or tracks[0].get('snippet',{}).get('isDraft'):raise RuntimeError('Russian track not uniquely serving')
 receipt=upload_caption.STATE/(CHANNEL+'_'+a.video_id+'_ru.json')
 saved=json.loads(receipt.read_text())
 if saved.get('state')!='confirmed' or saved.get('caption_id')!=tracks[0]['id'] or saved.get('channel_id')!=CHANNEL or saved.get('video_id')!=a.video_id:raise RuntimeError('Caption receipt does not match serving track')
 items=upload_caption.get_items(session,'playlistItems',{'part':'contentDetails','playlistId':PLAYLIST,'maxResults':50})
 if sum(i.get('contentDetails',{}).get('videoId')==a.video_id for i in items)!=1:raise RuntimeError('Video not uniquely present in Stories playlist')
 etag=v.get('etag')
 if not etag:raise RuntimeError('Missing video ETag')
 body={k:st[k] for k in schedule.WRITABLE if k in st};body['privacyStatus']='public'
 schedule.reserve(a.state,{'state':'outcome_unknown','channel_id':CHANNEL,'video_id':a.video_id,'privacy':'public'})
 fresh=schedule.read(session,CHANNEL,a.video_id)
 if fresh.get('etag')!=etag or fresh.get('status')!=st:raise RuntimeError('Video changed before update; inspect receipt')
 try:r=session.put(schedule.API+'videos',params={'part':'status'},json={'id':a.video_id,'status':body},headers={'If-Match':etag},timeout=60,allow_redirects=False)
 except Exception:raise RuntimeError('Update outcome unknown; inspect before retry') from None
 if r.status_code!=200:raise RuntimeError(f'Update HTTP {r.status_code}; inspect before retry')
 final=schedule.read(session,CHANNEL,a.video_id);new=final.get('status',{})
 if new.get('privacyStatus')!='public':raise RuntimeError('Public status not confirmed; inspect before retry')
 if any(k in new and new[k]!=val for k,val in body.items() if k!='privacyStatus'):raise RuntimeError('Other settings changed; inspect')
 schedule.mark_done(a.state,{'state':'confirmed','channel_id':CHANNEL,'video_id':a.video_id,'privacy':'public'})
 print(json.dumps(schedule.summary(final)))
if __name__=='__main__':
 try:main()
 except Exception as e:print('Error:',str(e) if isinstance(e,(RuntimeError,schedule.ScheduleError,upload_caption.CaptionError)) else type(e).__name__,file=sys.stderr);sys.exit(1)
