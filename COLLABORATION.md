# Совместная работа

Общий процесс — [workflow](docs/workflow.md), правила изменения проекта — [development](docs/development.md). Один MR может содержать несколько небольших проверенных этапов; отдельные сессии работают по независимым заданиям и общей версии исходников.

## Владение

Один run имеет координатора; task lease назначает исполнителя конкретного входа/revision. Не перезаписывать результат параллельной работы и не менять shared inputs активного выпуска без [migration](docs/migration.md). Независимые workers получают минимальный context packet и возвращают artifacts/evidence; личные черновики и чужие chats не являются рабочим материалом.

Paper Detour — default нового запроса без канала. Nuviko History активен. Stories остаётся ручным архивом вне автоматической очереди. Scenes on Repeat — отдельный английский киноканал. Русскоязычный «Нувико» жизненных историй ведёт коллега; он отделён от архива Stories RU/EN и History. Для него нужны собственные verified profile/owner/rights/calendar, без наследования архива по имени.

Ранее переданы непривязанные voice IDs: мужской `ZEchI3lWet1JsdNubYRY`, женский `nkvv6waLzFah2jTNUZGT`. Их provider/account/channel/language не подтверждены. Не назначать их автоматически и не менять действующие голоса.

## Что сохранять

Git: код, schemas, profiles, rules/skills, небольшие сценарии/исследования/manifests, лицензии и receipts в разрешённой области доступа. Media/cache/models/venv и credentials остаются в выбранном runtime storage. Не коммитить API keys, OAuth tokens, private signing key, `.env`, personal chat exports или монтажные сессии. Public video IDs/URLs и hashes не заменяют secret credentials.

Импортированный media path сохранять до verified relink. Source-only checkout не гарантирует наличие рабочего фильма. Retention/cleanup — [storage](docs/standards/storage.md). Общие brand assets и зависимости других runs не удалять как временные файлы.

## Ветка и MR

Проверить актуальный main и локальные изменения, создать feature branch, делать тематические commits с точными путями. Перед публикацией прочитать diff и результаты tests. Отправить только свою ветку и открыть MR в main; после review выполнить согласованный merge. Пользовательское поручение на этот рефакторинг разрешает подготовку и публикацию одного MR, не live выпуск видео.

Приватный Git remote: `git@github.com:kleksar/ytvideos.git`. Доступ коллег, protection и production infrastructure настраиваются отдельно; не подменять отсутствие credentials новым внешним сервисом или публикацией конфиденциальных материалов.
