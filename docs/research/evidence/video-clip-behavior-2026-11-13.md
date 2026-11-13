# Apollo 13 / Nuviko — ограниченная проверка исходных клипов

**Scope:** узкая read-only проверка только четырех указанных MP4. Никаких production/run CLI, внешних платных операций, новых файлов в episode tree, правок policy или публикации не выполнялось.

## Вывод для монтажа

**Результат по каждому клипу: проверка не завершена.** В доступном просмотре не обнаружен конкретный дефект, который оправдывал бы выбраковку. Сохранить все четыре оригинала как кандидаты и проверить в локальной монтажной пробе с утвержденным storyboard, соседними планами, реальными границами и принятым звуком/таймингом. Это не подтверждение пригодности в финальном монтаже.

Причина незавершенности: разрешенный packet содержит только MP4. В нем нет scene intent/storyboard, expected action/angle, выбранных интервалов, соседних shots, исходника/визуальных references и звуковых/тайминговых inputs. Поэтому нельзя проверить соответствие замыслу, используемые границы и монтажное влияние. Я не читал соседние JSON/результаты других проверок и не открывал содержимое `CLIP_REVIEW.md`.

## Файлы и измеренные свойства

FFmpeg `ffprobe` прочитал потоки/контейнер; SHA-256 снят с исходных байтов; полный decode каждого входа командой `ffmpeg -v error -i FILE -f null -` завершился exit 0 без сообщений об ошибках.

| Файл | SHA-256 | Длительность | Видеопоток | Цветовые теги | Аудиопоток | Decode |
|---|---|---:|---|---|---|---|
| `S001.mp4` | `928a963ae6801848863f9c418f225adff4d584827bdaaace61acd12d32ae1654` | 5.034667 s | H.264, 720×1280, 24/1 fps, yuv420p | primaries bt709; transfer iec61966-2-1; matrix smpte170m; range tv | AAC, 48 kHz, stereo | PASS |
| `S004.mp4` | `04175e7d1953743d215330b19ba4d12d7c82b13e73b65c6e659011cdce5a829c` | 5.034667 s | H.264, 720×1280, 24/1 fps, yuv420p | primaries bt709; transfer iec61966-2-1; matrix smpte170m; range tv | AAC, 48 kHz, stereo | PASS |
| `S010.mp4` | `4cf8aabd1824f057645d226ea67530f5ca3604f868e6ad131af5f37f1477c339` | 5.034667 s | H.264, 720×1280, 24/1 fps, yuv420p | primaries bt709; transfer iec61966-2-1; matrix smpte170m; range tv | AAC, 48 kHz, stereo | PASS |
| `S012.mp4` | `57b65ac8a9442d30e13b56a340faa66521b8a21b45647121804a92d149f70185` | 5.034667 s | H.264, 720×1280, 24/1 fps, yuv420p | primaries bt709; transfer iec61966-2-1; matrix smpte170m; range tv | AAC, 48 kHz, stereo | PASS |

These are source clips, not final exports. Their 720×1280 / 24 fps properties differ from Nuviko Short export settings 1440×2560 / 30 fps. The three color fields also do not report a uniform Rec.709 triplet. Record and handle these in the actual render/color path; this metadata alone is not evidence of a visible color defect. Audio stream presence/decode does not establish that it is audible, useful, licensed, synchronized, or intended for the edit.

## Visual observation and coverage

Opened the exact paths in QuickTime Player, played each from 00:00 to the 00:05 natural endpoint, then inspected the returned endpoint screenshot. The UI timeline showed playback stopped at 5 seconds for each. The capture gave only a still endpoint after each playback; it did not let me judge movement quality, intermediate frames, internal cuts, flicker, or audio. Therefore those checks remain **UNVERIFIED** despite successful playback and full decode.

- **S001:** endpoint shows the illustrated Nuviko traveler beside a dark rectangular equipment unit and a separate metal ring in a bright indoor workspace. In this still, the traveler is visually distinct from the photographic-looking environment/equipment, consistent with the channel's stated mixed 2D/photorealistic treatment. No visible endpoint defect established.
- **S004:** endpoint shows several men in white clothing inside a confined equipment-filled spacecraft-like interior. No visible endpoint defect established; historical/source accuracy and relation to the intended beat were not checked.
- **S010:** endpoint shows a seated man with a headset at a console; a map/display wall and another person appear behind him. No visible endpoint defect established; historical/source accuracy and relation to the intended beat were not checked.
- **S012:** endpoint shows hands handling a wrapped rectangular equipment unit and a metal hose/connector. No visible endpoint defect established; intended action and continuity were not checked.

