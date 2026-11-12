# JFK layered scene — independent V3 pilot

This is a 4.6-second, 540×960 / 30 fps test of one shot, not the one-minute finished video. It is independent of Palmier; no live project or earlier deliverable was altered.

- Video: `jfk_layered_scene_trial_v3.mp4` (138 video frames; container 4.62 s).
- Rebuild: `python3 build_scene_jfk_v3.py`; scene parameters/assets: `scene_jfk_v2_manifest.json` and the script. The subject and desk are one intact layer; the desk-free background and the foreground camera are separate. Animated glyphs use existing separate paper graphics. Gentle moving grain comes from an existing source.
- Horizontal paths over 4.6 seconds on a 540 px frame: background +6 px, subject/desk −7 px, foreground +10 px. Relative FG-to-subject displacement is 17 px, background-to-subject 13 px. Text changes scale, position and angle; the IQ digits move separately.
- Audio is copied from the prior IQ Gallery deliverable with `-c:a copy`; no audio was generated or re-encoded for this test.
- V1 retains a duplicate background desk and text near the picture frame. V2 removes the duplicate desk but the digit remains too close to the frame. V3 tightens/relocates digits and increases visible parallax. Prior test files are preserved.
- FFmpeg full decode completed without errors. Creator visually checked frames at 2.3 s and 4.5 s: the digits clear the frame and the microphone and subject remain connected to the desk in these frames. This is not a continuous visual or audio review. Independent QA of V3 has been requested; record its result separately.

## V4 — плавнее и синхронно

После запроса пользователя о резкой анимации создан `jfk_layered_scene_trial_v4.mp4`. Вход имени и группы IQ использует одну кривую smoothstep в одном интервале (0,45–1,25 с), одинаковые фейды, поэтому строки входят с той же скоростью и одновременно. Покачивание замедлено до цикла 6 секунд, масштаб ±3%, наклон ±1,2°; отдельные цифры разведены по фазе на 0,65 радиан, движение амплитудой примерно 1 px. Имя пересоздано прозрачным PNG `Source/Graphics/names/john_f_kennedy_roomy_v1.png` с расширенным tracking. Первый контакт-лист и полное декодирование проверены. Независимая оценка плавности и читаемости ожидается; непрерывный просмотр на нормальной скорости и прослушивание не выполнялись.
