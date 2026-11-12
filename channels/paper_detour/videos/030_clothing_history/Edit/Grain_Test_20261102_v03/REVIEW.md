# Grain Test 03 — амплитуда x3, зерно крупнее

Статус: `PRIVATE_YOUTUBE_READY_AWAITING_USER_REVIEW`. Пользователь поручил уменьшить амплитуду с×4 до×3 относительно первого теста, немного увеличить зерно и снова загрузить тот же15-секундный фрагмент наYouTube.

Амплитуда — сила отклонения яркости, а не количество зёрен. Test03: peak luma RMS3.6 (Test01=1.2; Test02=4.8), Gaussian sigma1.15 UHDpx (на15% больше Test02=1.0; FWHM ядра≈2.71px). Это численные параметры до кодирования, не обещание субъективной силы послеYouTube.

Сохранены чистый источник, startFrame811,450кадров/15.000с, три сценыV07–V09,1920x1080→3840x2160/30p, принятые камера и параллакс, бумажные акценты, seed20261102, rho0.65, luma-only/mask20/64/208/235, target45Mbps H.264High/tunegrain, BT.709 limited. Новый шум генерируется поверх чистого видео; прежнее зерно повторно не обрабатывается. Существующий AAC копируется без нового звука/микса.

Это технический private preview. Hashtags/Tags, отдельный thumbnail, плейлист, SRT, публичная публикация и расписание не запрошены. Английские metadata, category27, языкиen, audience/declaration сохранены из того же тестового контракта. Общий production preset/skill не меняется; субъективная приёмка остаётся пользователю. Для эпизодного уточнения действует разрешение CURRENT_CONTEXT пропустить повторный Extra High для030.

Команды из корня:

```sh
automation/image_motion/.venv/bin/python channels/paper_detour/videos/030_clothing_history/Edit/Grain_Test_20261102/render_grain.py channels/paper_detour/videos/030_clothing_history/Edit/Grain_Test_20261102_v03/preset.json
automation/image_motion/.venv/bin/python channels/paper_detour/videos/030_clothing_history/Edit/Grain_Test_20261102/verify_local.py channels/paper_detour/videos/030_clothing_history/Edit/Grain_Test_20261102_v03/preset.json
```

Предрендерный [storage audit](../MediaLifecycle/grain03-preflight-audit/audit.json) и [plan](../MediaLifecycle/grain03-preflight-plan/plan.json): отчёты построены, coverage errors0, bounded/non-exhaustive scope без livePalmier discovery; executable=false. Существующий active hold Edit и pins/current сохраняются. Аудит не является разрешением удаления. Место проверено по actual audit. Предыдущий Test02 остаётся сравнением до решения пользователя; его удаление в этом запросе не поручено. Ничего из чужих активных работ не меняется.

Короткая диагностика скорости масштабирования:10UHDкадров с автоматическим числом filter threads2.948с, сfilter_threads1=3.349с, SHA-256 кадров совпал. Медленный вариант не применён; алгоритм/encoder предыдущего теста сохранены. Полный AV playback и independent review не заявляются; итоговая техническая проверка относится только к новому файлу.

Локальная техническая проверка PASS:450frames/15.000с,3840x2160/30p,H.264High,BT.709limited,фактическое видео45.56Mbps. Полное декодирование всех потоков без ошибок; скопированный AAC побайтно совпал с тем же trim источника. SHA-256 чистого источника и samples80/243/400 совпали с Test02. Pre-encode RMS3.09-3.60; Cb/Cr до кодирования совпадают с чистыми. Диагностический noise projection gain после локального H.264 около0.62, не процент субъективной видимости. Просмотрены final-file samples80/243/400 (full-frame thumbnails и UHD1:1 crops), а также pre-encode crop80 Test02/Test03. Это адресная техническая проверка эффекта, не полная новая приёмка фильма; субъективное аудио/1080p comparison/independent review не выполнены.

## Готовый приватный тест

[Test03 наYouTube](https://www.youtube.com/watch?v=NcJAyqebXC4),videoID NcJAyqebXC4,каналPaperDetour/UCMVfdfaNxV3ZkI3_J3Eejzw. API readback:private,processed,processing succeeded; title/description/languages/category/audience/tags совпали. В плеере первоначально шёл1080p/30VP9(248), затем явно выбран2160p4K и подтверждены3840x2160@30,VP9(313),BT.709,Opus(251). Один экранный кадр музейной сцены просмотрен. Не заявляем полную субъективную AV-приёмку, полноценное сравнение1080p/2160p либо проверкуStudioCopyright. [Квитанция](youtube_receipt.json).

Параметры сохранены вpreset.json; общий workflow/skill и grain-free v13 не менялись. Ожидается оценка пользователя. Новый локальный MP4 сохранён; Test02 удерживается как сравнительный материал. Удаления и изменения внешних старых видео в этой итерации не выполнялись.

Пострендерный storage [audit](../MediaLifecycle/grain03-postupload-audit/audit.json) и [plan](../MediaLifecycle/grain03-postupload-plan/plan.json) записываются после фиксации новой выдачи. Текущий helper не удаляет медиа; source/Test02/Test03 pinned, остальные активные работы и Deliverables сохранены. Logical/allocated totals и ограничения покрытия — в отчёте; физическая экономия APFS не заявляется.
