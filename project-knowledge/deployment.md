# Deployment

## Target

VPS на Ubuntu Server 24.04.

Current target status: deployed on Timeweb VPS.

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

### Timeweb VPS

Timeweb VPS `81.200.145.88` is the current production runtime.

Runtime path:

```text
/opt/raflnetworkingbot
```

Service:

```text
raflnetworkingbot.service
```

Verified:

- `systemctl status raflnetworkingbot` shows `active (running)`.
- `journalctl -u raflnetworkingbot` shows polling and handled updates.
- Telegram manual QA in the working channel passed.

## Environment Variables

```env
BOT_TOKEN=
POST_ID=3
TARGET_CHAT_ID=-1003789946331
LOG_LEVEL=INFO
DEBUG_UPDATES=false
```

## Deploy Plan

1. Подключиться к Timeweb VPS по SSH.
2. Перейти в `/opt/raflnetworkingbot`.
3. Выполнить `git pull --ff-only`.
4. При изменении зависимостей выполнить `.venv/bin/pip install -r requirements.txt`.
5. Перезапустить `systemctl restart raflnetworkingbot`.
6. Проверить `systemctl status raflnetworkingbot`.
7. Проверить ответы в Telegram.

## Rollback

- Остановить systemd service на VPS.
- Временно запустить локальную версию на Mac с тем же `.env`.
- При необходимости откатить GitHub на предыдущий коммит и перезапустить service.

## Useful Commands

```bash
ssh root@81.200.145.88
cd /opt/raflnetworkingbot
systemctl status raflnetworkingbot --no-pager
journalctl -u raflnetworkingbot -f
systemctl restart raflnetworkingbot
```

## Recommended Next Hosting Options

- Timeweb Cloud minimal VPS: chosen and deployed.
- Selectel VPS/cloud: more reliable, more engineering-oriented.
- Render Starter: easiest operationally, but more expensive per always-on worker.
