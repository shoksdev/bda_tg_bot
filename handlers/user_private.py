from aiogram import F, types, Router
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command, or_f
from aiogram.utils.formatting import (
    as_list,
    as_marked_section,
    Bold,
)
from sqlalchemy.ext.asyncio import AsyncSession

from filters.chat_types import ChatTypeFilter

from keyboards.reply import get_keyboard

user_private_router = Router()
user_private_router.message.filter(ChatTypeFilter(["private"]))

USER_KEYBOARD = get_keyboard(
    "Получить информацию по товару",
    "Остановить уведомления",
    'Получить информацию из БД',
    placeholder="Выберите действие",
    sizes=(3,),
)


@user_private_router.message(CommandStart())
async def admin_features(message: types.Message):
    await message.answer("Что хотите сделать?", reply_markup=USER_KEYBOARD)