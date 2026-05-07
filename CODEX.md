# Codex Project Workflow

Проект ведется по spec-driven workflow: сначала фиксируем ожидания, затем техническое решение, затем маленькие задачи с проверками.

## Структура

```text
project-knowledge/
  project.md
  architecture.md
  patterns.md
  deployment.md

work/
  active/
  completed/
```

## Definition of Done

- acceptance criteria выполнены;
- тесты или проверки проведены и описаны;
- секреты не попали в репозиторий;
- `.env.example` актуален;
- документация обновлена;
- есть понятный способ деплоя и отката;
- post-deploy QA пройден после запуска на VPS.

## Правила безопасности

- Реальные токены хранить только в `.env` или переменных окружения сервера.
- В репозитории держать только `.env.example`.
- Не коммитить пароли, токены, SSH-ключи и доступы к VPS.

## Правило хостинга

Telegram-боты можно запускать на VPS или зарубежных cloud-сервисах. Для этого проекта выбран VPS, чтобы держать несколько будущих ботов на одном сервере.

## Telegram VPS Network Check

Для Telegram-ботов на VPS перед production-запуском обязательно проверить маршрут до Telegram API:

```bash
curl -4 -sS --max-time 20 https://api.telegram.org/bot$BOT_TOKEN/getMe
curl -6 -sS --max-time 20 https://api.telegram.org/bot$BOT_TOKEN/getMe
```

Если IPv4 зависает или даёт timeout, а IPv6 отвечает быстро, в aiogram-проектах принудительно использовать IPv6-сессию:

```python
import socket

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.enums import ParseMode

session = AiohttpSession(timeout=90)
session._connector_init["family"] = socket.AF_INET6
bot = Bot(
    token=token,
    session=session,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML),
)
```

Также для отправки сообщений нужен retry на `TelegramNetworkError` и `TelegramRetryAfter`, чтобы временный timeout Telegram API не терял reply.
