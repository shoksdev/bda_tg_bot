import asyncio

from aiogram import F, types, Router
from aiogram.filters import CommandStart, Command
from sqlalchemy.ext.asyncio import AsyncSession

from api.wildberries import get_info_about_product
from database.orm_queries import orm_add_application, orm_get_applications, orm_get_application
from filters.chat_types import ChatTypeFilter
from keyboards.inline import get_callback_btns
from keyboards.reply import get_keyboard

user_private_router = Router()
user_private_router.message.filter(ChatTypeFilter(["private"]))

USER_KEYBOARD = get_keyboard(
    'Получить информацию по товару',
    'Остановить уведомления',
    'Получить информацию из БД',
    placeholder="Выберите действие",
    sizes=(3,),
)

USER_INLINE = get_callback_btns(
    btns={
        "Подписаться": "subscribe",
    }
)


@user_private_router.message(CommandStart())
async def start_command(message: types.Message):
    await message.answer("Что хотите сделать?", reply_markup=USER_KEYBOARD)


@user_private_router.message(Command('menu'))
async def menu_command(message: types.Message):
    await message.answer("Что хотите сделать?", reply_markup=USER_KEYBOARD)


@user_private_router.message(F.text == 'Получить информацию из БД')
async def get_product_article(message: types.Message, session: AsyncSession):
    applications = (await orm_get_applications(session))[:5]
    for application in applications:
        await message.answer(f'Артикул товара: {application.product_article}\nID пользователя: {application.user_id}'
                             f'\nДата и время создания: {application.created}')


@user_private_router.message(F.text == "Получить информацию по товару")
async def get_product_article(message: types.Message):
    await message.answer(
        "Введите артикул товара", reply_markup=types.ReplyKeyboardRemove()
    )


@user_private_router.message(F.text.isdigit())
async def get_product_article(message: types.Message, session: AsyncSession):
    product_article = int(message.text)
    try:
        all_stocks_quantity, product_name, product_price, product_rating = get_info_about_product(product_article)
        message_text = (f'Название товара: {product_name}\nАртикул товара: {product_article}\n'
                        f'Цена товара: {product_price} рублей\nРейтинг товара: {product_rating}'
                        f'\nКоличество товара на всех складах: {all_stocks_quantity}')
        await message.answer(
            message_text,
            reply_markup=get_callback_btns(
                btns={
                    "Подписаться": f"subscribe_{product_article}",
                }
            ))
        await orm_add_application(session, message.from_user.id, product_article, message_text)
    except IndexError:
        await message.answer('Такого товара нет, введите другой артикул!')
        return


@user_private_router.message(F.text != '/menu')
async def get_product_article_exception_error(message: types.Message):
    await message.answer("Вы ввели недопустимые данные, введите артикул товара")


@user_private_router.callback_query(F.data.startswith("subscribe"))
async def subscribe_callback(callback: types.CallbackQuery, bot, session: AsyncSession):
    product_article = int(callback.data.split("_")[-1])
    user_id = callback.from_user.id
    message_text = (await orm_get_application(session, user_id, product_article))[-1].message_for_mailing
    await callback.answer("Вы успешно подписались на уведомления!")
    await send_message_periodically(bot, user_id, message_text)


async def send_message_periodically(bot, chat_id, message):
    while True:
        await bot.send_message(chat_id, message)
        await asyncio.sleep(5)