For all four: no interval boundaries or adjacent-shot edit were supplied. No local montage proof was made. No listening was performed; there is no PASS for speech/music or AV sync. No claim is made about the whole clip being visually free of artifacts, smooth, temporally coherent, factually accurate, or suitable for the promised scene.

## Next step

Provide or load the exact accepted scene plan (expected action/person/angle and used interval), adjacent plans, and the accepted audio/timing inputs. Then make a local montage proof without altering or replacing the originals; review the first/middle/last used frames, the entire chosen interval in motion, any internal shot changes, both neighboring cuts, and audio where it is intended to be used. Select exact source hashes and intervals only after that contextual review. If a confirmed issue appears, first assess a supported local trim/usable sub-interval and preserve provenance; consider replacement only for a material defect after reuse is assessed. No paid retry is recommended from this evidence.

## Документы и фактический журнал

Источник инструкций: полный `local instruction packet` (`scope=instructions_only`, `channel=nuviko_history`, `stage=review`, `format=short`). SHA-256 каждого встроенного pinned text сверил с указанным packet hash; все совпали. Прочитаны полный текст назначенного skill и полный текст каждого `reference_documents`:

| Документ | Packet SHA-256 |
|---|---|
| `.agents/skills/ytv-review-video/SKILL.md` | `cb52af54ca880d102e059a1a1a4b4b09c84b81cb34f97d77d7995dd3f0c7c07f` |
| `.agents/skills/ytv-start/references/task-execution.md` | `0bd8b658ea0a001c77ba55c692bc9faebf32afa4f606a8f5a24f02b74d32410d` |
| `docs/standards/delivery.md` | `06c493e9f7a53adf6076cd6055c0d893b7d26d61e89b8648aa42d3d107c624c1` |
| `docs/standards/visual.md` | `929ab9d432646638b71e00085ff1661d3c43e9e5bd268ec861de2099c7ee0823` |
| `docs/standards/audio.md` | `1bd2df8b3c71569a545f0bffc98c445757a72d54661d5420e538b0d118daff2a` |
| `.agents/skills/ytv-produce-video/references/video-clips.md` | `922e80bc04992f3c36d8a55cafd2635a2021d814a67ff7eb116dde7006a86c62` |
| `docs/standards/editorial.md` | `c0af5413703d9fcd202d6834b43d2f2c29f7add5391e84cb2b9ccf71623f8bde` |
| `docs/standards/narration.md` | `572f50d35b53272aa58e172f78b3d06f1f23e33c9013f7ade9c13e8ead4d1772` |
| `docs/standards/thumbnails.md` | `94c5ea7cab3454d7b05452854455747d46a5094702363a67414ef668a091e627` |
| `channels/nuviko_history/PROFILE.md` | `1086d164eb9fc2de03ddfabc6557b532c673007b328bd653d8842592178de799` |
| `channels/nuviko_history/brand/VISUAL_PROFILE.md` | `e5ea4bd85af96c175761d751dea802b48a16525b80bc8558a7f05529ba646cac` |

Actions/methods actually used: parsed packet JSON; extracted its embedded pinned texts to `local extracted packet directory` for reading; `shasum -a 256` on four exact MP4s; `ffprobe` for format/stream fields; FFmpeg full decode to null; QuickTime Player direct local-file playback and endpoint screenshot inspection. Checked for media-specific tools in the deferred tool registry; no dedicated playback-inspection tool was found. A browser `file://` tab attempt was rejected by browser URL policy, so no browser workaround was attempted; QuickTime provided native local playback. No software installation or external dispatch.

Limits: no task-specific storyboard/scene requirement or cut/timing context in the packet; no review of other files; no human independent review; endpoint screenshots are not complete visual-motion evidence; no listening; no local montage proof; no changes or paid actions.
