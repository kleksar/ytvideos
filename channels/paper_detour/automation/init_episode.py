#!/usr/bin/env python3
"""Create a Paper Detour workspace; preview by default, never migrate episodes."""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import re
import shlex
import sys

STORAGE_SCRIPTS = Path(__file__).resolve().parents[3] / '.agents/skills/ytv-media-lifecycle/scripts'
sys.path.insert(0, str(STORAGE_SCRIPTS))
import workspace as storage


PROJECT_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_VIDEOS_DIR = PROJECT_ROOT / "channels/paper_detour/videos"
DIRECTORIES = (
    "Research",
    "Storyboard",
    "Source/Script",
    "Source/Images",
    "Source/Audio",
    "Source/Voice",
    "Source/Graphics",
    "Edit",
    "Deliverables",
    "Packaging/Thumbnails/Concepts",
    "Packaging/Thumbnails/Upload",
    "Packaging/Metadata",
    "Packaging/Posts",
    "Shorts",
) + storage.LAYOUT


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Preview or create a fresh episode; never migrates existing assets."
    )
    parser.add_argument("episode_id", help="Three-digit episode ID, e.g. 002")
    parser.add_argument("slug", help="Lowercase ASCII slug, e.g. lake_nyos")
    parser.add_argument(
        "--videos-dir", type=Path, default=DEFAULT_VIDEOS_DIR,
        help="Existing directory that will contain the episode (default: channels/paper_detour/videos)",
    )
    parser.add_argument("--create", action="store_true", help="Create files; otherwise only preview")
    args = parser.parse_args()
    if not re.fullmatch(r"[0-9]{3}", args.episode_id) or args.episode_id == "000":
        parser.error("episode_id must be three digits between 001 and 999")
    if not re.fullmatch(r"[a-z0-9]+(?:_[a-z0-9]+)*", args.slug):
        parser.error("slug must use lowercase ASCII letters/digits separated by single underscores")
    return args


def files_for(episode_id: str, slug: str) -> dict[str, str]:
    return {
        "README.md": f"""# Paper Detour {episode_id}: {slug.replace('_', ' ')}

Статус: UNREGISTERED — новая рабочая заготовка. Текущие входы, версии,
разрешения и следующий результат хранить в [CURRENT_CONTEXT.md](CURRENT_CONTEXT.md).
Перед предметной работой пройти [AGENTS.md](AGENTS.md) и зарегистрировать выпуск
по [bootstrap]({PROJECT_ROOT}/.agent/CHANNEL_BOOTSTRAP.md).

- `Research/` — источники, факты, ограничения и конкуренты.
- `Source/Script/` и `Storyboard/` — сценарий и постановка, с точными версиями.
- `Source/Images/` — одна законченная статичная бумажная диорама на кадр;
  смена композиций прямыми склейками по правилам канала.
- `Source/` — постоянные оригиналы этого монтажа.
- `Assets/Generated/` — постоянные производные для импорта, включая подготовленные cue PNG.
- `Work/<run>/scratch` — воспроизводимые временные файлы; `previews` — варианты для проверки.
  Запуск, состояния и назначение файлов вести через [media lifecycle]({PROJECT_ROOT}/.agents/skills/ytv-media-lifecycle/SKILL.md).
- `Edit/` — журналы и манифесты; пакет `.palmier` управляется приложением.
- `Deliverables/` — локальный путь выдачи нового выпуска по умолчанию;
  иной принятый путь записать в CURRENT_CONTEXT, не переносить импортированные файлы.
- `Packaging/` — обложки, метаданные и черновики постов отдельно от исходников монтажа.
- `Shorts/` — связанные короткие видео, если они нужны.

Этот шаблон создаёт только локальную структуру. Материалы, проект Palmier,
генерация звука, экспорт и внешние действия им не поручаются.
""",
        "CURRENT_CONTEXT.md": f"""# Paper Detour {episode_id} — текущий контекст

- Регистрация: UNREGISTERED; добавить выпуск в реестр по bootstrap.
- Канал: Paper Detour; сверить поручение до начала предметной работы.
- Исходный запрос / запрошенный конечный результат: ещё не записаны.
- Язык продукта: EN по умолчанию; явное поручение другого языка имеет приоритет.
- Язык обсуждения / исходного текста: установить по запросу отдельно от языка продукта.
- Тема / принятое сюжетное обещание: UNVERIFIED.
- Текст: нет зафиксированной версии или пользовательского принятия.
- Постановка / картинки / cue sheet: нет зафиксированных версий.
- Речь / скорость / alignment: UNVERIFIED; шаблон не создаёт звук.
- Разрешения: UNKNOWN; проверить исходное поручение и сохранить его scope.
  Без действующего прямого разрешения новый звук не создавать; публикация не поручена шаблоном.
- Palmier projectId / timelineId / writer / snapshot: UNVERIFIED; проект не создан.
- Выдача: `Deliverables/` этого выпуска по умолчанию; иной принятый путь записать здесь.
- Хранение: `Assets/Generated/` для производных монтажа, `Work/<run>/` для scratch/previews;
  [layout](Edit/MediaLifecycle/layout.json). Актуальный комплект фиксировать через `promote` в `Deliverables/current.json` после QA.
- Проверки: UNVERIFIED; наличие заготовки не означает QA.
- Следующий результат: регистрация, затем первый незакрытый результат исходного запроса
  по [ytv-video-production]({PROJECT_ROOT}/.agents/skills/ytv-video-production/SKILL.md).

Здесь хранится текущая сводка со ссылками на точные версии и основания решений;
исторические квитанции сохраняются в соответствующих материалах выпуска.
""",
        "AGENTS.md": f"""# Точка входа Paper Detour

Сначала прочитать [корневой AGENTS.md]({PROJECT_ROOT}/AGENTS.md),
[обязательный bootstrap]({PROJECT_ROOT}/.agent/CHANNEL_BOOTSTRAP.md),
[реестр]({PROJECT_ROOT}/.agent/episode-registry.md),
[правила Paper Detour]({PROJECT_ROOT}/channels/paper_detour/AGENTS.md) и
[каталог skills]({PROJECT_ROOT}/.agent/skill-catalog.md).

До регистрации статус UNREGISTERED: этот шаблон не заменяет запись в реестре.
Прочитать [CURRENT_CONTEXT.md](CURRENT_CONTEXT.md); затем только нужные действию
источники состояния. Входной workflow —
[ytv-video-production]({PROJECT_ROOT}/.agents/skills/ytv-video-production/SKILL.md).
`.agents/skills` при наличии ссылается на единый канонический набор проекта.
Этот router не даёт разрешений на генерацию звука, монтаж или публикацию.
""",
        "Packaging/Thumbnails/GENERATION_LOG.md": f"""# {episode_id} — журнал генерации обложек

Каждая запись: дата, концепция, назначение, точный запрос, инструмент и модель
(если известна), входные референсы и их роль, исходник, производные файлы,
статус, проверки, ограничения и необходимые SHA-256. Фиксировать подтверждение
пользователя и результаты теста только после фактического получения.
""",
        "Packaging/Metadata/README.md": """# Метаданные и упаковка

Хранить пары заголовков и обложек, описания, главы и гипотезы испытания. Сверять
их с фактическим сценарием и окончательным монтажом. Черновики, редакционный
выбор, пользовательское утверждение и результаты A/B — разные статусы.
""",
    }


