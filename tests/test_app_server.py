"""App Server wire contracts, with synthetic responses and no network/model calls."""
import json
from pathlib import Path
import sys
import threading
import tempfile
import unittest
from unittest.mock import patch

from ytvideos.errors import WorkflowError
from ytvideos.packets import instruction_files
from ytvideos.runtime.app_server import AppServer, ImageNotSent, RpcError, RpcUnavailable, StdioRpc


class FakeRpc:
    def __init__(self, responses):
        self.responses = iter(responses)
        self.calls = []
        self.notifications = []

    def call(self, method, params):
        self.calls.append((method, params))
        value = next(self.responses)
        if isinstance(value, Exception):
            raise value
        return value

    def notify(self, method, params):
        self.notifications.append((method, params))


class ProtocolTests(unittest.TestCase):
    def worker_directory(self, *, legacy=False):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        directory = Path(temporary.name)
        packet = {"skill": {"path": ".agents/skills/ytv-produce-video/SKILL.md",
                            "text": "# Synthetic image skill\n"},
                  "references": [], "reference_documents": []}
        if legacy:
            files = {"TASK.json": json.dumps(packet).encode(),
                     "SKILL.md": packet["skill"]["text"].encode()}
        else:
            _, files = instruction_files(packet)
        for name, data in files.items():
            target = directory / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
        return directory

    def test_probe_pages_models_and_never_substitutes(self):
        rpc = FakeRpc([{"userAgent": "fixture"}, {"account": {"type": "chatgpt"}}, {"data": [{"model": "other"}], "nextCursor": "next"},
                       {"data": [{"model": "test-luna"}], "nextCursor": None}])
        result = AppServer(rpc, "test-luna").probe()
        self.assertEqual(result["model"], "test-luna")
        self.assertEqual(rpc.calls[-1][1]["cursor"], "next")
        self.assertEqual(rpc.notifications, [("initialized", {})])
        self.assertNotIn("thread/start", [name for name, _ in rpc.calls])
        with self.assertRaisesRegex(WorkflowError, "no fallback"):
            AppServer(FakeRpc([{}, {"account": {"type": "chatgpt"}}, {"data": []}]), "not-present").probe()

    def test_new_thread_and_explicit_skill_use_restricted_workdir(self):
        rpc = FakeRpc([{"thread": {"id": "thread-1"}, "model": "test-luna"}, {"data": []}, {"turn": {"id": "turn-1"}}])
        server = AppServer(rpc, "test-luna")
        directory = self.worker_directory()
        self.assertEqual(server.start_thread(directory), "thread-1")
        prompt = server.image_prompt("task-marker")
        self.assertEqual(server.start_image("thread-1", directory, prompt), "turn-1")
        self.assertFalse(rpc.calls[0][1]["ephemeral"])
        params = rpc.calls[-1][1]
        self.assertEqual(params["approvalPolicy"], "never")
        self.assertFalse(params["sandboxPolicy"]["networkAccess"])
        self.assertEqual(params["sandboxPolicy"]["writableRoots"], [str(directory)])
        self.assertEqual(params["input"][1]["type"], "skill")
        self.assertEqual(params["input"][1]["path"],
                         str(directory / "requirements/.agents/skills/ytv-produce-video/SKILL.md"))
        self.assertIn("skill.local_path", prompt)
        self.assertIn("task-marker", params["input"][0]["text"])
        self.assertNotIn("thread/fork", [name for name, _ in rpc.calls])

    def test_changed_model_or_absent_identifiers_fail_closed(self):
        with self.assertRaises(RpcUnavailable):
            AppServer(FakeRpc([{"thread": {"id": "x"}, "model": "other"}]), "wanted").start_thread("/tmp")
        with self.assertRaises(RpcUnavailable):
            AppServer(FakeRpc([{"data": []}, {}]), "wanted").start_image("x", self.worker_directory(), "test")

    def test_legacy_saved_packet_keeps_its_root_skill_attachment(self):
        directory = self.worker_directory(legacy=True)
        before = (directory / "TASK.json").read_bytes()
        rpc = FakeRpc([{"data": []}, {"turn": {"id": "legacy-turn"}}])
        self.assertEqual(AppServer(rpc, "fixture").start_image("thread", directory, "fixture"), "legacy-turn")
        self.assertEqual(rpc.calls[-1][1]["input"][1]["path"], str(directory / "SKILL.md"))
        self.assertEqual((directory / "TASK.json").read_bytes(), before)

    def test_changed_skill_or_escaping_descriptor_stops_before_native_generation(self):
        for mutation in ("changed", "escape", "unsupported"):
            with self.subTest(mutation=mutation):
                directory = self.worker_directory()
                task_file = directory / "TASK.json"
                task = json.loads(task_file.read_text())
                if mutation == "changed":
                    (directory / task["skill"]["local_path"]).write_text("altered skill")
                elif mutation == "escape":
                    task["skill"]["local_path"] = "../outside/SKILL.md"
                    task_file.write_text(json.dumps(task))
                else:
                    task["materialization_version"] = 99
                    task_file.write_text(json.dumps(task))
                rpc = FakeRpc([{"data": []}])
                with self.assertRaises(ImageNotSent):
                    AppServer(rpc, "fixture").start_image("thread", directory, "fixture")
                self.assertEqual([method for method, _ in rpc.calls], ["mcpServerStatus/list"])

    def test_history_reads_every_page_without_resuming(self):
        rpc = FakeRpc([{"data": [{"id": "t1"}], "nextCursor": "next"}, {"data": [{"id": "t2"}]}])
        self.assertEqual([t["id"] for t in AppServer(rpc, "fixture").turns("x")], ["t1", "t2"])
        self.assertEqual({method for method, _ in rpc.calls}, {"thread/turns/list"})
        self.assertEqual(rpc.calls[0][1]["itemsView"], "full")

    def test_read_fallback_only_for_unsupported_method(self):
        rpc = FakeRpc([RpcError("thread/turns/list", -32601), {"thread": {"turns": []}}])
        self.assertEqual(AppServer(rpc, "fixture").turns("x"), [])
        self.assertTrue(rpc.calls[-1][1]["includeTurns"])
        rpc = FakeRpc([RpcError("thread/turns/list", -32600)])
        with self.assertRaises(RpcError):
            AppServer(rpc, "fixture").turns("x")
        self.assertEqual(len(rpc.calls), 1)

    def test_repeated_cursor_and_partial_history_are_not_success(self):
        rpc = FakeRpc([{"data": [], "nextCursor": "x"}, {"data": [], "nextCursor": "x"}])
        with self.assertRaises(RpcUnavailable):
            AppServer(rpc, "fixture").turns("thread")
        with self.assertRaises(RpcUnavailable):
            AppServer(FakeRpc([{"data": "not history"}]), "fixture").turns("thread")

    def test_probe_rejects_api_key_or_missing_login(self):
        for account in ({"type": "apiKey"}, {}, None, {"type": "amazonBedrock"}):
            with self.subTest(account=account), self.assertRaises(WorkflowError):
                AppServer(FakeRpc([{}, {"account": account}]), "fixture").probe()

    def test_inherited_mcp_tools_stop_before_generation(self):
        rpc = FakeRpc([{"data": [{"name": "publishing-tools"}]}])
        with self.assertRaisesRegex(WorkflowError, "inherited MCP"):
            AppServer(rpc, "fixture").start_image("owned", "/tmp/owned", "fixture")
        self.assertEqual([name for name, _ in rpc.calls], ["mcpServerStatus/list"])


