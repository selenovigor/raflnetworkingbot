# Task 02: deploy-vps

Status: blocked

## Goal

Развернуть бота на VPS и обеспечить автозапуск.

## Current Blocker

JustHost VPS access is not usable yet:

- SSH proxy and direct IPv6 SSH open TCP connection but close before password prompt.
- Reboot did not fix SSH.
- Proxmox console was available but unstable.
- No bot files were deployed to the VPS.

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

- [ ] Бот работает на VPS.
- [ ] Локальный процесс на Mac остановлен.
- [ ] `systemctl status` показывает active.
- [ ] После reboot service поднимается автоматически.
- [ ] Тестовый канал получает ответы.

## Verification

- [ ] `systemctl status raflnetworkingbot`
- [ ] `journalctl -u raflnetworkingbot`
- [ ] Telegram manual QA.

## Next Actions

- [ ] Ask JustHost support to fix SSH access or reinstall VPS.
- [ ] If JustHost remains unstable, move to Timeweb Cloud, Selectel, Hetzner, or Render.
- [ ] Once stable SSH exists, continue with systemd deploy.
