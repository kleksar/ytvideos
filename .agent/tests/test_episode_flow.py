import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts' / 'episode_flow.py'
spec = importlib.util.spec_from_file_location('episode_flow', SCRIPT)
f = importlib.util.module_from_spec(spec); spec.loader.exec_module(f)

class FlowTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup)
        self.path = Path(self.tmp.name) / 'artifact.txt'; self.path.write_text('v1')
        self.state = f.new_state('episode', 'paper', 'ready_text', 'short')
        self.state.update(input_evidence='user supplied text', scope='full production')
    def done(self, stage):
        s = next(x for x in self.state['stages'] if x['id'] == stage)
        s['status'] = 'DONE'
        s['skill_runs'] = [{'skill': x, 'status': 'APPLIED', 'evidence': 'actual handoff record'} for x in s['skills']]
        if stage not in ('review', 'unlisted', 'release'):
            s['artifacts'] = [{'path': str(self.path), 'version': 'v1', 'sha256': f.digest(self.path)}]
    def test_three_routes_and_profiles(self):
        for channel in ('paper', 'nuviko'):
            for fmt in ('long', 'short'):
                for name in f.INPUTS:
                    with self.subTest(channel=channel, format=fmt, input=name):
                        state = f.new_state('x', channel, name, fmt)
                        stages = {stage['id']: stage['skills'] for stage in state['stages']}
                        self.assertEqual(stages['storyboard'], ['ytv-visual-direction'])
                        self.assertEqual('ytv-storycraft' in stages['script'], name != 'ready_text')
                        self.assertNotIn('ytv-history-verification', stages['script'])
                        if name == 'collaborative':
                            self.assertIn('ytv-storycraft', stages['develop_story'])
                            self.assertEqual('ytv-history-verification' in stages['develop_story'], channel == 'nuviko')
                        else:
                            self.assertNotIn('develop_story', stages)
                        self.assertEqual(f.assess(state)['errors'], [])
        s = f.new_state('x','nuviko','accepted_story','long')
        self.assertIn('ytv-youtube-ab-testing', next(x for x in s['stages'] if x['id']=='packaging')['skills'])
    def test_interruption_resume_does_not_mutate(self):
        self.done('script'); before=json.dumps(self.state,sort_keys=True)
        self.assertEqual(f.assess(self.state)['ready'], ['storyboard'])
        self.assertEqual(before,json.dumps(self.state,sort_keys=True))
    def test_music_gate_and_legacy_route(self):
        for name in ('script', 'storyboard', 'audio'): self.done(name)
        audio=next(s for s in self.state['stages'] if s['id']=='audio')
        self.assertTrue(any('music_handoff required' in e for e in f.assess(self.state)['errors']))
        handoff=Path(self.tmp.name)/'music.md'; handoff.write_text('actual decision and checks')
        audio['artifacts'].append({'path':str(handoff),'version':'v1','sha256':f.digest(handoff)})
        audio['music_handoff']={'mode':'exception','mix_path':str(self.path),'handoff_path':str(handoff),'edit_revision':'edit-v1','reason':'music does not suit this story'}
        audio['checks']=[{'name':name,'status':'PASS','reviewer':'editor','method':'listening','coverage':'full','evidence':'handoff'} for name in ('music_decision','mix_listening')]
        self.assertEqual(f.assess(self.state)['errors'],[])
        audio['music_handoff']['mode']='music'
        self.assertEqual(f.assess(self.state)['errors'],[])
        handoff.write_text('changed after recording')
        self.assertIn('audio',f.assess(self.state)['stale'])
        handoff.write_text('actual decision and checks')
        audio['music_handoff']['reason']=' '
        self.assertTrue(any('reason required' in e for e in f.assess(self.state)['errors']))
        audio['music_handoff']['reason']='music suits this story'
        audio['checks'][1]['status']='UNVERIFIED'
        self.assertTrue(any('mix_listening PASS' in e for e in f.assess(self.state)['errors']))
        self.state['schema_version']=1
        audio.pop('music_handoff'); audio['checks']=[]
        self.assertEqual(f.assess(self.state)['errors'],[])
    def test_decision_and_predecessor_cannot_be_skipped(self):
        self.done('packaging')
        self.assertTrue(any('preceding stage' in x for x in f.assess(self.state)['errors']))
    def test_stale_dependency_propagation_and_unrelated(self):
        a=self.state['stages'][0]; b=self.state['stages'][1]; c=self.state['stages'][2]
        a['artifacts']=[{'path':str(self.path),'version':'v1','sha256':f.digest(self.path)}]
        b['dependencies']=[{'path':str(self.path),'sha256':f.digest(self.path)}]
        other=Path(self.tmp.name)/'other'; other.write_text('ok')
        c['dependencies']=[{'path':str(other),'sha256':f.digest(other)}]
        self.path.write_text('changed'); report=f.assess(self.state)
        self.assertIn('script',report['stale']);self.assertIn('storyboard',report['stale']);self.assertNotIn('audio',report['stale'])
    def test_evidence_cannot_be_invented_by_check(self):
        self.done('script'); self.state['stages'][0]['checks']=[{'name':'listen','status':'PASS'}]
        self.assertTrue(any('evidence/reviewer' in x for x in f.assess(self.state)['errors']))
        self.done('storyboard'); self.state['stages'][1]['skill_runs']=[]
        self.assertTrue(any('skill needs' in x for x in f.assess(self.state)['errors']))
    def test_playlist_skill_in_all_production_routes(self):
        for channel in ('paper', 'nuviko'):
            for fmt in ('long', 'short'):
                for kind in f.INPUTS:
                    route=f.new_state('x',channel,kind,fmt)
                    package=next(s for s in route['stages'] if s['id']=='packaging')
                    self.assertIn('ytv-youtube-playlists',package['skills'])
                    self.assertNotIn('playlist_accepted',f.DECISIONS.values())
    def test_pending_playlist_proposal_is_not_a_new_gate(self):
        self.state['playlist_resolution']={'status':'new_proposed','name':'Example','decision':'pending'}
        self.assertEqual(f.assess(self.state)['ready'],['script'])
        self.assertEqual(f.assess(self.state)['errors'],[])
    def test_short_routes_and_preserve_ready_text(self):
        for kind in f.INPUTS:
            state=f.new_state('x','paper',kind,'short')
            stage=next(s for s in state['stages'] if s['id']==('develop_story' if kind=='collaborative' else 'script'))
            self.assertIn('ytv-shorts-loop',stage['skills'])
            self.assertEqual('ytv-shorts-story' in stage['skills'],kind!='ready_text')
            self.assertEqual(f.assess(state)['errors'],[])
        long=f.new_state('x','paper','accepted_story','long')
        self.assertNotIn('ytv-shorts-loop',next(s for s in long['stages'] if s['id']=='script')['skills'])
    def test_legacy_pending_short_requires_reconciled_route(self):
        state=f.new_state('x','paper','accepted_story','short')
        script=next(s for s in state['stages'] if s['id']=='script')
        script['skills']=[x for x in script['skills'] if x not in ('ytv-shorts-story','ytv-shorts-loop')]
        self.assertTrue(any('reconcile route' in e for e in f.assess(state)['errors']))
    def test_legacy_completed_short_does_not_retroactively_require_new_skills(self):
        self.done('script')
        stage=self.state['stages'][0]
        stage['skills']=[x for x in stage['skills'] if x not in ('ytv-shorts-story','ytv-shorts-loop')]
        stage['skill_runs']=[x for x in stage['skill_runs'] if x['skill'] in stage['skills']]
        report=f.assess(self.state)
        self.assertEqual(report['errors'],[])
        self.assertTrue(report['warnings'])
        self.assertEqual(report['ready'],['storyboard'])
    def test_old_storyboard_receipt_survives_but_cannot_complete_current_route(self):
        self.done('script')
        self.done('storyboard')
        stage = self.state['stages'][1]
        stage['skills'] = ['ytv-paper-storyboard']
        stage['skill_runs'][0]['skill'] = 'ytv-paper-storyboard'
        report = f.assess(self.state)
        self.assertEqual(report['errors'], [])
        self.assertTrue(report['warnings'])
        stage['status'] = 'PENDING'
        self.assertTrue(any('reconcile route' in e for e in f.assess(self.state)['errors']))
        stage['skills'] = ['ytv-visual-direction']
        self.assertEqual(f.assess(self.state)['errors'], [])
        stage['status'] = 'DONE'
        self.assertTrue(any('each applicable skill needs' in e for e in f.assess(self.state)['errors']))
    def test_completed_production_storyboard_keeps_evidence_for_both_channels(self):
        for channel in ('paper', 'nuviko'):
            with self.subTest(channel=channel):
                self.state = f.new_state('x', channel, 'ready_text', 'long')
                self.state.update(input_evidence='accepted narration', scope='full production')
                self.done('script')
                stage = next(s for s in self.state['stages'] if s['id'] == 'storyboard')
                stage['skills'] = ['ytv-video-production']
                self.done('storyboard')
                before = json.dumps(self.state, sort_keys=True)
                report = f.assess(self.state)
                self.assertEqual(report['errors'], [])
                self.assertEqual(report['ready'], ['audio'])
                self.assertTrue(report['warnings'])
                self.assertEqual(before, json.dumps(self.state, sort_keys=True))
                # Old evidence is retained, but cannot certify new visual-direction work.
                stage['skills'] = ['ytv-visual-direction']
                self.assertTrue(any('each applicable skill needs' in e for e in f.assess(self.state)['errors']))
                stage['status'] = 'PENDING'
                self.assertEqual(f.assess(self.state)['errors'], [])
                stage['skills'] = ['ytv-video-production']
                self.assertTrue(any('reconcile route' in e for e in f.assess(self.state)['errors']))
    def test_story_approval_gate(self):
        self.state=f.new_state('x','paper','collaborative','short'); self.state.update(input_evidence='brief',scope='full')
        self.done('develop_story')
        self.assertEqual(f.assess(self.state)['ready'], [])
        self.state['decisions']['story_accepted']={'accepted':True,'target':'story v1','evidence':'user message'}
        self.assertEqual(f.assess(self.state)['ready'], ['script'])
    def test_update_refuses_changed_snapshot(self):
        state=Path(self.tmp.name)/'flow.json'; candidate=Path(self.tmp.name)/'candidate.json'
        state.write_text(json.dumps(self.state)); candidate.write_text(json.dumps(self.state)); old=f.digest(state)
        state.write_text(state.read_text()+' ')
        args=[sys.executable,str(SCRIPT),'update',str(state),str(candidate),'--expected-sha256',old]
        before=state.read_bytes(); self.assertNotEqual(subprocess.run(args,capture_output=True).returncode,0); self.assertEqual(before,state.read_bytes())
        args[-1]=f.digest(state); self.assertEqual(subprocess.run(args,capture_output=True).returncode,0)
    def test_init_never_overwrites(self):
        p=Path(self.tmp.name)/'flow.json'; args=[sys.executable,str(SCRIPT),'init',str(p),'--episode','x','--channel','paper','--format','short','--input','ready_text']
        self.assertEqual(subprocess.run(args,capture_output=True).returncode,0); initial=p.read_bytes()
        self.assertNotEqual(subprocess.run(args,capture_output=True).returncode,0);self.assertEqual(initial,p.read_bytes())
if __name__ == '__main__':unittest.main()