class TransportTests(unittest.TestCase):
    def process(self, source, *, timeout=2):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        path = Path(temporary.name) / "fake_server.py"
        path.write_text(source)
        rpc = StdioRpc([sys.executable, "-u", str(path)], timeout=timeout)
        self.addCleanup(rpc.close)
        return rpc, Path(temporary.name)

    def test_json_lines_notifications_and_server_requests_are_safe(self):
        rpc, _ = self.process('''import json, sys
for line in sys.stdin:
    request = json.loads(line)
    if "method" not in request:
        continue
    print(json.dumps({"method":"item/agentMessage/delta", "params":{"delta":"fixture"}}), flush=True)
    print(json.dumps({"id":"permission", "method":"item/commandExecution/requestApproval", "params":{}}), flush=True)
    denied = json.loads(sys.stdin.readline())
    print(json.dumps({"id":request["id"], "result":{"denied":denied["error"]["code"] == -32601}}), flush=True)
''')
        self.assertTrue(rpc.call("test", {})["denied"])
        self.assertEqual(rpc.denied_requests, 1)

    def test_mutating_request_timeout_is_sent_only_once(self):
        rpc, directory = self.process('''import json, pathlib, sys, time
ready = json.loads(sys.stdin.readline())
print(json.dumps({"id": ready["id"], "result": {"ready": True}}), flush=True)
request = json.loads(sys.stdin.readline())
pathlib.Path(__file__).with_name("sent.json").write_text(json.dumps(request))
time.sleep(5)
''')
        rpc.call("fixture-ready", {})
        rpc.timeout = 0.2
        with self.assertRaises(RpcUnavailable):
            rpc.call("turn/start", {"threadId": "owned"})
        self.assertEqual(json.loads((directory / "sent.json").read_text())["method"], "turn/start")
        self.assertEqual(rpc._sequence, 2)

    def test_errors_do_not_leak_provider_text_and_disconnect_is_explicit(self):
        rpc, _ = self.process('''import json, sys
request = json.loads(sys.stdin.readline())
print(json.dumps({"id":request["id"],"error":{"code":-1,"message":"SECRET_FIXTURE"}}), flush=True)
''')
        with self.assertRaises(RpcError) as caught:
            rpc.call("test", {})
        self.assertNotIn("SECRET_FIXTURE", str(caught.exception))
        with self.assertRaises(RpcUnavailable):
            rpc.call("second", {})

    def test_late_unrelated_response_does_not_complete_request(self):
        rpc, _ = self.process('''import json, sys
request=json.loads(sys.stdin.readline())
print(json.dumps({"id":-1,"result":{"value":"wrong"}}),flush=True)
print(json.dumps({"id":request["id"],"result":{"value":"right"}}),flush=True)
''')
        self.assertEqual(rpc.call("test", {})["value"], "right")

    def test_worker_does_not_inherit_state_or_provider_secrets(self):
        with patch.dict("os.environ", {"YTV_DATABASE_URL": "secret-db", "OPENAI_API_KEY": "secret-key",
                                      "ELEVENLABS_API_KEY": "secret-tts", "YTV_SIGNING_KEY": "secret-signing"}):
            rpc, _ = self.process('''import json, os, sys
request = json.loads(sys.stdin.readline())
keys = [k for k in os.environ if k.startswith("YTV_") or k.endswith("API_KEY")]
print(json.dumps({"id": request["id"], "result": {"secret_names": keys}}), flush=True)
''')
        self.assertEqual(rpc.call("fixture-environment", {})["secret_names"], [])


    def test_write_to_unresponsive_subprocess_obeys_request_timeout(self):
        rpc, _ = self.process("import time; time.sleep(5)", timeout=0.15)
        errors = []
        def invoke():
            try:
                rpc.call("turn/start", {"text": "x" * (1024 * 1024)})
            except BaseException as exc:
                errors.append(exc)
        worker = threading.Thread(target=invoke, daemon=True)
        worker.start()
        worker.join(timeout=0.8)
        hung = worker.is_alive()
        if not hung:
            with self.assertRaises(RpcUnavailable):
                rpc.call("must-not-reuse-partial-stream", {})
        rpc.close()
        worker.join(timeout=1)
        self.assertFalse(hung, "request deadline must include blocked pipe writes")
        self.assertEqual(len(errors), 1)
        self.assertIsInstance(errors[0], RpcUnavailable)

    def test_malformed_error_is_sanitized_not_interpreted_as_provider_text(self):
        for error in (None, "SECRET_FIXTURE", {"code": "SECRET_FIXTURE"}, {"code": True}):
            source = "import json,sys\nr=json.loads(sys.stdin.readline())\n"
            source += "print(json.dumps({'id':r['id'],'error':" + repr(error) + "}),flush=True)\n"
            with self.subTest(error=error):
                rpc, _ = self.process(source)
                with self.assertRaises(RpcUnavailable) as caught:
                    rpc.call("test", {})
                self.assertNotIn("SECRET_FIXTURE", str(caught.exception))
