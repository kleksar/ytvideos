# Инвентаризация Stories/videos для согласования очистки

Дата: 2026-11-02. Ничего из перечисленного не удалено в рамках этой инвентаризации.

Корень: `/Users/diplomat/ytvideos/archive/legacy_stories/videos`. Рекурсивно перечислены все обнаруженные обычные видеофайлы; символьные ссылки и содержимое пакетов .palmier не обходились. Размеры номинальные: клоны APFS могут делить блоки, поэтому сумма не гарантирует освобождение такого же места.

## Как устроены материалы и как читать список

`Source` содержит изображения, озвучку и другие исходники. `Edit` содержит манифесты, данные монтажа и рендеры отдельных слоёв; MOV может быть подключён к таймлайну. `Deliverables` содержит выдачу, в том числе вложенную в `Shorts/<эпизод>/Deliverables`. Сценарии, SRT, журналы, проекты и исходники предлагается оставить. Проверка реальных ссылок во всех проектах Palmier и возможность повторного рендера не выполнены; упоминания в локальных документах могут быть историческими.

009: пять MP4 согласно README были загружены, API-статус зафиксирован 29 октября; актуальная проверка YouTube не выполнялась. Ранее удалили финал полного фильма, но не прошли вложенные Shorts — именно поэтому пять файлов остались.

025 v19 фигурирует как audio reference в манифесте нового Paper-проекта; 020 MP4 указан как APFS-клон внешнего файла. Это не доказательство безопасного удаления или количества высвобождаемого места. Эффект ряби исключён из предложений по прямому указанию пользователя.

## Итоги по группам

- **A. 009 Shorts — готовые MP4, предложение удалить после согласования**: 5 файлов, 249.9 МиБ.
- **B. 009 Shorts — MOV слои, решение отдельно после проверки восстановления**: 16 файлов, 1 912.6 МиБ.
- **C. Остальные MP4 и видео в Deliverables — кандидаты, проверить назначение и загрузку**: 24 файлов, 1 776.8 МиБ.
- **D. Другие MOV — возможные титры или исходные слои; решение отдельно**: 51 файлов, 6 871.2 МиБ.
- **E. Видео в Source — сохранить, возможные исходники**: 23 файлов, 494.8 МиБ.
- **F. Видео в Edit и других каталогах — кандидаты только после проверки назначения**: 11 файлов, 154.4 МиБ.

Всего перечислено: 130 видеофайлов, 11 459.6 МиБ. Группы E и D содержат материалы, которые нельзя считать готовыми роликами.

## Выпуски: номинальный размер перечисленных видео

- `017_galveston_1900` — 25 видео, 2 241.6 МиБ
- `009_black_death` — 21 видео, 2 162.4 МиБ
- `018_соседский_мальчик_назвал_меня_папой` — 16 видео, 1 617.0 МиБ
- `016_marseille_1720` — 15 видео, 1 059.4 МиБ
- `012_дорогой_подарок_оказался_семейной_реликвией` — 3 видео, 970.3 МиБ
- `011_парень_приводил_друга_на_каждое_свидание` — 2 видео, 640.3 МиБ
- `022_свадьба_сестры_в_подарок` — 16 видео, 444.7 МиБ
- `004_pompeii_short` — 4 видео, 421.5 МиБ
- `019_торт_с_чужим_именем` — 3 видео, 379.8 МиБ
- `020_rarovista_radio_game` — 5 видео, 359.8 МиБ
- `025_iq_gallery` — 3 видео, 246.7 МиБ
- `003_gus` — 2 видео, 245.4 МиБ
- `024_margorie_mccall_paper_detour` — 2 видео, 197.2 МиБ
- `015_девушка_моего_брата_приревновала_его_ко_мне` — 1 видео, 194.2 МиБ
- `023_margorie_mccall` — 1 видео, 119.4 МиБ
- `021_семейный_ужин_сюрприз` — 1 видео, 86.9 МиБ
- `027_doomscrolling_short` — 9 видео, 36.8 МиБ
- `029_paper_last_video` — 1 видео, 36.3 МиБ

## A. 009 Shorts — готовые MP4, предложение удалить после согласования

Пути относительно `archive/legacy_stories/videos/`; порядок — от большего размера к меньшему. Упоминание в JSON/MD — указатель для ручной проверки, а не подтверждение активного использования.

