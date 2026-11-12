# Общий G08 — реализация и проверка

Пользователь принял №8 и разрешил продолжить эту техническую задачу без ответа Extra High; консультационный проход не завершён и не является источником решений. Общие числа принадлежат `automation/image_motion/grain_presets.json`; интерфейс — `run.py apply --config /absolute/episode/Edit/ImageMotion/motion.json`.

`g08` включён по умолчанию. Чистая глубина/параллакс переиспользуются, отдельный finished derivative запекает camera→grain в координатах кадра. На копии таймлайна camera keys заменяются baked media и нейтральным transform; opacity/captions/audio сохраняются. `grain:none` явно оставляет прежний путь. Общая процедура и ограничения — в image-motion skill. Итоговое delivery encoding не менялось.

Проверки: 15 тестов, полный decode 122 кадров горизонтального watchmaker smoke (120 разных видимых кадров) и 32 кадров вертикального synthetic fixture (30 разных видимых кадров), SAR1:1/30fps/BT709limited/zeroPTS/noaudio; native field RMS/rho/mask/sigma, направления шести стандартных camera modes, отказ для неподдержанных эффектов, сохранение opacity/других дорожек в structural fixtures, отсутствие двойной камеры и реальный cache repeat без renderer. Автор просмотрел actual decoded watchmaker0/60/119 и native-pixel patch; это sampled self-review, не независимая или непрерывная проверка. Grain projection/correlation — численные коэффициенты, не проценты воспринимаемой сохранности. См. QA.json.

Live Palmier применение нового grain пути к выпуску не выполнялось; до экспорта конкретного фильма остаются live structural verification и scene×cue/frame QA. Existing production timelines/YouTube не менялись.

Первый development derivative f49ed5c15fcc79486953784b67483cbdbe2ad76134f07d4b04091876bde8e2ee.mp4 имел неполные colour tags: текущий FFmpeg не сохранил primaries/TRC только из encoder flags. Исправлено явным setparams в filter graph и strict finished-cache probe. Старый тестовый cache object не импортирован и не используется новым fingerprint; сохранён как диагностический артефакт, shared cache не очищался. Текущий пригодный derivative указан в QA.json.
