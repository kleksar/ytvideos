# Nuviko History

Сначала прочитать [root AGENTS](../../AGENTS.md), [bootstrap](../../.agent/CHANNEL_BOOTSTRAP.md) и точную запись выпуска в [реестре](../../.agent/episode-registry.md). `.agents/skills` направляет в единый набор проекта. Номер и slug не устанавливают канал. Статус, разрешения и принятые артефакты — в CURRENT_CONTEXT и action-relevant state_sources выпуска.

Подача рассказа и публичных материалов — root §11. Для сюжетных Shorts применять [shorts-story](../../.agents/skills/ytv-shorts-story/SKILL.md) и рассматривать переход финала к началу по [shorts-loop](../../.agents/skills/ytv-shorts-loop/SKILL.md). Источники и пределы фактчека хранить внутри проекта.

Производство использует [общий flow](../../.agents/skills/ytv-video-production/SKILL.md); заморозка и конкретные исключения — root и поручение пользователя. Язык готового контента задаёт общий flow; исторический канал отделён от русскоязычного канала жизненных историй.

- [Визуальный профиль](brand/VISUAL_PROFILE.md) и [его текущее состояние](brand/CURRENT_CONTEXT.md) задают рисованного путешественника, реалистичный исторический мир и субтитры. Оба принятых PNG героя передавать в связанные генерации.
- Голос и настройки — [канальный реестр](../../.agents/skills/ytv-audio-delivery/references/channel-voices.md); скорость 1,10× ровно один раз. Формат long 16:9, Short 9:16.
- Разработка истории из темы — [history-story](../../.agents/skills/ytv-history-story/SKILL.md) и [канальный стандарт](docs/STORYTELLING_STANDARD.md); принятый сценарий идёт в общий production по root §5.
- Сценовые PNG, движение цельного кадра, звук, субтитры и FFmpeg используют общих владельцев из [каталога](../../.agent/skill-catalog.md). Дословную речь, фактический alignment и проверки не подменять предположениями.
- Названия, обложки, описания, главы, плейлисты, A/B и release используют общие skills с профилем этого канала. Новый доступ/публикация — по фактическому решению пользователя и общему flow.
