import base64
import contextlib
from email.message import Message
import io
import json
import multiprocessing
import time
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import urllib.error

import tts


class Response:
    def __init__(self, data):
        self.data = data
        self.headers = Message()
        self.headers["Content-Type"] = "application/json"

    def __enter__(self):
        return self

    def __exit__(self, *args):
        pass

    def read(self):
        return self.data


class VoiceTests(unittest.TestCase):
    def setUp(self):
        self.cache = tempfile.TemporaryDirectory()
        self.addCleanup(self.cache.cleanup)
        env = patch.dict(os.environ, {"ELEVENLABS_CACHE_DIR": self.cache.name})
        env.start()
        self.addCleanup(env.stop)

    def test_channel_contract_blocks_mismatch_before_network(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            script = root / "text.txt"
            script.write_text("Hello", encoding="utf-8")
            with patch("tts.get_api_key") as key, patch("tts.urllib.request.urlopen") as send, contextlib.redirect_stderr(io.StringIO()):
                result = tts.main(["--channel", "paper_detour", "--voice-id", tts.channel_voice("nuviko_history"),
                                   "--en-text", str(script), "--output-dir", str(root / "out"), "--generate"])
            self.assertEqual(result, 1)
            key.assert_not_called()
            send.assert_not_called()
            self.assertFalse((root / "out").exists())

    def test_channel_routes_correct_id_and_rejects_unavailable_voice(self):
        for channel in ("paper_detour", "nuviko_history"):
            with self.subTest(channel=channel), tempfile.TemporaryDirectory() as folder:
                root = Path(folder)
                script = root / "text.txt"
                script.write_text("Hello", encoding="utf-8")
                with patch("tts.configured_keys", return_value=["key"]), patch("tts.verify_backup_voice", side_effect=tts.TTSError("unavailable")) as check, patch("tts.synthesize") as send, contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                    result = tts.main(["--channel", channel, "--en-text", str(script), "--output-dir", str(root / "out"), "--generate"])
                self.assertEqual(result, 1)
                check.assert_called_once_with("key", tts.channel_voice(channel))
                send.assert_not_called()

    def test_channel_is_mandatory_and_unique(self):
        self.assertNotEqual(tts.channel_voice("paper_detour"), tts.channel_voice("nuviko_history"))
        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            tts.arguments(["--output-dir", "/tmp/example"])

    def test_channel_request_uses_registry_id(self):
        result = {"audio_base64": base64.b64encode(b"ID3fake mp3").decode(), "alignment": None}
        for channel in ("paper_detour", "nuviko_history"):
            with self.subTest(channel=channel), tempfile.TemporaryDirectory() as folder:
                root = Path(folder)
                script = root / "text.txt"
                script.write_text("Hello", encoding="utf-8")
                voice_id = tts.channel_voice(channel)
                responses = [Response(json.dumps({"voice_id": voice_id}).encode()), Response(json.dumps(result).encode())]
                with patch("tts.configured_keys", return_value=["key"]), patch("tts.urllib.request.urlopen", side_effect=responses) as send, contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                    self.assertEqual(tts.main(["--channel", channel, "--en-text", str(script), "--output-dir", str(root / "out"), "--generate"]), 0)
                check, post = [call.args[0] for call in send.call_args_list]
                self.assertEqual(check.get_method(), "GET")
                self.assertIn("/text-to-speech/" + voice_id + "/", post.full_url)
                record = json.loads((root / "out" / "voice_en.request.json").read_text())
                self.assertEqual((record["channel"], record["voice_id"], record["status"]), (channel, voice_id, "success"))

    def test_optional_speed_in_request(self):
        result = {"audio_base64": base64.b64encode(b"ID3fake mp3").decode(),
                  "alignment": None, "normalized_alignment": None}
        with tempfile.TemporaryDirectory() as folder, contextlib.redirect_stderr(io.StringIO()):
            with patch("tts.urllib.request.urlopen", return_value=Response(json.dumps(result).encode())) as send:
                tts.synthesize("Hello", Path(folder) / "voice.mp3", api_key="secret", voice_id="testvoice", speed=0.8)
            self.assertEqual(json.loads(send.call_args.args[0].data)["voice_settings"]["speed"], 0.8)
        self.assertEqual(tts.voice_speed("0.7"), 0.7)
        self.assertEqual(tts.voice_speed("1.2"), 1.2)
        with self.assertRaises(tts.argparse.ArgumentTypeError):
            tts.voice_speed("0.69")

    def test_request_and_separate_alignment(self):
        result = {"audio_base64": base64.b64encode(b"ID3fake mp3").decode(),
                  "alignment": {"characters": ["П"], "character_start_times_seconds": [0], "character_end_times_seconds": [0.1]},
                  "normalized_alignment": None}
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "voice_ru.mp3"
            with patch("tts.urllib.request.urlopen", return_value=Response(json.dumps(result).encode())) as send:
                tts.synthesize("Привет", path, api_key="secret", voice_id="testvoice")
            request = send.call_args.args[0]
            payload = json.loads(request.data)
            self.assertIn("/with-timestamps?output_format=mp3_44100_128", request.full_url)
            self.assertEqual(payload["model_id"], "eleven_v4")
            self.assertEqual(payload["voice_settings"], {"stability": 1.0, "similarity_boost": 0.0})
            self.assertNotIn("language_code", payload)
            self.assertEqual(path.read_bytes(), b"ID3fake mp3")
            self.assertEqual(json.loads(path.with_suffix(".alignment.json").read_text())["alignment"], result["alignment"])

    def test_preflight_prevents_any_network_when_second_output_exists(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / "ru.txt").write_text("Привет", encoding="utf-8")
            (root / "en.txt").write_text("Hello", encoding="utf-8")
            (root / "voice_en.mp3").write_bytes(b"old")
            with patch("tts.urllib.request.urlopen") as send, contextlib.redirect_stderr(io.StringIO()):
                result = tts.main(["--channel", "paper_detour", "--ru-text", str(root / "ru.txt"), "--en-text", str(root / "en.txt"), "--output-dir", folder, "--generate"])
            self.assertEqual(result, 1)
            send.assert_not_called()
            self.assertFalse((root / "voice_ru.mp3").exists())

    def test_dry_run_never_fetches_key_or_calls_network(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / "ru.txt").write_text("Привет", encoding="utf-8")
            with patch("tts.get_api_key") as key, patch("tts.urllib.request.urlopen") as send, contextlib.redirect_stdout(io.StringIO()):
                result = tts.main(["--channel", "paper_detour", "--ru-text", str(root / "ru.txt"), "--output-dir", str(root / "new")])
            self.assertEqual(result, 0)
            key.assert_not_called()
            send.assert_not_called()
            self.assertFalse((root / "new").exists())

    def test_error_does_not_print_provider_response_or_secret(self):
        error = urllib.error.HTTPError("https://example.invalid", 401, "secret in error", {}, io.BytesIO(b"secret"))
        with tempfile.TemporaryDirectory() as folder, patch("tts.urllib.request.urlopen", side_effect=error):
            with self.assertRaises(tts.TTSError) as raised:
                tts.synthesize("text", Path(folder) / "out.mp3", api_key="secret", voice_id="testvoice")
            self.assertNotIn("secret", str(raised.exception))
            self.assertIn("401", str(raised.exception))

    def test_env_key_takes_precedence_over_keychain(self):
        with patch.dict(os.environ, {"ELEVENLABS_API_KEY": "test-key"}), patch("tts.subprocess.run") as run:
            self.assertEqual(tts.get_api_key(), "test-key")
            run.assert_not_called()

    def test_existing_file_is_not_replaced(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "voice.mp3"
            path.write_bytes(b"original")
            with self.assertRaises(tts.TTSError):
                tts.save_new(path, b"replacement")
            self.assertEqual(path.read_bytes(), b"original")

    def test_failover_auth_quota_and_multiple_accounts(self):
        result = {"audio_base64": base64.b64encode(b"ID3fake mp3").decode(), "alignment": None}
        def error(status, body):
            return urllib.error.HTTPError("https://example.invalid", status, "", {}, io.BytesIO(body))
        voice = Response(json.dumps({"voice_id": "testvoice"}).encode())
        replies = [error(401, b'{}'), voice, error(400, b'{"detail":{"status":"quota_exceeded"}}'), voice, Response(json.dumps(result).encode())]
        with tempfile.TemporaryDirectory() as folder, contextlib.redirect_stderr(io.StringIO()):
            with patch("tts.urllib.request.urlopen", side_effect=replies) as send:
                tts.synthesize_with_failover("Hello", Path(folder) / "voice.mp3", api_keys=["one", "two", "three"], voice_id="testvoice")
            self.assertEqual([c.args[0].get_method() for c in send.call_args_list], ["GET", "GET", "POST", "GET", "POST"])
            self.assertEqual(send.call_args.args[0].get_header("Xi-api-key"), "three")

    def test_synthesis_error_classification(self):
        for status, body, expected in [(401, b'{}', tts.AuthenticationUnavailable), (401, b'{"detail":{"code":"quota_exceeded"}}', tts.QuotaExceeded), (400, b'{"detail":{"status":"quota_exceeded"}}', tts.QuotaExceeded), (400, b'{"detail":{"code":"invalid_parameters"}}', tts.TTSError), (403, b'{"detail":{"code":"voice_access_denied"}}', tts.AccountUnavailable), (403, b'{}', tts.TTSError), (429, b'{}', tts.TTSError), (500, b'{}', tts.TTSError)]:
            with self.subTest(status=status, body=body), tempfile.TemporaryDirectory() as folder:
                error = urllib.error.HTTPError("https://example.invalid", status, "", {}, io.BytesIO(body))
                with patch("tts.urllib.request.urlopen", side_effect=error), self.assertRaises(expected) as raised:
                    tts.synthesize("text", Path(folder) / "out.mp3", api_key="secret", voice_id="testvoice")
                self.assertEqual(type(raised.exception), expected)

    def test_failover_stops_on_ambiguous_failure(self):
        with tempfile.TemporaryDirectory() as folder, patch("tts.verify_backup_voice"), patch("tts.synthesize", side_effect=tts.TTSError("unknown")) as send:
            with self.assertRaisesRegex(tts.TTSError, "unknown"):
                tts.synthesize_with_failover("Hello", Path(folder) / "voice.mp3", api_keys=["one", "two"], voice_id="testvoice")
            self.assertEqual(send.call_count, 1)

    def test_all_unavailable_is_clear_blocker(self):
        with tempfile.TemporaryDirectory() as folder, contextlib.redirect_stderr(io.StringIO()), patch("tts.verify_backup_voice", side_effect=tts.AccountUnavailable("unavailable")):
            with self.assertRaisesRegex(tts.TTSError, "ни один настроенный аккаунт"):
                tts.synthesize_with_failover("Hello", Path(folder) / "voice.mp3", api_keys=["one", "two"], voice_id="testvoice")

    def test_sparse_slots_and_dedup(self):
        with patch.dict(os.environ, {"ELEVENLABS_API_KEY": "one", "ELEVENLABS_API_KEY_3": "three", "ELEVENLABS_API_KEY_5": "one", "ELEVENLABS_KEYCHAIN_SLOTS": "4"}, clear=True), patch.object(tts.sys, "platform", "linux"):
            self.assertEqual(tts.configured_keys(), ["one", "three"])

    def test_cache_is_per_voice_and_expires(self):
        with patch("tts.verify_backup_voice") as check, patch("tts.time.time", return_value=1000):
            tts.preflight("one", "voice1", 10)
            tts.preflight("one", "voice1", 10)
            tts.preflight("one", "voice2", 10)
            self.assertEqual(check.call_count, 2)
        with patch("tts.verify_backup_voice") as check, patch("tts.time.time", return_value=1601):
            tts.preflight("one", "voice1", 10)
            check.assert_called_once()
        self.assertNotIn("one", (Path(self.cache.name) / "state.json").read_text())

    def test_quota_is_length_scoped_and_short_lived(self):
        with patch("tts.verify_backup_voice"), patch("tts.time.time", return_value=1000):
            tts.preflight("one", "voice", 10)
            tts.record_failure("one", "voice", 10, tts.QuotaExceeded())
            with self.assertRaises(tts.QuotaExceeded):
                tts.preflight("one", "voice", 10)
            tts.preflight("one", "voice", 9)
            tts.preflight("one", "voice", 10, model="different")
        with patch("tts.verify_backup_voice"), patch("tts.time.time", return_value=1061):
            tts.preflight("one", "voice", 10)

    def test_auth_failure_invalidates_cached_voice(self):
        with patch("tts.verify_backup_voice") as check, patch("tts.time.time", return_value=1000):
            tts.preflight("one", "voice", 10)
            tts.record_failure("one", "voice", 10, tts.AuthenticationUnavailable())
            with self.assertRaises(tts.AuthenticationUnavailable):
                tts.preflight("one", "voice", 10)
            self.assertEqual(check.call_count, 1)
        with patch("tts.verify_backup_voice") as check, patch("tts.time.time", return_value=1121):
            tts.preflight("one", "voice", 10)
            check.assert_called_once()

    def test_corrupt_cache_and_clock_rollback_recheck(self):
        (Path(self.cache.name) / "state.json").write_text("invalid")
        with patch("tts.verify_backup_voice") as check, patch("tts.time.time", return_value=1000):
            tts.preflight("one", "voice", 10)
            check.assert_called_once()
        with patch("tts.verify_backup_voice") as check, patch("tts.time.time", return_value=999):
            tts.preflight("one", "voice", 10)
            check.assert_called_once()

    def test_failed_check_is_shared_and_recovers_after_ttl(self):
        with patch("tts.verify_backup_voice", side_effect=tts.AuthenticationUnavailable("bad")) as check, patch("tts.time.time", return_value=1000):
            for _ in range(3):
                with self.assertRaises(tts.AuthenticationUnavailable):
                    tts.preflight("one", "voice", 10)
            self.assertEqual(check.call_count, 1)
        with patch("tts.verify_backup_voice") as check, patch("tts.time.time", return_value=1121):
            tts.preflight("one", "voice", 10)
            check.assert_called_once()

    def test_parallel_processes_check_voice_once(self):
        ctx = multiprocessing.get_context("fork")
        calls = ctx.Value("i", 0)
        ready = ctx.Event()
        results = ctx.Queue()
        def verify(*args):
            with calls.get_lock():
                calls.value += 1
            time.sleep(0.15)
        def worker():
            try:
                ready.wait(5)
                with patch("tts.verify_backup_voice", side_effect=verify):
                    tts.preflight("one", "voice", 10)
                results.put("ok")
            except Exception as exc:
                results.put(type(exc).__name__)
        processes = [ctx.Process(target=worker) for _ in range(10)]
        for process in processes:
            process.start()
        ready.set()
        for process in processes:
            process.join(8)
            self.assertEqual(process.exitcode, 0)
        self.assertEqual([results.get(timeout=1) for _ in processes], ["ok"] * 10)
        self.assertEqual(calls.value, 1)


if __name__ == "__main__":
    unittest.main()
