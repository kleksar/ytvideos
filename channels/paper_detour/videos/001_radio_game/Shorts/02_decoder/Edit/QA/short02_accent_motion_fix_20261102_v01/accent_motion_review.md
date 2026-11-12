# Short 02 — верхние акценты, целевой визуальный QA

- Видео: `Work/short02_accent_motion_fix_20261102_v01/previews/PAPER_DETOUR_001_SHORT02_ACCENT_MOTION_REVIEW_20261102_v04.mp4`
- SHA-256: `5045b616adb23bb7d0fd0a08f4a2c79583f4c682ebed3514c6e7c54cca1f284f`
- Проверены вход, конец входа, выдержка, начало выхода и последний кадр для всех девяти акцентов (45 декодированных кадров из MP4). Подробная выборка: `accent_motion_review.json`.
- Вход снизу вверх, неподвижная выдержка, выход вверх с opacity 1→0 и совмещение с нижними субтитрами: **PASS**. Контакт-листы: `technical/c01_entry_exit_frames.jpg`, `technical/accent_motion_contact_sheet.jpg`.
- Потоки и полное декодирование: **PASS**.
- Голос не менялся. AAC-пакеты скопированы из v03 stream copy; payload SHA-256 `b79ae037166a556920a11f642b6aeeeb5b57e3156e04dc1569f5f999995e4ab8`. Слуховая синхронизация субтитров и субъективное прослушивание остаются **UNVERIFIED**.
- Итог: **UNVERIFIED** до проверки слышимой синхронизации. Это targeted review анимации, не полный просмотр всех кадров.
