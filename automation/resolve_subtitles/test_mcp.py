import io
import json
import queue
from types import SimpleNamespace
import unittest
from mcp import ResolveMCP, BINARY

class Stream:
    def __init__(self): self.lines=[]; self.result=None
    def write(self,s): self.lines.append(json.loads(s))
    def flush(self): pass

class MCPTests(unittest.TestCase):
    def client(self):
        client=ResolveMCP.__new__(ResolveMCP)
        client.tools={'run_script':{'inputSchema':{'properties':{'script':{'type':'string'}}}},'get_image':{}}
        client.calls=[]
        client.rpc=lambda method,params: client.calls.append((method,params)) or {'content':[]}
        return client

    def test_only_exact_verified_run_script(self):
        client=self.client();client.run('result = 1')
        self.assertEqual(client.calls[0][1]['name'],'run_script')
        self.assertNotIn('unsafe',str(client.calls))
        client.tools={}
        with self.assertRaises(RuntimeError):client.run('result = 1')
        self.assertEqual(len(client.calls),1)

    def test_image_capability_and_frame_guard(self):
        client=self.client();client.image(12)
        self.assertEqual(client.calls[0][1]['arguments']['frame_offset'],12)
        with self.assertRaises(ValueError):client.image(-1)
        client.tools={}
        with self.assertRaises(RuntimeError):client.image(1)

    def test_response_deadline_without_hanging(self):
        client=ResolveMCP.__new__(ResolveMCP)
        client.timeout=.001;client.serial=0;client.messages=queue.Queue()
        client.process=SimpleNamespace(stdin=Stream())
        with self.assertRaises(TimeoutError):client.rpc('tools/list',{})
        self.assertEqual(client.process.stdin.lines[0]['id'],1)

    def test_timeout_constructor_rejects_before_process(self):
        with self.assertRaises(ValueError):ResolveMCP(timeout=0,process_factory=lambda *a,**k:self.fail('must not start'))

if __name__=='__main__':unittest.main()
