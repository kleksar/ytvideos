# Общие assets

Использовать только фактически доступный принятый файл с установленным owner, provenance, правами и hash. Запись старого каталога, похожее имя или JSON manifest без media не подтверждают наличие/лицензию.

Источники в репозитории: [brand assets](../channels/BRAND_ASSETS.md), [Paper scene references](../channels/paper_detour/brand/SCENE_IMAGE_REFERENCES.md), [Paper availability](../channels/paper_detour/brand/REFERENCE_STATUS.md), [Nuviko references](../channels/nuviko_history/brand/References/README.md), [Scenes brand](../channels/scenes_on_repeat/brand/README.md). Некоторые фактические материалы передаются в отдельном bundle; их отсутствие обозначать явно.

До новой генерации проверить пригодные existing artifacts/cache. Hash доказывает идентичность bytes, а не права или художественную приёмку. Сценовый packet содержит только нужные exact references. Импортированные пути сохранять до verified relink; общая библиотека не очищается как временный каталог отдельного run.

Жизненный цикл и cleanup — [storage](../docs/standards/storage.md). Не ссылаться на отсутствующие локальные dedupe manifests, screenshots, VPN logs и cleanup reports как на обязательные входы чистого checkout.