def print_registration(target: Path) -> None:
    """Describe the explicit remaining registration step without changing a registry."""
    try:
        episode_path = str(target.relative_to(PROJECT_ROOT))
    except ValueError:
        episode_path = str(target)
    print(f"UNREGISTERED: {episode_path}")
    print(f"Read: {PROJECT_ROOT / '.agent/CHANNEL_BOOTSTRAP.md'}")
    print("Add the Paper Detour path/canonical_path and CURRENT_CONTEXT.md pointers to:")
    print(f"  {PROJECT_ROOT / '.agent/episode-registry.json'}")
    print(f"  {PROJECT_ROOT / '.agent/episode-registry.md'}")
    print("Then install/check entrypoints from the project root:")
    print(f"  cd {shlex.quote(str(PROJECT_ROOT))}")
    print("  python3.11 .agent/scripts/install-entrypoints.py")


def main() -> int:
    args = parse_args()
    videos = args.videos_dir.expanduser().resolve()
    if not videos.is_dir():
        print(f"Error: videos directory does not exist: {videos}", file=sys.stderr)
        return 2
    # Check IDs across slugs, so a second episode cannot quietly reuse an ID.
    existing = sorted(p.name for p in videos.iterdir() if p.name.startswith(args.episode_id + "_"))
    if existing:
        print(f"Error: episode ID already exists: {', '.join(existing)}", file=sys.stderr)
        return 2
    target = videos / f"{args.episode_id}_{args.slug}"
    print(f"{'Create' if args.create else 'Preview'}: {target}")
    for path in DIRECTORIES:
        print(f"  {path}/")
    files = files_for(args.episode_id, args.slug)
    for path in files:
        print(f"  {path}")
    canonical_skills = PROJECT_ROOT / ".agents/skills"
    if canonical_skills.is_dir():
        print(f"  .agents/skills -> {canonical_skills}")
    else:
        print("Canonical skills directory unavailable; use the root bootstrap before work.")
    print_registration(target)
    if not args.create:
        print("Preview only; pass --create to write files.")
        return 0
    try:
        target.mkdir()  # exclusive: never merge with or overwrite an episode
        for path in DIRECTORIES:
            (target / path).mkdir(parents=True, exist_ok=True)
        for path, content in files.items():
            with (target / path).open("x", encoding="utf-8") as out:
                out.write(content)
        storage.initialize(target)
        if canonical_skills.is_dir():
            entrypoint = target / ".agents/skills"
            entrypoint.parent.mkdir()
            entrypoint.symlink_to(
                os.path.relpath(canonical_skills, entrypoint.parent), target_is_directory=True
            )
    except OSError as error:
        # Leave any partial new workspace in place for inspection rather than deleting data.
        print(f"Error creating workspace: {error}; inspect {target} before retrying", file=sys.stderr)
        return 1
    print("Created. No Palmier, video, export, or existing episode was modified.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
