import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
from export_fixture import passport
from pathlib import Path

from test_montage import m, bind_plan

ROOT = m.ROOT
spec = importlib.util.spec_from_file_location('upload_under_test', ROOT/'automation/youtube/upload.py')
u = importlib.util.module_from_spec(spec); spec.loader.exec_module(u)
CHANNEL = json.loads((ROOT/'automation/channels.json').read_text())['paper_detour']['channel_id']
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
        self.prepared=m.validate(self.plan,self.p)
        self.audio={'codec_name':'pcm_s16le','channels':2,'sample_rate':'44100'}
        command=m.final_command(self.plan,self.p,self.prepared,self.work,self.video,None,'libx264','800k',self.audio)
        self.passport=self.p/'export.json';self.passport.write_text(json.dumps(passport(m,self.manifest,self.prepared,self.audio,self.video)))
        self.command=self.work/'command.json';self.command.write_text(json.dumps(command))
        self.render=m.delivery.freeze_render(self.work,self.passport,self.command,self.contract['engine'],self.prepared,self.audio,self.manifest,self.video)
        m.delivery.write_receipt(self.video,'paper',self.contract,m.delivery.render_inputs(self.manifest,self.plan,self.p),render=self.render)
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

    def test_frozen_speed_policy_path_requires_matching_content(self):
        self.mark_reviewed()
        original = m.delivery.audio_binding
        def same_policy_at_another_path(plan, base):
            binding = original(plan, base)
            binding['speed_policy'] = dict(binding['speed_policy'], path='/another/snapshot/speed.json')
            return binding
        with patch.object(m.delivery, 'audio_binding', side_effect=same_policy_at_another_path):
            m.delivery.validate_release(self.video, CHANNEL)
        def changed_policy(plan, base):
            binding = same_policy_at_another_path(plan, base)
            binding['speed_policy']['sha256'] = '0' * 64
            return binding
        with patch.object(m.delivery, 'audio_binding', side_effect=changed_policy):
            with self.assertRaisesRegex(ValueError, 'Final audio binding differs'):
                m.delivery.validate_release(self.video, CHANNEL)

    def test_private_staging_and_owner_playback_have_distinct_gates(self):
        self.mark_reviewed()
        data = json.loads(self.receipt.read_text())
        media_hash = data['media']['sha256']
        evidence = data['acceptance']['evidence']
        data['technical_review'] = {'status': 'PASS', 'full_decode': 'PASS',
                                    'media_sha256': media_hash, 'evidence': evidence}
        checks = data['review']['checks']
        check = checks[next(iter(checks))]
        check['status'] = 'UNVERIFIED'
        self.receipt.write_text(json.dumps(data))
        m.delivery.validate_release(self.video, CHANNEL, private_staging=True)
        with self.assertRaisesRegex(ValueError, 'review incomplete'):
            m.delivery.validate_release(self.video, CHANNEL)

        data['playback_review'] = {'status': 'ACCEPTED', 'media_sha256': media_hash,
                                  'scope': 'final_mp4_with_audio_and_burned_in_captions',
                                  'evidence': evidence}
        self.receipt.write_text(json.dumps(data))
        m.delivery.validate_release(self.video, CHANNEL)

        check['status'] = 'FAIL'
        self.receipt.write_text(json.dumps(data))
        for private_staging in (True, False):
            with self.assertRaisesRegex(ValueError, 'Confirmed subtitle defect'):
                m.delivery.validate_release(self.video, CHANNEL, private_staging=private_staging)

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


    def test_tool_update_preserves_accepted_file_but_snapshot_tampering_fails(self):
        self.mark_reviewed()
        original=m.delivery.file_record
        engine_paths={r['path'] for r in self.contract['engine']}
        def changed(path):
            record=original(path)
            if str(Path(path).resolve()) in engine_paths:
                record['sha256']='f'*64
            return record
        with patch.object(m.delivery,'file_record',side_effect=changed):
            m.delivery.validate_release(self.video,CHANNEL)
        path=Path(self.render['engine'][0]['snapshot']['path']);path.write_text('tampered')
        self.rejected_before_network('Stale delivery input')

    def test_frozen_command_or_passport_tampering_fails(self):
        self.mark_reviewed()
        for key in ('command','export_contract'):
            path=Path(self.render[key]['snapshot']['path']);old=path.read_bytes()
            path.write_bytes(old+b' ')
            self.rejected_before_network('Stale delivery input')
            path.write_bytes(old)

    def test_historical_receipt_requires_audit_not_rerender(self):
        data=json.loads(self.receipt.read_text());data['schema']=m.delivery.SCHEMA
        self.receipt.write_text(json.dumps(data))
        self.rejected_before_network('saved-command audit')

    def test_export_mismatch_and_unsupported_control_fail(self):
        from copy import deepcopy
        p=json.loads(self.passport.read_text());argv=json.loads(self.command.read_text())
        for key,value in [('target_bit_rate','320k'),('channels',1),('sample_rate',48000)]:
            q=deepcopy(p);q['required_delivery']['audio_contract'][key]=value
            with self.assertRaisesRegex(ValueError,'setting mismatch'):
                m.delivery.check_export_settings(q,argv,self.prepared,self.audio,self.manifest,self.video)
        argv[argv.index('-b:a')+1]='192k'
        with self.assertRaisesRegex(ValueError,'below channel'):
            m.delivery.check_export_settings(p,argv,self.prepared,self.audio,self.manifest,self.video)
        argv=json.loads(self.command.read_text());p['encoding']['requested_arguments']['unsupported_gop']=60
        with self.assertRaisesRegex(ValueError,'Unsupported requested'):
            m.delivery.check_export_settings(p,argv,self.prepared,self.audio,self.manifest,self.video)

    def test_mono_stereo_and_aac_copy_contracts(self):
        for audio in ({'codec_name':'pcm_s16le','channels':1,'sample_rate':'44100'},
                      {'codec_name':'pcm_s16le','channels':2,'sample_rate':'48000'},
                      {'codec_name':'aac','channels':2,'sample_rate':'44100','profile':'LC'}):
            p=passport(m,self.manifest,self.prepared,audio,self.video)
            argv=m.final_command(self.plan,self.p,self.prepared,self.work,self.video,None,'libx264','800k',audio)
            result=m.delivery.check_export_settings(p,argv,self.prepared,audio,self.manifest,self.video)
            self.assertEqual(result['audio']['target_bit_rate'], 'STREAM_COPY' if audio['codec_name']=='aac' else (256000 if audio['channels']==2 else 192000))
            if audio['codec_name']=='aac':
                p['required_delivery']['audio_contract']['target_bit_rate']='256k'
                with self.assertRaisesRegex(ValueError,'setting mismatch'):
                    m.delivery.check_export_settings(p,argv,self.prepared,audio,self.manifest,self.video)


    def test_settings_mismatch_stops_before_any_scene_encoding(self):
        expected=json.loads(self.passport.read_text())
        expected['required_delivery']['audio_contract']['target_bit_rate']='320k'
        self.passport.write_text(json.dumps(expected))
        argv=['montage.py',str(self.manifest),'--output',str(self.p/'unrendered.mp4'),
              '--work-dir',str(self.p/'rejected-run'),'--export-contract',str(self.passport),
              '--encoder','libx264','--bitrate','800k']
        # Keep the exact requested output consistent so audio mismatch is reached.
        expected['preflight']['output_path']=str(self.p/'unrendered.mp4')
        self.passport.write_text(json.dumps(expected))
        audio={'streams':[{**self.audio,'duration':'4.0'}]}
        with patch.object(sys,'argv',argv), patch.object(m.subprocess,'check_output',return_value=json.dumps(audio).encode()), patch.object(m,'scene_render') as scene:
            with self.assertRaisesRegex(ValueError,'target_bit_rate'):
                m.main()
            scene.assert_not_called()
        self.assertFalse((self.p/'unrendered.mp4').exists())

    def test_historical_audit_preserves_acceptance_without_reencoding(self):
        import importlib.util
        with patch.dict(sys.modules,{'delivery':m.delivery}):
            spec=importlib.util.spec_from_file_location('historical_audit',m.HERE/'audit_render.py')
            helper=importlib.util.module_from_spec(spec);spec.loader.exec_module(helper)
        self.mark_reviewed()
        original=self.receipt.read_bytes()
        prepared=self.work/'plan.json'
        prepared.write_text(json.dumps({**self.prepared,'manifest_path':str(self.manifest)}))
        evidence=self.p/'audit.md';evidence.write_text('Synthetic saved-command assessment only')
        with patch.object(helper.subprocess,'check_output',return_value=json.dumps({'streams':[self.audio]}).encode()):
            report,bound=helper.audit(self.receipt,self.passport,self.command,prepared,self.p/'audit',evidence)
        self.assertEqual(report['status'],'SETTINGS_PASS')
        self.assertEqual(bound['acceptance'],json.loads(original)['acceptance'])
        self.assertEqual(self.receipt.read_bytes(),original)
        bound_path=self.p/'bound.json';bound_path.write_text(json.dumps(bound))
        m.delivery.validate_release(self.video,CHANNEL,bound_path)
        command=json.loads(self.command.read_text());command[command.index('-b:a')+1]='192k'
        self.command.write_text(json.dumps(command))
        with patch.object(helper.subprocess,'check_output',return_value=json.dumps({'streams':[self.audio]}).encode()):
            with self.assertRaisesRegex(ValueError,'below channel'):
                helper.audit(self.receipt,self.passport,self.command,prepared,self.p/'bad-audit')
        self.assertFalse((self.p/'bad-audit').exists())

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
