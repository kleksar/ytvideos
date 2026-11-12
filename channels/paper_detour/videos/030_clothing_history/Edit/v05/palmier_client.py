import json,urllib.request
from pathlib import Path
ROOT=Path('/Users/diplomat/ytvideos/channels/paper_detour/videos/030_clothing_history')
URL='http://127.0.0.1:19789/mcp'
H=Path('/tmp/paper030_mcp_headers').read_text();SID=next(x.split(':',1)[1].strip() for x in H.splitlines() if x.lower().startswith('mcp-session-id:'))
COUNT=100

def rpc(method,params):
 global COUNT
 COUNT+=1
 req=urllib.request.Request(URL,data=json.dumps({'jsonrpc':'2.0','id':COUNT,'method':method,'params':params}).encode(),headers={'Content-Type':'application/json','Accept':'application/json, text/event-stream','Mcp-Session-Id':SID})
 raw=urllib.request.urlopen(req,timeout=180).read().decode()
 resp=json.loads(''.join(x[5:].strip() for x in raw.splitlines() if x.startswith('data:') and x[5:].strip()))
 if 'error' in resp:raise RuntimeError(str(resp['error']))
 return resp['result']

def call(name,args):
 result=rpc('tools/call',{'name':name,'arguments':args})
 log=ROOT/'Edit/v05/mcp_receipts.jsonl'
 with log.open('a') as f:f.write(json.dumps({'tool':name,'arguments':args,'result':result},ensure_ascii=False)+'\n')
 if result.get('isError'):raise RuntimeError(str(result))
 parts=[x['text'] for x in result.get('content',[]) if x.get('type')=='text']
 if len(parts)==1:
  try:return json.loads(parts[0])
  except ValueError:return parts[0]
 return result

if __name__=='__main__':
 tools=rpc('tools/list',{})
 (ROOT/'Edit/v05/current_tools.json').write_text(json.dumps(tools,indent=2))
 print(json.dumps(call('get_media',{'projectId':'B1BA2D18'}),ensure_ascii=False)[:1500])
 snap=call('manage_snapshots',{'projectId':'B1BA2D18','timelineId':'A0A30D15','action':'save','name':'Before accepted story v05 assembly'})
 tl=call('create_timeline',{'projectId':'B1BA2D18','name':'Clothing History v05 — accepted story 3m10'})
 (ROOT/'Edit/v05/target.json').write_text(json.dumps({'projectId':'B1BA2D18','created':tl,'snapshot':snap},indent=2));print(json.dumps(tl))