- 53.8 МиБ — `009_black_death/Shorts/02_trade_routes/Deliverables/009_en_black_death_02_shorts_105_v2.mp4` — упомянут: `009_black_death/README.md`, `009_black_death/Edit/cleanup_2026-10-29_intermediate_caption_mov.json` и ещё 1
- 53.8 МиБ — `009_black_death/Shorts/05_labour/Deliverables/009_en_black_death_05_shorts_105_v2.mp4` — упомянут: `009_black_death/README.md`, `009_black_death/Edit/cleanup_2026-10-29_intermediate_caption_mov.json` и ещё 1
- 49.9 МиБ — `009_black_death/Shorts/01_intro/Deliverables/009_en_black_death_01_shorts_105.mp4` — упомянут: `009_black_death/README.md`, `009_black_death/Edit/cleanup_2026-10-29_intermediate_caption_mov.json` и ещё 1
- 48.2 МиБ — `009_black_death/Shorts/04_quarantine/Deliverables/009_en_black_death_04_shorts_105_v2.mp4` — упомянут: `009_black_death/README.md`, `009_black_death/Edit/cleanup_2026-10-29_intermediate_caption_mov.json` и ещё 1
- 44.2 МиБ — `009_black_death/Shorts/03_coins/Deliverables/009_en_black_death_03_shorts_105_v2.mp4` — упомянут: `009_black_death/README.md`, `009_black_death/Edit/cleanup_2026-10-29_intermediate_caption_mov.json` и ещё 2

## B. 009 Shorts — MOV слои, решение отдельно после проверки восстановления

Пути относительно `archive/legacy_stories/videos/`; порядок — от большего размера к меньшему. Упоминание в JSON/MD — указатель для ручной проверки, а не подтверждение активного использования.

- 137.4 МиБ — `009_black_death/Shorts/02_trade_routes/Edit/Captions/02_en_caption_overlay_safe.mov` — упомянут: `009_black_death/Edit/shorts_captions_notes.md`, `009_black_death/Shorts/02_trade_routes/Edit/manifest.before_photo_v3.json` и ещё 4
- 131.0 МиБ — `009_black_death/Shorts/05_labour/Edit/Captions/05_en_caption_overlay_face_safe.mov` — упомянут: `009_black_death/Shorts/05_labour/Edit/manifest.before_photo_v3.json`, `009_black_death/Shorts/05_labour/Edit/palmier_receipt.json` и ещё 1
- 130.0 МиБ — `009_black_death/Shorts/02_trade_routes/Edit/Speed105/Captions/02_en_caption_overlay_105.mov` — упомянут: `009_black_death/Shorts/02_trade_routes/Edit/palmier_receipt_105.json`
- 128.8 МиБ — `009_black_death/Shorts/02_trade_routes/Edit/Speed105/Captions/02_en_caption_overlay_105_v2.mov` — упомянут: `009_black_death/Shorts/02_trade_routes/Edit/manifest_105.json`, `009_black_death/Shorts/02_trade_routes/Edit/revision_receipt_105.json`
- 123.9 МиБ — `009_black_death/Shorts/05_labour/Edit/Speed105/Captions/05_en_caption_overlay_105.mov` — упомянут: `009_black_death/Shorts/05_labour/Edit/palmier_receipt_105.json`
- 123.1 МиБ — `009_black_death/Shorts/05_labour/Edit/Speed105/Captions/05_en_caption_overlay_105_v2.mov` — упомянут: `009_black_death/Shorts/05_labour/Edit/manifest_105.json`, `009_black_death/Shorts/05_labour/Edit/revision_receipt_105.json`
- 118.0 МиБ — `009_black_death/Shorts/04_quarantine/Edit/Captions/04_en_caption_overlay_safe.mov` — упомянут: `009_black_death/Edit/shorts_captions_notes.md`, `009_black_death/Shorts/04_quarantine/Edit/manifest.before_photo_v3.json` и ещё 2
- 117.7 МиБ — `009_black_death/Shorts/04_quarantine/Edit/Captions/04_en_caption_overlay.mov` — упомянут: `016_marseille_1720/Edit/cleanup_016_intermediate_2026-10-29.json`
- 117.1 МиБ — `009_black_death/Shorts/01_intro/Edit/Captions/01_en_caption_overlay_safe.mov` — упомянут: `009_black_death/Edit/shorts_captions_notes.md`, `009_black_death/Shorts/01_intro/Edit/palmier_receipt_105.json` и ещё 5
- 117.0 МиБ — `009_black_death/Shorts/01_intro/Edit/Captions/01_en_caption_overlay_photo_safe_v2.mov` — упомянут: `009_black_death/Edit/shorts_captions_notes.md`, `009_black_death/Shorts/01_intro/Edit/manifest.json`
- 113.0 МиБ — `009_black_death/Shorts/03_coins/Edit/Captions/03_en_caption_overlay_photo_safe.mov` — упомянут: `009_black_death/Edit/shorts_captions_notes.md`, `009_black_death/Shorts/03_coins/Edit/manifest.json`
- 112.5 МиБ — `009_black_death/Shorts/03_coins/Edit/Captions/03_en_caption_overlay.mov` — упомянут: `016_marseille_1720/Edit/cleanup_016_intermediate_2026-10-29.json`
- 112.3 МиБ — `009_black_death/Shorts/03_coins/Edit/Captions/03_en_caption_overlay_face_safe.mov` — упомянут: `009_black_death/Shorts/03_coins/Edit/palmier_receipt.json`, `009_black_death/Shorts/03_coins/Edit/manifest_illustrated_previous.json`
- 111.7 МиБ — `009_black_death/Shorts/01_intro/Edit/Speed105/Captions/01_en_caption_overlay_safe.mov` — упомянут: `009_black_death/Edit/shorts_captions_notes.md`, `009_black_death/Shorts/01_intro/Edit/palmier_receipt_105.json` и ещё 5
- 111.5 МиБ — `009_black_death/Shorts/04_quarantine/Edit/Speed105/Captions/04_en_caption_overlay_105.mov` — упомянут: `009_black_death/Shorts/04_quarantine/Edit/palmier_receipt_105.json`, `009_black_death/Shorts/04_quarantine/Edit/manifest_105.json`
- 107.7 МиБ — `009_black_death/Shorts/03_coins/Edit/Speed105/Captions/03_en_caption_overlay_safe_v2.mov` — упомянут: `009_black_death/Shorts/03_coins/Edit/palmier_receipt_105.json`, `009_black_death/Shorts/03_coins/Edit/manifest_105.json` и ещё 2

