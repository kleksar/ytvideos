# Сравнение аудиоэкспорта: Everyone, Paper и Nuviko

Срез исследования 2026-11-16, база `dbd23b4e`. Это evidence для диагностики жалобы на искажения Everyone, не новый канальный пресет и не слуховой PASS. Разделять требование, команду/receipt и измерение доступного файла.

## Требование и реализация

[Audio standard](../standards/audio.md#полный-микс): совместимый принятый AAC копировать; при новом кодировании AAC-LC mono 192 kbit/s, stereo не ниже 256 kbit/s. Частоту и каналы сохранять, если профиль не требует иного. Ни обязательного stereo/48 kHz для mono-речи, ни гарантии качества по bitrate нет.

[Shared renderer](../../automation/ffmpeg_montage/montage.py), функция `final_command`, принимает готовый полный mix: AAC → stream copy; другой codec → AAC 192k mono / 256k stereo. В этой функции нет audio loudnorm, компрессии или лимитера. [Delivery guard](../../automation/ffmpeg_montage/delivery.py) проверяет mapping, codec/profile, rate/channels и target bitrate; это не проверка тембра или слышимости.

| Пример | Что подтверждено сохранённой командой/контрактом | Граница evidence |
|---|---|---|
| Paper Neptune | PCM24, stereo 48 kHz → AAC-LC 256k; dry voice `atempo=1.10` один раз, center −2 dB; музыка −22 dB, fades, `amix normalize=0` | [Контракт](../../channels/paper_detour/research/2026-11-09-neptune/Edit/export-contract-v01.json), [handoff](../../channels/paper_detour/research/2026-11-09-neptune/Assets/Audio/HANDOFF.md). Это конкретный выпуск, не универсальные gains. В handoff listening UNVERIFIED |
| Nuviko History Harrison v03 | PCM mono 48 kHz → AAC-LC 192k | [Контракт](../../channels/nuviko_history/research/harrison-export-contract-v03.json). Сам контракт не заменяет probe master |
| Nuviko Stories 014 | исходная речь MP3 → `atempo=1.1`, 44.1 kHz mono AAC-LC 192k, видеопоток copy | [Фактическая команда](../../channels/nuviko_stories/videos/014_подарок_парню_и_незнакомец_с_книгами_толкина/Edit/014_en_audio_rebuild_command.json). Один speech input; не доказательство многослойного sound design |

Проверка доступных Mac-исходников отдельным media worker: Paper Atlantic Cable raw MP3 44.1 kHz mono/128k → conformed PCM24 48 kHz mono → full mix PCM24 48 kHz stereo (284.567 s); Neptune full mix PCM24 48 kHz stereo (32.3667 s); Harrison mix PCM24 48 kHz mono (47.31 s); Nuviko Great Escape raw MP3 44.1 kHz mono/128k, draft mix v1 PCM24 mono 44.1 kHz, v2 stereo 44.1 kHz. В проверенных четырёх channel roots MP4 не найден: свежий probe финальных экспортов этих каналов отсутствует. Не подменять его контрактами из таблицы.

## Everyone v9: измеренные файлы

Проверены cloud-файлы через `ffprobe -select_streams a:0 -show_entries stream=codec_name,profile,sample_rate,channels,channel_layout,bit_rate`:

| Файл | Codec | Rate / channels | Измеренный bitrate |
|---|---|---|---|
| `EVERYONE_WANTS_YOU_SOUND_V9_1080p30.mp4` | AAC-LC | 48 kHz stereo | 264535 bit/s |
| `EVERYONE_WANTS_YOU_SOUND_V9_PREVIEW.mp4` | AAC-LC | 48 kHz stereo | 134527 bit/s |

Master SHA-256: `56fd8a9c475e4077234179d52b389b908497d2d2b7fcb95ad7db9dab1bf9f88c`. Измеренный bitrate отличается от encoder target; это не отдельный дефект. Preview имеет другую аудиокодировку и не доказывает качество master. Разница может влиять на оценку, но **не установлена причиной жалобы**.

Архив `EVERYONE_REFERENCE_SOURCE_V9.zip`: 110879350 bytes, SHA-256 `93738a1dc21952c39173e33256d191476b4cf851724a2d0c6183b63f8dbf4317`; проверенная worker полная пересборка WAV `5e105cfbd0c734edcaa1da00f111d889d25e28c21355bf265c7396162d07f28c`. Это воспроизводимость, не субъективная приёмка v9.

В сохранённой цепочке `desire-sound-v2/mix.py` голос декодируется из исходного approved MP4; music/SFX складываются в float, сохраняются PCM24, общий gain статический. Последующие patches используют WAV, не предыдущий AAC master. Поэтому многочисленные номера версий сами по себе не доказывают каскад lossy-перекодирования всего микса. Но исходный voice уже прошёл lossy-экспорт: увеличение выходного bitrate его не восстановит.

В `desire-sound-v5/patch.py` отдельный SFX с `compression_drive` проходит `tanh`; это локальная нелинейная обработка, не лимитер всего голоса. В v6 crowd используется 75 ms grain shuffle и bandpass 130–750 Hz; в раннем foley есть синтезированные эффекты. Такие обработки/исходники — кандидаты для проверки конкретной жалобы, а не доказанные причины без таймкода и сравнения. Отсутствие clipping и хорошие LUFS не исключают нежелательный тембр, маскировку или артефакты исходника.

Дополнительная диагностика sound worker обнаружила upstream `render_video.py`: до freeze AAC применяется однопроходный `loudnorm I=-16:TP=-1.5:LRA=11`. Raw narration — PCM16 48 kHz, два идентичных канала; peak −4.47 dBFS, у approved freeze −1.01 dBFS. Оценка gain по пятисекундным окнам 1.95–2.76; после одного global gain raw→approved residual SNR 14.9 dB и correlation 0.984 отражают совокупное изменение, а не отдельно вклад loudnorm или AAC. Это подтверждённая upstream обработка, но не доказательство причины жалобы. У v9 PCM и decoded master clipping samples = 0, peak master −1.028 dBFS, stereo correlation 0.9887. Новый diagnostic preview должен копировать audio stream master; raw-voice/static-gain кандидат требует отдельного A/B, не считается автоматически исправленным.

## Вывод для исправления

Не менять все каналы на один формат и не обещать лечение заменой AAC на другой codec. Сначала сравнить точные source/stem, lossless mix, decoded master и фактически просмотренный preview на одном участке и сопоставимой громкости. Сохранить hashes и точную цепочку; отделить проблему исходника, обработки, баланса, кодирования и воспроизведения. Менять только подтверждённую область. Технический результат и listening QA записывать отдельно; при отсутствии прослушивания последний остаётся UNVERIFIED.
