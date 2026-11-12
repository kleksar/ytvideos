"""Episode-scoped calls to Palmier's discovered local MCP API; no package edits."""
import json
import pathlib
import time
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent

def call(name, arguments, label=None):
    record = {"jsonrpc": "2.0", "id": time.time_ns(), "method": "tools/call",
              "params": {"name": name, "arguments": arguments}}
    request = urllib.request.Request("http://127.0.0.1:19789/mcp", json.dumps(record).encode(),
                                    {"Content-Type": "application/json", "Accept": "application/json,text/event-stream"})
    with urllib.request.urlopen(request, timeout=180) as response:
        result = json.load(response)
    with (ROOT / "receipts.jsonl").open("a") as stream:
        stream.write(json.dumps({"request": record, "response": result}, ensure_ascii=False) + "\n")
    if label:
        (ROOT / (label + ".json")).write_text(json.dumps(result, ensure_ascii=False, indent=2))
    if result.get("error") or result.get("result", {}).get("isError"):
        raise RuntimeError(str(result)[:1800])
    content = result.get("result", {}).get("content", [])
    texts = [item.get("text", "") for item in content if item.get("type") == "text" or "text" in item]
    if len(texts) == 1:
        try:
            return json.loads(texts[0])
        except json.JSONDecodeError:
            return texts[0]
    return result.get("result", result)
