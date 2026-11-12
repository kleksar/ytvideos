# Весь ytvideos: инвентаризация для согласования удаления

Корень `/Users/diplomat/ytvideos`; проверены все доступные каталоги обычных файлов, включая содержимое пакетов проектов Palmier. Символические ссылки не обходились, чтобы не учитывать одно и то же дерево повторно. Ничего не удалено.

Обнаружено 16236 файлов, логический размер 54.19 ГиБ. Полный машинный список каждого файла: `YTVIDEOS_STORAGE_INVENTORY_2026-11-02.csv`. Данные снимка могут устареть при работе других сессий.

Размеры в таблицах — логические суммы размеров файлов, не гарантированное освобождение. APFS-клоны и снимки могут разделять или удерживать блоки. Учтённые пофайловые блоки в CSV тоже не равны гарантированной экономии. Ссылки из найденных `media.json` означают импорт в проект, но не доказывают использование актуальным таймлайном; отсутствие упоминания не доказывает отсутствие зависимости. Внешние проекты и актуальный статус YouTube не проверялись.

Рябь оставлена в отдельной группе R: пользователь сохранил её для эксперимента. Обычные исходники, озвучки, проекты и документацию предлагается сохранять. Никаких удалений до выбора пользователя.

## Категории

| Категория | Файлов | Логический размер |
|---|---:|---:|
| A — выдачи и финальные видео: кандидаты после проверки | 42 | 3.96 ГиБ |
| B — слои MOV и промежуточные мастера: проверить монтаж | 73 | 17.27 ГиБ |
| C — превью и промежуточные видео: проверить назначение | 182 | 3.99 ГиБ |
| D — изображения: сохранять до отдельной проверки | 5851 | 3.39 ГиБ |
| E — аудио: сохранить | 37 | 604.4 МиБ |
| F — документация и прочие файлы: сохранить | 3656 | 128.0 МиБ |
| I — исходники и библиотека: сохранить | 6303 | 12.11 ГиБ |
| P — проект Palmier: сохранять | 65 | 46.3 МиБ |
| R — рябь и связанные материалы: сохранить для эксперимента | 20 | 1.20 ГиБ |
| S — общий эффект: отдельно решить; проверить зависимости | 7 | 11.51 ГиБ |

## Разделы и выпуски по размеру

| Каталог | Файлов | Логический размер |
|---|---:|---:|
| `channels/paper_detour/Shared/Overlays` | 13 | 12.18 ГиБ |
| `channels/paper_detour/videos/028_taj_mahal` | 444 | 6.03 ГиБ |
| `channels/paper_detour/videos/033_time_stop` | 507 | 4.46 ГиБ |
| `channels/paper_detour/videos/001_radio_game` | 1186 | 3.80 ГиБ |
| `channels/nuviko_history/videos/017_galveston_1900` | 779 | 3.29 ГиБ |
| `channels/nuviko_history/videos/009_black_death` | 457 | 2.88 ГиБ |
| `channels/paper_detour/videos/030_clothing_history` | 1054 | 2.39 ГиБ |
| `channels/paper_detour/videos/003_iq_gallery` | 1953 | 1.92 ГиБ |
| `channels/paper_detour/videos/004_last_video` | 1059 | 1.75 ГиБ |
| `channels/nuviko_history/videos/016_marseille_1720` | 379 | 1.63 ГиБ |
| `channels/paper_detour/videos/007_joshua_jessica` | 1173 | 1.61 ГиБ |
| `channels/nuviko_stories/videos/018_соседский_мальчик_назвал_меня_папой` | 230 | 1.59 ГиБ |
| `channels/paper_detour/videos/009_knorozov_asya` | 346 | 1.02 ГиБ |
| `channels/paper_detour/videos/008_boyfriend_brought_friend` | 280 | 1011.2 МиБ |
| `channels/nuviko_stories/videos/012_дорогой_подарок_оказался_семейной_реликвией` | 47 | 980.1 МиБ |
| `channels/paper_detour/videos/027_doomscrolling_short` | 507 | 770.0 МиБ |
| `channels/nuviko_stories/footages` | 6 | 715.7 МиБ |
| `channels/nuviko_stories/videos/011_парень_приводил_друга_на_каждое_свидание` | 43 | 649.4 МиБ |
| `channels/paper_detour/videos/032_galveston_1900` | 439 | 591.8 МиБ |
| `channels/paper_detour/videos/031_jascon4_okene` | 388 | 489.4 МиБ |
| `channels/nuviko_stories/videos/022_свадьба_сестры_в_подарок` | 181 | 479.0 МиБ |
| `channels/nuviko_history/videos/004_pompeii_short` | 58 | 467.1 МиБ |
| `channels/nuviko_stories/videos/019_торт_с_чужим_именем` | 127 | 403.2 МиБ |
| `channels/paper_detour/legacy/020_rarovista_radio_game` | 15 | 359.8 МиБ |
| `channels/paper_detour/legacy/025_iq_gallery` | 68 | 353.2 МиБ |
| `projects/borisenko/pilot_001` | 762 | 290.4 МиБ |
| `channels/paper_detour/videos/002_margorie_mccall` | 192 | 285.7 МиБ |
| `archive/unclassified_episodes/003_gus` | 45 | 257.5 МиБ |
| `channels/nuviko_stories/videos/015_девушка_моего_брата_приревновала_его_ко_мне` | 98 | 205.2 МиБ |
| `channels/paper_detour/legacy/024_margorie_mccall_paper_detour` | 5 | 197.2 МиБ |
| `archive/unclassified_episodes/023_margorie_mccall` | 497 | 189.3 МиБ |
| `channels/nuviko_stories/videos/021_семейный_ужин_сюрприз` | 358 | 175.9 МиБ |
| `channels/nuviko_history/videos/002_pompeii` | 168 | 113.8 МиБ |
| `channels/paper_detour/videos/036_trinaxodon_broomistega` | 87 | 108.7 МиБ |
| `channels/paper_detour/experiments` | 83 | 104.1 МиБ |
| `channels/paper_detour/brand` | 88 | 103.3 МиБ |
| `.agent/experiments` | 40 | 95.1 МиБ |
| `channels/paper_detour/legacy/027_doomscrolling_short` | 208 | 91.4 МиБ |
| `channels/paper_detour/videos/035_mantis_shrimp_club` | 80 | 56.9 МиБ |
| `channels/nuviko_stories/videos/013_сестра_пришла_на_помолвку_в_свадебном_платье` | 486 | 56.1 МиБ |
| `channels/paper_detour/videos/005_ai_future_of_work` | 58 | 50.3 МиБ |
| `channels/paper_detour/research` | 272 | 46.9 МиБ |
| `channels/nuviko_stories/videos/001_brother_ex_best_friend` | 28 | 44.8 МиБ |
| `channels/paper_detour/legacy/029_paper_last_video` | 3 | 36.3 МиБ |
| `channels/paper_detour/videos/006_herculaneum_scrolls` | 65 | 33.9 МиБ |
| `channels/nuviko_stories/videos/014_подарок_парню_и_незнакомец_с_книгами_толкина` | 98 | 15.9 МиБ |
| `channels/nuviko_stories/assets` | 7 | 15.8 МиБ |

## Особо крупные случаи

- `channels/paper_detour/Shared/Overlays/Film_Grain/paper_film_grain_visible_15min_270x480_30fps_v01.mov`: 10.21 ГиБ. Это preparation reservoir; он импортирован в Palmier-проект 028 и указан в его текущем контексте. Короткий общий цикл также существует, но замену в 028 не проверяли. Возможное предложение только с учётом последствий для монтажа.
- `channels/paper_detour/videos/033_time_stop/Edit/Automation/time_stop_visual_v01/film_grain_v01.mov`: 3.62 ГиБ; упомянут в манифесте и квитанции превью. Выпуск активно редактировался; проверить актуальный проект.
- `channels/paper_detour/videos/028_taj_mahal/Edit/Overlays/028_film_grain_full_length_v01_540x960_30fps_40pct.mov` и `...v02_540x960_30fps_full_alpha.mov`: соответственно 2.12 и 1.21 ГиБ; оба импортированы в проект 028. Возможные старые слои, но не подтверждено, что можно удалить без последствий.
- `channels/paper_detour/videos/028_taj_mahal/Edit/Previews/` содержит три MOV по 0.58–0.59 ГиБ; отдельно выбрать после проверки версий.
- `channels/paper_detour/videos/033_time_stop/Deliverables/` — текущая локальная версия; по записи H.264 загружен как private, финальная локальная выдача ещё не принята пользователем.
- `channels/paper_detour/videos/028_taj_mahal/Deliverables/` — финальный MP4; по записи выпуск опубликован, но актуальный YouTube read-back в этой инвентаризации не выполнялся.
- Повторяющиеся копии общего зерна по ~498 МиБ задокументированы как APFS-клоны: удаление одной ссылки может почти не освободить места.
- `channels/paper_detour/legacy/025_iq_gallery/...v19.mp4` указан как аудио-референс в манифесте актуальной версии Paper 003.

## Все видеофайлы по категориям и размеру

Пути относительно корня. Отметка `Palmier media.json` — обнаруженная ссылка в файле проекта; это не полный анализ таймлайна.


### A — выдачи и финальные видео: кандидаты после проверки — 42 видео, 3.96 ГиБ

