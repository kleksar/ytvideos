# Локальный PostgreSQL для общего состояния

`compose.yml` запускает PostgreSQL 17 с named volume, healthcheck и портом только `127.0.0.1:5432`. Это база состояния, не запущенный image worker, ChatGPT bridge или media storage.

Скопировать `.env.example` в локальный `.env`, задать собственный `YTV_POSTGRES_PASSWORD` и согласованный `YTV_DATABASE_URL`. Не сохранять секреты в Git. Private approval signing key в worker `.env` не помещать.

```bash
docker compose --env-file .env -f ops/compose.yml up -d
```

CLI автоматически `.env` не читает. Передать `YTV_DATABASE_URL`, `YTV_WORKSPACE`, `YTV_APPROVAL_PUBLIC_KEY` через окружение процесса или разрешённый dotenv runner; verifier key публичный, signer остаётся в trusted host. Использовать один DSN/общий storage для взаимодействующих workers.

Не применять `down -v` к рабочему volume ради устранения ошибки: это удаляет данные. Backup/restore проверить отдельно. Для production несколько хостов, TLS/network access, secrets management, backups, monitoring и worker availability требуют конкретного deployment. Наличие этого compose не подтверждает 24/7 исполнение.
