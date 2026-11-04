# Paper Detour — профиль канала

Вход: [root](../../AGENTS.md), [bootstrap](../../.agent/CHANNEL_BOOTSTRAP.md), точный episode bundle и актуальный контекст выпуска (передаются отдельно). Paper Detour и прежнее имя Rarovista обозначают один канал.

## Производство

Фильм и Short выполняются по [утверждённому общему flow Paper/Nuviko](../../.agents/skills/ytv-video-production/SKILL.md). Он задаёт автономность и контрольные точки; ниже — канальные настройки.

Самостоятельные посты/карусели — [Posts Playbook](docs/YOUTUBE_POSTS_PLAYBOOK.md). Подача рассказа — root §11, Shorts — [общий стандарт хука](../../.agent/SHORTS_STORY_STANDARD.md) и [решение о возможной петле](../../.agents/skills/ytv-shorts-loop/SKILL.md).

## Язык продукта

Язык готового контента и работа с русским исходником — по [общему production skill](../../.agents/skills/ytv-video-production/SKILL.md#язык-готового-контента).

## Изображение и текст

- Одна исходная сцена — законченная полноформатная статичная бумажная диорама; композиции сменяются прямыми склейками. [Scene profile](../../.agents/skills/ytv-scene-images/references/paper-detour.md) владеет материалом, качеством и реальными эталонами.
- [Paper storyboard](../../.agents/skills/ytv-paper-storyboard/SKILL.md) задаёт композиционные решения; производство/проверка PNG выполняются общим scene-images. Согласованный media manifest задаёт пути общих импортов; его передают вместе с нужными медиа. Импортированные зависимости сохраняют свои пути.
- [Paper subtitles](../../.agents/skills/ytv-paper-subtitles/SKILL.md) задаёт оформление дословной строки.
- Принятый эталон отдельного выпуска и его локальные изображения передаются вместе с соответствующим episode bundle; в source-only клоне выпускные reference packs отсутствуют.
- Разрешённые движения цельной картинки и их сочетания выполняет общий [image-motion](../../.agents/skills/ytv-image-motion/SKILL.md). Субтитры сохраняют собственный слой и геометрию.

## Настройки и выпуск

Единственный голос канала и порядок проверки — [канальный реестр голосов](../../.agents/skills/ytv-audio-delivery/references/channel-voices.md); скорость 1,10×, ровно один раз. Разрешения на звук — root §5.

Общие владельцы: [доставка](../../.agents/skills/ytv-video-export/references/delivery.md), [MP4 review/technical QA](../../.agents/skills/ytv-video-qa/references/export-review.md), [упаковка](../../.agents/skills/ytv-video-packaging/SKILL.md), [release](../../.agents/skills/ytv-youtube-release/SKILL.md), [очистка](../../.agents/skills/ytv-media-lifecycle/SKILL.md). Упаковка использует визуальный профиль Paper. Календарная политика — [release strategy](docs/SHORTS_RELEASE_STRATEGY.md).

Для нового длинного фильма визуальная конечная заставка — по [Paper стандарту](../../.agents/skills/ytv-paper-production/references/end-screens.md); её нативные элементы сохраняет release. Старые принятые выпуски сохраняют своё состояние.

Монтаж через FFmpeg по root и общему flow. Конкретные разрешения и пути хранятся в текущем контексте выпуска; существующие зависимости других выпусков сохраняются.
