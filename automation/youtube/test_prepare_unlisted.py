import copy
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import prepare_unlisted as m

CHANNEL='UC'+'a'*22
VIDEO='a'*11
FILM='b'*11
PLAYLIST='PL1234'

def video(privacy='private'):
    return {'id': VIDEO, 'etag': 'etag1', 'snippet': {'channelId': CHANNEL,
      'title': 'Title', 'categoryId': '27', 'description': 'Existing description',
      'defaultLanguage': 'en', 'defaultAudioLanguage': 'en', 'tags': ['history']},
      'status': {'privacyStatus': privacy, 'embeddable': True, 'license': 'youtube',
                 'publicStatsViewable': True, 'selfDeclaredMadeForKids': False,
                 'containsSyntheticMedia': True},
      'processingDetails': {'processingStatus': 'succeeded'}}

class Response:
    status_code=200

class Session:
    def __init__(self, initial): self.v=copy.deepcopy(initial); self.writes=0
    def put(self, url, params, json, headers, **kw):
        assert headers == {'If-Match':'etag1'}
        self.writes += 1
        self.v[params['part']].update(json[params['part']])
        return Response()

class TestChanges(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup)
        self.state=Path(self.tmp.name)/'receipt.json'
    def test_privacy_preserves_status_and_verifies(self):
        sess=Session(video())
        with patch.object(m,'read',side_effect=lambda *a: copy.deepcopy(sess.v)):
            result=m.update(sess, CHANNEL, VIDEO, self.state, 'privacy')
        self.assertEqual(sess.writes, 1)
        self.assertEqual(sess.v['status']['privacyStatus'],'unlisted')
        self.assertTrue(sess.v['status']['containsSyntheticMedia'])
        self.assertEqual(result['state'],'confirmed')
        self.assertEqual(result['after']['selfDeclaredMadeForKids'],False)
    def test_description_preserves_language_and_checks_film(self):
        sess=Session(video('unlisted'))
        movie=video('unlisted');movie['id']=FILM
        def read(_,__,ident): return copy.deepcopy(movie if ident == FILM else sess.v)
        with patch.object(m,'read',side_effect=read):
            m.update(sess, CHANNEL, VIDEO, self.state, 'description', FILM)
        self.assertIn('https://www.youtube.com/watch?v='+FILM,sess.v['snippet']['description'])
        self.assertEqual(sess.v['snippet']['defaultAudioLanguage'],'en')
        self.assertEqual(sess.v['snippet']['tags'],['history'])
    def test_unsafe_or_uncertain_conditions_block(self):
        sess=Session(video())
        movie=video('private');movie['id']=FILM
        def read(_,__,ident): return copy.deepcopy(movie if ident == FILM else sess.v)
        with patch.object(m,'read',side_effect=read):
            with self.assertRaises(m.ScheduleError):m.update(sess,CHANNEL,VIDEO,self.state,'description',FILM)
        self.assertEqual(sess.writes,0)
        sess.v['status']['publishAt']='2026-11-03T16:00:00Z'
        with patch.object(m,'read',side_effect=lambda *a: copy.deepcopy(sess.v)):
            with self.assertRaises(m.ScheduleError):m.update(sess,CHANNEL,VIDEO,self.state,'privacy')
        self.assertEqual(sess.writes,0)
    def test_uncertain_put_keeps_receipt_and_blocks_retry(self):
        sess=Session(video())
        def unknown(*a,**k): raise TimeoutError()
        sess.put=unknown
        with patch.object(m,'read',side_effect=lambda *a: copy.deepcopy(sess.v)):
            with self.assertRaises(m.ScheduleError):m.update(sess,CHANNEL,VIDEO,self.state,'privacy')
            self.assertIn('outcome_unknown',self.state.read_text())
            with self.assertRaises(m.ScheduleError):m.update(sess,CHANNEL,VIDEO,self.state,'privacy')
    def test_playlist_existing_does_not_write(self):
        class S:
            def post(self,*a,**k): raise AssertionError('must not post')
        def items(_, resource, params):
            if resource=='playlists': return [{'id': PLAYLIST,'snippet':{'channelId':CHANNEL}}]
            return [{'id':'item','contentDetails':{'videoId':VIDEO}}]
        with patch.object(m,'read',return_value=video('unlisted')), patch.object(m,'read_items',side_effect=items):
            result=m.add_playlist(S(),CHANNEL,VIDEO,PLAYLIST,self.state)
        self.assertEqual(result['result'],'already_present')
        self.assertFalse(self.state.exists())

if __name__=='__main__':unittest.main()
