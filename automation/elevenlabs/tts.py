#!/usr/bin/env python3
"""Create independently resumable RU/EN voice assets with ElevenLabs."""

import argparse
import base64
import binascii
import contextlib
import fcntl
import importlib.util
import json
import hashlib
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request

_config_path = Path(__file__).resolve().parents[1] / 'helpers/channel_config.py'
_config_spec = importlib.util.spec_from_file_location('tts_channel_config', _config_path)
channel_config = importlib.util.module_from_spec(_config_spec)
_config_spec.loader.exec_module(channel_config)
MODEL_ID = "eleven_v4"
OUTPUT_FORMAT = "mp3_44100_128"
MAX_V4_CHARS = 10000


class TTSError(Exception):
    pass


class AccountUnavailable(TTSError):
    pass


class QuotaExceeded(AccountUnavailable):
    pass


class AuthenticationUnavailable(AccountUnavailable):
    pass


class VoiceUnavailable(AccountUnavailable):
    pass


def unit_interval(value):
    try:
        number = float(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("ожидается число от 0 до 1") from exc
    if not 0 <= number <= 1:
        raise argparse.ArgumentTypeError("ожидается число от 0 до 1")
    return number


def voice_speed(value):
    try:
        number = float(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("ожидается скорость от 0.7 до 1.2") from exc
    if not 0.7 <= number <= 1.2:
        raise argparse.ArgumentTypeError("ожидается скорость от 0.7 до 1.2")
    return number


def channel_voice(channel):
    try:
        return channel_config.voice_id(channel)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        raise TTSError(f"не удалось определить канальный голос для {channel}: {exc}") from None


def arguments(argv=None):
    parser = argparse.ArgumentParser(description="Озвучка UTF-8 текстов RU/EN через ElevenLabs. Без --generate сеть не используется.", allow_abbrev=False)
    parser.add_argument("--ru-text", type=Path, help="путь к утверждённому русскому тексту")
    parser.add_argument("--en-text", type=Path, help="путь к утверждённому английскому тексту")
    parser.add_argument("--output-dir", type=Path, required=True, help="каталог Source/Voice для результата")
    parser.add_argument("--channel", required=True, choices=channel_config.configured_channels())
    parser.add_argument("--voice-id", help="необязательная проверка ID; должен совпадать с реестром")
    parser.add_argument("--model", default=MODEL_ID)
    parser.add_argument("--stability", type=unit_interval, default=1.0)
    parser.add_argument("--similarity", type=unit_interval, default=0.0)
    parser.add_argument("--speed", type=voice_speed, default=None,
                        help="скорость генерации ElevenLabs от 0.7 до 1.2; по умолчанию не задаётся")
    parser.add_argument("--generate", action="store_true", help="действительно отправить платные запросы")
    return parser.parse_args(argv)


def prepare(args):
    if not re.fullmatch(r"[A-Za-z0-9_-]+", args.voice_id):
        raise TTSError("некорректный voice ID")
    if not re.fullmatch(r"[A-Za-z0-9_-]+", args.model):
        raise TTSError("некорректный ID модели")
    if not args.ru_text and not args.en_text:
        raise TTSError("нужен хотя бы один входной файл: --ru-text и/или --en-text")
    if args.output_dir.exists() and not args.output_dir.is_dir():
        raise TTSError("output-dir существует, но не является каталогом")
    jobs = []
    for language, path in (("ru", args.ru_text), ("en", args.en_text)):
        if path is None:
            continue
        try:
            content = path.read_text(encoding="utf-8").strip()
        except (OSError, UnicodeError) as exc:
            raise TTSError(f"не удалось прочитать UTF-8 текст {language}: {path}") from exc
        if not content:
            raise TTSError(f"пустой текст {language}: {path}")
        if args.model == MODEL_ID and len(content) > MAX_V4_CHARS:
            raise TTSError(f"текст {language} превышает 10 000 символов для Eleven v4; разделите его вручную")
        destination = args.output_dir / f"voice_{language}.mp3"
        for output in (destination, destination.with_suffix(".alignment.json"), destination.with_suffix(".request.json")):
            if output.exists() or output.is_symlink():
                raise TTSError(f"файл уже существует: {output}; используйте другой каталог или запустите только недостающий язык")
        jobs.append((language, content, destination))
    return jobs


def synthesize(text, destination, *, api_key, voice_id, model=MODEL_ID,
               stability=1.0, similarity=0.0, speed=None):
    """One request, no automatic retries. Never overwrites an existing asset."""
    query = urllib.parse.urlencode({"output_format": OUTPUT_FORMAT})
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}/with-timestamps?{query}"
    voice_settings = {"stability": stability, "similarity_boost": similarity}
    if speed is not None:
        voice_settings["speed"] = speed
    payload = json.dumps({"text": text, "model_id": model, "voice_settings": voice_settings}, ensure_ascii=False).encode("utf-8")
    request = urllib.request.Request(url, data=payload, headers={
        "xi-api-key": api_key, "Content-Type": "application/json", "Accept": "application/json",
    }, method="POST")
    try:
        with urllib.request.urlopen(request, timeout=180) as response:
            content_type = response.headers.get_content_type()
            if content_type != "application/json":
                raise TTSError(f"неожиданный тип ответа API: {content_type}")
            response_data = response.read()
    except urllib.error.HTTPError as exc:
        # Do not print the response: it may contain user text or other sensitive data.
        try:
            detail = json.loads(exc.read(65536)).get("detail", {})
            code = detail.get("code") or detail.get("status") if isinstance(detail, dict) else None
        except (ValueError, TypeError, AttributeError, OSError):
            code = None
        if exc.code in (400, 401, 402) and code in ("quota_exceeded", "insufficient_credits"):
            raise QuotaExceeded("ElevenLabs сообщает о недостатке кредитов") from None
        if exc.code == 401:
            raise AuthenticationUnavailable("ElevenLabs отклонил ключ (HTTP 401)") from None
        if exc.code == 403 and code in ("insufficient_permissions", "voice_access_denied", "model_access_denied", "feature_not_available", "workspace_access_denied"):
            raise AccountUnavailable("ElevenLabs отклонил доступ аккаунта (HTTP 403)") from None
        raise TTSError(f"ElevenLabs вернул HTTP {exc.code}; проверьте ключ, доступ к голосу и модели, лимит и параметры") from None
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        raise TTSError("ошибка связи с ElevenLabs; результат и расход кредитов на стороне сервиса неизвестны, проверьте историю перед повтором") from None
    try:
        result = json.loads(response_data)
        audio = base64.b64decode(result["audio_base64"], validate=True)
        alignment = {"alignment": result.get("alignment"), "normalized_alignment": result.get("normalized_alignment")}
    except (ValueError, TypeError, KeyError, AttributeError, binascii.Error):
        raise TTSError("API вернул некорректный ответ; проверьте историю сервиса перед повтором") from None
    if len(audio) < 4 or not (audio.startswith(b"ID3") or (audio[0] == 0xff and audio[1] & 0xe0 == 0xe0)):
        raise TTSError("API вернул пустой или не похожий на MP3 ответ; файл не сохранён")
    save_new(destination, audio)
    save_new(destination.with_suffix(".alignment.json"), (json.dumps(alignment, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
    if alignment["alignment"] is None:
        print(f"Внимание: API не вернул alignment для {destination}; потребуется отдельная синхронизация.", file=sys.stderr)


def save_new(destination, data):
    temp_path = None
    try:
        destination.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile(dir=destination.parent, prefix=".tts-", delete=False) as temp:
            temp_path = Path(temp.name)
            temp.write(data)
            temp.flush()
            os.fsync(temp.fileno())
        # Atomic creation without replacing existing files, even in a race.
        os.link(temp_path, destination)
    except OSError:
        raise TTSError(f"ответ получен, но файл {destination} не сохранён; проверьте историю сервиса перед повтором") from None
    finally:
        if temp_path is not None:
            temp_path.unlink(missing_ok=True)


def get_api_key(*, slot=1, backup=False):
    if backup:
        slot = 2
    suffix = "" if slot == 1 else f"_{slot}"
    key = os.environ.get("ELEVENLABS_API_KEY" + suffix, "").strip()
    if key:
        return key
    if sys.platform == "darwin":
        service = "yt-stories-elevenlabs" + ("" if slot == 1 else f"-{slot}")
        try:
            result = subprocess.run(
                ["/usr/bin/security", "find-generic-password", "-a", "yt-stories", "-s", service, "-w"],
                capture_output=True, text=True, timeout=30, check=False,
            )
            if result.returncode == 0:
                return result.stdout.strip()
        except (OSError, subprocess.TimeoutExpired):
            pass
    return ""


def configured_keys():
    # Environment slots may be sparse. Additional Keychain slots must be listed explicitly.
    slots = {1, 2}
    for name in os.environ:
        match = re.fullmatch(r"ELEVENLABS_API_KEY_([1-9][0-9]*)", name)
        if match:
            slots.add(int(match.group(1)))
    configured = os.environ.get("ELEVENLABS_KEYCHAIN_SLOTS", "")
    if configured:
        for value in configured.split(","):
            if not re.fullmatch(r"[1-9][0-9]*", value.strip()):
                raise TTSError("ELEVENLABS_KEYCHAIN_SLOTS должен содержать номера через запятую")
            slots.add(int(value.strip()))
    keys = []
    for slot in sorted(slots):
        key = get_api_key(slot=slot)
        if key and key not in keys:
            keys.append(key)
    return keys


def verify_backup_voice(api_key, voice_id):
    request = urllib.request.Request(f"https://api.elevenlabs.io/v1/voices/{voice_id}",
                                     headers={"xi-api-key": api_key})
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            data = json.load(response)
        if not isinstance(data, dict) or data.get("voice_id") != voice_id:
            raise VoiceUnavailable("аккаунт не подтвердил тот же voice ID")
    except urllib.error.HTTPError as exc:
        if exc.code == 401:
            raise AuthenticationUnavailable("аккаунт отклонил ключ (HTTP 401)") from None
        if exc.code in (403, 404):
            raise VoiceUnavailable(f"аккаунт не подтвердил доступ к голосу (HTTP {exc.code})") from None
        raise TTSError(f"проверка голоса вернула HTTP {exc.code}; генерация остановлена") from None
    except (urllib.error.URLError, TimeoutError, OSError, ValueError):
        raise TTSError("не удалось проверить голос из-за ошибки связи или ответа; генерация остановлена") from None


# Shared across worktrees/processes of this local user. No API keys or request text are stored.
VOICE_TTL = 600
FAIL_TTL = 120
QUOTA_TTL = 60


def cache_path():
    return Path(os.environ.get("ELEVENLABS_CACHE_DIR", Path.home() / ".cache" / "ytvideos" / "elevenlabs"))


@contextlib.contextmanager
def locked_cache():
    directory = cache_path()
    try:
        directory.mkdir(parents=True, exist_ok=True, mode=0o700)
        os.chmod(directory, 0o700)
        with (directory / "lock").open("a+b") as lock:
            os.chmod(directory / "lock", 0o600)
            fcntl.flock(lock, fcntl.LOCK_EX)
            path = directory / "state.json"
            try:
                state = json.loads(path.read_text())
                if not isinstance(state, dict) or state.get("version") != 1 or not isinstance(state.get("accounts"), dict):
                    state = {"version": 1, "accounts": {}}
            except (OSError, ValueError):
                state = {"version": 1, "accounts": {}}
            yield state
            temp_name = None
            try:
                with tempfile.NamedTemporaryFile(mode="w", dir=directory, prefix=".state-", delete=False) as temp:
                    temp_name = temp.name
                    json.dump(state, temp, separators=(",", ":"))
                    temp.flush()
                    os.fsync(temp.fileno())
                os.replace(temp_name, path)
            finally:
                if temp_name and os.path.exists(temp_name):
                    os.unlink(temp_name)
    except OSError:
        raise TTSError("не удалось использовать локальный кеш ElevenLabs; проверьте права каталога") from None


def current(stamp, ttl):
    return isinstance(stamp, (int, float)) and 0 <= time.time() - stamp < ttl


def account_id(key):
    return hashlib.sha256(key.encode()).hexdigest()


def preflight(key, voice_id, text_length, model=MODEL_ID):
    # Lock spans the read-only voice check: only one process performs it per account/voice/TTL.
    with locked_cache() as state:
        account = state["accounts"].setdefault(account_id(key), {})
        if current(account.get("auth_failed"), FAIL_TTL):
            raise AuthenticationUnavailable("ключ недавно отклонён")
        quota = account.get("quota", {}).get(model, {})
        if isinstance(quota, dict) and current(quota.get("time"), QUOTA_TTL) and text_length >= quota.get("length", float("inf")):
            raise QuotaExceeded("недавно подтверждена нехватка кредитов")
        voices = account.setdefault("voices", {})
        voice = voices.get(voice_id, {})
        if isinstance(voice, dict):
            if current(voice.get("ok"), VOICE_TTL):
                return
            if current(voice.get("failed"), FAIL_TTL):
                raise VoiceUnavailable("голос недавно был недоступен")
        try:
            verify_backup_voice(key, voice_id)
        except AuthenticationUnavailable:
            account["auth_failed"] = time.time()
            # Persist the failure before reporting it to the caller.
            failure = AuthenticationUnavailable("ключ отклонён")
        except VoiceUnavailable:
            voices[voice_id] = {"failed": time.time()}
            failure = VoiceUnavailable("голос недоступен")
        else:
            voices[voice_id] = {"ok": time.time()}
            failure = None
    if failure:
        raise failure


def record_failure(key, voice_id, text_length, error, model=MODEL_ID):
    with locked_cache() as state:
        account = state["accounts"].setdefault(account_id(key), {})
        if isinstance(error, AuthenticationUnavailable):
            account["auth_failed"] = time.time()
            account["voices"] = {}
        elif isinstance(error, QuotaExceeded):
            account.setdefault("quota", {})[model] = {"time": time.time(), "length": text_length}
        else:
            # Authorization can be model-specific; don't cache it across models.
            account.setdefault("voices", {}).pop(voice_id, None)


def synthesize_with_failover(text, destination, *, api_keys, voice_id, **settings):
    if not api_keys:
        raise TTSError("не найден ни один ключ ElevenLabs; настройте ключ и повторите")
    for index, key in enumerate(api_keys, 1):
        try:
            preflight(key, voice_id, len(text), settings.get("model", MODEL_ID))
            try:
                synthesize(text, destination, api_key=key, voice_id=voice_id, **settings)
            except AccountUnavailable as exc:
                record_failure(key, voice_id, len(text), exc, settings.get("model", MODEL_ID))
                raise
            return
        except AccountUnavailable as exc:
            print(f"Аккаунт {index}: {exc}; пробуем следующий, если он есть.", file=sys.stderr)
    raise TTSError("ни один настроенный аккаунт ElevenLabs не подошёл: проверьте ключи, квоту и доступ к тому же voice ID") from None


def main(argv=None):
    args = arguments(argv)
    try:
        selected_voice = channel_voice(args.channel)
        if args.voice_id is not None and args.voice_id != selected_voice:
            raise TTSError("voice ID не совпадает с голосом канала; запрос остановлен")
        args.voice_id = selected_voice
        jobs = prepare(args)
        for language, content, destination in jobs:
            print(f"{language}: {len(content)} символов → {destination}")
        print(f"Голос: {args.voice_id}; модель: {args.model}; формат: {OUTPUT_FORMAT}; stability: {args.stability}; similarity: {args.similarity}; speed: {args.speed if args.speed is not None else 'не задана'}")
        if not args.generate:
            print("Проверка завершена без сети и без расхода кредитов. Для генерации добавьте --generate.")
            return 0
        keys = configured_keys()
        if not keys:
            raise TTSError("не найден ни один ключ ElevenLabs; настройте ключ и повторите")
        for language, content, destination in jobs:
            receipt = destination.with_suffix(".request.json")
            record = {"channel": args.channel, "voice_id": args.voice_id, "model": args.model,
                      "format": OUTPUT_FORMAT, "stability": args.stability, "similarity": args.similarity,
                      "speed": args.speed, "text_sha256": hashlib.sha256(content.encode("utf-8")).hexdigest(),
                      "status": "request_started"}
            save_new(receipt, (json.dumps(record, ensure_ascii=False, indent=2) + "\n").encode())
            synthesize_with_failover(content, destination, api_keys=keys, voice_id=args.voice_id, model=args.model,
                       stability=args.stability, similarity=args.similarity, speed=args.speed)
            record.update(status="success", audio_sha256=hashlib.sha256(destination.read_bytes()).hexdigest())
            receipt.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            print(f"Готово: {language} → {destination}")
        return 0
    except TTSError as exc:
        print(f"Ошибка: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
