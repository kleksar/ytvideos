#!/usr/bin/env python3
"""Prepare a silent master and an iPhone cue sheet from a Shorts release receipt."""

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
from tempfile import TemporaryDirectory


ROOT = Path(__file__).resolve().parents[1]
VISIBILITY = {
    "private": "Ограниченный доступ",
    "unlisted": "Доступ по ссылке",
    "public": "Открытый доступ",
}


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def video_streamhash(path):
    return subprocess.check_output([
        "ffmpeg", "-v", "error", "-nostdin", "-i", str(path),
        "-map", "0:v:0", "-c:v", "copy", "-f", "streamhash", "-",
    ], text=True).strip()


def validate_master(path, review_hash, expected_sha):
    streams = json.loads(subprocess.check_output([
        "ffprobe", "-v", "error", "-show_entries", "stream=codec_type,width,height",
        "-of", "json", str(path),
    ]))["streams"]
    if (len(streams) != 1 or streams[0]["codec_type"] != "video"
            or streams[0]["width"] >= streams[0]["height"]):
        raise ValueError("Мастер должен содержать только вертикальное видео.")
    if video_streamhash(path) != review_hash:
        raise ValueError("Видеопоток мастера отличается от согласованного MP4.")
    if expected_sha and sha256(path) != expected_sha:
        raise ValueError("SHA-256 мастера отличается от квитанции выпуска.")


def prepare_master(review, master, expected_sha):
    review_hash = video_streamhash(review)
    if master.exists():
        validate_master(master, review_hash, expected_sha)
        return

    master.parent.mkdir(parents=True, exist_ok=True)
    with TemporaryDirectory(prefix=".shorts-handoff-", dir=master.parent) as folder:
        candidate = Path(folder) / master.name
        subprocess.run([
            "ffmpeg", "-v", "error", "-nostdin", "-i", str(review),
            "-map", "0:v:0", "-c:v", "copy", "-map_metadata", "-1",
            "-map_chapters", "-1", "-movflags", "+faststart", str(candidate),
        ], check=True)
        validate_master(candidate, review_hash, expected_sha)
        try:
            os.link(candidate, master)
        except FileExistsError:
            validate_master(master, review_hash, expected_sha)


def cue_sheet(release, master):
    sound = release["native_sound"]
    url = sound["url"]
    if not re.fullmatch(r"https://www\.youtube\.com/source/[\w-]{11}/shorts", url):
        raise ValueError("Укажите точный URL карточки звука YouTube Shorts.")
    start = sound.get("full_track_start_seconds")
    if start is None or not 0 <= start < float("inf"):
        raise ValueError("Укажите проверенное начало отрывка в полной записи.")
    minutes, seconds = divmod(round(start * 100), 6000)
    timecode = f"{minutes}:{seconds // 100:02d},{seconds % 100:02d}"
    cuts = " · ".join(f"{cut:.2f}".replace(".", ",") for cut in sound["cut_seconds"])
    channel = release["channel"]
    visibility = VISIBILITY[release["requested_final_visibility"]]
    return (
        f"# {sound['title']} — {sound['artist']}\n\n"
        f"Канал **{channel['title']}** ({channel['handle']})\n\n"
        f"Мастер **{master.name}**\n\n"
        f"1. В приложении YouTube открой [карточку звука]({url}), "
        "нажми «Использовать этот звук» и импортируй мастер из «Фото».\n"
        f"2. Начни отрывок около **{timecode}** полной записи. "
        f"Сверь удары со склейками в ролике ({cuts} с).\n"
        f"3. Выбери **«{visibility}»** и загрузи Short по поручению. "
        "В плеере проверь, что карточка открывает тот же звук.\n"
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("release", type=Path, help="Путь к RELEASE.json")
    args = parser.parse_args()
    try:
        release = json.loads(args.release.read_text(encoding="utf-8"))
        review = (ROOT / release["accepted_review"]["path"]).resolve()
        master = (ROOT / release["upload_master"]["path"]).resolve()
        if review == master or master.suffix.lower() != ".mp4":
            raise ValueError("Укажите отдельный путь к мастеру MP4.")
        sheet = cue_sheet(release, master)
        if sha256(review) != release["accepted_review"]["sha256"]:
            raise ValueError("SHA-256 согласованного MP4 отличается от квитанции выпуска.")
        prepare_master(review, master, release["upload_master"].get("sha256"))
        sheet_path = master.with_name(f"{master.stem}-iPhone.md")
        sheet_path.write_text(sheet, encoding="utf-8")
    except (OSError, KeyError, ValueError, TypeError, subprocess.CalledProcessError) as error:
        parser.exit(1, f"{error}\n")
    print(master)
    print(sheet_path)


if __name__ == "__main__":
    main()
