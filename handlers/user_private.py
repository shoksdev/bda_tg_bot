from aiogram import F, types, Router
from aiogram.filters import CommandStart, Command
from sqlalchemy.ext.asyncio import AsyncSession

from api.wildberries import get_info_about_product
from database.orm_queries import orm_add_application, orm_get_applications
from filters.chat_types import ChatTypeFilter
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
        await message.answer(f'Название товара: {product_name}\nАртикул товара: {product_article}'
                             f'\nЦена товара: {product_price} рублей\nРейтинг товара: {product_rating}'
                             f'\nКоличество товара на всех складах: {all_stocks_quantity}')
        await orm_add_application(session, message.from_user.id, product_article)
    except IndexError:
        await message.answer('Такого товара нет, введите другой артикул!')
        return


@user_private_router.message(F.text != '/menu')
async def get_product_article_exception_error(message: types.Message):
    await message.answer("Вы ввели недопустимые данные, введите артикул товара")
