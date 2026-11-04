# Общая автоматизация ytvideos

Общие сервисы используют профили конкретных каналов и не назначают канал по номеру выпуска. Перед работой читать [root AGENTS](../AGENTS.md), [bootstrap](../.agent/CHANNEL_BOOTSTRAP.md) и применимый skill из [каталога](../.agent/skill-catalog.md).

- [ElevenLabs](elevenlabs/README.md) — TTS по канальному реестру; перед платным запросом действуют полномочия audio owner.
- [YouTube](youtube/README.md) — OAuth, чтение состояния и порученные изменения через release/upload.
- [FFmpeg montage](ffmpeg_montage/README.md) — текущая сборка Paper Detour и Nuviko History.
- [Пословные тайминги](captions/README.md) и [субтитры](subtitles/README.md) — подготовка текста и alignment с канальным оформлением.
- [Palmier](palmier/README.md) — сохранённые инструменты старых проектов; текущий Paper/Nuviko production использует FFmpeg.

Исторический журнал личных Stories, `pipeline.py`, `voice_run.py`, `runs/` и [RUNBOOK](../channels/nuviko_stories/automation/RUNBOOK.md) находятся в `channels/nuviko_stories/automation/`. Запускать их из корня проекта полным каноническим путём. Общий CLI TTS — `python3 automation/elevenlabs/tts.py --help`; справка сама не выполняет синтез. Журнал фиксирует фактический результат, но не доказывает качество медиа или текущее состояние внешнего сервиса.

Схема каталогов — [CHANNEL_LAYOUT](../.agent/CHANNEL_LAYOUT.md).
