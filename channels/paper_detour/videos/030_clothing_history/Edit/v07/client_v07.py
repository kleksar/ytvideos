import json
import sys
from pathlib import Path
ROOT = Path('/Users/diplomat/ytvideos/channels/paper_detour/videos/030_clothing_history')
sys.path.insert(0, str(ROOT / 'Edit/v05'))
from palmier_client import rpc
def call(name, args):
    result = rpc('tools/call', {'name': name, 'arguments': args})
    with (ROOT / 'Edit/v07/mcp_receipts.jsonl').open('a') as stream:
        stream.write(json.dumps({'tool': name, 'arguments': args, 'result': result}, ensure_ascii=False) + '\n')
    if result.get('isError'):
        raise RuntimeError(str(result))
    parts = [x['text'] for x in result.get('content', []) if x.get('type') == 'text']
    if len(parts) == 1:
        try: return json.loads(parts[0])
        except ValueError: return parts[0]
    return result
