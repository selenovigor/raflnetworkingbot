# Task 02: deploy-vps

Status: done

## Goal

Развернуть бота на VPS и обеспечить автозапуск.

## Current Blocker

JustHost VPS access is not usable yet:

- SSH proxy and direct IPv6 SSH open TCP connection but close before password prompt.
- Reboot did not fix SSH.
- Proxmox console was available but unstable.
- No bot files were deployed to the VPS.

Resolution: moved deployment to Timeweb VPS `81.200.145.88`.

## Scope

### In

- SSH-подключение.
- Установка Python/git.
- Клонирование GitHub-репозитория.
- `.env` на сервере.
- systemd service.
- Post-deploy QA.

### Out

- Docker.
- CI/CD.
- Мониторинг beyond systemd logs.

## Acceptance Criteria

- [x] Бот работает на VPS.
- [x] Локальный процесс на Mac остановлен.
- [x] `systemctl status` показывает active.
- [x] Service enabled for reboot autostart.
- [x] Рабочий канал получает ответы.

## Verification

- [x] `systemctl status raflnetworkingbot`
- [x] `journalctl -u raflnetworkingbot`
- [x] Telegram manual QA.

## Next Actions

- [x] Move to Timeweb VPS.
- [x] Configure systemd deploy.
- [x] Verify production Telegram reply.