- 334.0 МиБ — `channels/paper_detour/videos/001_radio_game/Deliverables/001_en_long_paper_world_20261031_audio256.mp4`
- 271.6 МиБ — `channels/paper_detour/videos/033_time_stop/Deliverables/Paper_Detour_033_time_stop_EN_1080x1920_30fps_v01.mp4`
- 244.0 МиБ — `channels/paper_detour/videos/030_clothing_history/Deliverables/PAPER_DETOUR_030_CLOTHING_HISTORY_EN_v06.mp4`
- 227.2 МиБ — `channels/paper_detour/legacy/020_rarovista_radio_game/Deliverables/020_en_long_radio_game.mp4`
- 225.8 МиБ — `channels/paper_detour/videos/008_boyfriend_brought_friend/Deliverables/008_boyfriend_friend_en_1080x1920_30fps_silent_v01_20261101.mp4`
- 194.2 МиБ — `channels/nuviko_stories/videos/015_девушка_моего_брата_приревновала_его_ко_мне/Deliverables/015_ru_shorts_110_audio192.mp4`
- 162.3 МиБ — `channels/paper_detour/videos/008_boyfriend_brought_friend/Deliverables/008_boyfriend_friend_en_1080x1920_30fps_voice_v04_animated_accents_20261101.mp4`
- 162.3 МиБ — `channels/paper_detour/videos/008_boyfriend_brought_friend/Deliverables/008_boyfriend_friend_en_1080x1920_30fps_voice_v06_unified_titles_20261101.mp4`
- 162.1 МиБ — `channels/paper_detour/videos/008_boyfriend_brought_friend/Deliverables/008_boyfriend_friend_en_1080x1920_30fps_voice_v05_editorial_cues_20261101.mp4`
- 137.5 МиБ — `channels/paper_detour/videos/028_taj_mahal/Deliverables/028_taj_mahal_en_short_1080x1920_30fps_v10_fine_grain25_voice192_20261102.mp4`
- 132.8 МиБ — `archive/unclassified_episodes/003_gus/Deliverables/003_ru_shorts_v2.mp4`
- 122.7 МиБ — `channels/paper_detour/legacy/025_iq_gallery/Deliverables/archive/025_iq_gallery_paper_detour_60s_v18_linear_fade_candidate.mp4`
- 120.3 МиБ — `channels/paper_detour/legacy/025_iq_gallery/Deliverables/025_iq_gallery_paper_detour_60s_v19.mp4`
- 112.7 МиБ — `archive/unclassified_episodes/003_gus/Deliverables/003_en_shorts_v2.mp4`
- 98.6 МиБ — `channels/paper_detour/legacy/024_margorie_mccall_paper_detour/Deliverables/002_en_margorie_mccall_paper_accents_audio320.mp4`
- 98.6 МиБ — `channels/paper_detour/legacy/024_margorie_mccall_paper_detour/Deliverables/002_en_margorie_mccall_paper_epitaph_audio320.mp4`
- 97.2 МиБ — `channels/paper_detour/videos/002_margorie_mccall/Deliverables/002_en_margorie_mccall_paper_accents_20261031_palmier_raw.mp4`
- 90.0 МиБ — `channels/paper_detour/videos/031_jascon4_okene/Deliverables/031_jascon4_okene_en_short_1080x1920_30fps_v11_fine_grain25.mp4`
- 57.6 МиБ — `channels/paper_detour/videos/007_joshua_jessica/Deliverables/007_joshua_jessica_en_short_1080x1920_30fps_paper_full_frame_v02_20261101.mp4`
- 53.9 МиБ — `channels/nuviko_history/videos/016_marseille_1720/Deliverables/016_en_marseille_04_shorts_audio192.mp4`
- 53.8 МиБ — `channels/nuviko_history/videos/009_black_death/Shorts/02_trade_routes/Deliverables/009_en_black_death_02_shorts_105_v2.mp4`
- 53.8 МиБ — `channels/nuviko_history/videos/009_black_death/Shorts/05_labour/Deliverables/009_en_black_death_05_shorts_105_v2.mp4`
- 53.2 МиБ — `channels/nuviko_history/videos/016_marseille_1720/Deliverables/016_en_marseille_04_shorts_palmier.mp4`
- 50.3 МиБ — `channels/nuviko_history/videos/016_marseille_1720/Deliverables/016_en_marseille_01_shorts_audio192.mp4`
- 50.3 МиБ — `channels/nuviko_history/videos/016_marseille_1720/Deliverables/016_en_marseille_01_shorts_caption_safe_v2_audio192.mp4`
- 49.9 МиБ — `channels/nuviko_history/videos/009_black_death/Shorts/01_intro/Deliverables/009_en_black_death_01_shorts_105.mp4`
- 49.8 МиБ — `channels/nuviko_history/videos/016_marseille_1720/Deliverables/016_en_marseille_01_shorts_palmier.mp4`
- 49.7 МиБ — `channels/nuviko_history/videos/016_marseille_1720/Deliverables/016_en_marseille_01_shorts_caption_safe_v2_palmier.mp4`
- 49.4 МиБ — `channels/nuviko_history/videos/016_marseille_1720/Deliverables/016_en_marseille_03_shorts_audio192.mp4`
- 48.8 МиБ — `channels/nuviko_history/videos/016_marseille_1720/Deliverables/016_en_marseille_03_shorts_palmier.mp4`
- 48.2 МиБ — `channels/nuviko_history/videos/009_black_death/Shorts/04_quarantine/Deliverables/009_en_black_death_04_shorts_105_v2.mp4`
- 47.1 МиБ — `channels/paper_detour/legacy/020_rarovista_radio_game/Deliverables/02_decoder_more_accents_20261031.mp4`
- 46.2 МиБ — `channels/nuviko_history/videos/016_marseille_1720/Deliverables/016_en_marseille_02_shorts_audio192.mp4`
- 45.7 МиБ — `channels/nuviko_history/videos/016_marseille_1720/Deliverables/016_en_marseille_02_shorts_palmier.mp4`
- 44.2 МиБ — `channels/nuviko_history/videos/009_black_death/Shorts/03_coins/Deliverables/009_en_black_death_03_shorts_105_v2.mp4`
- 43.3 МиБ — `channels/paper_detour/videos/009_knorozov_asya/Deliverables/009_knorozov_asya_en_short_1080x1920_30fps_fullmix_v04_20261101.mp4`
- 41.1 МиБ — `channels/paper_detour/videos/009_knorozov_asya/Deliverables/009_knorozov_asya_en_short_1080x1920_30fps_fullmix_v03_20261101.mp4`
- 37.8 МиБ — `channels/paper_detour/legacy/020_rarovista_radio_game/Deliverables/001_short_01_fullgrain_audio320_20261031.mp4`
- 36.3 МиБ — `channels/paper_detour/legacy/029_paper_last_video/Deliverables/004_en_last_video_v5_constant_grain_20261101.mp4`
- 24.3 МиБ — `channels/paper_detour/legacy/020_rarovista_radio_game/Deliverables/03_stereo_text_en_shorts_v2.mp4`
- 23.5 МиБ — `channels/paper_detour/legacy/020_rarovista_radio_game/Deliverables/02_decoder_en_shorts_v2.mp4`
- 3.6 МиБ — `channels/paper_detour/legacy/025_iq_gallery/Deliverables/025_iq_gallery_en_preview_v2.mp4`

### B — слои MOV и промежуточные мастера: проверить монтаж — 73 видео, 17.27 ГиБ

