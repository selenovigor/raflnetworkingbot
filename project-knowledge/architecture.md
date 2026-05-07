# Architecture

## Stack

- Python 3.9+
- aiogram 3
- Telegram Bot API через long polling
- systemd на VPS для постоянного запуска

## Runtime Model

Комментарии Telegram-канала приходят боту как сообщения в привязанной группе обсуждений. Бот фильтрует сообщения по:

- `TARGET_CHAT_ID` - ID группы обсуждений;
- `POST_ID` - ID корневого сообщения/треда под нужным постом.

## Data

База данных не используется. Все тексты ответов статичны и хранятся в `bot.py`.

## Message Flow

1. Пользователь пишет комментарий под постом.
2. Telegram отправляет update боту.
3. Бот проверяет, что сообщение не от бота, чат совпадает с `TARGET_CHAT_ID`, а тред совпадает с `POST_ID`.
4. Бот нормализует текст.
5. Для `1`-`5` случайно выбирает один ответ из пула вариантов для этой цифры.
6. Для другого текста отправляет fallback.
7. Для каждого третьего валидного цифрового запроса пользователя в этом чате/треде добавляет subscribe reminder.
8. Ответ отправляется через reply на сообщение пользователя.

## Runtime State

In-memory counter tracks valid numeric requests by `(chat_id, thread_id, user_id)`. It is used only for every-third-request subscribe reminder and resets on process restart.
