import json, os, pathlib, subprocess, sys, tempfile, unittest
P=pathlib.Path(__file__).resolve().parents[1] / 'scripts' / 'composer_recovery.py'
OLD=P.with_name('composer_lock.py')
class Tests(unittest.TestCase):
 def setUp(self):
  self.d=tempfile.TemporaryDirectory(); self.path=pathlib.Path(self.d.name); self.env=dict(os.environ,YTVIDEOS_CHATGPT_SESSION_LOCK=str(self.path/'lock')); self.prompt=self.path/'prompt'; self.prompt.write_text('first\nsecond',encoding='utf8'); self.ps=[]
 def tearDown(self):
  for p in self.ps:
   if p.poll() is None: p.kill(); p.communicate()
  self.d.cleanup()
 def start(self,task='one'):
  p=subprocess.Popen([sys.executable,str(P),'--task-id',task],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,env=self.env);self.ps.append(p);return p,json.loads(p.stdout.readline())
 def send(self,p,**kw):
  p.stdin.write(json.dumps(kw)+'\n');p.stdin.flush();return json.loads(p.stdout.readline())
 def prep(self,p):
  return self.send(p,op='prepare',chat='chat-1',history_anchor='prior-message',prompt_file=str(self.prompt),initial_empty=True)
 def test_exclusivity_and_normal_release(self):
  a,r=self.start();self.assertEqual(r['event'],'READY'); self.assertEqual(self.prep(a)['event'],'PREPARED')
  b,r=self.start('two');self.assertEqual(r['event'],'LOCK_BUSY');b.wait()
  self.assertEqual(self.send(a,op='inserted',chat='chat-1',observed_text='first\nsecond')['event'],'INSERTED')
  self.assertEqual(self.send(a,op='send_attempt',chat='chat-1',observed_text='first\nsecond',history='none')['event'],'SEND_ATTEMPT_RECORDED')
  self.assertEqual(self.send(a,op='confirmed',chat='chat-1',posted_text='first\nsecond',composer_empty=True)['event'],'LOCK_RELEASED');a.wait()
  c,r=self.start('three');self.assertEqual(r['event'],'READY');c.stdin.close();c.wait()
 def test_crash_before_verified_insertion_does_not_clear(self):
  a,_=self.start();self.prep(a);a.kill();a.wait();b,r=self.start('two');self.assertEqual(r['event'],'NEEDS_INSPECTION')
  r=self.send(b,op='reconcile',chat='chat-1',history='partial',observed_text='second',no_intervening_edit=True);self.assertEqual(r['event'],'STOP')
  b.stdin.close();b.wait()
 def test_inserted_recovery_requires_exact_text_and_history(self):
  a,_=self.start();self.prep(a);self.send(a,op='inserted',chat='chat-1',observed_text='first\nsecond');a.kill();a.wait()
  b,_=self.start('two')
  self.assertEqual(self.send(b,op='reconcile',chat='chat-1',history='unknown',observed_text='first\nsecond',no_intervening_edit=True)['event'],'STOP')
  self.assertEqual(self.send(b,op='reconcile',chat='chat-1',history='none',observed_text='personal draft',no_intervening_edit=True)['event'],'STOP')
  self.assertEqual(self.send(b,op='reconcile',chat='chat-1',history='none',observed_text='first\nsecond',no_intervening_edit=False)['event'],'STOP')
  self.assertEqual(self.send(b,op='reconcile',chat='chat-1',history='partial',observed_text='first\nsecond',no_intervening_edit=True)['event'],'EXACT_AGENT_DRAFT')
  self.assertEqual(self.send(b,op='cleared',chat='chat-1',composer_empty=False)['event'],'ERROR')
  self.assertEqual(self.send(b,op='cleared',chat='chat-1',composer_empty=True)['history'],'partial');b.wait()
 def test_legacy_cannot_erase_v2_state(self):
  a,_=self.start();self.prep(a);a.kill();a.wait()
  z=subprocess.run([sys.executable,str(OLD),'--task-id','old','--controlled'],input='INSPECTED\n',text=True,capture_output=True,env=self.env,timeout=3)
  self.assertEqual(z.returncode,4);self.assertIn('use composer_recovery.py',z.stdout)
 def test_wrong_text_not_sent(self):
  a,_=self.start();self.prep(a)
  self.assertEqual(self.send(a,op='inserted',chat='chat-1',observed_text='edited')['event'],'ERROR')
  self.assertEqual(self.send(a,op='send_attempt',chat='chat-1',observed_text='edited',history='none')['event'],'ERROR')
  a.stdin.close();self.assertEqual(a.wait(),4)
 def test_crash_after_send_is_uncertain_and_no_blind_retry(self):
  a,_=self.start();self.prep(a);self.send(a,op='inserted',chat='chat-1',observed_text='first\nsecond');self.send(a,op='send_attempt',chat='chat-1',observed_text='first\nsecond',history='none');a.kill();a.wait()
  b,_=self.start('two')
  self.assertEqual(self.send(b,op='prepare',chat='chat-1',history_anchor='old',prompt_file=str(self.prompt),initial_empty=True)['event'],'ERROR')
  self.assertEqual(self.send(b,op='reconcile',chat='chat-1',history='unknown',observed_text='',composer_empty=True)['event'],'STOP')
  self.assertEqual(self.send(b,op='reconcile',chat='chat-1',history='full',observed_text='',composer_empty=True)['history'],'full');b.wait()
 def test_crash_during_clear_requires_reinspection(self):
  a,_=self.start();self.prep(a);self.send(a,op='inserted',chat='chat-1',observed_text='first\nsecond');a.kill();a.wait()
  b,_=self.start('two');self.send(b,op='reconcile',chat='chat-1',history='none',observed_text='first\nsecond',no_intervening_edit=True);b.kill();b.wait()
  c,_=self.start('three')
  self.assertEqual(self.send(c,op='cleared',chat='chat-1',composer_empty=True)['event'],'ERROR')
  self.assertEqual(self.send(c,op='reconcile',chat='chat-1',history='none',observed_text='personal draft',no_intervening_edit=True)['event'],'STOP')
  c.stdin.close();c.wait()
 def test_partial_hold_survives_new_work_and_blocks_identical_retry(self):
  a,_=self.start();prepared=self.prep(a);a.kill();a.wait()
  b,_=self.start('recover');self.assertEqual(self.send(b,op='reconcile',chat='chat-1',history='partial',observed_text='',composer_empty=True)['event'],'RESOLVED');b.wait()
  c,_=self.start('next');r=self.prep(c);self.assertEqual(r['event'],'SUBMISSION_HOLD');self.assertEqual(r['operation_id'],prepared['operation_id'])
  self.prompt.write_text('different',encoding='utf8');self.assertEqual(self.prep(c)['event'],'PREPARED');c.kill();c.wait()
  d,_=self.start('recover2');self.assertEqual(self.send(d,op='reconcile',chat='chat-1',history='none',observed_text='',composer_empty=True)['event'],'RESOLVED');d.wait()
  self.prompt.write_text('first\nsecond',encoding='utf8');e,_=self.start('next2');self.assertEqual(self.prep(e)['event'],'SUBMISSION_HOLD');e.stdin.close();e.wait()
 def test_partial_hold_release_requires_exact_identity_and_decision(self):
  a,_=self.start();prepared=self.prep(a);a.kill();a.wait();b,_=self.start('recover');self.send(b,op='reconcile',chat='chat-1',history='partial',observed_text='',composer_empty=True);b.wait()
  c,_=self.start('decider');h=prepared['prompt_sha256'];o=prepared['operation_id']
  self.assertEqual(self.send(c,op='release_submission_hold',prompt_sha256=h,operation_id=o,chat='other',reason='reviewed',history_rechecked=True)['event'],'ERROR')
  self.assertEqual(self.send(c,op='release_submission_hold',prompt_sha256=h,operation_id=o,chat='chat-1',reason='',history_rechecked=True)['event'],'ERROR')
  self.assertEqual(self.send(c,op='release_submission_hold',prompt_sha256=h,operation_id=o,chat='chat-1',reason='reviewed the partial message',history_rechecked=True)['event'],'SUBMISSION_HOLD_RELEASED')
  self.assertEqual(self.prep(c)['event'],'PREPARED');c.kill();c.wait()
 def test_legacy_cannot_bypass_partial_hold(self):
  a,_=self.start();self.prep(a);a.kill();a.wait();b,_=self.start('recover');self.send(b,op='reconcile',chat='chat-1',history='partial',observed_text='',composer_empty=True);b.wait()
  for options in ([],['--controlled']):
   z=subprocess.run([sys.executable,str(OLD),'--task-id','old']+options,input='',text=True,capture_output=True,env=self.env,timeout=3)
   self.assertEqual(z.returncode,4)
 def test_ten_cooperating_contenders_cannot_acquire_busy_lock(self):
  a,_=self.start();self.prep(a)
  contenders=[]
  for i in range(10):
   p=subprocess.Popen([sys.executable,str(P),'--task-id','other-'+str(i)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,env=self.env);contenders.append(p)
  for p in contenders:
   self.assertEqual(json.loads(p.stdout.readline())['event'],'LOCK_BUSY');p.communicate(timeout=3)
  a.stdin.close();a.wait()
 def test_ten_waiters_acquire_after_release(self):
  owner,_=self.start(); waiters=[]
  for i in range(10):
   p=subprocess.Popen([sys.executable,str(P),'--task-id','waiting-'+str(i),'--wait-seconds','5'],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,env=self.env);p.stdin.close();p.stdin=None;waiters.append(p)
  owner.stdin.close();owner.wait()
  for p in waiters:
   out,err=p.communicate(timeout=8); self.assertEqual(p.returncode,0,err);self.assertEqual(json.loads(out)['event'],'READY')
 def test_bounded_wait_does_not_interrupt_owner(self):
  owner,_=self.start()
  p=subprocess.run([sys.executable,str(P),'--task-id','timeout','--wait-seconds','0.2'],input='',capture_output=True,text=True,env=self.env,timeout=3)
  self.assertEqual(p.returncode,3);self.assertEqual(json.loads(p.stdout)['event'],'LOCK_BUSY');self.assertIsNone(owner.poll())
  owner.stdin.close();owner.wait()
 def test_full_recovered_send_blocks_identical_retry(self):
  a,_=self.start();self.prep(a);a.kill();a.wait();b,_=self.start('recover');self.assertEqual(self.send(b,op='reconcile',chat='chat-1',history='full',observed_text='',composer_empty=True)['event'],'RESOLVED');b.wait()
  c,_=self.start('retry');r=self.prep(c);self.assertEqual(r['event'],'SUBMISSION_HOLD');self.assertEqual(r['history'],'full');c.stdin.close();c.wait()
 def test_legacy_resolved_full_is_migrated_to_hold(self):
  import hashlib
  h=hashlib.sha256(self.prompt.read_bytes()).hexdigest()
  state={'version':2,'status':'resolved','history':'full','prompt_sha256':h,'operation_id':'legacy-op','chat':'chat-1','task_id':'legacy'}
  (self.path/'lock.state.json').write_text(json.dumps(state))
  p,r=self.start('new');self.assertEqual(r['event'],'READY');result=self.prep(p);self.assertEqual(result['event'],'SUBMISSION_HOLD');self.assertEqual(result['operation_id'],'legacy-op');p.stdin.close();p.wait()
 def test_indefinite_wait_auto_continues_after_release(self):
  owner,_=self.start()
  w=subprocess.Popen([sys.executable,str(P),'--task-id','waiter','--wait'],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,env=self.env);self.ps.append(w)
  self.assertEqual(json.loads(w.stdout.readline())['event'],'WAITING')
  self.assertIsNone(w.poll());owner.stdin.close();owner.wait()
  self.assertEqual(json.loads(w.stdout.readline())['event'],'GRANTED')
  w.stdin.write('{"op":"activate"}\n');w.stdin.flush();self.assertEqual(json.loads(w.stdout.readline())['event'],'READY')
  w.stdin.close();self.assertEqual(w.wait(timeout=3),0)
 def test_disconnected_waiter_does_not_take_lock(self):
  owner,_=self.start()
  w=subprocess.Popen([sys.executable,str(P),'--task-id','cancel','--wait'],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,env=self.env);self.ps.append(w)
  self.assertEqual(json.loads(w.stdout.readline())['event'],'WAITING');w.stdin.close()
  self.assertEqual(json.loads(w.stdout.readline())['event'],'CANCELLED');self.assertEqual(w.wait(timeout=3),0)
  self.assertIsNone(owner.poll());owner.stdin.close();owner.wait()
  n,r=self.start('next');self.assertEqual(r['event'],'READY');n.stdin.close();n.wait()
 def test_unactivated_grant_releases(self):
  w=subprocess.Popen([sys.executable,str(P),'--task-id','idle','--wait','--activation-seconds','0.2'],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,env=self.env);self.ps.append(w)
  self.assertEqual(json.loads(w.stdout.readline())['event'],'GRANTED')
  self.assertEqual(json.loads(w.stdout.readline())['event'],'ACTIVATION_TIMEOUT');self.assertEqual(w.wait(timeout=3),4)
  n,r=self.start('next');self.assertEqual(r['event'],'READY');n.stdin.close();n.wait()
 def test_grant_disconnect_and_early_input_do_not_hold_lock(self):
  owner,_=self.start()
  w=subprocess.Popen([sys.executable,str(P),'--task-id','early','--wait'],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,env=self.env);self.ps.append(w)
  self.assertEqual(json.loads(w.stdout.readline())['event'],'WAITING');w.stdin.write('premature\n');w.stdin.flush()
  self.assertEqual(json.loads(w.stdout.readline())['event'],'EARLY_INPUT');self.assertEqual(w.wait(timeout=3),4)
  owner.stdin.close();owner.wait()
  w=subprocess.Popen([sys.executable,str(P),'--task-id','gone','--wait'],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,env=self.env);self.ps.append(w)
  self.assertEqual(json.loads(w.stdout.readline())['event'],'GRANTED');w.stdin.close()
  self.assertEqual(json.loads(w.stdout.readline())['event'],'CANCELLED');self.assertEqual(w.wait(timeout=3),0)
  n,r=self.start('next');self.assertEqual(r['event'],'READY');n.stdin.close();n.wait()
 def test_ten_indefinite_waiters_continue(self):
  import concurrent.futures
  owner,_=self.start();ws=[]
  for i in range(10):
   w=subprocess.Popen([sys.executable,str(P),'--task-id','wait-'+str(i),'--wait','--activation-seconds','5'],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,env=self.env);self.ps.append(w);ws.append(w)
  for w in ws:self.assertEqual(json.loads(w.stdout.readline())['event'],'WAITING')
  owner.stdin.close();owner.wait()
  def follow(w):
   if json.loads(w.stdout.readline())['event']!='GRANTED':return False
   w.stdin.write('{"op":"activate"}\n');w.stdin.flush()
   ready=json.loads(w.stdout.readline())['event'];w.stdin.close();return ready=='READY' and w.wait(timeout=8)==0
  with concurrent.futures.ThreadPoolExecutor(max_workers=10) as pool:self.assertTrue(all(pool.map(follow,ws)))
 def test_waiter_after_owner_crash_stops_for_inspection(self):
  owner,_=self.start();self.prep(owner)
  w=subprocess.Popen([sys.executable,str(P),'--task-id','next','--wait'],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,env=self.env);self.ps.append(w)
  self.assertEqual(json.loads(w.stdout.readline())['event'],'WAITING');owner.kill();owner.wait()
  self.assertEqual(json.loads(w.stdout.readline())['event'],'GRANTED');w.stdin.write('{"op":"activate"}\n');w.stdin.flush()
  state=json.loads(w.stdout.readline());self.assertEqual(state['event'],'NEEDS_INSPECTION');self.assertEqual(state['state']['task_id'],'one')
  self.assertEqual(self.prep(w)['event'],'ERROR');w.stdin.close();self.assertEqual(w.wait(timeout=3),4)
if __name__=='__main__':unittest.main()
