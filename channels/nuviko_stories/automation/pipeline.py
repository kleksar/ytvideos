#!/usr/bin/env python3
"""Local, explicit state tracking for story production; no remote actions."""

import argparse
import contextlib
import datetime
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import sys
import tempfile
import unicodedata
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parent.parent
STAGES = ("story", "voice", "edit", "render", "review", "upload")
LANGUAGES = ("ru", "en")
FILE_STAGES = {"story", "voice", "render"}
SCHEMA_VERSION = 1


def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")


@contextlib.contextmanager
def locked(root):
    directory = root / "automation" / "runs"
    directory.mkdir(parents=True, exist_ok=True)
    with (directory / ".lock").open("a+") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        try:
            yield directory
        finally:
            fcntl.flock(lock, fcntl.LOCK_UN)


def save(path, data):
    # Write a complete JSON file then atomically replace the previous version.
    tmp_path = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=path.parent,
                                         prefix=".state-", delete=False) as handle:
            tmp_path = Path(handle.name)
            json.dump(data, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(str(tmp_path), str(path))
    finally:
        if tmp_path is not None and tmp_path.exists():
            tmp_path.unlink()


def read_run(directory, episode):
    if not re.fullmatch(r"[0-9]{3,}", episode) or int(episode) < 1:
        raise ValueError("ID выпуска должен быть положительным числом минимум из трёх цифр")
    path = directory / (episode + ".json")
    if not path.is_file():
        raise ValueError("Выпуск {} не найден".format(episode))
    with path.open(encoding="utf-8") as handle:
        data = json.load(handle)
    if data.get("schema_version") != SCHEMA_VERSION or data.get("episode") != episode:
        raise ValueError("Неизвестная версия или несовпадение ID файла состояния")
    return path, data


def directory_id(name):
    """Read an ID from either a historical name or the current ID_slug form."""
    match = re.fullmatch(r"([0-9]+)(?:_.*)?", name)
    return int(match.group(1)) if match and int(match.group(1)) > 0 else None


def topic_slug(topic):
    """Build a safe, readable directory suffix, retaining Unicode letters."""
    name = unicodedata.normalize("NFKC", topic).lower()
    pieces = []
    separator = False
    for character in name:
        if character.isalnum():
            if separator and pieces:
                pieces.append("_")
            pieces.append(character)
            separator = False
        else:
            separator = True
    return "".join(pieces)[:60].rstrip("_") or "untitled"


def episode_directory(root, episode):
    """Resolve one episode, accepting legacy aliases only when they agree."""
    if not re.fullmatch(r"[0-9]{3,}", episode) or int(episode) < 1:
        raise ValueError("ID выпуска должен быть положительным числом минимум из трёх цифр")
    videos = root / "videos"
    matches = [p for p in videos.iterdir() if directory_id(p.name) == int(episode)] if videos.exists() else []
    if not matches:
        raise ValueError(f"Каталог выпуска {episode} не найден")
    if any(not p.is_dir() for p in matches):
        raise ValueError(f"Каталог или ссылка выпуска {episode} недоступны")
    targets = {p.resolve() for p in matches}
    if len(targets) != 1:
        raise ValueError(f"Найдено несколько разных каталогов выпуска {episode}")
    # Return the actual location rather than a historical compatibility alias.
    return targets.pop()


def create(root, directory, topic):
    # Count both current names and old aliases; even a dangling link reserves its ID.
    used = set()
    videos = root / "videos"
    if videos.exists():
        used.update(value for p in videos.iterdir() if (value := directory_id(p.name)) is not None)
    used.update(int(p.stem) for p in directory.glob("*.json") if p.stem.isdigit())
    episode = "{:03d}".format(max(used, default=0) + 1)
    stamp = now()
    data = {"schema_version": SCHEMA_VERSION, "episode": episode, "topic": topic,
            "created_at": stamp, "updated_at": stamp,
            "languages": {lang: {stage: {"status": "pending", "attempts": 0}
                                  for stage in STAGES} for lang in LANGUAGES},
            "events": [{"time": stamp, "action": "created"}]}
    # Reserve a directory, but never touch an existing one or any Palmier package.
    target = videos / (episode + "_" + topic_slug(topic))
    data["directory"] = target.name
    target.mkdir(parents=True, exist_ok=False)
    for part in ("Source/Archive", "Source/Storyboard", "Source/Voice", "Edit/Captions", "Deliverables"):
        (target / part).mkdir(parents=True)
    save(directory / (episode + ".json"), data)
    return data


def artifact(path):
    source = Path(path).expanduser().resolve(strict=True)
    if not source.is_file():
        raise ValueError("Артефакт должен быть обычным файлом")
    digest = hashlib.sha256()
    with source.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return {"path": str(source), "bytes": source.stat().st_size, "sha256": digest.hexdigest()}


def transition(data, language, stage, action, note=None, path=None, url=None):
    stages = data["languages"][language]
    state = stages[stage]
    status = state["status"]
    if action == "start":
        if status not in ("pending", "failed"):
            raise ValueError("Начать можно только ожидающий или неудавшийся этап")
        index = STAGES.index(stage)
        if index and stages[STAGES[index - 1]]["status"] != "completed":
            raise ValueError("Сначала завершите этап {}".format(STAGES[index - 1]))
        state["status"] = "in_progress"
        state["attempts"] += 1
    elif action == "fail":
        if status != "in_progress" or not note:
            raise ValueError("Для ошибки нужен запущенный этап и описание --note")
        state["status"] = "failed"
        state["last_error"] = note
    else:
        if status != "in_progress":
            raise ValueError("Сначала запустите этап командой start")
        if stage in FILE_STAGES:
            if not path:
                raise ValueError("Для этого этапа укажите готовый файл через --file")
            state["artifact"] = artifact(path)
        elif stage == "upload":
            parsed = urlparse(url or "")
            if parsed.scheme != "https" or parsed.hostname not in ("youtube.com", "www.youtube.com", "youtu.be", "studio.youtube.com"):
                raise ValueError("Укажите HTTPS-ссылку на YouTube через --url")
            if not note:
                raise ValueError("Укажите подтверждённую приватность и канал через --note")
            state["url"] = url
        elif not note:
            raise ValueError("Опишите выполненную работу/проверку через --note")
        state["status"] = "completed"
        state.pop("last_error", None)
    stamp = now()
    state["updated_at"] = stamp
    event = {"time": stamp, "language": language, "stage": stage, "action": action}
    if note:
        event["note"] = note
    data["events"].append(event)
    data["updated_at"] = stamp


def parser():
    result = argparse.ArgumentParser(description="Состояние производства двух версий истории (без удалённых действий)")
    commands = result.add_subparsers(dest="command", required=True)
    init = commands.add_parser("init", help="Создать следующий выпуск")
    init.add_argument("--topic", default="", help="Тема, если уже известна")
    status = commands.add_parser("status", help="Показать состояние")
    status.add_argument("episode")
    for command in ("start", "complete", "fail"):
        action = commands.add_parser(command, help="Отметить состояние этапа")
        action.add_argument("episode")
        action.add_argument("language", choices=LANGUAGES)
        action.add_argument("stage", choices=STAGES)
        action.add_argument("--note")
        if command == "complete":
            action.add_argument("--file", dest="path")
            action.add_argument("--url")
    return result


def main(argv=None, root=ROOT):
    args = parser().parse_args(argv)
    try:
        with locked(root) as directory:
            if args.command == "init":
                data = create(root, directory, args.topic)
            else:
                path, data = read_run(directory, args.episode)
                if args.command != "status":
                    transition(data, args.language, args.stage, args.command, args.note,
                               getattr(args, "path", None), getattr(args, "url", None))
                    save(path, data)
            print(json.dumps(data, ensure_ascii=False, indent=2))
        return 0
    except (ValueError, OSError, json.JSONDecodeError) as exc:
        print("Ошибка: {}".format(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