- 3.62 ГиБ — `channels/paper_detour/videos/033_time_stop/Edit/Automation/time_stop_visual_v01/film_grain_v01.mov`
- 2.12 ГиБ — `channels/paper_detour/videos/028_taj_mahal/Edit/Overlays/028_film_grain_full_length_v01_540x960_30fps_40pct.mov` — Palmier media.json: `channels/paper_detour/videos/028_taj_mahal/Paper Detour 028 Taj Mahal Montage Draft 20261101.palmier/media.json`
- 1.21 ГиБ — `channels/paper_detour/videos/028_taj_mahal/Edit/Overlays/028_film_grain_full_length_v02_540x960_30fps_full_alpha.mov` — Palmier media.json: `channels/paper_detour/videos/028_taj_mahal/Paper Detour 028 Taj Mahal Montage Draft 20261101.palmier/media.json`
- 602.6 МиБ — `channels/paper_detour/videos/028_taj_mahal/Edit/Previews/028_en_v08_grain_prores_mezzanine_20261102.mov`
- 595.4 МиБ — `channels/paper_detour/videos/028_taj_mahal/Edit/Previews/028_en_v10_fine_grain25_prores_20261102.mov`
- 591.1 МиБ — `channels/paper_detour/videos/028_taj_mahal/Edit/Previews/028_en_v09_fine_grain_under_text_prores_20261102.mov`
- 378.7 МиБ — `channels/nuviko_stories/videos/012_дорогой_подарок_оказался_семейной_реликвией/Edit/Captions/012_ru_caption_overlay_110.mov`
- 372.9 МиБ — `channels/nuviko_stories/videos/011_парень_приводил_друга_на_каждое_свидание/Edit/Captions/011_ru_caption_overlay.mov` — Palmier media.json: `channels/nuviko_stories/videos/001_brother_ex_best_friend/1.palmier/media.json`
- 299.0 МиБ — `channels/nuviko_stories/videos/012_дорогой_подарок_оказался_семейной_реликвией/Edit/Captions/012_en_caption_overlay_110.mov`
- 293.3 МиБ — `channels/nuviko_stories/videos/019_торт_с_чужим_именем/Edit/Captions/ru_pulse_overlay_019_v3.mov` — Palmier media.json: `channels/nuviko_stories/videos/001_brother_ex_best_friend/1.palmier/media.json`
- 292.6 МиБ — `channels/nuviko_stories/videos/012_дорогой_подарок_оказался_семейной_реликвией/Edit/Captions/012_en_caption_overlay_110_89px.mov`
- 267.3 МиБ — `channels/nuviko_stories/videos/011_парень_приводил_друга_на_каждое_свидание/Edit/Captions/011_en_caption_overlay_110_89px.mov` — Palmier media.json: `channels/nuviko_stories/videos/001_brother_ex_best_friend/1.palmier/media.json`
- 245.9 МиБ — `channels/nuviko_stories/videos/018_соседский_мальчик_назвал_меня_папой/Edit/Captions/ru_pulse_overlay_018.mov`
- 244.3 МиБ — `channels/nuviko_stories/videos/018_соседский_мальчик_назвал_меня_папой/Edit/Captions/ru_pulse_overlay_018_v2.mov`
- 244.3 МиБ — `channels/nuviko_stories/videos/018_соседский_мальчик_назвал_меня_папой/Edit/Captions/ru_pulse_overlay_018_v3.mov`
- 215.0 МиБ — `channels/nuviko_stories/videos/018_соседский_мальчик_назвал_меня_папой/Edit/EN_Final/018_en_captions_110_prores.mov`
- 210.8 МиБ — `channels/nuviko_stories/videos/018_соседский_мальчик_назвал_меня_папой/Edit/EN_SafeDraft/018_en_captions_dynamic.mov`
- 208.3 МиБ — `channels/nuviko_stories/videos/018_соседский_мальчик_назвал_меня_папой/Edit/EN_SafeDraft/018_en_captions_safe_draft.mov`
- 138.8 МиБ — `channels/nuviko_history/videos/004_pompeii_short/Edit/Captions/004_en_v3_caption_overlay.mov` — Palmier media.json: `channels/nuviko_stories/videos/001_brother_ex_best_friend/1.palmier/media.json`
- 138.4 МиБ — `channels/nuviko_history/videos/004_pompeii_short/Edit/Captions/004_en_v2_caption_overlay.mov` — Palmier media.json: `channels/nuviko_stories/videos/001_brother_ex_best_friend/1.palmier/media.json`
- 137.4 МиБ — `channels/nuviko_history/videos/009_black_death/Shorts/02_trade_routes/Edit/Captions/02_en_caption_overlay_safe.mov` — Palmier media.json: `channels/nuviko_stories/videos/001_brother_ex_best_friend/1.palmier/media.json`
- 131.0 МиБ — `channels/nuviko_history/videos/009_black_death/Shorts/05_labour/Edit/Captions/05_en_caption_overlay_face_safe.mov` — Palmier media.json: `channels/nuviko_stories/videos/001_brother_ex_best_friend/1.palmier/media.json`
- 130.0 МиБ — `channels/nuviko_history/videos/009_black_death/Shorts/02_trade_routes/Edit/Speed105/Captions/02_en_caption_overlay_105.mov` — Palmier media.json: `channels/nuviko_stories/videos/001_brother_ex_best_friend/1.palmier/media.json`
- 128.8 МиБ — `channels/nuviko_history/videos/009_black_death/Shorts/02_trade_routes/Edit/Speed105/Captions/02_en_caption_overlay_105_v2.mov` — Palmier media.json: `channels/nuviko_stories/videos/001_brother_ex_best_friend/1.palmier/media.json`
- 123.9 МиБ — `channels/nuviko_history/videos/009_black_death/Shorts/05_labour/Edit/Speed105/Captions/05_en_caption_overlay_105.mov` — Palmier media.json: `channels/nuviko_stories/videos/001_brother_ex_best_friend/1.palmier/media.json`
- 123.1 МиБ — `channels/nuviko_history/videos/009_black_death/Shorts/05_labour/Edit/Speed105/Captions/05_en_caption_overlay_105_v2.mov` — Palmier media.json: `channels/nuviko_stories/videos/001_brother_ex_best_friend/1.palmier/media.json`
- 120.4 МиБ — `channels/nuviko_history/videos/016_marseille_1720/Shorts/04_marseille/Edit/Captions/04_en_caption_overlay_safe_v2.mov` — Palmier media.json: `channels/nuviko_stories/videos/001_brother_ex_best_friend/1.palmier/media.json`
- 119.4 МиБ — `archive/unclassified_episodes/023_margorie_mccall/Edit/023_v6_caption_source_prores4444.mov`
- 118.0 МиБ — `channels/nuviko_history/videos/009_black_death/Shorts/04_quarantine/Edit/Captions/04_en_caption_overlay_safe.mov`
- 117.7 МиБ — `channels/nuviko_history/videos/009_black_death/Shorts/04_quarantine/Edit/Captions/04_en_caption_overlay.mov`
- 117.1 МиБ — `channels/nuviko_history/videos/009_black_death/Shorts/01_intro/Edit/Captions/01_en_caption_overlay_safe.mov` — Palmier media.json: `channels/nuviko_stories/videos/001_brother_ex_best_friend/1.palmier/media.json`
- 117.0 МиБ — `channels/nuviko_history/videos/009_black_death/Shorts/01_intro/Edit/Captions/01_en_caption_overlay_photo_safe_v2.mov`
- 115.0 МиБ — `channels/nuviko_history/videos/016_marseille_1720/Shorts/03_marseille/Edit/Captions/03_en_caption_overlay_safe_v2.mov` — Palmier media.json: `channels/nuviko_stories/videos/001_brother_ex_best_friend/1.palmier/media.json`
- 113.0 МиБ — `channels/nuviko_history/videos/009_black_death/Shorts/03_coins/Edit/Captions/03_en_caption_overlay_photo_safe.mov`
- 112.5 МиБ — `channels/nuviko_history/videos/009_black_death/Shorts/03_coins/Edit/Captions/03_en_caption_overlay.mov`
- 112.3 МиБ — `channels/nuviko_history/videos/009_black_death/Shorts/03_coins/Edit/Captions/03_en_caption_overlay_face_safe.mov` — Palmier media.json: `channels/nuviko_stories/videos/001_brother_ex_best_friend/1.palmier/media.json`
- 111.7 МиБ — `channels/nuviko_history/videos/009_black_death/Shorts/01_intro/Edit/Speed105/Captions/01_en_caption_overlay_safe.mov` — Palmier media.json: `channels/nuviko_stories/videos/001_brother_ex_best_friend/1.palmier/media.json`
- 111.5 МиБ — `channels/nuviko_history/videos/009_black_death/Shorts/04_quarantine/Edit/Speed105/Captions/04_en_caption_overlay_105.mov` — Palmier media.json: `channels/nuviko_stories/videos/001_brother_ex_best_friend/1.palmier/media.json`
- 110.1 МиБ — `channels/nuviko_history/videos/017_galveston_1900/Edit/Captions/02_en_caption_overlay_odom.mov`
- 109.4 МиБ — `channels/nuviko_history/videos/017_galveston_1900/Edit/Captions/02_en_caption_overlay_odom_restart_20261029.mov` — Palmier media.json: `channels/nuviko_stories/videos/001_brother_ex_best_friend/1.palmier/media.json`
- 109.2 МиБ — `channels/nuviko_history/videos/016_marseille_1720/Shorts/01_marseille/Edit/Captions/01_en_caption_overlay_safe.mov` — Palmier media.json: `channels/nuviko_stories/videos/001_brother_ex_best_friend/1.palmier/media.json`
- 109.2 МиБ — `channels/nuviko_history/videos/016_marseille_1720/Shorts/01_marseille/Edit/Captions/01_en_caption_overlay_safe_v2.mov` — Palmier media.json: `channels/nuviko_stories/videos/001_brother_ex_best_friend/1.palmier/media.json`
- 108.4 МиБ — `channels/nuviko_history/videos/016_marseille_1720/Shorts/02_marseille/Edit/Captions/02_en_caption_overlay_safe.mov` — Palmier media.json: `channels/nuviko_stories/videos/001_brother_ex_best_friend/1.palmier/media.json`
- 107.7 МиБ — `channels/nuviko_history/videos/009_black_death/Shorts/03_coins/Edit/Speed105/Captions/03_en_caption_overlay_safe_v2.mov` — Palmier media.json: `channels/nuviko_stories/videos/001_brother_ex_best_friend/1.palmier/media.json`
- 104.4 МиБ — `channels/nuviko_history/videos/017_galveston_1900/Edit/Captions/04_en_caption_overlay_odom.mov`
- 103.6 МиБ — `channels/nuviko_history/videos/017_galveston_1900/Edit/Captions/04_en_caption_overlay_odom_restart_20261029.mov` — Palmier media.json: `channels/nuviko_stories/videos/001_brother_ex_best_friend/1.palmier/media.json`
- 101.9 МиБ — `channels/nuviko_history/videos/017_galveston_1900/Edit/Captions/03_en_caption_overlay_odom.mov`
- 101.5 МиБ — `channels/nuviko_history/videos/017_galveston_1900/Edit/Captions/01_en_caption_overlay_odom.mov` — Palmier media.json: `channels/nuviko_stories/videos/001_brother_ex_best_friend/1.palmier/media.json`, `channels/nuviko_stories/videos/001_brother_ex_best_friend/1.palmier/media.json`
- 101.3 МиБ — `channels/nuviko_history/videos/017_galveston_1900/Edit/Captions/03_en_caption_overlay_odom_shot1safe_v3.mov` — Palmier media.json: `channels/nuviko_stories/videos/001_brother_ex_best_friend/1.palmier/media.json`
- 101.3 МиБ — `channels/nuviko_history/videos/017_galveston_1900/Edit/Captions/03_en_caption_overlay_odom_restart_20261029.mov` — Palmier media.json: `channels/nuviko_stories/videos/001_brother_ex_best_friend/1.palmier/media.json`, `channels/nuviko_stories/videos/001_brother_ex_best_friend/1.palmier/media.json`
- 99.4 МиБ — `channels/nuviko_history/videos/017_galveston_1900/Edit/Captions/05_en_caption_overlay_odom.mov`
- 98.8 МиБ — `channels/nuviko_history/videos/017_galveston_1900/Edit/Captions/05_en_caption_overlay_odom_restart_20261029.mov` — Palmier media.json: `channels/nuviko_stories/videos/001_brother_ex_best_friend/1.palmier/media.json`
- 97.3 МиБ — `channels/nuviko_history/videos/017_galveston_1900/Edit/Captions/02_en_caption_overlay_odom_scene_repositioned.mov`
- 96.7 МиБ — `channels/nuviko_history/videos/017_galveston_1900/Edit/Captions/02_en_caption_overlay_v2.mov`
- 96.4 МиБ — `channels/nuviko_history/videos/017_galveston_1900/Edit/Captions/02_en_caption_overlay.mov`
- 92.7 МиБ — `channels/nuviko_stories/videos/022_свадьба_сестры_в_подарок/Edit/Captions/022_canonical_overlay.mov` — Palmier media.json: `channels/nuviko_stories/videos/001_brother_ex_best_friend/1.palmier/media.json`
- 90.1 МиБ — `channels/nuviko_history/videos/017_galveston_1900/Edit/Captions/01_en_caption_overlay.mov`
- 88.4 МиБ — `channels/nuviko_history/videos/017_galveston_1900/Edit/Captions/05_en_caption_overlay_v2.mov`
- 88.3 МиБ — `channels/nuviko_history/videos/017_galveston_1900/Edit/Captions/05_en_caption_overlay.mov`
- 87.5 МиБ — `channels/nuviko_history/videos/017_galveston_1900/Edit/Captions/04_en_caption_overlay.mov`
- 87.3 МиБ — `channels/nuviko_history/videos/017_galveston_1900/Edit/Captions/01_en_caption_overlay_v2.mov`
- 87.0 МиБ — `channels/nuviko_history/videos/017_galveston_1900/Edit/Captions/04_en_caption_overlay_v2.mov`
- 86.9 МиБ — `channels/nuviko_stories/videos/021_семейный_ужин_сюрприз/Edit/Captions/021_canonical_overlay.mov`
- 85.2 МиБ — `channels/nuviko_history/videos/017_galveston_1900/Edit/Captions/03_en_caption_overlay.mov`
- 84.4 МиБ — `channels/nuviko_history/videos/004_pompeii_short/Edit/Captions/004_en_caption_overlay.mov` — Palmier media.json: `channels/nuviko_stories/videos/001_brother_ex_best_friend/1.palmier/media.json`
- 83.9 МиБ — `channels/nuviko_history/videos/017_galveston_1900/Edit/Captions/03_en_caption_overlay_v2.mov`
- 78.8 МиБ — `channels/nuviko_history/videos/017_galveston_1900/Edit/Captions/03_en_caption_overlay_odom_scene_repositioned.mov`
- 74.3 МиБ — `channels/nuviko_history/videos/017_galveston_1900/Edit/Captions/05_en_caption_overlay_odom_scene_repositioned.mov`
- 48.0 МиБ — `channels/nuviko_stories/videos/018_соседский_мальчик_назвал_меня_папой/Edit/EN_Final/018_en_captions_110.mov`
- 46.3 МиБ — `channels/nuviko_stories/videos/019_торт_с_чужим_именем/Edit/Captions/ru_pulse_overlay_019_v2.mov`
- 40.3 МиБ — `channels/nuviko_stories/videos/019_торт_с_чужим_именем/Edit/Captions/ru_pulse_overlay_019.mov`
- 36.7 МиБ — `channels/nuviko_history/videos/017_galveston_1900/Edit/Captions/04_en_caption_overlay_odom_scene_repositioned_interrupted.mov`
- 32.0 МиБ — `channels/nuviko_history/videos/017_galveston_1900/Edit/Captions/04_en_caption_overlay_odom_scene_repositioned.mov`

