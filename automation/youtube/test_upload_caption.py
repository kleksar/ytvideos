import json
import tempfile
import unittest
from pathlib import Path
import upload_caption as u

CHANNEL='UC'+'a'*22
VIDEO='b'*11
SRT='1\n00:00:00,000 --> 00:00:01,000\nFirst\n\n2\n00:00:01,000 --> 00:00:02,000\nSecond\n'
class Response:
 def __init__(self, data, status=200): self.data=data; self.status_code=status
 def json(self): return self.data
class Session:
 def __init__(self): self.tracks=[];self.posts=0;self.privacy='private';self.owner=CHANNEL;self.processing='succeeded';self.timeout=False
 def get(self,url,params,**kwargs):
  endpoint=url.rsplit('/',1)[-1]
  if endpoint=='channels': return Response({'items':[{'id':self.owner}]})
  if endpoint=='videos': return Response({'items':[{'id':VIDEO,'snippet':{'channelId':self.owner},'status':{'privacyStatus':self.privacy},'processingDetails':{'processingStatus':self.processing}}]})
  if endpoint=='captions': return Response({'items':list(self.tracks)})
  raise AssertionError(endpoint)
 def post(self,*args,**kwargs):
  self.posts+=1
  if self.timeout: raise TimeoutError()
  self.tracks.append({'id':'caption1','snippet':{'videoId':VIDEO,'language':'en','trackKind':'standard','status':'serving','isDraft':False}})
  return Response({'id':'caption1'})
class CaptionTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.base=Path(self.tmp.name);self.srt=self.base/'test.srt';self.srt.write_text(SRT);self.state=self.base/'state';self.receipt=self.base/'receipt.json';self.receipt.write_text(json.dumps({'phase':'complete','video_id':VIDEO,'fingerprint':{'channel_id':CHANNEL,'body':{'status':{'privacyStatus':'private'}}}}));self.session=Session()
 def upload(self): return u.upload(self.session,CHANNEL,VIDEO,self.srt,self.receipt,self.state,sleep=lambda n:None)
 def test_success_idempotent(self):
  self.assertEqual(self.upload()['result'],'uploaded');self.assertEqual(self.upload()['result'],'existing_confirmed');self.assertEqual(self.session.posts,1)
 def test_timeout_blocks_retry(self):
  self.session.timeout=True
  with self.assertRaises(u.CaptionError):self.upload()
  self.session.timeout=False
  with self.assertRaisesRegex(u.CaptionError,'outcome unknown'):self.upload()
  self.assertEqual(self.session.posts,1)
 def test_existing_manual_track_blocks(self):
  self.session.tracks=[{'id':'other','snippet':{'language':'en-US','trackKind':'standard'}}]
  with self.assertRaisesRegex(u.CaptionError,'already exists'):self.upload()
  self.assertEqual(self.session.posts,0)
 def test_asr_track_does_not_block(self):
  self.session.tracks=[{'id':'asr','snippet':{'language':'en','trackKind':'ASR'}}]
  self.assertEqual(self.upload()['result'],'uploaded')
 def test_public_and_wrong_channel_block(self):
  self.session.privacy='public'
  with self.assertRaisesRegex(u.CaptionError,'not private'):self.upload()
  self.session.privacy='private';self.session.owner='UC'+'c'*22
  with self.assertRaisesRegex(u.CaptionError,'channel does not match'):self.upload()
  self.assertEqual(self.session.posts,0)
 def test_processing_pending_blocks(self):
  self.session.processing='processing'
  with self.assertRaisesRegex(u.CaptionError,'processing'):self.upload()
  self.assertEqual(self.session.posts,0)
 def test_modified_srt_blocks_reuse(self):
  self.upload();self.srt.write_text(SRT.replace('First','Changed'))
  with self.assertRaisesRegex(u.CaptionError,'does not match'):self.upload()
  self.assertEqual(self.session.posts,1)
 def test_overlapping_cues_block(self):
  self.srt.write_text(SRT.replace('00:00:01,000 --> 00:00:02,000','00:00:00,500 --> 00:00:02,000'))
  with self.assertRaisesRegex(u.CaptionError,'overlap'):self.upload()
  self.assertEqual(self.session.posts,0)
 def test_wrong_upload_receipt_blocks(self):
  self.receipt.write_text('{}')
  with self.assertRaisesRegex(u.CaptionError,'receipt does not match'):self.upload()
  self.assertEqual(self.session.posts,0)
if __name__=='__main__':unittest.main()
