# G08 one-command integration — consultation unavailable; explicit exception

- Date: 2026-11-02; coordinator personally in Google Chrome.
- URL: https://chatgpt.com/c/6ae819c4-39b0-83eb-be49-4786cd819bb9
- Exact visible label before **both** requests: «Extra High, 4 из 5. Используйте клавиши со стрелками влево и вправо для настройки мощности.»
- Inputs: user accepted G08; existing `automation/image_motion/run.py`, `render.py`, accepted Matrix10_v02 renderer and canonical motion automation contract.

## Prompt

Ты — консультант в уже открытом ChatGPT Extra High. Требование координатора выполнено этим обращением; дай ответ здесь, не открывай другой ChatGPT. Одна техническая задача: как минимально безопасно добавить принятый пользователем G08 (RMS3, sigma.77px при1440p,30Hz,rho.35, luma-only, маска20/64/208/235) в имеющийся one-command image_motion apply. Факты кода: baseline Palmier still timeline; depth/parallax per-scene MP4 cache,N+2frames; после импорта Palmier накладывает camera position/scale endpoint keys; остальные дорожки должны совпадать. Глобального grain shader API нет в изученном helper. Grain обязан оставаться в координатах экрана ПОСЛЕ камеры; иначе zoom растит зерно. Можно запечь camera+grain в отдельный derivative cache от чистогоdepthcache, нейтрализовать только запечённые camera keys/transform у целевого клипа, прочие tracks/cues/audio не менять. Стандартные6режимов имеют линейные двухточечные равномерные scale>=1,pan normalized top-left; existing может быть сложнее. Не хотим внедрять полный export orchestration или ручной work в будущие выпуски. Оцени этот путь и предложи границы отказа для неподдержанных camera/crop/rotation, fingerprints/idempotency, sigma scaling для9:16 и UHD, порядок цвета и защиту от двойного зерна/камеры. Нужен короткий конкретный контракт реализации, без новых творческих пресетов и без переписывания всей системы. Исходные импортированные cache paths сохраняем, derivative новый. Звук не создаём, YouTube не трогаем.

Visible result: only «Спроектировал семейство эффектов, масштабирование и монтаж». No substantive answer.

## One short retry

Сейчас виден только статус «Спроектировал семейство эффектов, масштабирование и монтаж». Самого ответа нет. Дай прямо здесь краткий содержательный контракт по предыдущему запросу: порядок запекания, ограничения камеры, sigma scaling и cache/idempotency. Без других действий.

Visible result: only «Собрал единый контракт пайплайна с масштабированием, шумом и границами камеры». No substantive answer; consultation **NOT COMPLETED**. No design attributed to this consultation.

## Explicit user authorization

After reporting the limitation and stopping the dependent branch, the coordinator asked whether this technical task could continue without Extra High. User answered: **«Да, продолжай без Extra High»**. This is a task-specific exception, not a change to root policy for future work. Implementation continued under that exception, using the approved G08 values and existing renderer/cache conventions. Acceptance is recorded next to the watchmaker experiment; actual technical checks are in `Edit/CommonG08/`.