### C — превью и промежуточные видео: проверить назначение — 182 видео, 3.99 ГиБ

- 243.9 МиБ — `channels/paper_detour/videos/030_clothing_history/Edit/v05/Accepted_delivery_v05.mp4`
- 243.6 МиБ — `channels/paper_detour/videos/030_clothing_history/Edit/v06/Palmier_export.mp4`
- 243.6 МиБ — `channels/paper_detour/videos/030_clothing_history/Edit/v05/Palmier_export.mp4`
- 228.2 МиБ — `channels/paper_detour/videos/001_radio_game/Edit/FFmpeg/review_draft/001_review_draft.mp4`
- 227.2 МиБ — `channels/paper_detour/videos/001_radio_game/Edit/FFmpeg/final_render/001_review_draft.mp4`
- 222.2 МиБ — `channels/paper_detour/videos/001_radio_game/Edit/FFmpeg/review_draft/001_review_video_only.mp4`
- 221.1 МиБ — `channels/paper_detour/videos/001_radio_game/Edit/FFmpeg/final_render/001_review_video_only.mp4`
- 201.1 МиБ — `channels/paper_detour/videos/003_iq_gallery/Edit/automated_workflow/archive/qa_rejected_20261101/025_iq_gallery_paper_detour_60s_v3_text_overlap_candidate.mp4`
- 131.9 МиБ — `channels/paper_detour/videos/028_taj_mahal/Edit/Previews/028_taj_mahal_en_short_1080x1920_30fps_v02_grain_voice_candidate_20261102.mp4`
- 100.3 МиБ — `channels/paper_detour/videos/033_time_stop/Edit/Previews/Paper_Detour_033_time_stop_EN_mix_preview_v05.mp4`
- 77.5 МиБ — `channels/paper_detour/videos/003_iq_gallery/Edit/automated_workflow/archive/previous_v2_audio_reference_20261031.mp4`
- 76.6 МиБ — `channels/paper_detour/videos/003_iq_gallery/Edit/palmier/raw_palmier_003_60s.mp4`
- 76.5 МиБ — `channels/paper_detour/videos/003_iq_gallery/Edit/palmier/raw_palmier_003_60s_v2.mp4`
- 60.0 МиБ — `channels/nuviko_history/videos/004_pompeii_short/Edit/004_palmier_export.mp4`
- 57.6 МиБ — `channels/nuviko_stories/videos/022_свадьба_сестры_в_подарок/Edit/022_canonical_raw.mp4`
- 57.5 МиБ — `channels/paper_detour/videos/004_last_video/Edit/preview_unfinished_20261031.mp4`
- 57.5 МиБ — `channels/paper_detour/videos/004_last_video/Edit/preview_v3_unfinished_20261031.mp4`
- 57.5 МиБ — `channels/paper_detour/videos/004_last_video/Edit/preview_v4_unfinished_20261031.mp4`
- 57.5 МиБ — `channels/paper_detour/videos/004_last_video/Edit/preview_v2_unfinished_20261031.mp4`
- 56.9 МиБ — `channels/paper_detour/videos/007_joshua_jessica/Edit/Automation/Renders/007_joshua_jessica_short_20261101_palmier_v04_raw.mp4`
- 50.0 МиБ — `channels/paper_detour/videos/009_knorozov_asya/Edit/Archive/009_knorozov_asya_en_short_1080x1920_30fps_silent_v01_20261101.mp4`
- 47.6 МиБ — `channels/paper_detour/videos/027_doomscrolling_short/Edit/Previews/PD027_Minnie_v03_visual_only_20261101.mp4`
- 45.4 МиБ — `channels/paper_detour/videos/028_taj_mahal/Edit/Previews/028_en_v08_grain_voice192_candidate.mp4`
- 44.9 МиБ — `channels/paper_detour/videos/027_doomscrolling_short/Edit/Previews/PD027_Minnie_PaperDiorama_v02_20261101_review.mp4`
- 44.8 МиБ — `channels/paper_detour/videos/028_taj_mahal/Edit/Previews/028_en_v07_film_grain_25pct_20261102.mp4`
- 44.8 МиБ — `channels/paper_detour/videos/028_taj_mahal/Edit/Previews/028_en_v08_film_grain_20pct_20261102.mp4`
- 44.8 МиБ — `channels/paper_detour/videos/027_doomscrolling_short/Edit/Previews/PD027_Minnie_FullStills_v01_20261101_review.mp4`
- 44.8 МиБ — `channels/paper_detour/videos/028_taj_mahal/Edit/Previews/028_en_v03_palmier_grain_under_text_20261102.mp4`
- 44.5 МиБ — `channels/paper_detour/videos/027_doomscrolling_short/Edit/Previews/PD027_Minnie_PaperDiorama_v02_20261101_render.mp4`
- 44.4 МиБ — `channels/paper_detour/videos/027_doomscrolling_short/Edit/Previews/PD027_Minnie_FullStills_v01_20261101_render.mp4`
- 42.4 МиБ — `channels/paper_detour/videos/028_taj_mahal/Edit/Previews/028_en_v04_full_alpha_grain_20261102.mp4`
- 42.4 МиБ — `channels/paper_detour/videos/028_taj_mahal/Edit/Previews/028_taj_mahal_en_short_1080x1920_30fps_voice_v01_palmier_audio64_review_20261101.mp4`
- 38.9 МиБ — `channels/paper_detour/videos/003_iq_gallery/Edit/palmier/raw_palmier_003_fixed.mp4`
- 38.9 МиБ — `channels/paper_detour/videos/003_iq_gallery/Edit/palmier/raw_palmier_003.mp4`
- 34.6 МиБ — `channels/paper_detour/videos/009_knorozov_asya/Edit/Archive/009_knorozov_asya_en_short_1080x1920_30fps_fullmix_v02_20261101.mp4`
- 29.0 МиБ — `channels/paper_detour/videos/030_clothing_history/Delivery/030_v03_silent_review/PAPER_DETOUR_030_v03_silent_image_cut_review.mp4`
- 28.8 МиБ — `channels/paper_detour/videos/028_taj_mahal/Edit/Previews/028_visible_film_grain_balanced_4s.mp4`
- 20.3 МиБ — `channels/paper_detour/videos/028_taj_mahal/Edit/Previews/028_film_grain_25pct_4s_check.mp4`
- 18.9 МиБ — `channels/paper_detour/videos/028_taj_mahal/Edit/Previews/028_visible_film_grain_4s_check.mp4`
- 17.5 МиБ — `channels/paper_detour/videos/028_taj_mahal/Edit/Previews/028_film_grain_20pct_4s_check.mp4`
- 14.5 МиБ — `channels/paper_detour/videos/003_iq_gallery/Edit/automated_workflow/test_mixed_dimensions_fullhd.mp4`
- 14.5 МиБ — `channels/paper_detour/videos/003_iq_gallery/Edit/automated_workflow/test_grouped_fullhd.mp4`
- 14.2 МиБ — `channels/paper_detour/videos/003_iq_gallery/Edit/automated_workflow/preview_two_scenes_offset_v1.mp4`
- 14.2 МиБ — `channels/paper_detour/videos/003_iq_gallery/Edit/automated_workflow/preview_two_scenes.mp4`
- 14.1 МиБ — `channels/paper_detour/videos/003_iq_gallery/Edit/automated_workflow/test_technical_fullhd.mp4`
- 13.7 МиБ — `channels/paper_detour/videos/003_iq_gallery/Edit/automated_workflow/preview_text_occlusion_v1.mp4`
- 13.6 МиБ — `channels/paper_detour/videos/003_iq_gallery/Edit/automated_workflow/preview_text_occlusion_v2.mp4`
- 13.3 МиБ — `channels/paper_detour/legacy/027_doomscrolling_short/Edit/QC/visual_preview_silent_v2.mp4`
- 13.3 МиБ — `channels/paper_detour/legacy/027_doomscrolling_short/Edit/QC/visual_preview_silent.mp4`
- 7.0 МиБ — `channels/paper_detour/videos/001_radio_game/Edit/FFmpeg/final_render/segments/041.mp4`
- 6.9 МиБ — `channels/paper_detour/videos/001_radio_game/Edit/FFmpeg/review_draft/segments/029.mp4`
- 6.9 МиБ — `channels/paper_detour/videos/001_radio_game/Edit/FFmpeg/final_render/segments/029.mp4`
- 6.9 МиБ — `channels/paper_detour/videos/001_radio_game/Edit/FFmpeg/review_draft/segments/041.mp4`
- 6.3 МиБ — `channels/paper_detour/videos/001_radio_game/Edit/FFmpeg/review_draft/segments/031.mp4`
- 6.3 МиБ — `channels/paper_detour/videos/001_radio_game/Edit/FFmpeg/final_render/segments/031.mp4`
- 6.0 МиБ — `channels/paper_detour/videos/001_radio_game/Edit/FFmpeg/final_render/segments/040.mp4`
- 6.0 МиБ — `channels/paper_detour/videos/001_radio_game/Edit/FFmpeg/review_draft/segments/016.mp4`
- 6.0 МиБ — `channels/paper_detour/videos/001_radio_game/Edit/FFmpeg/final_render/segments/016.mp4`
- 5.9 МиБ — `channels/paper_detour/videos/001_radio_game/Edit/FFmpeg/review_draft/segments/040.mp4`
- 5.9 МиБ — `channels/paper_detour/videos/001_radio_game/Edit/FFmpeg/final_render/segments/039.mp4`
- 5.9 МиБ — `channels/paper_detour/videos/001_radio_game/Edit/FFmpeg/review_draft/segments/034.mp4`
- 5.9 МиБ — `channels/paper_detour/videos/001_radio_game/Edit/FFmpeg/final_render/segments/034.mp4`
- 5.8 МиБ — `channels/paper_detour/videos/001_radio_game/Edit/FFmpeg/review_draft/segments/039.mp4`
- 5.8 МиБ — `channels/paper_detour/videos/001_radio_game/Edit/FFmpeg/review_draft/segments/025.mp4`
- 5.7 МиБ — `channels/paper_detour/videos/001_radio_game/Edit/FFmpeg/review_draft/segments/018.mp4`
- 5.7 МиБ — `channels/paper_detour/videos/001_radio_game/Edit/FFmpeg/review_draft/segments/011.mp4`
- 5.7 МиБ — `channels/paper_detour/videos/001_radio_game/Edit/FFmpeg/final_render/segments/011.mp4`
- 5.7 МиБ — `channels/paper_detour/brand/paper_world_reference/layered_parallax_reference.mp4`
- 5.6 МиБ — `channels/paper_detour/videos/001_radio_game/Edit/FFmpeg/final_render/segments/025.mp4`
- 5.5 МиБ — `channels/paper_detour/videos/001_radio_game/Edit/FFmpeg/review_draft/segments/013.mp4`
- 5.5 МиБ — `channels/paper_detour/videos/001_radio_game/Edit/FFmpeg/review_draft/segments/019.mp4`
- 5.5 МиБ — `channels/paper_detour/videos/001_radio_game/Edit/FFmpeg/review_draft/segments/017.mp4`
- 5.5 МиБ — `channels/paper_detour/videos/001_radio_game/Edit/FFmpeg/final_render/segments/013.mp4`
- 5.4 МиБ — `channels/paper_detour/videos/001_radio_game/Edit/FFmpeg/final_render/segments/018.mp4`
- 5.4 МиБ — `channels/paper_detour/videos/001_radio_game/Edit/FFmpeg/final_render/segments/005.mp4`
- 5.3 МиБ — `channels/paper_detour/videos/001_radio_game/Edit/FFmpeg/review_draft/segments/010.mp4`
- 5.3 МиБ — `channels/paper_detour/videos/001_radio_game/Edit/FFmpeg/final_render/segments/010.mp4`
- 5.3 МиБ — `channels/paper_detour/videos/001_radio_game/Edit/FFmpeg/review_draft/segments/005.mp4`
- 5.3 МиБ — `channels/paper_detour/videos/001_radio_game/Edit/FFmpeg/final_render/segments/027.mp4`
- 5.3 МиБ — `channels/paper_detour/videos/001_radio_game/Edit/FFmpeg/review_draft/segments/006.mp4`
- 5.3 МиБ — `channels/paper_detour/videos/001_radio_game/Edit/FFmpeg/final_render/segments/006.mp4`
- 5.3 МиБ — `channels/paper_detour/videos/001_radio_game/Edit/FFmpeg/final_render/segments/019.mp4`
- 5.2 МиБ — `channels/paper_detour/videos/001_radio_game/Edit/FFmpeg/review_draft/segments/032.mp4`
- 5.2 МиБ — `channels/paper_detour/videos/001_radio_game/Edit/FFmpeg/review_draft/segments/027.mp4`
- 5.2 МиБ — `channels/paper_detour/videos/001_radio_game/Edit/FFmpeg/review_draft/segments/015.mp4`
- 5.1 МиБ — `channels/paper_detour/videos/001_radio_game/Edit/FFmpeg/review_draft/segments/009.mp4`
- 5.1 МиБ — `channels/paper_detour/videos/001_radio_game/Edit/FFmpeg/final_render/segments/009.mp4`
- 5.1 МиБ — `channels/paper_detour/videos/001_radio_game/Edit/FFmpeg/final_render/segments/032.mp4`
- 5.1 МиБ — `channels/paper_detour/videos/001_radio_game/Edit/FFmpeg/final_render/segments/015.mp4`
- 5.1 МиБ — `channels/paper_detour/videos/001_radio_game/Edit/FFmpeg/review_draft/segments/045.mp4`
- 5.1 МиБ — `channels/paper_detour/videos/001_radio_game/Edit/FFmpeg/final_render/segments/045.mp4`
- 5.1 МиБ — `channels/paper_detour/videos/001_radio_game/Edit/FFmpeg/final_render/segments/037.mp4`
- 5.0 МиБ — `channels/paper_detour/videos/001_radio_game/Edit/FFmpeg/review_draft/segments/037.mp4`
- 5.0 МиБ — `channels/paper_detour/videos/001_radio_game/Edit/FFmpeg/review_draft/segments/044.mp4`
- 5.0 МиБ — `channels/paper_detour/videos/001_radio_game/Edit/FFmpeg/final_render/segments/044.mp4`
- 5.0 МиБ — `channels/paper_detour/videos/001_radio_game/Edit/FFmpeg/final_render/segments/017.mp4`
- 4.8 МиБ — `channels/paper_detour/videos/001_radio_game/Edit/FFmpeg/review_draft/segments/012.mp4`
- 4.8 МиБ — `channels/paper_detour/videos/001_radio_game/Edit/FFmpeg/final_render/segments/012.mp4`
- 4.7 МиБ — `channels/paper_detour/videos/001_radio_game/Edit/FFmpeg/review_draft/segments/003.mp4`
- 4.7 МиБ — `channels/paper_detour/videos/001_radio_game/Edit/FFmpeg/final_render/segments/003.mp4`
- 4.6 МиБ — `channels/paper_detour/videos/001_radio_game/Edit/FFmpeg/final_render/segments/035.mp4`
- 4.6 МиБ — `channels/paper_detour/videos/001_radio_game/Edit/FFmpeg/review_draft/segments/043.mp4`
- 4.6 МиБ — `channels/paper_detour/videos/001_radio_game/Edit/FFmpeg/final_render/segments/043.mp4`
- 4.6 МиБ — `channels/paper_detour/videos/001_radio_game/Edit/FFmpeg/review_draft/segments/033.mp4`
- 4.6 МиБ — `channels/paper_detour/videos/001_radio_game/Edit/FFmpeg/review_draft/segments/020.mp4`
- 4.6 МиБ — `channels/paper_detour/videos/001_radio_game/Edit/FFmpeg/final_render/segments/020.mp4`
- 4.6 МиБ — `channels/paper_detour/videos/001_radio_game/Edit/FFmpeg/review_draft/segments/035.mp4`
- 4.5 МиБ — `channels/paper_detour/videos/001_radio_game/Edit/FFmpeg/final_render/segments/028.mp4`
- 4.5 МиБ — `channels/paper_detour/videos/001_radio_game/Edit/FFmpeg/review_draft/segments/028.mp4`
- 4.5 МиБ — `channels/paper_detour/videos/001_radio_game/Edit/FFmpeg/final_render/segments/004.mp4`
- 4.5 МиБ — `channels/paper_detour/videos/001_radio_game/Edit/FFmpeg/final_render/segments/033.mp4`
- 4.4 МиБ — `channels/paper_detour/videos/001_radio_game/Edit/FFmpeg/review_draft/segments/021.mp4`
- 4.4 МиБ — `channels/paper_detour/videos/001_radio_game/Edit/FFmpeg/final_render/segments/021.mp4`
- 4.4 МиБ — `channels/paper_detour/videos/001_radio_game/Edit/FFmpeg/review_draft/segments/004.mp4`
- 4.4 МиБ — `channels/paper_detour/videos/001_radio_game/Edit/FFmpeg/final_render/segments/024.mp4`
- 4.4 МиБ — `channels/paper_detour/videos/001_radio_game/Edit/FFmpeg/review_draft/segments/024.mp4`
- 4.4 МиБ — `channels/paper_detour/videos/006_herculaneum_scrolls/Edit/offline_silent_layer_test/silent_layer_test_v03.mp4`
- 4.3 МиБ — `channels/paper_detour/videos/001_radio_game/Edit/FFmpeg/review_draft/segments/014.mp4`
- 4.3 МиБ — `channels/paper_detour/videos/001_radio_game/Edit/FFmpeg/final_render/segments/014.mp4`
- 4.3 МиБ — `channels/paper_detour/videos/001_radio_game/Edit/FFmpeg/review_draft/segments/038.mp4`
- 4.3 МиБ — `channels/paper_detour/videos/001_radio_game/Edit/FFmpeg/final_render/segments/038.mp4`
- 4.0 МиБ — `channels/paper_detour/videos/001_radio_game/Edit/FFmpeg/review_draft/segments/046.mp4`
- 4.0 МиБ — `channels/paper_detour/videos/001_radio_game/Edit/FFmpeg/final_render/segments/046.mp4`
- 4.0 МиБ — `channels/paper_detour/videos/001_radio_game/Edit/FFmpeg/review_draft/segments/023.mp4`
- 4.0 МиБ — `channels/paper_detour/videos/001_radio_game/Edit/FFmpeg/final_render/segments/023.mp4`
- 3.8 МиБ — `channels/paper_detour/videos/001_radio_game/Edit/FFmpeg/review_draft/segments/026.mp4`
- 3.8 МиБ — `channels/paper_detour/videos/001_radio_game/Edit/FFmpeg/final_render/segments/026.mp4`
- 3.7 МиБ — `channels/paper_detour/videos/001_radio_game/Edit/FFmpeg/review_draft/segments/008.mp4`
- 3.7 МиБ — `channels/paper_detour/videos/001_radio_game/Edit/FFmpeg/final_render/segments/008.mp4`
- 3.4 МиБ — `channels/paper_detour/videos/003_iq_gallery/Edit/independent_trial_20261101/two_scene_motion_trial.mp4`
- 3.2 МиБ — `channels/paper_detour/videos/001_radio_game/Edit/FFmpeg/review_draft/segments/007.mp4`
- 3.2 МиБ — `channels/paper_detour/videos/001_radio_game/Edit/FFmpeg/final_render/segments/007.mp4`
- 3.2 МиБ — `channels/paper_detour/videos/001_radio_game/Edit/FFmpeg/review_draft/segments/000.mp4`
- 3.2 МиБ — `channels/paper_detour/videos/001_radio_game/Edit/FFmpeg/final_render/segments/000.mp4`
- 3.1 МиБ — `channels/paper_detour/videos/001_radio_game/Edit/FFmpeg/review_draft/segments/042.mp4`
- 3.1 МиБ — `channels/paper_detour/videos/001_radio_game/Edit/FFmpeg/final_render/segments/042.mp4`
- 3.0 МиБ — `channels/paper_detour/videos/001_radio_game/Edit/FFmpeg/review_draft/segments/002.mp4`
- 3.0 МиБ — `channels/paper_detour/videos/001_radio_game/Edit/FFmpeg/final_render/segments/002.mp4`
- 2.9 МиБ — `channels/paper_detour/videos/001_radio_game/Edit/FFmpeg/review_draft/segments/036.mp4`
- 2.9 МиБ — `channels/paper_detour/videos/001_radio_game/Edit/FFmpeg/final_render/segments/036.mp4`
- 2.9 МиБ — `channels/paper_detour/videos/001_radio_game/Edit/FFmpeg/review_draft/segments/001.mp4`
- 2.9 МиБ — `channels/paper_detour/videos/001_radio_game/Edit/FFmpeg/final_render/segments/001.mp4`
- 2.7 МиБ — `channels/paper_detour/videos/001_radio_game/Edit/FFmpeg/final_render/segments/030.mp4`
- 2.7 МиБ — `channels/paper_detour/videos/001_radio_game/Edit/FFmpeg/review_draft/segments/030.mp4`
- 2.4 МиБ — `channels/paper_detour/videos/001_radio_game/Edit/FFmpeg/review_draft/segments/022.mp4`
- 2.4 МиБ — `channels/paper_detour/videos/001_radio_game/Edit/FFmpeg/final_render/segments/022.mp4`
- 2.1 МиБ — `channels/paper_detour/legacy/027_doomscrolling_short/Edit/QC/preview_segments/scene_06.mp4`
- 1.9 МиБ — `channels/paper_detour/videos/003_iq_gallery/Edit/independent_trial_20261101/jfk_layered_scene_trial.mp4`
- 1.9 МиБ — `channels/paper_detour/videos/003_iq_gallery/Edit/independent_trial_20261101/jfk_layered_scene_trial_v2.mp4`
- 1.9 МиБ — `channels/paper_detour/videos/003_iq_gallery/Edit/independent_trial_20261101/jfk_layered_scene_trial_v3.mp4`
- 1.9 МиБ — `channels/paper_detour/videos/003_iq_gallery/Edit/independent_trial_20261101/jfk_layered_scene_trial_v4.mp4`
- 1.8 МиБ — `channels/paper_detour/videos/030_clothing_history/Edit/parallax_trial_20261102/scene_08.mp4`
- 1.8 МиБ — `channels/paper_detour/videos/030_clothing_history/Edit/parallax_trial_20261102/scene_09.mp4`
- 1.5 МиБ — `channels/paper_detour/legacy/027_doomscrolling_short/Edit/QC/preview_segments/scene_04.mp4`
- 1.5 МиБ — `channels/paper_detour/legacy/027_doomscrolling_short/Edit/QC/preview_segments/scene_05.mp4`
- 1.5 МиБ — `channels/paper_detour/legacy/027_doomscrolling_short/Edit/QC/preview_segments/scene_01.mp4`
- 1.5 МиБ — `channels/paper_detour/legacy/027_doomscrolling_short/Edit/QC/preview_segments/scene_07.mp4`
- 1.4 МиБ — `channels/paper_detour/videos/030_clothing_history/Edit/parallax_trial_20261102/scene_10.mp4`
- 1.1 МиБ — `channels/paper_detour/legacy/027_doomscrolling_short/Edit/QC/preview_segments/scene_02.mp4`
- 1.0 МиБ — `channels/paper_detour/legacy/027_doomscrolling_short/Edit/QC/preview_segments/scene_03.mp4`
- 1.0 МиБ — `channels/paper_detour/videos/030_clothing_history/Edit/parallax_trial_20261102/scene_06.mp4`
- 1.0 МиБ — `channels/paper_detour/videos/030_clothing_history/Edit/parallax_trial_20261102/scene_02.mp4`
- 0.9 МиБ — `channels/paper_detour/videos/030_clothing_history/Edit/parallax_trial_20261102/scene_03.mp4`
- 0.9 МиБ — `.agent/experiments/parallax_single_image_20261102/parallax_very_strong.mp4`
- 0.9 МиБ — `.agent/experiments/parallax_single_image_20261102/parallax_strong.mp4`
- 0.9 МиБ — `channels/paper_detour/videos/030_clothing_history/Edit/parallax_trial_20261102/scene_07.mp4`
- 0.9 МиБ — `.agent/experiments/parallax_single_image_20261102/parallax_preview.mp4`
- 0.9 МиБ — `channels/paper_detour/videos/030_clothing_history/Edit/parallax_trial_20261102/scene_01.mp4`
- 0.9 МиБ — `.agent/experiments/parallax_single_image_20261102/parallax_preview_8_32_64.mp4`
- 0.9 МиБ — `.agent/experiments/parallax_single_image_20261102/parallax_medium.mp4`
- 0.9 МиБ — `.agent/experiments/parallax_single_image_20261102/history/parallax_preview_initial.mp4`
- 0.7 МиБ — `channels/paper_detour/videos/030_clothing_history/Edit/parallax_trial_20261102/scene_05.mp4`
- 0.7 МиБ — `channels/paper_detour/videos/030_clothing_history/Edit/parallax_trial_20261102/scene_04.mp4`
- 0.4 МиБ — `channels/paper_detour/videos/003_iq_gallery/Edit/automated_workflow/test_technical_output_2.mp4`
- 0.4 МиБ — `channels/paper_detour/videos/003_iq_gallery/Edit/automated_workflow/test_technical_output_3.mp4`
- 0.4 МиБ — `channels/paper_detour/videos/003_iq_gallery/Edit/automated_workflow/test_technical_output.mp4`
- 0.3 МиБ — `channels/paper_detour/videos/003_iq_gallery/Edit/automated_workflow/test_anchor_right_bottom_v2.mp4`
- 0.3 МиБ — `channels/paper_detour/videos/003_iq_gallery/Edit/automated_workflow/test_anchor_default_v2.mp4`
- 0.3 МиБ — `channels/paper_detour/videos/003_iq_gallery/Edit/automated_workflow/test_layer_offset_minus55.mp4`
- 0.3 МиБ — `channels/paper_detour/videos/003_iq_gallery/Edit/automated_workflow/test_mixed_dimensions.mp4`
- 0.3 МиБ — `channels/paper_detour/videos/003_iq_gallery/Edit/automated_workflow/test_grouped_mixed.mp4`
- 0.3 МиБ — `channels/paper_detour/videos/030_clothing_history/Edit/parallax_trial_20261102/scene_11.mp4`

