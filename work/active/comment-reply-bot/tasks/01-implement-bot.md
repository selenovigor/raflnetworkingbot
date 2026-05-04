# Task 01: implement-bot

Status: done

## Goal

Сделать Telegram-бота, который отвечает в комментариях под одним постом.

## Scope

### In

- aiogram bot.
- Ответы `1`-`5`.
- Fallback.
- Фильтр по `POST_ID` и `TARGET_CHAT_ID`.
- `.env.example`.

### Out

- БД.
- Админка.
- Несколько постов.

## Acceptance Criteria

- [x] Бот запускается.
- [x] Синтаксис проходит.
- [x] Ответы отправляются reply.
- [x] Локальный Telegram-тест прошёл.

## Verification

- [x] `python3 -m py_compile bot.py`
- [x] Ручной тест в тестовом канале.
