# Deployment

## Target

VPS на Ubuntu Server 24.04.

Current target status: blocked on JustHost VPS access.

## Server Shape

- 1 CPU
- 1 GB RAM
- 20 GB NVMe
- IPv4 or IPv6 with working SSH access

## Hosting History

### Render

Render Background Worker was considered and partially configured. It was paused because the minimum paid worker was relatively expensive for one simple Telegram bot, and each separate worker would add recurring cost.

### JustHost VPS

JustHost VPS was ordered as a cheaper multi-bot host. The panel showed an IPv6-only VPS with IPv4 proxy SSH access.

Observed issue:

- `ssh -p <proxy-port> root@4to6.justhost.asia` connected to TCP but closed before password prompt.
- Direct IPv6 SSH also reset/closed before authentication.
- Reboot did not fix it.
- Proxmox web console was available but unstable.

Conclusion: deployment is blocked until JustHost support fixes SSH/console access, or the project moves to a more stable provider.

## Environment Variables

```env
BOT_TOKEN=
POST_ID=3
TARGET_CHAT_ID=-1003789946331
LOG_LEVEL=INFO
DEBUG_UPDATES=false
```

## Deploy Plan

1. Получить стабильный VPS with working SSH.
2. Установить `git`, `python3`, `python3-venv`.
3. Клонировать `https://github.com/selenovigor/raflnetworkingbot.git`.
4. Создать `.env` на сервере.
5. Создать virtualenv и установить зависимости.
6. Создать systemd service.
7. Остановить локальный бот на Mac, чтобы не было Telegram polling conflict.
8. Запустить service на VPS.
9. Проверить ответы в тестовом канале.

## Rollback

- Остановить systemd service на VPS.
- Временно запустить локальную версию на Mac с тем же `.env`.
- При необходимости откатить GitHub на предыдущий коммит и перезапустить service.

## Recommended Next Hosting Options

- Timeweb Cloud minimal VPS: simpler Russian UI, likely less friction.
- Selectel VPS/cloud: more reliable, more engineering-oriented.
- Render Starter: easiest operationally, but more expensive per always-on worker.
