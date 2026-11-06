import copy, hashlib, json, tempfile, unittest
from pathlib import Path
from unittest.mock import patch
import publish_public as m

CHANNEL='UC'+'a'*22
VIDEO='a'*11
PLAYLIST='PL1234'

def video():
    return {'id':VIDEO,'etag':'etag1','snippet':{'channelId':CHANNEL},
      'status':{'privacyStatus':'private','embeddable':True,'license':'youtube',
                'publicStatsViewable':True,'selfDeclaredMadeForKids':False},
      'processingDetails':{'processingStatus':'succeeded'}}

class Response:
    status_code=200
class Session:
    def __init__(self): self.v=video();self.writes=0
    def put(self,url,params,json,headers,**kw):
        assert headers=={'If-Match':'etag1'}
        self.writes+=1;self.v['status'].update(json['status']);return Response()

class PublicTest(unittest.TestCase):
    def setUp(self):
        caption_reads = patch('schedule.get_json', side_effect=lambda *args: {'items': self.items(*args)})
        caption_reads.start()
        self.addCleanup(caption_reads.stop)
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        root=Path(self.tmp.name);self.upload=root/'upload.json';self.caption=root/'caption.json';self.state=root/'state.json'
        self.srt=root/'captions.srt';self.srt.write_text('1\n00:00:00,000 --> 00:00:01,000\nHello\n')
        self.upload.write_text(json.dumps({'phase':'complete','video_id':VIDEO,'fingerprint':{'channel_id':CHANNEL,'body':{'status':{'privacyStatus':'private','containsSyntheticMedia':True}}}}))
        self.caption.write_text(json.dumps({'state':'confirmed','channel_id':CHANNEL,'video_id':VIDEO,'caption_id':'cap1','srt_sha256':hashlib.sha256(self.srt.read_bytes()).hexdigest()}))
    def args(self): return (CHANNEL,VIDEO,PLAYLIST,'en',self.srt,self.upload,self.caption,self.state)
    def items(self,session,resource,params):
        if resource=='captions':return [{'id':'cap1','snippet':{'videoId':VIDEO,'language':'en','isDraft':False,'status':'serving'}}]
        if resource=='playlists':return [{'id':PLAYLIST,'snippet':{'channelId':CHANNEL}}]
        if resource=='playlistItems':return [{'id':'item','contentDetails':{'videoId':VIDEO}}]
        raise AssertionError(resource)
    def test_valid_private_upload_publishes_once_and_confirms(self):
        sess=Session()
        with patch.object(m,'read',side_effect=lambda *a: copy.deepcopy(sess.v)),patch.object(m,'read_items',side_effect=self.items):
            result=m.publish(sess,*self.args())
            self.assertEqual(result['privacy'],'public');self.assertEqual(sess.writes,1)
            self.assertTrue(sess.v['status']['containsSyntheticMedia'])
            self.assertEqual(json.loads(self.state.read_text())['state'],'confirmed')
            with self.assertRaises(m.ScheduleError):m.publish(sess,*self.args())
            self.assertEqual(sess.writes,1)
    def test_mismatched_caption_blocks_before_write(self):
        sess=Session(); c=json.loads(self.caption.read_text());c['srt_sha256']='other';self.caption.write_text(json.dumps(c))
        with patch.object(m,'read',side_effect=lambda *a:copy.deepcopy(sess.v)),patch.object(m,'read_items',side_effect=self.items):
            with self.assertRaises(m.ScheduleError):m.publish(sess,*self.args())
        self.assertEqual(sess.writes,0);self.assertFalse(self.state.exists())
    def test_unprocessed_or_scheduled_blocks(self):
        for mode in ('processing','schedule'):
            sess=Session()
            if mode=='processing':sess.v['processingDetails']['processingStatus']='processing'
            else:sess.v['status']['publishAt']='2099-01-01T00:00:00Z'
            with patch.object(m,'read',side_effect=lambda *a:copy.deepcopy(sess.v)),patch.object(m,'read_items',side_effect=self.items):
                with self.assertRaises(m.ScheduleError):m.publish(sess,*self.args())
            self.assertEqual(sess.writes,0);self.assertFalse(self.state.exists())
    def test_changed_etag_after_reservation_blocks_put(self):
        sess=Session(); calls=0
        def read(*a):
            nonlocal calls
            calls+=1;x=copy.deepcopy(sess.v)
            if calls>1:x['etag']='changed'
            return x
        with patch.object(m,'read',side_effect=read),patch.object(m,'read_items',side_effect=self.items):
            with self.assertRaises(m.ScheduleError):m.publish(sess,*self.args())
        self.assertEqual(sess.writes,0);self.assertEqual(json.loads(self.state.read_text())['state'],'outcome_unknown')
    def test_uncertain_put_reserves_receipt_and_blocks_retry(self):
        sess=Session();sess.put=lambda *a,**k: (_ for _ in ()).throw(TimeoutError())
        with patch.object(m,'read',side_effect=lambda *a:copy.deepcopy(sess.v)),patch.object(m,'read_items',side_effect=self.items):
            with self.assertRaises(m.ScheduleError):m.publish(sess,*self.args())
            self.assertEqual(json.loads(self.state.read_text())['state'],'outcome_unknown')
            with self.assertRaises(m.ScheduleError):m.publish(sess,*self.args())
    def test_bad_playlist_and_nonserving_caption_block(self):
        for resource in ('playlists','captions'):
            sess=Session()
            def broken(session,name,params):
                if name==resource:return []
                return self.items(session,name,params)
            with patch.object(m,'read',side_effect=lambda *a:copy.deepcopy(sess.v)),patch.object(m,'read_items',side_effect=broken),patch('schedule.get_json',side_effect=lambda *args: {'items': broken(*args)}):
                with self.assertRaises(m.ScheduleError):m.publish(sess,*self.args())
            self.assertEqual(sess.writes,0)

if __name__=='__main__':unittest.main()