### I — исходники и библиотека: сохранить — 38 видео, 3.67 ГиБ

- 497.6 МиБ — `channels/paper_detour/videos/007_joshua_jessica/Source/Graphics/film_grain_8s_prores4444.mov`
- 497.6 МиБ — `channels/paper_detour/videos/001_radio_game/Source/Graphics/film_grain_8s_prores4444.mov` — Palmier media.json: `channels/paper_detour/videos/001_radio_game/Rarovista_001.palmier/media.json`
- 497.6 МиБ — `channels/paper_detour/videos/009_knorozov_asya/Source/Graphics/film_grain_8s_prores4444.mov`
- 497.6 МиБ — `channels/paper_detour/videos/004_last_video/Edit/Automation/parallel_20261101/Assets/film_grain_8s_prores4444.mov`
- 495.9 МиБ — `channels/paper_detour/videos/001_radio_game/Shorts/02_decoder/Source/Graphics/director_trial_20261031/film_grain_vertical_8s_prores4444.mov`
- 159.8 МиБ — `channels/nuviko_stories/footages/xn-Ra65Ci10.mp4` — Palmier media.json: `channels/nuviko_stories/videos/001_brother_ex_best_friend/1.palmier/media.json`
- 152.8 МиБ — `channels/nuviko_stories/footages/DIPYcm3BRSA.mp4` — Palmier media.json: `channels/nuviko_stories/videos/001_brother_ex_best_friend/1.palmier/media.json`
- 148.1 МиБ — `channels/nuviko_stories/footages/mflCRjfK5Xk.mp4` — Palmier media.json: `channels/nuviko_stories/videos/001_brother_ex_best_friend/1.palmier/media.json`
- 145.8 МиБ — `channels/nuviko_stories/footages/VQl3NO_02Pc.mp4` — Palmier media.json: `channels/nuviko_stories/videos/001_brother_ex_best_friend/1.palmier/media.json`
- 109.3 МиБ — `channels/nuviko_stories/footages/yjNaP3rN47o.mp4` — Palmier media.json: `channels/nuviko_stories/videos/001_brother_ex_best_friend/1.palmier/media.json`
- 55.7 МиБ — `channels/nuviko_stories/videos/022_свадьба_сестры_в_подарок/Source/Broll/pexels/8257213.mp4`
- 53.8 МиБ — `channels/nuviko_stories/videos/022_свадьба_сестры_в_подарок/Source/Broll/pexels/9908107.mp4`
- 50.1 МиБ — `projects/borisenko/pilot_001/Source/К чему эти разговоры если гибнyт русские люди.mp4`
- 47.5 МиБ — `channels/nuviko_stories/videos/018_соседский_мальчик_назвал_меня_папой/Source/Broll/pexels/5703047.mp4`
- 39.2 МиБ — `channels/nuviko_stories/videos/022_свадьба_сестры_в_подарок/Source/Broll/pexels/9903485.mp4`
- 34.5 МиБ — `channels/nuviko_stories/videos/018_соседский_мальчик_назвал_меня_папой/Source/Broll/pexels/6693575.mp4`
- 32.7 МиБ — `channels/nuviko_stories/videos/018_соседский_мальчик_назвал_меня_папой/Source/Broll/pexels/6790430.mp4`
- 25.8 МиБ — `channels/nuviko_stories/videos/022_свадьба_сестры_в_подарок/Source/Broll/pexels/5536123.mp4`
- 25.7 МиБ — `channels/nuviko_stories/videos/018_соседский_мальчик_назвал_меня_папой/Source/Broll/pexels/8063956.mp4`
- 22.6 МиБ — `channels/nuviko_stories/videos/022_свадьба_сестры_в_подарок/Source/Broll/pexels/5977260.mp4`
- 20.9 МиБ — `channels/nuviko_stories/videos/022_свадьба_сестры_в_подарок/Source/Broll/pexels/6324567.mp4` — Palmier media.json: `channels/nuviko_stories/videos/001_brother_ex_best_friend/1.palmier/media.json`
- 18.8 МиБ — `channels/nuviko_stories/videos/018_соседский_мальчик_назвал_меня_папой/Source/Broll/pexels/7964887.mp4`
- 17.6 МиБ — `channels/nuviko_stories/videos/018_соседский_мальчик_назвал_меня_папой/Source/Broll/pexels/5758774.mp4`
- 17.1 МиБ — `channels/nuviko_stories/videos/022_свадьба_сестры_в_подарок/Source/Broll/pexels/6931246.mp4` — Palmier media.json: `channels/nuviko_stories/videos/001_brother_ex_best_friend/1.palmier/media.json`
- 12.4 МиБ — `channels/nuviko_stories/videos/022_свадьба_сестры_в_подарок/Source/Broll/pexels/8765271.mp4`
- 11.9 МиБ — `channels/nuviko_stories/videos/022_свадьба_сестры_в_подарок/Source/Broll/pexels/10238452.mp4` — Palmier media.json: `channels/nuviko_stories/videos/001_brother_ex_best_friend/1.palmier/media.json`
- 11.9 МиБ — `channels/nuviko_stories/videos/018_соседский_мальчик_назвал_меня_папой/Source/Broll/pexels/10238452.mp4`
- 11.9 МиБ — `channels/nuviko_stories/assets/broll/pexels/10238452.mp4`
- 10.7 МиБ — `channels/nuviko_stories/videos/022_свадьба_сестры_в_подарок/Source/Broll/pexels/6386551.mp4`
- 7.2 МиБ — `channels/nuviko_stories/videos/022_свадьба_сестры_в_подарок/Source/Broll/pexels/8247208.mp4`
- 6.8 МиБ — `channels/nuviko_stories/videos/018_соседский_мальчик_назвал_меня_папой/Source/Broll/pexels/11640552.mp4`
- 6.0 МиБ — `channels/nuviko_stories/videos/022_свадьба_сестры_в_подарок/Source/Broll/pexels/32054941.mp4` — Palmier media.json: `channels/nuviko_stories/videos/001_brother_ex_best_friend/1.palmier/media.json`
- 5.8 МиБ — `channels/nuviko_stories/videos/022_свадьба_сестры_в_подарок/Source/Broll/pexels/8246470.mp4`
- 5.4 МиБ — `channels/nuviko_stories/videos/022_свадьба_сестры_в_подарок/Source/Broll/pexels/8873334.mp4`
- 5.0 МиБ — `channels/nuviko_stories/videos/018_соседский_мальчик_назвал_меня_папой/Source/Broll/pexels/8478035.mp4`
- 0.7 МиБ — `channels/paper_detour/videos/003_iq_gallery/Source/Images/iq_gallery_type_fade_20261101/JFK_IQ119_Berlin_motorcade_fade_preview_v02.mp4`
- 0.7 МиБ — `channels/paper_detour/videos/003_iq_gallery/Source/Images/iq_gallery_type_fade_20261101/JFK_IQ119_Berlin_motorcade_fade_preview_v01.mp4`
- 0.6 МиБ — `channels/paper_detour/videos/003_iq_gallery/Source/Images/iq_gallery_type_fade_20261101/JFK_IQ119_type_fade_preview_v01.mp4`

