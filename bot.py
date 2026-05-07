import asyncio
import json
import logging
import os
import random
import re
from typing import Optional

from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import Message


RESPONSES = {
    "1": [
        """<b>Одиночка с телефоном</b>

<b>Вайб:</b> «Я видел это в Wyscout еще до того, как это стало мейнстримом».

<b>Стиль «Аналитик с окраины»:</b>
Пока на трибунах жгут файеры, ты в телефоне сверяешь тепловые карты. Твой путь — аналитический штаб «Крыльев Советов». Найдешь таланта в ФНЛ-2 и докажешь, что по xG он круче Холанда.""",
        """<b>Одиночка с телефоном</b>

<b>Вайб:</b> «Я видел это в Wyscout еще до того, как это стало мейнстримом».

<b>Стиль «Инсайдер из телеги»:</b>
Ты тот самый парень, от которого ждут пост «Done deal! 🏁». Твой телефон — это пульт от трансферного рынка. Тебе бы вести анонимный канал про интриги РПЛ, от которого икается всем агентам.""",
        """<b>Одиночка с телефоном</b>

<b>Вайб:</b> «Я видел это в Wyscout еще до того, как это стало мейнстримом».

<b>Стиль «Тактический зануда»:</b>
Тебе не интересно, кто забил — тебе интересно, почему опорник не перекрыл линию паса. Твоя тема — делать разборы для Sports.ru или Okko, после которых зрители наконец поймут, что такое «ложная девятка».""",
    ],
    "2": [
        """<b>Компания у барной стойки</b>

<b>Вайб:</b> «Знаю всех, от повара на базе до президента лиги».

<b>Стиль «SMM Спартака»:</b>
Ты мастер ловить хайп на ровном месте. Можешь сделать виральный мем из судейской ошибки или заставить легионера выучить частушку. Твоя стихия — самый дерзкий медиа-отдел страны.""",
        """<b>Компания у барной стойки</b>

<b>Вайб:</b> «Знаю всех, от повара на базе до президента лиги».

<b>Стиль «Агент-перехватчик»:</b>
Ты зашел за соком, а вышел с контрактом на три года. Твой нетворкинг — это искусство. Твое место на переговорах в лобби пятизвездочных отелей, где решаются судьбы чемпионства.""",
        """<b>Компания у барной стойки</b>

<b>Вайб:</b> «Знаю всех, от повара на базе до президента лиги».

<b>Стиль «Медиалига»:</b>
Для тебя футбол без трэш-тока — это физкультура. Твой вайб — «Амкал» или 2DROTS. Ты залетишь в индустрию через микрофон, харизму и умение делать из матча шоу на миллионы просмотров.""",
    ],
    "3": [
        """<b>Спикер у экрана</b>

<b>Вайб:</b> «Я здесь, чтобы переписать правила игры».

<b>Стиль «CEO в режиме ожидания»:</b>
Ты не слушаешь спикера, ты оцениваешь его слабые стороны. Твой план — забрать это кресло через пару сезонов. Твои амбиции — уровень управления топ-клубом РПЛ, где нужна железная рука.""",
        """<b>Спикер у экрана</b>

<b>Вайб:</b> «Я здесь, чтобы переписать правила игры».

<b>Стиль «Архитектор мерча»:</b>
Тебе мало просто побед, ты хочешь, чтобы клуб был самым стильным. Твой путь — Head of Creative. Ты тот, кто переоденет команду из скучного адидаса в коллаб с модным домом и продаст это как искусство.""",
        """<b>Спикер у экрана</b>

<b>Вайб:</b> «Я здесь, чтобы переписать правила игры».

<b>Стиль «Реформатор»:</b>
Тебе тесно в текущих форматах. Ты пришел внедрять чипы в мячи и VR-трансляции. Твоя цель — сделать футбол понятным поколению зумеров, даже если олдскульные фанаты будут против.""",
    ],
    "4": [
        """<b>Стол с визитками</b>

<b>Вайб:</b> «Меньше слов, больше цифр в годовом отчете».

<b>Стиль «Коммерческий хищник»:</b>
Ты видишь рекламную площадь даже на гетрах футболистов. Твой идеальный рабочий день — закрыть сделку с букмекером, которая покроет бюджет клуба на сезон. Прямая дорога в коммерческий отдел «Зенита».""",
        """<b>Стол с визитками</b>

<b>Вайб:</b> «Меньше слов, больше цифр в годовом отчете».

<b>Стиль «Директор Match Day»:</b>
Для тебя футбол начинается с парковки и заканчивается очередью за хот-догами. Ты знаешь, как забить трибуны до отказа даже в понедельник в -10°C. Твой результат — аншлаги и выручка.""",
        """<b>Стол с визитками</b>

<b>Вайб:</b> «Меньше слов, больше цифр в годовом отчете».

<b>Стиль «Партнер по спецпроектам»:</b>
Ты умеешь скрещивать нескрещиваемое. Привести авиакомпанию в спонсоры регионального клуба? Легко. Ты строишь систему, в которой футбол — это прибыльный бизнес, а не дотация.""",
    ],
    "5": [
        """<b>Двое в креслах</b>

<b>Вайб:</b> «Решаем вопросы, пока остальные шумят».

<b>Стиль «Спортивный дир»:</b>
Минимум прессы, максимум влияния. Ты из тех, кто выбирает тренера по философии, а не по фамилии. Твой ориентир — европейская модель управления, где всё решает долгосрочная стратегия.""",
        """<b>Двое в креслах</b>

<b>Вайб:</b> «Решаем вопросы, пока остальные шумят».

<b>Серый кардинал:</b>
Тебе не нужно представляться, тебя и так знают те, кто надо. Ты строишь связи годами и решаешь конфликты одним звонком. Твой вход в индустрию — через элитный консалтинг и доверие владельцев.""",
        """<b>Двое в креслах</b>

<b>Вайб:</b> «Решаем вопросы, пока остальные шумят».

<b>Стиль «Хранитель традиций»:</b>
Ты создаешь ДНК клуба. Тебе важно, чтобы игроки понимали, за какой ромб они бьются. Твоя работа — превратить обычную команду в «клуб-семью» с миллионами преданных фанатов.""",
    ],
}

