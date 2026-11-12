# Channel layout architecture consultation

Date 2026-11-04. Visible Google Chrome label before prompt: **Extra High**. Chat: https://chatgpt.com/g/g-p-6ae147d3975481919b5bfda6935777d0-yt-video/c/6aeb4a18-baac-83ed-80e0-b4f6dfb8f084

Task: verify the user's requested `channels/paper_detour`, `channels/nuviko_history` layout using the actual mixed Stories inventory. Proposed separate Nuviko life-story channel, archive for UNVERIFIED, common automation at root, reversible path/content migration with media hashes and temporary compatibility routers. Asked for risks and boundaries only, no execution or publication. The full prompt is retained in the chat. Initial display failed; loading the completed response exposed the entire substantive answer, personally read by the coordinator.

## Completed answer

Схема в целом корректна. Главный принцип: классифицировать материалы по подтверждённой принадлежности к проекту, а не по исходной директории или похожему названию.

Границы раскладки

channels/paper_detour/ — только подтверждённые материалы Paper Detour, включая установленные алиасы.

channels/nuviko_history/ — исторические выпуски по реестру.

channels/nuviko_stories/ — жизненные сюжеты текущего русскоязычного Нувико.

archive/unclassified_episodes/ — неопознанные и UNVERIFIED, без предположений о канале.

automation/ — действительно общие инструменты; специфичные конфигурации остаются у каналов.

channels/borisenko/ — допустимо, но отдельный проект дубляжа логичнее разместить в projects/borisenko/, если это не самостоятельный канал.

brand/ и shared/ — разграничивать по фактическому использованию. Общий бренд Nuviko нельзя автоматически считать принадлежащим History.

Главные риски

Ошибочная атрибуция: каждый перенос выпуска должен опираться на реестр или другое подтверждение.

Несовместимость старых путей: смешанный stories/ нельзя заменить одним symlink на разные каталоги. Нужны адресные совместимые маршруты.

Скрытые зависимости: абсолютные пути, Markdown-ссылки, Python imports, CI, скрипты, AGENTS.md, skills и конфигурации.

Потеря идентичности: сохранить episode ID, исходные имена, регистры и media hashes.

Неполный rollback: одной карты перемещений недостаточно при изменении содержимого файлов.

Критерий готовности

Манифест old_path → canonical_path → evidence, проверенные hashes, разрешённые ссылки и импорты, успешные локальные проверки и протестированный rollback.

Миграцию выполнять поэтапно. Сначала классификация и инвентаризация, затем перемещения, совместимость и проверка. Публикационные процессы не затрагивать.

## Applied boundaries

Use projects/borisenko because its README identifies a dubbing project, not an established channel. Nuviko traveler belongs to History as confirmed by channel profile/user task. Keep channel-specific legacy story pipeline and run state with nuviko_stories; move common services into root automation. Backup before mutation, inventory and media pins in Work/channel_layout_20261104. Consultancy is design guidance, not user authorization or independent QA.