## C. Остальные MP4 и видео в Deliverables — кандидаты, проверить назначение и загрузку

Пути относительно `archive/legacy_stories/videos/`; порядок — от большего размера к меньшему. Упоминание в JSON/MD — указатель для ручной проверки, а не подтверждение активного использования.

- 227.2 МиБ — `020_rarovista_radio_game/Deliverables/020_en_long_radio_game.mp4` — упомянут: `020_rarovista_radio_game/020_EN_LONG_VERIFICATION.md`; задокументирован APFS-клон другого файла
- 194.2 МиБ — `015_девушка_моего_брата_приревновала_его_ко_мне/Deliverables/015_ru_shorts_110_audio192.mp4` — упомянут: `015_девушка_моего_брата_приревновала_его_ко_мне/AGENTS_STATUS_20261101.md`, `015_девушка_моего_брата_приревновала_его_ко_мне/README.md` и ещё 2
- 132.8 МиБ — `003_gus/Deliverables/003_ru_shorts_v2.mp4` — упомянут: `003_gus/README.md`
- 122.7 МиБ — `025_iq_gallery/Deliverables/archive/025_iq_gallery_paper_detour_60s_v18_linear_fade_candidate.mp4`
- 120.3 МиБ — `025_iq_gallery/Deliverables/025_iq_gallery_paper_detour_60s_v19.mp4` — упомянут: `025_iq_gallery/README.md`, `025_iq_gallery/Deliverables/025_iq_gallery_paper_detour_60s_v19.mp4.report.json`; ссылка как audio reference в channels/paper_detour/videos/003_iq_gallery/Edit/automated_workflow/iq_gallery_v24_manifest.json
- 112.7 МиБ — `003_gus/Deliverables/003_en_shorts_v2.mp4` — упомянут: `003_gus/README.md`
- 98.6 МиБ — `024_margorie_mccall_paper_detour/Deliverables/002_en_margorie_mccall_paper_accents_audio320.mp4`
- 98.6 МиБ — `024_margorie_mccall_paper_detour/Deliverables/002_en_margorie_mccall_paper_epitaph_audio320.mp4`
- 53.9 МиБ — `016_marseille_1720/Deliverables/016_en_marseille_04_shorts_audio192.mp4` — упомянут: `016_marseille_1720/README.md`
- 53.2 МиБ — `016_marseille_1720/Deliverables/016_en_marseille_04_shorts_palmier.mp4` — упомянут: `016_marseille_1720/Edit/Shorts/04_manifest_palmier_receipt_export.json`
- 50.3 МиБ — `016_marseille_1720/Deliverables/016_en_marseille_01_shorts_audio192.mp4`
- 50.3 МиБ — `016_marseille_1720/Deliverables/016_en_marseille_01_shorts_caption_safe_v2_audio192.mp4`
- 49.8 МиБ — `016_marseille_1720/Deliverables/016_en_marseille_01_shorts_palmier.mp4` — упомянут: `016_marseille_1720/Edit/Shorts/01_manifest_palmier_receipt_export.json`
- 49.7 МиБ — `016_marseille_1720/Deliverables/016_en_marseille_01_shorts_caption_safe_v2_palmier.mp4` — упомянут: `016_marseille_1720/Edit/Shorts/01_manifest_caption_safe_v2_palmier_receipt_export.json`
- 49.4 МиБ — `016_marseille_1720/Deliverables/016_en_marseille_03_shorts_audio192.mp4` — упомянут: `016_marseille_1720/Edit/YouTube/short_03_upload_verification.json`
- 48.8 МиБ — `016_marseille_1720/Deliverables/016_en_marseille_03_shorts_palmier.mp4` — упомянут: `016_marseille_1720/Edit/Shorts/03_manifest_palmier_receipt_export.json`
- 47.1 МиБ — `020_rarovista_radio_game/Deliverables/02_decoder_more_accents_20261031.mp4`
- 46.2 МиБ — `016_marseille_1720/Deliverables/016_en_marseille_02_shorts_audio192.mp4`
- 45.7 МиБ — `016_marseille_1720/Deliverables/016_en_marseille_02_shorts_palmier.mp4` — упомянут: `016_marseille_1720/Edit/Shorts/02_manifest_palmier_receipt_export.json`
- 37.8 МиБ — `020_rarovista_radio_game/Deliverables/001_short_01_fullgrain_audio320_20261031.mp4` — упомянут: `027_doomscrolling_short/Edit/PaperDetour_rework/TEXT_SCORE.md`
- 36.3 МиБ — `029_paper_last_video/Deliverables/004_en_last_video_v5_constant_grain_20261101.mp4`
- 24.3 МиБ — `020_rarovista_radio_game/Deliverables/03_stereo_text_en_shorts_v2.mp4` — упомянут: `020_rarovista_radio_game/Edit/SHORTS_RENDER_PRO_V2.md`, `020_rarovista_radio_game/Deliverables/03_stereo_text_en_shorts_v2.verification.json`
- 23.5 МиБ — `020_rarovista_radio_game/Deliverables/02_decoder_en_shorts_v2.mp4` — упомянут: `020_rarovista_radio_game/Edit/SHORTS_RENDER_PRO_V2.md`, `020_rarovista_radio_game/Deliverables/02_decoder_en_shorts_v2.verification.json`
- 3.6 МиБ — `025_iq_gallery/Deliverables/025_iq_gallery_en_preview_v2.mp4` — упомянут: `025_iq_gallery/README.md`

