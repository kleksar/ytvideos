#!/usr/bin/env python3
"""Generate recorded story voices with a durable, conservative request boundary."""
import argparse
import importlib.util
import json
from pathlib import Path
import sys
from types import SimpleNamespace

import pipeline

_SPEC = importlib.util.spec_from_file_location("stories_tts", Path(__file__).resolve().parents[3] / "automation" / "elevenlabs" / "tts.py")
tts = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(tts)


def checked_artifact(record, label):
    if not isinstance(record, dict) or not all(k in record for k in ("path", "bytes", "sha256")):
        raise ValueError(f"нет подтверждённого файла {label}")
    actual = pipeline.artifact(record["path"])
    # The recorded path may be a compatibility link after a directory rename.
    # Content identity still needs to match before any paid request is made.
    if any(actual[key] != record[key] for key in ("bytes", "sha256")):
        raise ValueError(f"файл {label} изменён после регистрации: {record['path']}")
    return Path(actual["path"])


def plan(root, data, languages, voice_id):
    jobs = []
    for language in languages:
        stages = data["languages"][language]
        if stages["story"]["status"] != "completed":
            raise ValueError(f"{language}: сначала завершите этап story")
        source = checked_artifact(stages["story"].get("artifact"), f"story {language}")
        voice = stages["voice"]
        if voice["status"] == "completed":
            if voice.get("request", {}).get("voice_id") != voice_id:
                raise ValueError(f"{language}: голос существующей записи неизвестен или не совпадает с каналом; проверьте происхождение вручную")
            checked_artifact(voice.get("artifact"), f"voice {language}")
            if "alignment" in voice:
                checked_artifact(voice["alignment"], f"alignment {language}")
            print(f"{language}: уже завершено, запрос пропущен")
            continue
        if voice["status"] != "pending" or voice["attempts"] != 0:
            raise ValueError(f"{language}: этап voice уже запускался; проверьте файлы и историю ElevenLabs, затем разрешите состояние вручную")
        args = SimpleNamespace(voice_id=voice_id, model=tts.MODEL_ID,
                               ru_text=source if language == "ru" else None,
                               en_text=source if language == "en" else None,
                               output_dir=pipeline.episode_directory(root, data["episode"]) / "Source" / "Voice")
        jobs.extend(tts.prepare(args))
    return jobs


def run(root, episode, languages, generate=False, *, channel):
    voice_id = tts.channel_voice(channel)
    # The lock spans requests: another local worker cannot start the same paid job.
    with pipeline.locked(root) as directory:
        path, data = pipeline.read_run(directory, episode)
        jobs = plan(root, data, languages, voice_id)
        for language, content, destination in jobs:
            print(f"{language}: {len(content)} символов → {destination}")
        if not generate:
            print("Проверка без сети и без расхода кредитов. Для запроса укажите --generate.")
            return
        if not jobs:
            return
        key = tts.get_api_key()
        if not key:
            raise ValueError("не найден ключ ElevenLabs в окружении или macOS Keychain")
        tts.verify_backup_voice(key, voice_id)
        for language, content, destination in jobs:
            pipeline.transition(data, language, "voice", "start")
            state = data["languages"][language]["voice"]
            state["request"] = {"story_sha256": data["languages"][language]["story"]["artifact"]["sha256"],
                                "destination": str(destination), "channel": channel, "voice_id": voice_id,
                                "model": tts.MODEL_ID, "format": tts.OUTPUT_FORMAT,
                                "stability": 1.0, "similarity": 0.0}
            # Persist intent before the call; an interrupted run is never retried automatically.
            pipeline.save(path, data)
            tts.synthesize_with_failover(content, destination, api_key=key, voice_id=voice_id,
                           model=tts.MODEL_ID, stability=1.0, similarity=0.0)
            alignment = destination.with_suffix(".alignment.json")
            with alignment.open(encoding="utf-8") as handle:
                alignment_data = json.load(handle)
            if not isinstance(alignment_data, dict):
                raise ValueError(f"{language}: не удалось подтвердить файл таймингов")
            pipeline.transition(data, language, "voice", "complete", path=str(destination))
            state["alignment"] = pipeline.artifact(alignment)
            pipeline.save(path, data)
            print(f"{language}: голос и файл таймингов сохранены; качество не проверено")


def main(argv=None, root=pipeline.ROOT):
    parser = argparse.ArgumentParser(description="Озвучка подтверждённых текстов с записью в журнал")
    parser.add_argument("episode")
    parser.add_argument("--channel", required=True, choices=("paper_detour", "nuviko_history"))
    parser.add_argument("--language", choices=pipeline.LANGUAGES, action="append", help="только выбранный язык; по умолчанию оба")
    parser.add_argument("--generate", action="store_true", help="отправить платные запросы")
    args = parser.parse_args(argv)
    try:
        run(root, args.episode, list(dict.fromkeys(args.language or pipeline.LANGUAGES)), args.generate, channel=args.channel)
        return 0
    except (ValueError, OSError, json.JSONDecodeError, tts.TTSError) as exc:
        print(f"Ошибка: {exc}", file=sys.stderr)
        print("Если запрос уже начался, не повторяйте его до проверки журнала и истории ElevenLabs.", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
