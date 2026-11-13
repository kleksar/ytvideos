---
name: ytv-operate
description: "Inspect or recover saved ytvideos runs, leases, blockers, uncertain operations, worker capabilities, storage and budgets. Use for status, restart, cancellation, cleanup, thumbnail experiment readback or published Shorts retention analysis."
---

# Состояние, восстановление и обслуживание

До действий выполнить [обязательную процедуру](../ytv-start/references/task-execution.md): прочитать pinned skill/требования/точные входы и проверить описанный способ. Пробел или неразрешённый конфликт — blocker затронутого этапа; не подставлять свои defaults и не менять правила ради продолжения.

CLI и точные outputs/receipts: [task contract](../../../docs/operations/task-contract.md).

Для запроса о результатах опубликованного Short получить `ytv instructions --channel CHANNEL_ID --stage retention --format short` и прочитать полный skill и все `reference_documents`. Выполнить [разбор удержания](references/shorts-retention.md): реальные данные → конкретный участок → гипотеза → следующий опыт. Этот read-only разбор не требует нового run; при отсутствии данных выполнить доступную часть и назвать точный пробел. Передать сохранённое наблюдение следующему research явно по ID/path.

Для управления существующим run прочитать `status` и `next`, его version pins, leases, blockers и pending/UNKNOWN external operations. Для миграции читать [migration](../../../docs/migration.md); для хранения — [storage](../../../docs/standards/storage.md); для capabilities — [runtime](../../../docs/operations/runtime.md).

Для явно порученного переноса runtime выполнить [процедуру миграции](references/runtime-migration.md): сначала проверяемый plan, затем применение к тому же run и сверка сохранённых входов.

1. Resume восстанавливает состояние из store и artifacts. Если явное согласие уже есть в текущей беседе, но gate ещё закрыт, зарегистрировать его штатным `approve` по task contract: тот же показанный artifact/revision, реальное сообщение и стабильная ссылка на него. Не просить повторного согласия, не создавать новый run и не генерировать проверенный output заново.
2. Проверить, что worker использует закреплённый code/profile/skills. Несовпадение — blocker конкретного run, а не разрешение тихо заменить его правила.
3. Устранение blocker подтвердить evidence и выполнять `unblock` только после повторной проверки инструкций/входов по [общей процедуре](../ytv-start/references/task-execution.md#блокер-и-продолжение). Истёкшую lease возвращать по контракту приложения. Stale worker не может перезаписать текущую revision. UNKNOWN требует reconciliation существующей операции; отсутствие локального ответа не означает, что provider ничего не сделал.
4. Для очереди контролировать caps, review backlog, fairness, rate-limit cooldown и бюджет. Не открывать дополнительные чаты, если координатор не успевает принимать результаты. Состояние пула сохранять вне сессии.
5. При отмене запретить новые tasks/effects; проверить уже отправленные операции. Отмена локального ожидания не откатывает YouTube upload/schedule.
6. Для thumbnail follow-up сверять отдельно сохранённый plan, фактическое состояние setup/readback и provider result с evidence; сохранять mode, варианты и пробелы данных. Не смешивать CTR, impressions, watch-time-share и общий retention и не выводить winner без фактического provider verdict. См. [thumbnail experiments](../../../docs/operations/thumbnail-experiments.md). Cleanup делать только по manifest/ownership/dependencies и storage policy. Сохранить фактический receipt, отдельные ошибки и pending actions.

Возвращать короткий operational result: состояние, завершённые artifacts, текущие blockers, следующая готовая задача и реальные ограничения. Метрики active production time отделять от ожидания пользователя; UNKNOWN cost не превращать в ноль. Read-only status не требует нового творческого review.