## D. Другие MOV — возможные титры или исходные слои; решение отдельно

Пути относительно `archive/legacy_stories/videos/`; порядок — от большего размера к меньшему. Упоминание в JSON/MD — указатель для ручной проверки, а не подтверждение активного использования.

- 378.7 МиБ — `012_дорогой_подарок_оказался_семейной_реликвией/Edit/Captions/012_ru_caption_overlay_110.mov` — упомянут: `012_дорогой_подарок_оказался_семейной_реликвией/Edit/palmier_receipt.json`, `012_дорогой_подарок_оказался_семейной_реликвией/Edit/verification.md`
- 372.9 МиБ — `011_парень_приводил_друга_на_каждое_свидание/Edit/Captions/011_ru_caption_overlay.mov`
- 299.0 МиБ — `012_дорогой_подарок_оказался_семейной_реликвией/Edit/Captions/012_en_caption_overlay_110.mov` — упомянут: `012_дорогой_подарок_оказался_семейной_реликвией/Edit/palmier_receipt_en.json`
- 293.3 МиБ — `019_торт_с_чужим_именем/Edit/Captions/ru_pulse_overlay_019_v3.mov` — упомянут: `019_торт_с_чужим_именем/README.md`, `019_торт_с_чужим_именем/Edit/019_ru_caption_install_receipt.json` и ещё 1
- 292.6 МиБ — `012_дорогой_подарок_оказался_семейной_реликвией/Edit/Captions/012_en_caption_overlay_110_89px.mov` — упомянут: `012_дорогой_подарок_оказался_семейной_реликвией/Edit/palmier_receipt_en.json`, `012_дорогой_подарок_оказался_семейной_реликвией/Edit/verification_en.md`
- 267.3 МиБ — `011_парень_приводил_друга_на_каждое_свидание/Edit/Captions/011_en_caption_overlay_110_89px.mov` — упомянут: `011_парень_приводил_друга_на_каждое_свидание/Edit/palmier_receipt_en.json`, `011_парень_приводил_друга_на_каждое_свидание/Edit/verification_en.md`
- 245.9 МиБ — `018_соседский_мальчик_назвал_меня_папой/Edit/Captions/ru_pulse_overlay_018.mov` — упомянут: `018_соседский_мальчик_назвал_меня_папой/Edit/018_ru_caption_import_receipt.json`, `018_соседский_мальчик_назвал_меня_папой/Edit/Captions/ru_pulse_overlay_018.mov.json`
- 244.3 МиБ — `018_соседский_мальчик_назвал_меня_папой/Edit/Captions/ru_pulse_overlay_018_v2.mov` — упомянут: `018_соседский_мальчик_назвал_меня_папой/Edit/Captions/ru_pulse_overlay_018_v2.mov.json`
- 244.3 МиБ — `018_соседский_мальчик_назвал_меня_папой/Edit/Captions/ru_pulse_overlay_018_v3.mov` — упомянут: `018_соседский_мальчик_назвал_меня_папой/Edit/018_ru_caption_v3_install_receipt.json`, `018_соседский_мальчик_назвал_меня_папой/Edit/018_ru_montage_qa.md` и ещё 1
- 215.0 МиБ — `018_соседский_мальчик_назвал_меня_папой/Edit/EN_Final/018_en_captions_110_prores.mov` — упомянут: `018_соседский_мальчик_назвал_меня_папой/Edit/018_en_montage_qa.md`
- 210.8 МиБ — `018_соседский_мальчик_назвал_меня_папой/Edit/EN_SafeDraft/018_en_captions_dynamic.mov` — упомянут: `018_соседский_мальчик_назвал_меня_папой/Edit/018_en_montage_qa.md`, `018_соседский_мальчик_назвал_меня_папой/Edit/EN_SafeDraft/018_en_safe_v2_palmier_receipt.json`
- 208.3 МиБ — `018_соседский_мальчик_назвал_меня_папой/Edit/EN_SafeDraft/018_en_captions_safe_draft.mov`
- 138.8 МиБ — `004_pompeii_short/Edit/Captions/004_en_v3_caption_overlay.mov` — упомянут: `004_pompeii_short/README.md`
- 138.4 МиБ — `004_pompeii_short/Edit/Captions/004_en_v2_caption_overlay.mov`
- 120.4 МиБ — `016_marseille_1720/Shorts/04_marseille/Edit/Captions/04_en_caption_overlay_safe_v2.mov` — упомянут: `016_marseille_1720/Edit/Shorts/04_manifest.json`, `016_marseille_1720/Edit/Shorts/04_manifest_palmier_receipt.json`
- 119.4 МиБ — `023_margorie_mccall/Edit/023_v6_caption_source_prores4444.mov` — упомянут: `023_margorie_mccall/README.md`, `023_margorie_mccall/Edit/render_plan_023_actual.json`
- 115.0 МиБ — `016_marseille_1720/Shorts/03_marseille/Edit/Captions/03_en_caption_overlay_safe_v2.mov` — упомянут: `009_black_death/Shorts/03_coins/Edit/palmier_receipt_105.json`, `009_black_death/Shorts/03_coins/Edit/manifest_105.json` и ещё 2
- 110.1 МиБ — `017_galveston_1900/Edit/Captions/02_en_caption_overlay_odom.mov` — упомянут: `017_galveston_1900/Edit/Shorts/02_manifest_odom_pre_restart_20261029.json`, `017_galveston_1900/Edit/Shorts/02_manifest_odom_draft.json`
- 109.4 МиБ — `017_galveston_1900/Edit/Captions/02_en_caption_overlay_odom_restart_20261029.mov` — упомянут: `017_galveston_1900/Edit/Shorts/02_manifest_palmier_receipt.json`, `017_galveston_1900/Edit/Shorts/02_manifest.json` и ещё 1
- 109.2 МиБ — `016_marseille_1720/Shorts/01_marseille/Edit/Captions/01_en_caption_overlay_safe.mov` — упомянут: `009_black_death/Edit/shorts_captions_notes.md`, `009_black_death/Shorts/01_intro/Edit/palmier_receipt_105.json` и ещё 5
- 109.2 МиБ — `016_marseille_1720/Shorts/01_marseille/Edit/Captions/01_en_caption_overlay_safe_v2.mov` — упомянут: `016_marseille_1720/Edit/Shorts/01_manifest_caption_safe_v2_palmier_receipt.json`, `016_marseille_1720/Edit/Shorts/01_manifest_caption_safe_v2.json`
- 108.4 МиБ — `016_marseille_1720/Shorts/02_marseille/Edit/Captions/02_en_caption_overlay_safe.mov` — упомянут: `009_black_death/Edit/shorts_captions_notes.md`, `009_black_death/Shorts/02_trade_routes/Edit/manifest.before_photo_v3.json` и ещё 4
- 104.4 МиБ — `017_galveston_1900/Edit/Captions/04_en_caption_overlay_odom.mov` — упомянут: `017_galveston_1900/Edit/Shorts/04_manifest_odom_draft.json`, `017_galveston_1900/Edit/Shorts/04_manifest_odom_pre_restart_20261029.json`
- 103.6 МиБ — `017_galveston_1900/Edit/Captions/04_en_caption_overlay_odom_restart_20261029.mov` — упомянут: `017_galveston_1900/Edit/Shorts/04_manifest_odom_draft.json`, `017_galveston_1900/Edit/Shorts/04_manifest_assembly_placeholders_palmier_receipt.json` и ещё 2
- 101.9 МиБ — `017_galveston_1900/Edit/Captions/03_en_caption_overlay_odom.mov` — упомянут: `017_galveston_1900/Edit/Shorts/03_manifest_odom_pre_restart_20261029.json`, `017_galveston_1900/Edit/Shorts/03_manifest_odom_draft.json`
- 101.5 МиБ — `017_galveston_1900/Edit/Captions/01_en_caption_overlay_odom.mov` — упомянут: `017_galveston_1900/Edit/Voice/ODOM_VOICE_QA.md`, `017_galveston_1900/Edit/Shorts/01_manifest_palmier_receipt.json` и ещё 4
- 101.3 МиБ — `017_galveston_1900/Edit/Captions/03_en_caption_overlay_odom_shot1safe_v3.mov` — упомянут: `017_galveston_1900/Edit/Shorts/03_manifest_v3_palmier_receipt.json`, `017_galveston_1900/Edit/Shorts/03_manifest_v3.json`
- 101.3 МиБ — `017_galveston_1900/Edit/Captions/03_en_caption_overlay_odom_restart_20261029.mov` — упомянут: `017_galveston_1900/Edit/Shorts/03_manifest.json`, `017_galveston_1900/Edit/Shorts/03_manifest_palmier_receipt.json` и ещё 3
- 99.4 МиБ — `017_galveston_1900/Edit/Captions/05_en_caption_overlay_odom.mov` — упомянут: `017_galveston_1900/Edit/Voice/ODOM_VOICE_QA.md`, `017_galveston_1900/Edit/Shorts/05_manifest_odom_pre_restart_20261029.json` и ещё 1
- 98.8 МиБ — `017_galveston_1900/Edit/Captions/05_en_caption_overlay_odom_restart_20261029.mov` — упомянут: `017_galveston_1900/Edit/Shorts/05_manifest_odom_draft.json`, `017_galveston_1900/Edit/Shorts/05_manifest_palmier_receipt.json` и ещё 1
- 97.3 МиБ — `017_galveston_1900/Edit/Captions/02_en_caption_overlay_odom_scene_repositioned.mov`
- 96.7 МиБ — `017_galveston_1900/Edit/Captions/02_en_caption_overlay_v2.mov` — упомянут: `017_galveston_1900/Edit/Shorts/02_manifest_draft.json`
- 96.4 МиБ — `017_galveston_1900/Edit/Captions/02_en_caption_overlay.mov` — упомянут: `009_black_death/Edit/cleanup_2026-10-29_intermediate_caption_mov.json`, `016_marseille_1720/Edit/cleanup_016_intermediate_2026-10-29.json`
- 92.7 МиБ — `022_свадьба_сестры_в_подарок/Edit/Captions/022_canonical_overlay.mov` — упомянут: `022_свадьба_сестры_в_подарок/Edit/render-plan.json`, `022_свадьба_сестры_в_подарок/Edit/render-plan-unverified-source-draft.json` и ещё 4
- 90.1 МиБ — `017_galveston_1900/Edit/Captions/01_en_caption_overlay.mov` — упомянут: `009_black_death/Edit/shorts_captions_notes.md`, `009_black_death/Edit/cleanup_2026-10-29_intermediate_caption_mov.json` и ещё 1
- 88.4 МиБ — `017_galveston_1900/Edit/Captions/05_en_caption_overlay_v2.mov` — упомянут: `017_galveston_1900/Edit/Captions/QA.md`, `017_galveston_1900/Edit/Shorts/05_manifest_draft.json`
- 88.3 МиБ — `017_galveston_1900/Edit/Captions/05_en_caption_overlay.mov` — упомянут: `009_black_death/Edit/cleanup_2026-10-29_intermediate_caption_mov.json`
- 87.5 МиБ — `017_galveston_1900/Edit/Captions/04_en_caption_overlay.mov` — упомянут: `016_marseille_1720/Edit/cleanup_016_intermediate_2026-10-29.json`
- 87.3 МиБ — `017_galveston_1900/Edit/Captions/01_en_caption_overlay_v2.mov` — упомянут: `017_galveston_1900/Edit/Captions/QA.md`, `017_galveston_1900/Edit/Shorts/01_manifest_draft.json`
- 87.0 МиБ — `017_galveston_1900/Edit/Captions/04_en_caption_overlay_v2.mov` — упомянут: `017_galveston_1900/Edit/Shorts/04_manifest_draft.json`
- 86.9 МиБ — `021_семейный_ужин_сюрприз/Edit/Captions/021_canonical_overlay.mov` — упомянут: `021_семейный_ужин_сюрприз/Edit/021_canonical_assembly_receipt.json`, `021_семейный_ужин_сюрприз/Edit/render-plan.json` и ещё 2
- 85.2 МиБ — `017_galveston_1900/Edit/Captions/03_en_caption_overlay.mov` — упомянут: `016_marseille_1720/Edit/cleanup_016_intermediate_2026-10-29.json`
- 84.4 МиБ — `004_pompeii_short/Edit/Captions/004_en_caption_overlay.mov`
- 83.9 МиБ — `017_galveston_1900/Edit/Captions/03_en_caption_overlay_v2.mov` — упомянут: `017_galveston_1900/Edit/Shorts/03_manifest_draft.json`
- 78.8 МиБ — `017_galveston_1900/Edit/Captions/03_en_caption_overlay_odom_scene_repositioned.mov`
- 74.3 МиБ — `017_galveston_1900/Edit/Captions/05_en_caption_overlay_odom_scene_repositioned.mov`
- 48.0 МиБ — `018_соседский_мальчик_назвал_меня_папой/Edit/EN_Final/018_en_captions_110.mov` — упомянут: `018_соседский_мальчик_назвал_меня_папой/Edit/018_en_montage_qa.md`
- 46.3 МиБ — `019_торт_с_чужим_именем/Edit/Captions/ru_pulse_overlay_019_v2.mov` — упомянут: `019_торт_с_чужим_именем/Edit/Captions/ru_pulse_overlay_019_v2.mov.json`
- 40.3 МиБ — `019_торт_с_чужим_именем/Edit/Captions/ru_pulse_overlay_019.mov` — упомянут: `019_торт_с_чужим_именем/Edit/Captions/ru_pulse_overlay_019.mov.json`
- 36.7 МиБ — `017_galveston_1900/Edit/Captions/04_en_caption_overlay_odom_scene_repositioned_interrupted.mov`
- 32.0 МиБ — `017_galveston_1900/Edit/Captions/04_en_caption_overlay_odom_scene_repositioned.mov`

