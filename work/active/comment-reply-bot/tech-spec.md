# Tech Spec: comment-reply-bot

Status: implemented, pending VPS deploy

## 1. Context

User spec: `work/active/comment-reply-bot/user-spec.md`

## 2. Requirements Traceability

| User requirement | Technical implementation | Test/verification |
| --- | --- | --- |
| Только один пост | `belongs_to_target_post()` проверяет `POST_ID` | Тест в тестовом канале |
| Только нужный чат | Проверка `TARGET_CHAT_ID` | Логи `chat_id=-1003789946331` |
| Reply пользователю | `message.reply(answer)` | Ручная проверка |
| Игнорировать ботов | `message.from_user.is_bot` | Code review |
| Цифры `1`-`5` | `normalize_answer()` + `RESPONSES` | Ручной тест |
| Отбивка | `FALLBACK_RESPONSE` | Ручной тест |

## 3. Architecture

Один Python-процесс на aiogram long polling. Состояние не хранится. Конфигурация через env.

## 4. Files

| File | Action | Purpose |
| --- | --- | --- |
| `bot.py` | create | Основная логика бота |
| `requirements.txt` | create | Python-зависимости |
| `.env.example` | create | Документация env-переменных |
| `Procfile` | create | Альтернативный запуск на PaaS |
| `README.md` | create | Инструкция |
| `project-knowledge/*` | create | Документация проекта |

## 5. Data Model

БД не нужна.

## 6. External Contracts

| Event | Input | Output | Errors |
| --- | --- | --- | --- |
| Telegram message | Text message in discussion group | Reply with selected text or fallback | Telegram network/rate errors |

## 7. Testing Strategy

- Unit: не добавлялись, логика малая.
- Static: `python3 -m py_compile bot.py`.
- Manual: тестовый канал, сообщения `1`-`5`, произвольный текст, другой пост.

## 8. Security and Privacy

- `BOT_TOKEN` хранить только в `.env` или env сервера.
- Старый токен после теста перевыпустить через BotFather `/revoke`.
- Пользовательские сообщения не сохраняются.

## 9. Deployment Notes

- Target: Ubuntu VPS.
- Process manager: systemd.
- Rollback: остановить systemd на VPS, временно вернуть локальный запуск.

## 10. Acceptance Verification Plan

- [x] Синтаксис проходит.
- [x] Локальный тест в Telegram проходит.
- [ ] systemd service активен на VPS.
- [ ] Тестовый канал работает при выключенном локальном процессе.
