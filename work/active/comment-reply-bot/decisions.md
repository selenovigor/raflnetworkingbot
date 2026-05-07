# Decisions: comment-reply-bot

## Decision Log

| Date | Decision | Alternatives | Why | Consequences |
| --- | --- | --- | --- | --- |
| 2026-04-27 | Python + aiogram | Node.js, python-telegram-bot | Простой стек для Telegram polling | Минимальный код, легко деплоить |
| 2026-04-27 | Без БД | SQLite/Postgres | Нет состояния и аналитики в первой версии | Проще эксплуатация |
| 2026-04-27 | VPS вместо Render | Render Background Worker | Render дороговат за одного простого бота; VPS позволит держать несколько ботов | Нужно администрировать сервер |
| 2026-04-27 | Long polling | Webhooks | Проще на VPS, не нужен домен/HTTPS | Только один активный процесс на токен |
| 2026-05-07 | JustHost VPS marked unstable/blocked | Keep debugging JustHost, switch provider, return to Render | SSH closes before authentication and console is unreliable | Need stable VPS or managed worker before production launch |
| 2026-05-07 | Deploy to Timeweb VPS with systemd | Render, JustHost, Selectel | Stable SSH access and reusable VPS for future bots | Need server maintenance, but bot survives Mac shutdown |

## Notes

- Перед боевым запуском токен надо перевыпустить через BotFather `/revoke`.
- Для боевого канала нужно заново определить `POST_ID` и `TARGET_CHAT_ID`.
- Do not store VPS passwords or bot tokens in project docs.
