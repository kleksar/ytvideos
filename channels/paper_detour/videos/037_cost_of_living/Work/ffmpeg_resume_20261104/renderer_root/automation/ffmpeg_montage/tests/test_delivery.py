import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from test_montage import m, bind_plan

ROOT = m.ROOT
spec = importlib.util.spec_from_file_location('upload_under_test', ROOT/'stories/automation/youtube/upload.py')
u = importlib.util.module_from_spec(spec); spec.loader.exec_module(u)
CHANNEL = json.loads((ROOT/'stories/automation/channels.json').read_text())['paper_detour']['channel_id']
META = {'title':'Fixture','description':'Fixture','category_id':'22','language':'en','made_for_kids':False}


class NoNetwork:
    def __getattr__(self, name):
        raise AssertionError('Readiness failure reached network: ' + name)


class DeliveryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.p = Path(self.temp.name)
        (self.p/'image.png').write_bytes(b'image identity fixture')
        (self.p/'words.json').write_text(json.dumps([
            {'text':'Sailors','start':.11,'end':.3},
            {'text':'came','start':.5,'end':.7},
            {'text':'home.','start':1.,'end':1.2}]))
        self.plan = bind_plan({'channel':'paper','format':'short','canvas':[720,1280],
                              'audio':'audio.m4a','subtitles':{'mode':'words','words':'words.json'},
                              'scenes':[{'image':'image.png','start_frame':0,'end_frame':120,
                                         'direction':'left_to_right','zoom':'in'}]},self.p)
        self.manifest=self.p/'plan.json';self.manifest.write_text(json.dumps(self.plan))
        self.work=self.p/'work';self.work.mkdir()
        m.caption_sequence(self.plan,self.p,self.work,[720,1280],120)
        self.contract=json.loads((self.work/'subtitle_contract.json').read_text())
        self.video=self.p/'review.mp4';self.video.write_bytes(b'encoded file identity fixture')
        m.delivery.write_receipt(self.video,'paper',self.contract,m.delivery.render_inputs(self.manifest,self.plan,self.p))
        self.receipt=Path(str(self.video)+'.delivery.json')

    def tearDown(self):self.temp.cleanup()

    def mark_reviewed(self):
        # Explicit synthetic evidence for gate tests, never a production review.
        evidence=self.p/'review-evidence.txt';evidence.write_text('Synthetic test evidence only.')
        data=json.loads(self.receipt.read_text())
        for check in data['review']['checks'].values():
            check.update(status='PASS',reviewer='test fixture',method='synthetic gate test',coverage='fixture only',evidence=m.delivery.file_record(evidence))
        data['acceptance']={'accepted':True,'media_sha256':m.delivery.sha256(self.video),'evidence':m.delivery.file_record(evidence)}
        self.receipt.write_text(json.dumps(data))

    def rejected_before_network(self, pattern):
        with self.assertRaisesRegex(u.UploadError,pattern):
            u.upload(NoNetwork(),self.video,META,CHANNEL,self.p/'state.json')
        self.assertFalse((self.p/'state.json').exists())

    def test_missing_and_unreviewed_receipt_fail_before_network(self):
        self.rejected_before_network('review incomplete')
        self.receipt.unlink();self.rejected_before_network('Missing delivery')

    def test_complete_evidence_and_exact_media_pass_local_gate(self):
        self.mark_reviewed()
        m.delivery.validate_release(self.video,CHANNEL)

    def test_changed_audio_text_map_profile_image_or_plan_is_stale(self):
        self.mark_reviewed()
        for path in (self.p/'audio.m4a',self.p/'transcript.txt',self.p/'words.json',self.p/'image.png',self.manifest):
            with self.subTest(path=path.name):
                original=path.read_bytes();path.write_bytes(original+b' ')
                self.rejected_before_network('Stale delivery input')
                path.write_bytes(original)
        data=json.loads(self.receipt.read_text())
        data['subtitles']['profiles'][0]['sha256']='0'*64
        self.receipt.write_text(json.dumps(data));self.rejected_before_network('Stale delivery input')

    def test_changed_media_acceptance_or_requirements_fail(self):
        self.mark_reviewed();original=self.video.read_bytes();self.video.write_bytes(b'replacement')
        self.rejected_before_network('does not match');self.video.write_bytes(original)
        data=json.loads(self.receipt.read_text());data['acceptance']['media_sha256']='0'*64
        self.receipt.write_text(json.dumps(data));self.rejected_before_network('User acceptance')
        data['open_requirements']=['finish requested change']
        self.receipt.write_text(json.dumps(data));self.rejected_before_network('remain open')

    def test_missing_speed_or_wrong_speed_fails_preparation(self):
        for value in (None,1.,True,float('nan')):
            with self.subTest(value=value):
                self.plan['audio_contract']['applied_speed']=value
                with self.assertRaisesRegex(ValueError,'voice speed'):
                    m.delivery.validate_words(self.plan,self.p,120)

    def test_unbound_stale_and_frame_colliding_maps_fail(self):
        path=self.p/'words.json';original=path.read_text()
        for field in ('audio_sha256','transcript_sha256'):
            data=json.loads(original);data[field]='0'*64;path.write_text(json.dumps(data))
            with self.assertRaises(ValueError):m.delivery.validate_words(self.plan,self.p,120)
        data=json.loads(original);data['words'][1]['text']='changed';path.write_text(json.dumps(data))
        with self.assertRaisesRegex(ValueError,'transcript'):m.delivery.validate_words(self.plan,self.p,120)
        data=json.loads(original);data['words'][0].update(start=.111,end=.112);data['words'][1].update(start=.113,end=.114);path.write_text(json.dumps(data))
        with self.assertRaisesRegex(ValueError,'collide'):m.delivery.validate_words(self.plan,self.p,120)

    def test_continuity_highlight_events_and_draft_semantics(self):
        groups=json.loads((self.work/'caption_groups.json').read_text())
        intervals=groups['display_intervals']
        self.assertEqual(intervals[0]['start_frame'],0);self.assertEqual(intervals[-1]['end_frame'],120)
        self.assertTrue(all(a['end_frame']==b['start_frame'] for a,b in zip(intervals,intervals[1:])))
        self.assertEqual([event['frame'] for event in groups['word_events']],[0,4,15,30])
        self.assertEqual(groups['status'],'REVIEW_REQUIRED')
        self.assertEqual(groups['grouping_source'],'automatic_draft')
        self.assertTrue(m.grouping.boundary_warnings([[{'text':'wave'},{'text':'of'},{'text':'the'}],[{'text':'plague.'}]]))

    def test_prepare_uses_same_contract_without_video_encoding(self):
        # No valid media/PNG is needed: prepare validates identities, tokens and
        # actual font pixels. It must not start FFmpeg or infer audible review.
        output=self.p/'not-rendered.mp4';work=self.p/'prepared'
        subprocess.run([sys.executable,str(m.HERE/'montage.py'),str(self.manifest),'--output',str(output),
                        '--work-dir',str(work),'--prepare-subtitles'],check=True,capture_output=True)
        self.assertFalse(output.exists())
        self.assertEqual(json.loads((work/'subtitle_contract.json').read_text()),self.contract)
        self.assertTrue(all(c['status']=='UNVERIFIED' for c in json.loads((work/'subtitle_review.json').read_text())['checks'].values()))

    def test_visual_review_binding_changes_with_scene_and_motion(self):
        import copy
        plan=copy.deepcopy(self.plan)
        plan['scenes'][0]['zoom']='out'
        changed=m.delivery.subtitle_contract(plan,self.p,[720,1280],120,self.contract['groups'],self.contract['resolved'])
        self.assertNotEqual(m.delivery.fingerprint(changed),m.delivery.fingerprint(self.contract))
        inputs=m.delivery.render_inputs(self.manifest,self.plan,self.p)
        with self.assertRaisesRegex(ValueError,'review is stale'):
            m.delivery.write_receipt(self.p/'new.mp4','paper',changed,inputs,m.delivery.review_template(self.contract))

    def test_exact_quote_free_forced_map_and_invalid_times(self):
        spec=importlib.util.spec_from_file_location('forced',ROOT/'.agents/skills/ytv-srt/scripts/forced_alignment.py')
        helper=importlib.util.module_from_spec(spec);spec.loader.exec_module(helper)
        result=helper.build_map('“Sailors came home.”','fixture',{'word_segments':[
            {'word':'Sailors','start':.1,'end':.3},
            {'word':'came','start':.5,'end':.7},
            {'word':'home.','start':1.,'end':1.2}]})
        self.assertEqual([word['text'] for word in result['words']],['Sailors','came','home.'])
        self.assertEqual(result['status'],'REVIEW_REQUIRED')
        for start,end in ((.3,.3),(.4,.2)):
            with self.assertRaisesRegex(ValueError,'Invalid'):
                helper.build_map('word','fixture',{'word_segments':[{'word':'word','start':start,'end':end}]})

    def test_local_style_overrides_and_overlay_bypass_are_rejected(self):
        self.plan['subtitles']['style']={'highlight':'red'}
        with self.assertRaisesRegex(ValueError,'shared format profile'):
            m.delivery.validate_words(self.plan,self.p,120)
        self.plan['subtitles']={'mode':'overlay','path':'image.png'}
        with self.assertRaisesRegex(ValueError,'subtitles.mode'):m.validate(self.plan,self.p)

if __name__=='__main__':unittest.main()