### R — рябь и связанные материалы: сохранить для эксперимента — 9 видео, 1.20 ГиБ

- 354.3 МиБ — `channels/paper_detour/Shared/Overlays/CRT_Ripple/paper_crt_ripple_6x_15min_540x960_30fps_v01.mov` — Palmier media.json: `channels/paper_detour/videos/028_taj_mahal/Paper Detour 028 Taj Mahal Montage Draft 20261101.palmier/media.json`
- 334.5 МиБ — `channels/paper_detour/Shared/Overlays/CRT_Ripple/paper_crt_ripple_6x_15min_960x540_30fps_v01.mov`
- 244.1 МиБ — `channels/paper_detour/videos/030_clothing_history/Edit/v07/CRT_RIPPLE_X2_EXPERIMENT_EN_v07.mp4`
- 243.7 МиБ — `channels/paper_detour/videos/030_clothing_history/Edit/v07/Palmier_CRT_ripple_x2_native.mp4`
- 43.2 МиБ — `channels/paper_detour/videos/028_taj_mahal/Edit/Previews/028_en_v05_CRT_ripple_20261102.mp4`
- 3.2 МиБ — `channels/paper_detour/Shared/Overlays/CRT_Ripple/paper_crt_ripple_6x_8s_540x960_30fps_v01.mov`
- 3.0 МиБ — `channels/paper_detour/videos/001_radio_game/Source/Graphics/crt_soft_ripple_6x_8s_prores4444.mov` — Palmier media.json: `channels/paper_detour/videos/001_radio_game/Rarovista_001.palmier/media.json`
- 3.0 МиБ — `channels/paper_detour/videos/001_radio_game/Source/Graphics/crt_soft_ripple_8s_prores4444.mov` — Palmier media.json: `channels/paper_detour/videos/001_radio_game/Rarovista_001.palmier/media.json`
- 2.3 МиБ — `channels/paper_detour/videos/028_taj_mahal/Edit/Previews/028_CRT_ripple_visual_sample_4s.mp4`

