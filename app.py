import asyncio
import os

from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

from middlewares.database_middleware import DataBaseSession

from database.engine import create_db, drop_db, session_maker

from handlers.user_private import user_private_router

from commands.commands import private


bot = Bot(token=os.getenv('TELEGRAM_TOKEN'), parse_mode=ParseMode.HTML)

dp = Dispatcher()
dp.include_router(user_private_router)


async def on_startup(bot):

    run_param = False
    if run_param:
        await drop_db()

    await create_db()


async def main():
    dp.startup.register(on_startup)

    dp.update.middleware(DataBaseSession(session_pool=session_maker))

    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_my_commands(commands=private, scope=types.BotCommandScopeAllPrivateChats())
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

asyncio.run(main())