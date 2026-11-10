import json, os, subprocess, sys, tempfile, unittest
from pathlib import Path

SCRIPT = Path(__file__).with_name('rules_sync.py')
if not SCRIPT.exists(): SCRIPT = Path(__file__).resolve().parents[1] / 'scripts' / 'rules_sync.py'
REAL = Path(__file__).resolve().parents[2]
class RulesTest(unittest.TestCase):
 def setUp(self):
  self.tmp = tempfile.TemporaryDirectory(); self.root = Path(self.tmp.name); self.store = self.root/'store'; self.src = self.root/'source'; self.src.mkdir(); (self.src/'rule.md').write_text('unsaved version')
 def tearDown(self): self.tmp.cleanup()
 def run_cli(self, *args, expect=0):
  r = subprocess.run([sys.executable,str(SCRIPT),*map(str,args)], text=True, capture_output=True)
  self.assertEqual(r.returncode, expect, r.stderr + r.stdout); return r.stdout
 def spec(self, ident='a', files=None, impact='review', formats=None):
  return {'id':ident,'summary':'test','channels':['paper'],'formats':formats or ['long'],'stages':['render','qa'],'impact':impact,'files':files or ['rule.md']}
 def publish(self, records, source=None):
  spec = self.root / (os.urandom(6).hex()+'.json'); spec.write_text(json.dumps(records)); return self.run_cli('publish','--store',self.store,'--source',source or self.src,'--changes',spec)
 def check(self, channel='paper', format='long', stage='render', expect=0):
  out = self.run_cli('check','--store',self.store,'--session','session1','--channel',channel,'--format',format,'--stage',stage,expect=expect); return json.loads(out) if out else None
 def test_filters_snapshot_ack_and_version(self):
  self.publish([self.spec()]); self.assertEqual(self.check(format='short')['pending'], []); p=self.check(expect=2); self.assertEqual(Path(p['pending'][0]['files'][0]['snapshot_path']).read_text(),'unsaved version')
  (self.src/'rule.md').write_text('new uncommitted edit'); self.assertEqual(Path(p['pending'][0]['files'][0]['snapshot_path']).read_text(),'unsaved version')
  self.run_cli('ack','--store',self.store,'--session','session1','--manifest-sha256',p['manifest_sha256'],'--read-and-assessed','a'); self.assertEqual(self.check()['pending'],[])
  self.publish([self.spec('b')]); self.run_cli('ack','--store',self.store,'--session','session1','--manifest-sha256',p['manifest_sha256'],'--read-and-assessed','a',expect=1); self.assertEqual([e['id'] for e in self.check(expect=2)['pending']],['b'])
 def test_errors_unknown_and_corruption(self):
  self.check(expect=1); self.publish([self.spec(impact='unclassified')]); self.assertEqual(len(self.check(channel='other',format='short',stage='other',expect=2)['pending']),1)
  p=self.check(expect=2); Path(p['pending'][0]['files'][0]['snapshot_path']).write_text('corrupt'); self.check(expect=1)
 def test_real_frame_end_screen_classification(self):
  frame='channels/paper_detour/AGENTS.md'; end='.agents/skills/ytv-video-production/references/paper-end-screens.md'
  a=self.spec('frame',[frame],formats=['short','long']); b=self.spec('ending',[end]); self.publish([a,b], REAL)
  self.assertEqual([x['id'] for x in self.check(expect=2)['pending']],['frame','ending']); self.assertEqual([x['id'] for x in self.check(format='short',expect=2)['pending']],['frame']); self.assertEqual(self.check(channel='history')['pending'],[])
 def test_concurrent_publish(self):
  paths=[]
  for id in ('x','y'):
   f=self.root/(id+'.json'); f.write_text(json.dumps([self.spec(id)])); paths.append(f)
  procs=[subprocess.Popen([sys.executable,str(SCRIPT),'publish','--store',str(self.store),'--source',str(self.src),'--changes',str(f)],stdout=subprocess.PIPE,stderr=subprocess.PIPE) for f in paths]
  for p in procs:
   out,err=p.communicate(); self.assertEqual(p.returncode,0,(out,err))
  self.assertEqual({x['id'] for x in self.check(expect=2)['pending']},{'x','y'})
 def test_traversal_and_duplicate(self):
  self.publish([self.spec()]); f=self.root/'bad.json'; f.write_text(json.dumps([self.spec('bad',['../outside'])])); self.run_cli('publish','--store',self.store,'--source',self.src,'--changes',f,expect=1)
  f.write_text(json.dumps([self.spec()])); self.run_cli('publish','--store',self.store,'--source',self.src,'--changes',f,expect=1)
if __name__=='__main__': unittest.main()
