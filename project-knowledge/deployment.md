# Deployment

## Target

VPS на Ubuntu Server 24.04, Frankfurt.

## Server Shape

- 1 CPU
- 1 GB RAM
- 20 GB NVMe
- 1 IPv4

## Environment Variables

```env
BOT_TOKEN=
POST_ID=3
TARGET_CHAT_ID=-1003789946331
LOG_LEVEL=INFO
DEBUG_UPDATES=false
```

## Deploy Plan

1. Подключиться к VPS по SSH.
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
