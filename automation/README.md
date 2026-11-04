# Общая автоматизация ytvideos

Общие сервисы используют профили конкретных каналов и не назначают канал по номеру выпуска. Перед работой читать [root AGENTS](../AGENTS.md), [bootstrap](../.agent/CHANNEL_BOOTSTRAP.md) и применимый skill из [каталога](../.agent/skill-catalog.md).

- [ElevenLabs](elevenlabs/README.md) — TTS по канальному реестру; перед платным запросом действуют полномочия audio owner.
- [YouTube](youtube/README.md) — OAuth, чтение состояния и порученные изменения через release/upload.
- [FFmpeg montage](ffmpeg_montage/README.md) — сборка по проверяемому плану и профилю доставки.
- [Пословные тайминги](captions/README.md) и [субтитры](subtitles/README.md) — подготовка текста и alignment с канальным оформлением.
- [Image motion](image_motion/pyproject.toml) — переносимая сборка движения сцен на зафиксированных Python-зависимостях.

Сборка видео для всех текущих каналов выполняется через FFmpeg по плану и профилю доставки. Старые episode bundles могут содержать исходные материалы и фактические квитанции прошлых выпусков; они не являются текущим процессом и не должны восстанавливаться как инструкция. Общий CLI TTS: `python3 automation/elevenlabs/tts.py --help`; справка сама не выполняет синтез.

Схема каталогов — [CHANNEL_LAYOUT](../.agent/CHANNEL_LAYOUT.md).
