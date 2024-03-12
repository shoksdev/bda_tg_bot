import asyncio
import os

from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import BotCommand
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

from middlewares.database import DataBaseMiddleware

from database.engine import create_database, session_maker

from handlers.user_private import user_private_router


bot = Bot(token=os.getenv('TELEGRAM_TOKEN'), default=DefaultBotProperties(parse_mode=ParseMode.HTML))

dp = Dispatcher()
dp.include_router(user_private_router)

# Создаём список команд для бота
private = [
    BotCommand(command='menu', description='Посмотреть меню'),
]

async def on_startup(bot):
    """При запуске бота создаём базу данных"""

    # await drop_database()

    await create_database()


async def main():
    dp.startup.register(on_startup)
    dp.update.middleware(DataBaseMiddleware(session_pool=session_maker))
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_my_commands(commands=private, scope=types.BotCommandScopeAllPrivateChats())
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

asyncio.run(main())
