import json,os,pathlib,subprocess,sys,tempfile,unittest,fcntl
P=pathlib.Path(__file__).resolve().parents[1] / 'scripts' / 'wait_for_resolution.py'
class MonitorTests(unittest.TestCase):
 def setUp(self):
  self.temp=tempfile.TemporaryDirectory();self.d=pathlib.Path(self.temp.name);self.lock=self.d/'lock';self.lock.touch();self.state=self.d/'lock.state.json';self.env=dict(os.environ,YTVIDEOS_CHATGPT_SESSION_LOCK=str(self.lock));self.ps=[]
 def tearDown(self):
  for p in self.ps:
   if p.poll() is None:p.kill()
   p.wait(timeout=10)
   for stream in (p.stdin,p.stdout,p.stderr):
    if stream is not None:stream.close()
  self.temp.cleanup()
 def write(self,**kwargs):
  p=self.d/'new';p.write_text(json.dumps(kwargs));os.replace(p,self.state)
 def start(self):
  p=subprocess.Popen([sys.executable,str(P),'--operation-id','op-A','--interval-seconds','0.05'],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,env=self.env);self.ps.append(p);self.assertEqual(json.loads(p.stdout.readline())['event'],'WAITING_FOR_RESOLUTION');return p
 def test_ten_waiters_do_not_hold_lock_and_resume_after_resolution(self):
  self.write(operation_id='op-A',status='armed',prompt='private')
  ps=[self.start() for _ in range(10)]
  with self.lock.open('r+') as f:
   fcntl.flock(f,fcntl.LOCK_EX|fcntl.LOCK_NB);self.write(operation_id='op-A',status='resolved')
   for p in ps:self.assertEqual(json.loads(p.stdout.readline())['event'],'RETRY');self.assertEqual(p.wait(timeout=3),0)
   fcntl.flock(f,fcntl.LOCK_UN)
 def test_cancel_does_not_touch_state(self):
  self.write(operation_id='op-A',status='send_attempted');before=self.state.read_bytes();p=self.start();p.stdin.close();self.assertEqual(json.loads(p.stdout.readline())['event'],'CANCELLED');p.wait(timeout=3);self.assertEqual(self.state.read_bytes(),before)
 def test_different_operation_requires_reinspection(self):
  self.write(operation_id='op-A',status='armed');p=self.start();self.write(operation_id='op-B',status='armed');self.assertEqual(json.loads(p.stdout.readline())['event'],'STATE_CHANGED');self.assertEqual(p.wait(timeout=3),4)
 def test_empty_or_invalid_journal_cannot_signal_success(self):
  self.state.write_text('{invalid');p=self.start();self.write(operation_id='op-A',status='armed');self.assertIsNone(p.poll());self.write(operation_id='op-A',status='verified');self.assertEqual(json.loads(p.stdout.readline())['event'],'RETRY');p.wait(timeout=3)
 def test_early_input_is_rejected(self):
  self.write(operation_id='op-A',status='armed');p=self.start();p.stdin.write('foo\n');p.stdin.flush();self.assertEqual(json.loads(p.stdout.readline())['event'],'EARLY_INPUT');self.assertEqual(p.wait(timeout=3),4)
if __name__=='__main__':unittest.main()
