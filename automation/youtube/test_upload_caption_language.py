import copy,json,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
import upload_caption_language as m
CHANNEL='UC'+'a'*22
VIDEO='a'*11
class Response:
 def __init__(self,body,status=200):self.body=body;self.status_code=status
 def json(self):return self.body
class Session:
 def __init__(self):self.items=[];self.posts=0
 def post(self,*a,**k):
  self.posts+=1; self.items=[{'id':'caption','snippet':{'language':'ru','videoId':VIDEO,'isDraft':False,'status':'serving','trackKind':'standard'}}]
  return Response({'id':'caption'},201)
class TestLanguageCaption(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);base=Path(self.tmp.name)
  self.srt=base/'x.srt';self.srt.write_text('1\n00:00:00,000 --> 00:00:01,000\nТест\n')
  self.receipt=base/'upload.json';self.receipt.write_text(json.dumps({'phase':'complete','video_id':VIDEO,'fingerprint':{'channel_id':CHANNEL,'body':{'status':{'privacyStatus':'private'}}}}));self.base=base
 def run_upload(self,s):return m.upload(s,CHANNEL,VIDEO,'ru',self.srt,self.receipt,state_dir=self.base,sleep=lambda _:None)
 def test_upload_then_repeat_checks_receipt_without_duplicate(self):
  s=Session()
  with patch.object(m,'verify',return_value={}),patch.object(m,'get_items',side_effect=lambda *a,**k:copy.deepcopy(s.items)):
   x=self.run_upload(s);self.assertEqual(x['status'],'serving');self.assertEqual(s.posts,1)
   y=self.run_upload(s);self.assertEqual(y['result'],'existing_confirmed');self.assertEqual(s.posts,1)
 def test_existing_track_without_receipt_blocks(self):
  s=Session();s.items=[{'id':'old','snippet':{'language':'ru','trackKind':'standard'}}]
  with patch.object(m,'verify',return_value={}),patch.object(m,'get_items',side_effect=lambda *a,**k:copy.deepcopy(s.items)):
   with self.assertRaises(m.CaptionError):self.run_upload(s)
  self.assertEqual(s.posts,0)
 def test_timeout_receipt_prevents_blind_retry(self):
  s=Session();s.post=lambda *a,**k:(_ for _ in ()).throw(TimeoutError())
  with patch.object(m,'verify',return_value={}),patch.object(m,'get_items',return_value=[]):
   with self.assertRaises(m.CaptionError):self.run_upload(s)
   with self.assertRaises(m.CaptionError):self.run_upload(s)
  state=self.base/(CHANNEL+'_'+VIDEO+'_ru.json');self.assertEqual(json.loads(state.read_text())['state'],'outcome_unknown')
if __name__=='__main__':unittest.main()