## E. Видео в Source — сохранить, возможные исходники

Пути относительно `archive/legacy_stories/videos/`; порядок — от большего размера к меньшему. Упоминание в JSON/MD — указатель для ручной проверки, а не подтверждение активного использования.

- 55.7 МиБ — `022_свадьба_сестры_в_подарок/Source/Broll/pexels/8257213.mp4`
- 53.8 МиБ — `022_свадьба_сестры_в_подарок/Source/Broll/pexels/9908107.mp4`
- 47.5 МиБ — `018_соседский_мальчик_назвал_меня_папой/Source/Broll/pexels/5703047.mp4` — упомянут: `018_соседский_мальчик_назвал_меня_папой/Source/Broll/pexels/manifest.json`, `018_соседский_мальчик_назвал_меня_папой/Edit/018_en_broll_imports.json` и ещё 5
- 39.2 МиБ — `022_свадьба_сестры_в_подарок/Source/Broll/pexels/9903485.mp4`
- 34.5 МиБ — `018_соседский_мальчик_назвал_меня_папой/Source/Broll/pexels/6693575.mp4` — упомянут: `018_соседский_мальчик_назвал_меня_папой/Source/Broll/pexels/manifest.json`, `018_соседский_мальчик_назвал_меня_папой/Edit/018_en_broll_imports.json` и ещё 5
- 32.7 МиБ — `018_соседский_мальчик_назвал_меня_папой/Source/Broll/pexels/6790430.mp4` — упомянут: `018_соседский_мальчик_назвал_меня_папой/Source/Broll/pexels/manifest.json`, `018_соседский_мальчик_назвал_меня_папой/Edit/018_en_broll_imports.json` и ещё 11
- 25.8 МиБ — `022_свадьба_сестры_в_подарок/Source/Broll/pexels/5536123.mp4`
- 25.7 МиБ — `018_соседский_мальчик_назвал_меня_папой/Source/Broll/pexels/8063956.mp4` — упомянут: `018_соседский_мальчик_назвал_меня_папой/Source/Broll/pexels/manifest.json`, `018_соседский_мальчик_назвал_меня_папой/Edit/018_en_broll_imports.json` и ещё 5
- 22.6 МиБ — `022_свадьба_сестры_в_подарок/Source/Broll/pexels/5977260.mp4`
- 20.9 МиБ — `022_свадьба_сестры_в_подарок/Source/Broll/pexels/6324567.mp4` — упомянут: `022_свадьба_сестры_в_подарок/Edit/episode-package.json`, `022_свадьба_сестры_в_подарок/Edit/shot_draft.json` и ещё 7
- 18.8 МиБ — `018_соседский_мальчик_назвал_меня_папой/Source/Broll/pexels/7964887.mp4` — упомянут: `018_соседский_мальчик_назвал_меня_папой/Source/Broll/pexels/manifest.json`, `018_соседский_мальчик_назвал_меня_папой/Edit/018_en_broll_imports.json` и ещё 11
- 17.6 МиБ — `018_соседский_мальчик_назвал_меня_папой/Source/Broll/pexels/5758774.mp4` — упомянут: `018_соседский_мальчик_назвал_меня_папой/Source/Broll/pexels/manifest.json`, `018_соседский_мальчик_назвал_меня_папой/Edit/018_en_broll_imports.json` и ещё 5
- 17.1 МиБ — `022_свадьба_сестры_в_подарок/Source/Broll/pexels/6931246.mp4` — упомянут: `022_свадьба_сестры_в_подарок/Edit/episode-package.json`, `022_свадьба_сестры_в_подарок/Edit/shot_draft.json` и ещё 7
- 12.4 МиБ — `022_свадьба_сестры_в_подарок/Source/Broll/pexels/8765271.mp4` — упомянут: `022_свадьба_сестры_в_подарок/Edit/render-plan-unverified-source-draft.json`
- 11.9 МиБ — `022_свадьба_сестры_в_подарок/Source/Broll/pexels/10238452.mp4` — упомянут: `022_свадьба_сестры_в_подарок/Edit/episode-package.json`, `022_свадьба_сестры_в_подарок/Edit/shot_draft.json` и ещё 19
- 11.9 МиБ — `018_соседский_мальчик_назвал_меня_папой/Source/Broll/pexels/10238452.mp4` — упомянут: `022_свадьба_сестры_в_подарок/Edit/episode-package.json`, `022_свадьба_сестры_в_подарок/Edit/shot_draft.json` и ещё 19
- 10.7 МиБ — `022_свадьба_сестры_в_подарок/Source/Broll/pexels/6386551.mp4`
- 7.2 МиБ — `022_свадьба_сестры_в_подарок/Source/Broll/pexels/8247208.mp4`
- 6.8 МиБ — `018_соседский_мальчик_назвал_меня_папой/Source/Broll/pexels/11640552.mp4` — упомянут: `018_соседский_мальчик_назвал_меня_папой/Source/Broll/pexels/manifest.json`, `018_соседский_мальчик_назвал_меня_папой/Edit/018_en_broll_imports.json` и ещё 10
- 6.0 МиБ — `022_свадьба_сестры_в_подарок/Source/Broll/pexels/32054941.mp4` — упомянут: `022_свадьба_сестры_в_подарок/Edit/episode-package.json`, `022_свадьба_сестры_в_подарок/Edit/shot_draft.json` и ещё 5
- 5.8 МиБ — `022_свадьба_сестры_в_подарок/Source/Broll/pexels/8246470.mp4`
- 5.4 МиБ — `022_свадьба_сестры_в_подарок/Source/Broll/pexels/8873334.mp4` — упомянут: `022_свадьба_сестры_в_подарок/Edit/render-plan-unverified-source-draft.json`
- 5.0 МиБ — `018_соседский_мальчик_назвал_меня_папой/Source/Broll/pexels/8478035.mp4` — упомянут: `018_соседский_мальчик_назвал_меня_папой/Source/Broll/pexels/manifest.json`, `018_соседский_мальчик_назвал_меня_папой/Edit/018_en_broll_imports.json` и ещё 11