FALLBACK_RESPONSE = """Здесь работают только цифры
Посмотри на картинку и напиши номер — от 1 до 5"""

SUBSCRIBE_REMINDER = """Не забудь подписаться на наши проекты
– Креативная работа в футболе: @rafl_work
– Эстетика русского футбола: @raflmedia"""

valid_answer_counts: dict[tuple[int, int, int], int] = {}
STATE_FILE = "state.json"
DEFAULT_POST_MARKER = "К кому первым подойдешь на нетворкинге?"


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


def get_int_env(name: str) -> Optional[int]:
    value = os.getenv(name)
    if not value:
        return None
    return int(value)


def load_state() -> dict:
    try:
        with open(STATE_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


def save_state(state: dict) -> None:
    with open(STATE_FILE, "w", encoding="utf-8") as file:
        json.dump(state, file, ensure_ascii=False, indent=2)


def get_text_for_marker(message: Message) -> str:
    return message.text or message.caption or ""


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


def belongs_to_active_post(message: Message, state: dict, fallback_post_id: Optional[int], fallback_chat_id: Optional[int]) -> bool:
    active_post_id = state.get("active_post_id") or fallback_post_id
    active_chat_id = state.get("active_chat_id") or fallback_chat_id

    if active_post_id is None:
        return False

    return belongs_to_target_post(message, int(active_post_id), active_chat_id)


def activate_discussion_post_if_marker(message: Message, state: dict, post_marker: str, target_chat_id: Optional[int]) -> bool:
    if target_chat_id is not None and message.chat.id != target_chat_id:
        return False

    text = get_text_for_marker(message)
    if post_marker.casefold() not in text.casefold():
        return False

    state["active_post_id"] = message.message_id
    state["active_chat_id"] = message.chat.id
    save_state(state)
    logging.info(
        "activated discussion post chat_id=%s post_id=%s marker=%r",
        message.chat.id,
        message.message_id,
        post_marker,
    )
    return True


def should_add_subscribe_reminder(message: Message) -> bool:
    if not message.from_user:
        return False

    counter_key = (
        message.chat.id,
        message.message_thread_id or 0,
        message.from_user.id,
    )
    valid_answer_counts[counter_key] = valid_answer_counts.get(counter_key, 0) + 1

    return valid_answer_counts[counter_key] % 3 == 0


async def main() -> None:
    logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))

    token = get_required_env("BOT_TOKEN")
    fallback_post_id = get_int_env("POST_ID")
    target_chat_id = get_optional_int_env("TARGET_CHAT_ID")
    debug_updates = get_bool_env("DEBUG_UPDATES")
    source_channel_id = get_optional_int_env("SOURCE_CHANNEL_ID")
    post_marker = os.getenv("POST_MARKER", DEFAULT_POST_MARKER)
    state = load_state()

    bot = Bot(token=token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()

    @dp.channel_post()
    async def handle_channel_post(message: Message) -> None:
        if source_channel_id is not None and message.chat.id != source_channel_id:
            return

        text = get_text_for_marker(message)
        if post_marker.casefold() not in text.casefold():
            return

        state["active_post_id"] = message.message_id
        state["active_channel_id"] = message.chat.id
        state.pop("active_chat_id", None)
        save_state(state)
        logging.info(
            "activated channel post channel_id=%s post_id=%s marker=%r",
            message.chat.id,
            message.message_id,
            post_marker,
        )

    @dp.message()
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

        if activate_discussion_post_if_marker(message, state, post_marker, target_chat_id):
            return

        if not message.text:
            return

        if not belongs_to_active_post(message, state, fallback_post_id, target_chat_id):
            return

        if state.get("active_chat_id") != message.chat.id:
            state["active_chat_id"] = message.chat.id
            save_state(state)
            logging.info(
                "linked discussion chat active_chat_id=%s active_post_id=%s",
                message.chat.id,
                state.get("active_post_id") or fallback_post_id,
            )

        answer_key = normalize_answer(message.text)
        answer_options = RESPONSES.get(answer_key)
        answer = random.choice(answer_options) if answer_options else FALLBACK_RESPONSE
        if answer_key and should_add_subscribe_reminder(message):
            answer = f"{answer}\n\n{SUBSCRIBE_REMINDER}"

        await message.reply(answer)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
