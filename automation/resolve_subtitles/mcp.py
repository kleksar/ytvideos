"""Bounded, read-only client for the installed official Resolve MCP process."""
import json
import queue
import subprocess
import threading

BINARY = '/Applications/DaVinci Resolve/DaVinci Resolve.app/Contents/Applications/ResolveMCP'

class ResolveMCP:
    def __init__(self, timeout=15, process_factory=subprocess.Popen):
        if not 0 < timeout <= 120:
            raise ValueError('timeout must be 0..120 seconds')
        self.timeout, self.serial = timeout, 0
        self.process = process_factory([BINARY], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                       stderr=subprocess.DEVNULL, text=True, bufsize=1)
        self.messages = queue.Queue()
        threading.Thread(target=self._read, daemon=True).start()
        try:
            self.rpc('initialize', {'protocolVersion':'2024-11-05','capabilities':{},
                'clientInfo':{'name':'ytv-subtitle-readback','version':'1'}})
            self.process.stdin.write(json.dumps({'jsonrpc':'2.0','method':'notifications/initialized'})+'\n')
            self.process.stdin.flush()
            self.tools = {t['name']:t for t in self.rpc('tools/list', {}).get('tools', [])}
        except Exception:
            self.close()
            raise

    def _read(self):
        for line in self.process.stdout:
            try:
                self.messages.put(json.loads(line))
            except ValueError:
                self.messages.put({'reader_error':'invalid JSON from official MCP'})
        self.messages.put({'reader_error':'official MCP closed stdout'})

    def rpc(self, method, params):
        import time
        self.serial += 1
        ident = self.serial
        self.process.stdin.write(json.dumps({'jsonrpc':'2.0','id':ident,'method':method,'params':params})+'\n')
        self.process.stdin.flush()
        deadline = time.monotonic() + self.timeout
        while True:
            remaining = deadline-time.monotonic()
            if remaining <= 0:
                raise TimeoutError('official MCP response deadline')
            try:
                response = self.messages.get(timeout=remaining)
            except queue.Empty as exc:
                raise TimeoutError('official MCP response deadline') from exc
            if 'reader_error' in response:
                raise RuntimeError(response['reader_error'])
            if response.get('id') != ident:
                continue
            if 'error' in response:
                raise RuntimeError(str(response['error']))
            return response['result']

    def image(self, offset):
        if type(offset) is not int or offset < 0:
            raise ValueError('nonnegative frame offset required')
        if 'get_image' not in self.tools:
            raise RuntimeError('official MCP get_image unavailable')
        result = self.rpc('tools/call', {'name':'get_image','arguments':{
            'source':'timeline','frame_offset':offset,'max_dimension':960}})
        if result.get('isError'):
            raise RuntimeError('official MCP image readback failed')
        return result

    def close(self):
        self.process.terminate()
        try:
            self.process.wait(timeout=3)
        except subprocess.TimeoutExpired:
            self.process.kill()
            self.process.wait(timeout=3)

    def run(self, script):
        descriptor = self.tools.get('run_script', {})
        schema = descriptor.get('inputSchema', {})
        if schema.get('properties', {}).get('script', {}).get('type') != 'string':
            raise RuntimeError('verified official run_script schema unavailable')
        response = self.rpc('tools/call', {'name':'run_script', 'arguments':{'script':script,'timeout':60}})
        if response.get('isError'):
            raise RuntimeError('Resolve script failed: '+str(response.get('content', [])))
        # Keep transport envelope intact: caller checks the actual returned result.
        return response

    def position_api(self):
        schema = self.tools.get('search_scripting_api', {}).get('inputSchema', {})
        if schema.get('properties', {}).get('pattern', {}).get('type') != 'string':
            raise RuntimeError('official scripting API discovery unavailable')
        response = self.rpc('tools/call', {'name':'search_scripting_api', 'arguments':{
            'api':'DaVinciResolveScript.pyi', 'pattern':'SetPosition|TimelineItemPosition'}})
        text = '\n'.join(c.get('text','') for c in response.get('content', []))
        if response.get('isError') or 'SetPosition' not in text or 'startFrame' not in text:
            raise RuntimeError('installed official API does not document required subtitle positioning')
        return response
