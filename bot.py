import asyncio
import logging
import os
import re
from typing import Optional

from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import Message


RESPONSES = {
    "1": """<b>Одиночка с телефоном</b>

Ты не ищешь внимания — ты систематизируешь наблюдения
Тебе комфортнее смотреть, анализировать и понимать, чем говорить первым

В спортивной индустрии такие формируют смысл.
Аналитики, редакторы, сценаристы.

Ты входишь в индустрию через контент и глубину.""",
    "2": """<b>Компания у барной стойки</b>

Ты входишь в индустрию через людей.
Легко начинаешь разговор и быстро становишься частью любой среды

Для тебя нетворкинг — это способ существования.
SMM-менеджер, комьюнити-менеджер, продюсер событий

В мире спорта, где всё держится на связях,
ты сразу оказываешься внутри процессов.""",
    "3": """<b>Спикер у экрана</b>

Ты входишь в индустрию через амбицию.
Тебе важнее доступ к сильным людям и знаниям, чем комфорт

Ты идёшь к тем, кто принимает решения — потому что хочешь быть среди них.
Бренд-менеджер, креативный директор, Head of Media

Ты быстро оказываешься там, где формируется стратегия.""",
    "4": """<b>Стол с визитками</b>

Ты входишь в индустрию через действия.
Чётко понимаешь, зачем ты здесь и какой результат тебе нужен.

Маркетолог, менеджер по партнёрствам, продюсер.

Пока другие ищут себя — ты собираешь вокруг себя систему возможностей.""",
    "5": """<b>Двое в креслах</b>

Ты входишь в индустрию через доверие
Выбираешь разговоры, которые имеют вес и могут что-то изменить

Креативный продюсер, арт-директор, стратег.

Ты строишь связи и позиции, которые невозможно занять случайно.""",
}

FALLBACK_RESPONSE = """Здесь работают только цифры
Посмотри на картинку и напиши номер — от 1 до 5"""


def get_required_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


def get_optional_int_env(name: str) -> Optional[int]:
    value = os.getenv(name)
    if not value:
        return None
    return int(value)


def get_bool_env(name: str) -> bool:
    return os.getenv(name, "").lower() in {"1", "true", "yes", "on"}


def normalize_answer(text: Optional[str]) -> Optional[str]:
    if not text:
        return None

    normalized = text.strip()
    match = re.fullmatch(r"([1-5])[\s.。]*", normalized)
    if not match:
        return None

    return match.group(1)


def belongs_to_target_post(message: Message, post_id: int, target_chat_id: Optional[int]) -> bool:
    if message.from_user and message.from_user.is_bot:
        return False

    if target_chat_id is not None and message.chat.id != target_chat_id:
        return False

    possible_root_ids = set()

    if message.message_thread_id:
        possible_root_ids.add(message.message_thread_id)

    if message.reply_to_message:
        possible_root_ids.add(message.reply_to_message.message_id)

    return post_id in possible_root_ids


async def main() -> None:
    logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))

    token = get_required_env("BOT_TOKEN")
    post_id = int(get_required_env("POST_ID"))
    target_chat_id = get_optional_int_env("TARGET_CHAT_ID")
    debug_updates = get_bool_env("DEBUG_UPDATES")

    bot = Bot(token=token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()

    @dp.message(F.text)
    async def handle_comment(message: Message) -> None:
        if debug_updates:
            logging.info(
                "message chat_id=%s message_id=%s thread_id=%s reply_to=%s text=%r",
                message.chat.id,
                message.message_id,
                message.message_thread_id,
                message.reply_to_message.message_id if message.reply_to_message else None,
                message.text,
            )

        if not belongs_to_target_post(message, post_id, target_chat_id):
            return

        answer_key = normalize_answer(message.text)
        answer = RESPONSES.get(answer_key, FALLBACK_RESPONSE)

        await message.reply(answer)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
