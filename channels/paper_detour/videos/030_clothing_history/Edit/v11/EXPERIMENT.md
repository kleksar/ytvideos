# Clothing history — native Full HD grain test v11

Проверяется только фактура зерна на Full HD ролике Paper Detour. Сила оставлена на заданных пользователем **33%**. Контроль — v10 с текстурой 540×960 и той же opacity.

## Источник и таймлайн

- Исходный резерв: `Shared/Overlays/Film_Grain/paper_film_grain_visible_15min_270x480_30fps_v01.mov`.
- Создан один 8-секундный цикл ProRes 4444 alpha размером 1920×1080, 30 fps, 240 кадров. Четыре на четыре участки собраны из 270×480 участков резерва с временными смещениями 0, 15, …, 225 кадров и повёрнуты до ландшафтной ориентации; масштабирования зерна при сборке нет. Source alpha не усиливалась повторно.
- SHA-256 цикла: `9459ca3890454b4ec9dbf9728d37aab83b59b0a0abf21b2ef85bd18a78b172fe`.
- Копия v10 сохранена как отдельный Palmier timeline v11. На одной дорожке `Grain` 24 клипа без пропусков покрывают кадры `[0,5700)`; opacity каждого — `0.33`, normal blend, полноэкранный центр. Остальные дорожки не менялись.
- Project `B1BA2D18`, timeline `E6076D37`, pre-edit snapshot `52212257`.

## Финальный тестовый MP4

- `PAPER_DETOUR_030_NATIVE_FULLHD_GRAIN_33_EN_v11.mp4`: 1920×1080, 30 fps, 190 секунд, H.264, 1,193,901,605 bytes.
- Финальный видеопоток кодирован через libx264, preset medium, CRF 16, tune grain, yuv420p, BT.709.
- Принятый AAC mix сохранён без перекодирования. Выходной AAC payload совпадает с source mix SHA-256 `3ba2d8175d566eff1addd0b5278b82fd36616a5e41da0e68cba1531939321e6e`.
- Финальный файл SHA-256: `eec8e2515b886dc10060e08a0979cdd0fb7a619a472a7db9564e01d74f699862`.

YouTube review copy: [v11 private](https://www.youtube.com/watch?v=TWAObKXZVJ8). Сравнивать с [v10 fine grain 33%](https://www.youtube.com/watch?v=HwniKlV8S9Q).
