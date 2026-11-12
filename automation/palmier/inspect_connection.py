#!/usr/bin/env python3
"""List Palmier projects or inspect one exact project/timeline ID without editing."""
import argparse
import json
import sys
import urllib.error
import urllib.request

ENDPOINT = "http://127.0.0.1:19789/mcp"  # Palmier's bundled MCP bridge
PROTOCOL = "2025-06-18"


class PalmierConnection:
    def __init__(self):
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
            "MCP-Protocol-Version": PROTOCOL,
        }
        self.seq = 0

    def request(self, method, params=None, notification=False):
        message = {"jsonrpc": "2.0", "method": method}
        if params is not None:
            message["params"] = params
        if not notification:
            self.seq += 1
            message["id"] = self.seq
        request = urllib.request.Request(ENDPOINT, data=json.dumps(message).encode(),
                                         headers=self.headers, method="POST")
        with urllib.request.urlopen(request, timeout=20) as response:
            session = response.headers.get("Mcp-Session-Id")
            if session:
                self.headers["Mcp-Session-Id"] = session
            body = response.read().decode("utf-8")
            content_type = response.headers.get("Content-Type", "")
        if notification:
            return None
        if "text/event-stream" in content_type:
            messages = [json.loads(line[5:].strip()) for line in body.splitlines()
                        if line.startswith("data:") and line[5:].strip()]
            replies = [m for m in messages if m.get("id") == self.seq]
            if not replies:
                raise RuntimeError("Palmier did not return a matching response")
            reply = replies[-1]
        else:
            reply = json.loads(body)
        if "error" in reply:
            raise RuntimeError(f"Palmier MCP error: {reply['error']}")
        return reply["result"]

    def connect(self):
        result = self.request("initialize", {
            "protocolVersion": PROTOCOL, "capabilities": {},
            "clientInfo": {"name": "yt-stories-inspect", "version": "1.0"},
        })
        self.headers["MCP-Protocol-Version"] = result["protocolVersion"]
        self.request("notifications/initialized", notification=True)

    def read_tool(self, name, arguments):
        # Explicit allowlist: this diagnostic cannot mutate a project or spend credits.
        allowed = (
            name == "manage_project" and arguments == {"action": "list"}
            or name == "get_media" and set(arguments) == {"projectId"}
            and isinstance(arguments.get("projectId"), str) and bool(arguments["projectId"])
            or name == "get_timeline" and set(arguments) == {"projectId", "timelineId"}
            and all(isinstance(arguments.get(k), str) and arguments[k]
                    for k in ("projectId", "timelineId"))
        )
        if not allowed:
            raise ValueError("Only read-only project discovery is supported")
        result = self.request("tools/call", {"name": name, "arguments": arguments})
        if result.get("isError"):
            raise RuntimeError(f"Palmier refused the read: {result.get('content')}")
        texts = [c["text"] for c in result.get("content", []) if c.get("type") == "text"]
        if len(texts) != 1:
            raise RuntimeError("Unexpected Palmier response; inspect current tool schema")
        return json.loads(texts[0])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-id", help="Exact ID from manage_project/list")
    parser.add_argument("--timeline-id", help="Exact ID from get_media for that project")
    args = parser.parse_args()
    if args.timeline_id and not args.project_id:
        parser.error("--timeline-id requires --project-id")
    try:
        connection = PalmierConnection()
        connection.connect()
        projects = connection.read_tool("manage_project", {"action": "list"})
        result = {"projects": projects,
                  "note": "Use exact projectId and timelineId; visibility does not select the edit target."}
        if args.project_id:
            project = next((x for x in projects.get("projects", [])
                            if x.get("id") == args.project_id), None)
            if not project or not project.get("isAccessible"):
                raise ValueError("Project ID was not found or is not accessible")
            if not project.get("isOpen"):
                raise ValueError("Project is not loaded; open it in the background, then inspect again")
            inventory = connection.read_tool("get_media", {"projectId": args.project_id})
            result["project"] = {k: project.get(k) for k in ("id", "name", "path", "isOpen", "isVisible")}
            result["timelines"] = inventory.get("timelines", [])
            if args.timeline_id:
                matches = [x for x in result["timelines"] if x.get("timelineId") == args.timeline_id]
                if len(matches) != 1:
                    raise ValueError("Timeline ID is not present in the selected project's media inventory")
                result["selected_timeline"] = connection.read_tool("get_timeline", {
                    "projectId": args.project_id, "timelineId": args.timeline_id})
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (OSError, ValueError, KeyError, RuntimeError, urllib.error.URLError) as exc:
        print(f"Cannot inspect Palmier: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