### S — общий эффект: отдельно решить; проверить зависимости — 5 видео, 11.51 ГиБ

- 10.21 ГиБ — `channels/paper_detour/Shared/Overlays/Film_Grain/paper_film_grain_visible_15min_270x480_30fps_v01.mov` — Palmier media.json: `channels/paper_detour/videos/028_taj_mahal/Paper Detour 028 Taj Mahal Montage Draft 20261101.palmier/media.json`
- 497.6 МиБ — `channels/paper_detour/Shared/Overlays/Film_Grain/paper_film_grain_8s_960x540_30fps_prores4444_v01.mov`
- 372.1 МиБ — `channels/paper_detour/Shared/Overlays/Film_Grain/paper_film_grain_visible_8s_540x960_30fps_v01.mov`
- 369.4 МиБ — `channels/paper_detour/Shared/Overlays/Film_Grain/paper_fine_grain_8s_singletrack_540x960_30fps_v01.mov`
- 92.9 МиБ — `channels/paper_detour/Shared/Overlays/Film_Grain/paper_film_grain_visible_8s_270x480_30fps_v01.mov`

## Изображения: крупные накопления по папкам выпусков

Это исходники и рабочие изображения, не готовые видео; данные приведены для оценки и отдельного решения, не как разрешение удалить.

- `channels/paper_detour/videos/003_iq_gallery` — 1712 изображений, 1.31 ГиБ
- `channels/paper_detour/videos/004_last_video` — 771 изображений, 1.02 ГиБ
- `channels/paper_detour/videos/007_joshua_jessica` — 1035 изображений, 1021.1 МиБ
- `channels/nuviko_history/videos/017_galveston_1900` — 465 изображений, 934.2 МиБ
- `channels/paper_detour/videos/030_clothing_history` — 865 изображений, 870.0 МиБ
- `channels/nuviko_history/videos/009_black_death` — 262 изображений, 628.5 МиБ
- `channels/paper_detour/videos/001_radio_game` — 826 изображений, 594.5 МиБ
- `channels/paper_detour/videos/032_galveston_1900` — 423 изображений, 591.0 МиБ
- `channels/paper_detour/videos/027_doomscrolling_short` — 424 изображений, 542.6 МиБ
- `channels/paper_detour/videos/033_time_stop` — 431 изображений, 490.6 МиБ
- `channels/nuviko_history/videos/016_marseille_1720` — 193 изображений, 477.2 МиБ
- `channels/paper_detour/videos/031_jascon4_okene` — 281 изображений, 395.7 МиБ
- `channels/paper_detour/videos/028_taj_mahal` — 300 изображений, 316.4 МиБ
- `channels/paper_detour/videos/009_knorozov_asya` — 284 изображений, 306.8 МиБ
- `channels/paper_detour/videos/008_boyfriend_brought_friend` — 211 изображений, 295.9 МиБ
- `channels/paper_detour/videos/002_margorie_mccall` — 84 изображений, 139.2 МиБ
- `channels/paper_detour/videos/036_trinaxodon_broomistega` — 65 изображений, 107.8 МиБ
- `channels/paper_detour/brand` — 73 изображений, 97.4 МиБ
- `channels/paper_detour/legacy/025_iq_gallery` — 52 изображений, 97.0 МиБ
- `channels/paper_detour/experiments` — 51 изображений, 92.1 МиБ
- `.agent/experiments` — 30 изображений, 89.9 МиБ
- `channels/nuviko_history/videos/002_pompeii` — 50 изображений, 82.3 МиБ
- `channels/nuviko_stories/videos/021_семейный_ужин_сюрприз` — 237 изображений, 73.9 МиБ
- `channels/paper_detour/videos/035_mantis_shrimp_club` — 48 изображений, 56.0 МиБ
- `channels/paper_detour/legacy/027_doomscrolling_short` — 164 изображений, 50.5 МиБ
- `channels/nuviko_stories/videos/013_сестра_пришла_на_помолвку_в_свадебном_платье` — 363 изображений, 44.7 МиБ
- `channels/nuviko_history/videos/004_pompeii_short` — 26 изображений, 44.2 МиБ
- `channels/paper_detour/research` — 49 изображений, 42.8 МиБ
- `channels/paper_detour/videos/005_ai_future_of_work` — 30 изображений, 42.2 МиБ
- `archive/unclassified_episodes/023_margorie_mccall` — 108 изображений, 35.6 МиБ
- `channels/paper_detour/videos/006_herculaneum_scrolls` — 20 изображений, 25.0 МиБ
- `channels/nuviko_stories/videos/022_свадьба_сестры_в_подарок` — 60 изображений, 23.8 МиБ

