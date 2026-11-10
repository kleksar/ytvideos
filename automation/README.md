# Технические средства

Новые runs запускаются через `src/ytvideos`: task context, claims, guards, outputs и receipts. Этот каталог содержит исполняемые средства, которые adapters используют в разрешённом scope. Прямой запуск helper не является обходом approval, channel, budget или неизвестного outcome.

| Средства | Контракт |
|---|---|
| [elevenlabs](elevenlabs/README.md) | Exact accepted text, verified channel voice, provider outcome |
| [captions](captions/README.md) | Character alignment → исходная word map |
| [ffmpeg_montage](ffmpeg_montage/README.md) | Versioned plan, profiles, subtitle/export contracts, MP4 provenance |
| [subtitles](subtitles/README.md) | Дополнительные прозрачные экранные слои по проверенной карте |
| [youtube](youtube/README.md) | Authorized channel, private resumable upload, captions, metadata/schedule read-back |
| `helpers/` | Перенесённые инструменты QA, grouping, lifecycle, session и validators |

[Общие стандарты](../.agent/documentation-index.md) · [Runtime capabilities](../docs/operations/runtime.md)
