---
name: ytv-operate
description: "Inspect or recover saved ytvideos runs, leases, blockers, uncertain external operations, worker capabilities, storage and budgets. Use for status, restart, cancellation and cleanup."
---

# Состояние, восстановление и обслуживание

CLI и точные outputs/receipts: [task contract](../../../docs/operations/task-contract.md).

Прочитать `status` и `next` нужного run, его version pins, leases, blockers и pending/UNKNOWN external operations. Для миграции читать [migration](../../../docs/migration.md); для хранения — [storage](../../../docs/standards/storage.md); для capabilities — [runtime](../../../docs/operations/runtime.md).

1. Resume восстанавливает состояние из store и artifacts. Не спрашивать заново уже зафиксированное одобрение и не генерировать сохранённый проверенный output ради нового чата.
2. Проверить, что worker использует закреплённый code/profile/skills. Несовпадение — blocker конкретного run, а не разрешение тихо заменить его правила.
3. Истёкшую lease возвращать по контракту приложения. Stale worker не может перезаписать текущую revision. UNKNOWN требует reconciliation существующей операции; отсутствие локального ответа не означает, что provider ничего не сделал.
4. Для очереди контролировать caps, review backlog, fairness, rate-limit cooldown и бюджет. Не открывать дополнительные чаты, если координатор не успевает принимать результаты. Состояние пула сохранять вне сессии.
5. При отмене запретить новые tasks/effects; проверить уже отправленные операции. Отмена локального ожидания не откатывает YouTube upload/schedule.
6. Cleanup делать только по manifest/ownership/dependencies и storage policy. Сохранить фактический receipt, отдельные ошибки и pending actions.

Возвращать короткий operational result: состояние, завершённые artifacts, текущие blockers, следующая готовая задача и реальные ограничения. Метрики active production time отделять от ожидания пользователя; UNKNOWN cost не превращать в ноль. Read-only status не требует нового творческого review.
