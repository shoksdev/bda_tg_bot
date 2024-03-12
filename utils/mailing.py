import asyncio

from aiogram import Bot

mailing_user_states = {}


async def mailing(bot: Bot, user_id: int, message: str, delay: int):
    """Отправляем сообщение пользователю каждые 5 минут"""

    while mailing_user_states.get(user_id, False):
        await bot.send_message(user_id, message)
        await asyncio.sleep(delay)
