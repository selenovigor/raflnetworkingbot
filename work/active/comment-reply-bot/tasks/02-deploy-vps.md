# Task 02: deploy-vps

Status: todo

## Goal

Развернуть бота на VPS и обеспечить автозапуск.

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
