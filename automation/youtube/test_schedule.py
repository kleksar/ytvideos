#!/usr/bin/env python3
"""Tests use an in-memory fake session; no network or credentials."""
import json,tempfile,unittest
from pathlib import Path
import schedule
C='UC'+'a'*22;V='b'*11
class Response:
 def __init__(self,data,status=200):self.data=data;self.status_code=status
 def json(self):return self.data
class Fake:
 def __init__(self):
  self.video={'id':V,'etag':'etag1','snippet':{'channelId':C},'status':{'privacyStatus':'private','embeddable':True,'license':'youtube','publicStatsViewable':True,'selfDeclaredMadeForKids':False,'containsSyntheticMedia':True},'processingDetails':{'processingStatus':'succeeded'}};self.puts=0;self.fail=False
 def get(self,url,**kwargs):return Response({'items':[{'id':C}]}) if url.endswith('channels') else Response({'items':[self.video]})
 def put(self,url,**kwargs):
  self.puts+=1
  if self.fail:raise TimeoutError()
  assert kwargs['headers']=={'If-Match':'etag1'}
  self.video['status'].update(kwargs['json']['status']);return Response(self.video)
class Tests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.d=Path(self.tmp.name);self.r=self.d/'upload.json';self.state=self.d/'schedule.json';self.r.write_text(json.dumps({'phase':'complete','video_id':V,'fingerprint':{'channel_id':C,'body':{'status':{'privacyStatus':'private'}}}}));self.s=Fake();self.when='2099-10-29T16:00:00-04:00'
 def run_set(self):return schedule.set_schedule(self.s,C,V,self.when,self.r,self.state,True)
 def test_dst_changes_utc_but_not_local(self):
  p=schedule.plan('2026-10-29T16:00','America/New_York',4);self.assertEqual([x['utc'][11:16] for x in p['slots']],['20:00','20:00','20:00','21:00'])
 def test_ambiguous_local_time_rejected(self):
  with self.assertRaises(schedule.ScheduleError):schedule.local_time('2026-11-01T01:30','America/New_York')
 def test_schedule_and_idempotent_read(self):
  self.assertEqual(self.run_set()['result'],'scheduled');self.assertEqual(self.run_set()['result'],'already_scheduled');self.assertEqual(self.s.puts,1);self.assertEqual(json.loads(self.state.read_text())['state'],'confirmed');self.assertTrue(self.s.video['status']['containsSyntheticMedia'])
 def test_uncertain_write_blocks_retry(self):
  self.s.fail=True
  with self.assertRaises(schedule.ScheduleError):self.run_set()
  self.s.fail=False
  with self.assertRaises(schedule.ScheduleError):self.run_set()
  self.assertEqual(self.s.puts,1)
 def test_existing_different_schedule_rejected(self):
  self.s.video['status']['publishAt']='2099-11-01T21:00:00Z'
  with self.assertRaises(schedule.ScheduleError):self.run_set()
  self.assertEqual(self.s.puts,0)
 def test_wrong_channel_or_public_rejected(self):
  self.s.video['snippet']['channelId']='UC'+'z'*22
  with self.assertRaises(schedule.ScheduleError):self.run_set()
  self.s.video['snippet']['channelId']=C;self.s.video['status']['privacyStatus']='public'
  with self.assertRaises(schedule.ScheduleError):self.run_set()
  self.assertEqual(self.s.puts,0)
 def test_past_rejected(self):
  with self.assertRaises(schedule.ScheduleError):schedule.set_schedule(self.s,C,V,'2001-01-01T00:00:00Z',self.r,self.state,True)
  self.assertEqual(self.s.puts,0)
if __name__=='__main__':unittest.main()