## Остальные файлы от 20 МиБ

Для полноты: изображения, звук, архивы и прочие крупные файлы. Обычно их предлагается сохранить до отдельной проверки.

- 77.5 МиБ — `channels/nuviko_history/videos/017_galveston_1900/Source/Archive/Gresham_Highsmith_2012/LC-DIG-highsm-18754-original.tif` — I — исходники и библиотека: сохранить
- 76.1 МиБ — `channels/nuviko_history/videos/017_galveston_1900/Source/Archive/Gresham_Highsmith_2012/LC-DIG-highsm-18756-original.tif` — I — исходники и библиотека: сохранить
- 69.3 МиБ — `projects/borisenko/pilot_001/Deliverables/pilot_001_english_full_mix.wav` — E — аудио: сохранить
- 65.6 МиБ — `channels/paper_detour/videos/001_radio_game/Edit/publication_20261030/mix_candidate_no_sfx_20261031.wav` — E — аудио: сохранить
- 65.6 МиБ — `channels/paper_detour/videos/001_radio_game/Edit/publication_20261030/mix_candidate_pcm_voice_corrected_20261031.wav` — E — аудио: сохранить
- 65.6 МиБ — `channels/paper_detour/videos/001_radio_game/Edit/publication_20261030/mix_candidate.wav` — E — аудио: сохранить
- 65.6 МиБ — `channels/paper_detour/videos/001_radio_game/Edit/publication_20261030/mix_candidate_pcm_voice_unity_pan_20261031.wav` — E — аудио: сохранить
- 65.6 МиБ — `channels/paper_detour/videos/001_radio_game/Edit/publication_20261030/mix_candidate_pcm_voice_20261031.wav` — E — аудио: сохранить
- 65.6 МиБ — `channels/paper_detour/videos/001_radio_game/Edit/publication_20261030/mix_candidate_no_sfx_corrected_20261031.wav` — E — аудио: сохранить
- 59.5 МиБ — `channels/nuviko_history/videos/009_black_death/Source/Long/Voice/black_death_en_voice_105.wav` — I — исходники и библиотека: сохранить
- 56.3 МиБ — `channels/paper_detour/videos/009_knorozov_asya/Storyboard/Paper_Detour_009_Import_Kit.zip` — F — документация и прочие файлы: сохранить
- 55.7 МиБ — `projects/borisenko/pilot_001/Source/Maxim_Orlov_english_speed_095.wav` — I — исходники и библиотека: сохранить
- 52.2 МиБ — `channels/paper_detour/videos/030_clothing_history/Source/Audio/v05/full_mix.wav` — I — исходники и библиотека: сохранить
- 48.3 МиБ — `channels/nuviko_history/videos/017_galveston_1900/Source/Long/Voice/odom_voice_en_105.wav` — I — исходники и библиотека: сохранить
- 48.3 МиБ — `channels/nuviko_history/videos/017_galveston_1900/Source/Voice/odom_5vsg/film/voice_en_105.wav` — I — исходники и библиотека: сохранить
- 45.2 МиБ — `channels/nuviko_history/videos/016_marseille_1720/Source/Long/Voice/voice_en_105.wav` — I — исходники и библиотека: сохранить
- 45.2 МиБ — `channels/nuviko_history/videos/016_marseille_1720/Source/Voice/film/voice_en_105.wav` — I — исходники и библиотека: сохранить
- 43.8 МиБ — `channels/paper_detour/videos/001_radio_game/Source/Audio/paper_sound_design/music_bed_continuous_260s.wav` — I — исходники и библиотека: сохранить
- 41.9 МиБ — `channels/nuviko_history/videos/017_galveston_1900/Source/Voice/film/voice_en_105.wav` — I — исходники и библиотека: сохранить
- 30.2 МиБ — `channels/nuviko_history/videos/009_black_death/Edit/Long/VoiceCheck/part_01_105.wav` — E — аудио: сохранить
- 29.3 МиБ — `channels/nuviko_history/videos/009_black_death/Edit/Long/VoiceCheck/part_02_105.wav` — E — аудио: сохранить
- 23.0 МиБ — `channels/paper_detour/videos/001_radio_game/Source/Voice/v3/generated/voice_en.wav` — I — исходники и библиотека: сохранить
- 20.7 МиБ — `channels/nuviko_history/videos/002_pompeii/Source/Voice/ElevenLabs_At_first,_lightweight_white_stones_began_.mp3` — I — исходники и библиотека: сохранить

## Символьные ссылки

Ссылки не обходились; их цели могут лежать за пределами корня.

- `channels/paper_detour/.agents/skills` → `../../.agents/skills`
- `channels/paper_detour/videos/.agents/skills` → `../../../.agents/skills`
- `channels/paper_detour/videos/001_radio_game/.agents/skills` → `../../../../.agents/skills`
- `channels/paper_detour/videos/002_margorie_mccall/.agents/skills` → `../../../../.agents/skills`
- `channels/paper_detour/videos/003_iq_gallery/.agents/skills` → `../../../../.agents/skills`
- `channels/paper_detour/videos/004_last_video/.agents/skills` → `../../../../.agents/skills`
- `channels/paper_detour/videos/005_ai_future_of_work/.agents/skills` → `../../../../.agents/skills`
- `channels/paper_detour/videos/006_herculaneum_scrolls/.agents/skills` → `../../../../.agents/skills`
- `channels/paper_detour/videos/007_joshua_jessica/.agents/skills` → `../../../../.agents/skills`
- `channels/paper_detour/videos/008_boyfriend_brought_friend/.agents/skills` → `../../../../.agents/skills`
- `channels/paper_detour/videos/009_knorozov_asya/.agents/skills` → `../../../../.agents/skills`
- `channels/paper_detour/videos/010_smart_tv_surveillance/.agents/skills` → `../../../../.agents/skills`
- `channels/paper_detour/videos/027_doomscrolling_short/.agents/skills` → `../../../../.agents/skills`
- `channels/paper_detour/videos/028_taj_mahal/.agents/skills` → `../../../../.agents/skills`
- `channels/paper_detour/videos/030_clothing_history/.agents/skills` → `../../../../.agents/skills`
- `channels/paper_detour/videos/031_jascon4_okene/.agents/skills` → `../../../../.agents/skills`
- `channels/paper_detour/videos/032_galveston_1900/.agents/skills` → `../../../../.agents/skills`
- `channels/paper_detour/videos/033_time_stop/.agents/skills` → `../../../../.agents/skills`
- `channels/paper_detour/videos/034_zebra_stripes/.agents/skills` → `../../../../.agents/skills`
- `channels/paper_detour/videos/035_mantis_shrimp_club/.agents/skills` → `../../../../.agents/skills`
- `channels/paper_detour/videos/036_trinaxodon_broomistega/.agents/skills` → `../../../../.agents/skills`
- `archive/legacy_stories/.agents/skills` → `../../.agents/skills`
- `archive/legacy_stories/videos/.agents/skills` → `../../../.agents/skills`
- `channels/nuviko_stories/videos/001_brother_ex_best_friend/.agents/skills` → `../../../../.agents/skills`
- `channels/nuviko_history/videos/002_pompeii/.agents/skills` → `../../../../.agents/skills`
- `archive/unclassified_episodes/003` → `003_gus`
- `archive/unclassified_episodes/003_gus/.agents/skills` → `../../../../.agents/skills`
- `channels/nuviko_history/videos/004_pompeii_short/.agents/skills` → `../../../../.agents/skills`
- `channels/nuviko_history/videos/009_black_death/.agents/skills` → `../../../../.agents/skills`
- `channels/nuviko_stories/videos/011_парень_приводил_друга_на_каждое_свидание/.agents/skills` → `../../../../.agents/skills`
- `channels/nuviko_stories/videos/012_дорогой_подарок_оказался_семейной_реликвией/.agents/skills` → `../../../../.agents/skills`
- `channels/nuviko_stories/videos/013_сестра_пришла_на_помолвку_в_свадебном_платье/.agents/skills` → `../../../../.agents/skills`
- `channels/nuviko_stories/videos/014_подарок_парню_и_незнакомец_с_книгами_толкина/.agents/skills` → `../../../../.agents/skills`
- `channels/nuviko_stories/videos/015_девушка_моего_брата_приревновала_его_ко_мне/.agents/skills` → `../../../../.agents/skills`
- `channels/nuviko_history/videos/016_marseille_1720/.agents/skills` → `../../../../.agents/skills`
- `channels/nuviko_history/videos/017_galveston_1900/.agents/skills` → `../../../../.agents/skills`
- `channels/nuviko_stories/videos/018_соседский_мальчик_назвал_меня_папой/.agents/skills` → `../../../../.agents/skills`
- `channels/nuviko_stories/videos/019_торт_с_чужим_именем/.agents/skills` → `../../../../.agents/skills`
- `channels/paper_detour/legacy/020_rarovista_radio_game/.agents/skills` → `../../../../.agents/skills`
- `channels/nuviko_stories/videos/021_семейный_ужин_сюрприз/.agents/skills` → `../../../../.agents/skills`
- `channels/nuviko_stories/videos/022_свадьба_сестры_в_подарок/.agents/skills` → `../../../../.agents/skills`
- `archive/unclassified_episodes/023_margorie_mccall/.agents/skills` → `../../../../.agents/skills`
- `channels/paper_detour/legacy/024_margorie_mccall_paper_detour/.agents/skills` → `../../../../.agents/skills`
- `channels/paper_detour/legacy/025_iq_gallery/.agents/skills` → `../../../../.agents/skills`
- `channels/nuviko_history/videos/026_doomscrolling_history/.agents/skills` → `../../../../.agents/skills`
- `channels/paper_detour/legacy/027_doomscrolling_short/.agents/skills` → `../../../../.agents/skills`
- `archive/unclassified_episodes/028_drug_policy/.agents/skills` → `../../../../.agents/skills`
- `channels/paper_detour/legacy/029_paper_last_video/.agents/skills` → `../../../../.agents/skills`
- `channels/nuviko_history/videos/035_when_wages_rose/.agents/skills` → `../../../../.agents/skills`
- `channels/nuviko_stories/videos/1` → `001_brother_ex_best_friend`
- `channels/nuviko_history/videos/2` → `002_pompeii`

Ошибок обхода не зарегистрировано.
