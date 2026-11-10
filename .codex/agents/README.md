# Роли независимых задач

| Роль | Область |
|---|---|
| coordinator | Выбирает ready tasks из store, создаёт context packets, принимает результаты и следит за backlog |
| worker | Выполняет одну задачу/сцену, возвращает реальные artifacts/evidence, не изменяет approvals/policy |
| reviewer | Проверяет exact artifact и пишет findings/coverage, не редактирует его и не одобряет за пользователя |

Имена ролей не задают дополнительные полномочия или гарантированную независимость. Инструментальные permissions, модель, лимиты и запуск принадлежат фактическому runtime. Основная production модель — GPT-6 Luna; TOML не выдумывает доступный model ID или возможность запуска отсутствующего backend.

Новый worker получает самодостаточный packet без всей истории координатора. Переиспользовать slot только при подтверждённом reset контекста. Авторский повторный проход помечать self-review; independent review требует действительно отдельного исполнителя/контекста.

[Контракты runtime](../../docs/operations/runtime.md) · [Каталог skills](../../.agent/skill-catalog.md) · [Адаптивная очередь](../../docs/architecture/adaptive-workers.md)