## F. Видео в Edit и других каталогах — кандидаты только после проверки назначения

Пути относительно `archive/legacy_stories/videos/`; порядок — от большего размера к меньшему. Упоминание в JSON/MD — указатель для ручной проверки, а не подтверждение активного использования.

- 60.0 МиБ — `004_pompeii_short/Edit/004_palmier_export.mp4`
- 57.6 МиБ — `022_свадьба_сестры_в_подарок/Edit/022_canonical_raw.mp4` — упомянут: `022_свадьба_сестры_в_подарок/Edit/022_export_job_observation.json`, `022_свадьба_сестры_в_подарок/Edit/022_canonical_export_receipt.json` и ещё 3
- 13.3 МиБ — `027_doomscrolling_short/Edit/QC/visual_preview_silent_v2.mp4` — упомянут: `027_doomscrolling_short/Edit/Captions/QA.md`, `027_doomscrolling_short/Edit/QC/VISUAL_PREVIEW_QA.md`
- 13.3 МиБ — `027_doomscrolling_short/Edit/QC/visual_preview_silent.mp4` — упомянут: `027_doomscrolling_short/Edit/QC/VISUAL_PREVIEW_QA.md`
- 2.1 МиБ — `027_doomscrolling_short/Edit/QC/preview_segments/scene_06.mp4`
- 1.5 МиБ — `027_doomscrolling_short/Edit/QC/preview_segments/scene_04.mp4`
- 1.5 МиБ — `027_doomscrolling_short/Edit/QC/preview_segments/scene_05.mp4`
- 1.5 МиБ — `027_doomscrolling_short/Edit/QC/preview_segments/scene_01.mp4`
- 1.5 МиБ — `027_doomscrolling_short/Edit/QC/preview_segments/scene_07.mp4`
- 1.1 МиБ — `027_doomscrolling_short/Edit/QC/preview_segments/scene_02.mp4`
- 1.0 МиБ — `027_doomscrolling_short/Edit/QC/preview_segments/scene_03.mp4`

## Сохранить

- Все исходные изображения и озвучки, в том числе `Source/Images`, `Source/Voice`, исходные видео группы E.
- Проекты, таймлайны, сценарии, документацию, SRT, JSON-тайминги, манифесты и журналы.
- Эффект ряби и его исходники для эксперимента.

После выбора групп каждым файлам нужна проверка зависимостей и возможности пересборки; никакие файлы в этом документе не считаются автоматически безопасными к удалению.
