#!/usr/bin/env python3
"""Create independently resumable RU/EN voice assets with ElevenLabs."""

import argparse
import base64
import binascii
import json
import hashlib
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import urllib.error
import urllib.parse
import urllib.request

VOICE_REGISTRY = Path(__file__).resolve().with_name("channel_voices.json")
MODEL_ID = "eleven_v4"
OUTPUT_FORMAT = "mp3_44100_128"
MAX_V4_CHARS = 10000


class TTSError(Exception):
    pass


class QuotaExceeded(TTSError):
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
        registry = json.loads(VOICE_REGISTRY.read_text(encoding="utf-8"))
        voices = registry["channels"]
        if set(voices) != {"paper_detour", "nuviko_history"}:
            raise ValueError("неверный состав каналов")
        ids = [entry["voice_id"] for entry in voices.values()]
        if len(set(ids)) != 2 or any(not re.fullmatch(r"[A-Za-z0-9_-]+", value) for value in ids):
            raise ValueError("голоса должны быть разными и иметь корректные ID")
        return voices[channel]["voice_id"]
    except (OSError, ValueError, KeyError, TypeError) as exc:
        raise TTSError(f"не удалось определить канальный голос для {channel}: {exc}") from None


def arguments(argv=None):
    parser = argparse.ArgumentParser(description="Озвучка UTF-8 текстов RU/EN через ElevenLabs. Без --generate сеть не используется.")
    parser.add_argument("--ru-text", type=Path, help="путь к утверждённому русскому тексту")
    parser.add_argument("--en-text", type=Path, help="путь к утверждённому английскому тексту")
    parser.add_argument("--output-dir", type=Path, required=True, help="каталог Source/Voice для результата")
    parser.add_argument("--channel", required=True, choices=("paper_detour", "nuviko_history"))
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
        if exc.code in (400, 402) and code in ("quota_exceeded", "insufficient_credits"):
            raise QuotaExceeded("ElevenLabs сообщает о недостатке кредитов") from None
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


def get_api_key(*, backup=False):
    key = os.environ.get("ELEVENLABS_API_KEY_2" if backup else "ELEVENLABS_API_KEY", "").strip()
    if key:
        return key
    if sys.platform == "darwin":
        try:
            result = subprocess.run(
                ["/usr/bin/security", "find-generic-password", "-a", "yt-stories", "-s", "yt-stories-elevenlabs-2" if backup else "yt-stories-elevenlabs", "-w"],
                capture_output=True, text=True, timeout=30, check=False,
            )
            if result.returncode == 0:
                return result.stdout.strip()
        except (OSError, subprocess.TimeoutExpired):
            pass
    return ""


def verify_backup_voice(api_key, voice_id):
    request = urllib.request.Request(f"https://api.elevenlabs.io/v1/voices/{voice_id}",
                                     headers={"xi-api-key": api_key})
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            data = json.load(response)
        if not isinstance(data, dict) or data.get("voice_id") != voice_id:
            raise TTSError("резервный аккаунт не подтвердил тот же voice ID")
    except urllib.error.HTTPError as exc:
        raise TTSError(f"не удалось подтвердить голос {voice_id} на резервном аккаунте (HTTP {exc.code}); проверьте доступ к голосу и права ключа") from None
    except (urllib.error.URLError, TimeoutError, OSError, ValueError):
        raise TTSError("не удалось проверить голос на резервном аккаунте; генерация остановлена") from None


def synthesize_with_failover(text, destination, *, api_key, voice_id, **settings):
    try:
        synthesize(text, destination, api_key=api_key, voice_id=voice_id, **settings)
    except QuotaExceeded:
        backup = get_api_key(backup=True)
        if not backup:
            raise TTSError("основному аккаунту не хватает кредитов; резервный ключ не найден или недоступен") from None
        verify_backup_voice(backup, voice_id)
        print("Основному аккаунту не хватает кредитов; используется резервный.", file=sys.stderr)
        try:
            synthesize(text, destination, api_key=backup, voice_id=voice_id, **settings)
        except QuotaExceeded:
            raise TTSError("кредитов не хватает ни на основном, ни на резервном аккаунте") from None


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
        key = get_api_key()
        if not key:
            raise TTSError("не найден ключ ELEVENLABS_API_KEY или запись macOS Keychain yt-stories-elevenlabs")
        verify_backup_voice(key, args.voice_id)
        for language, content, destination in jobs:
            receipt = destination.with_suffix(".request.json")
            record = {"channel": args.channel, "voice_id": args.voice_id, "model": args.model,
                      "format": OUTPUT_FORMAT, "stability": args.stability, "similarity": args.similarity,
                      "speed": args.speed, "text_sha256": hashlib.sha256(content.encode("utf-8")).hexdigest(),
                      "status": "request_started"}
            save_new(receipt, (json.dumps(record, ensure_ascii=False, indent=2) + "\n").encode())
            synthesize_with_failover(content, destination, api_key=key, voice_id=args.voice_id, model=args.model,
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
