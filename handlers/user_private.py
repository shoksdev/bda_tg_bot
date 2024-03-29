from aiogram import F, types, Router
from aiogram.filters import CommandStart, Command
from sqlalchemy.ext.asyncio import AsyncSession

from api.wildberries import get_info_about_product
from database.orm_queries import orm_add_application, orm_get_applications, orm_get_application
from filters.chat_types import ChatTypeFilter
from keyboards.inline import get_inline_keyboard
from keyboards.reply import get_reply_keyboard
from utils.mailing import mailing, mailing_user_states

user_private_router = Router()
user_private_router.message.filter(ChatTypeFilter(['private']))

USER_KEYBOARD = get_reply_keyboard(
    'Получить информацию по товару',
    'Остановить уведомления',
    'Получить информацию из БД',
    placeholder="Выберите действие",
    sizes=(2,),
)

@user_private_router.message(CommandStart())
async def start_command(message: types.Message):
    """Обрабатываем команду /start"""

    await message.answer('Здравствуйте! Я ваш виртуальный помощник, чем я могу быть полезен?',
                         reply_markup=USER_KEYBOARD)


@user_private_router.message(Command('menu'))
async def menu_command(message: types.Message):
    """Обрабатываем команду /menu"""

    await message.answer('Здравствуйте! Я ваш виртуальный помощник, чем я могу быть полезен?',
                         reply_markup=USER_KEYBOARD)


@user_private_router.message(F.text == 'Получить информацию из БД')
async def get_applications_from_database(message: types.Message, session: AsyncSession):
    """Получаем последние 5 записей из базы данных и выводим их пользователю"""

    applications = (await orm_get_applications(session))[:5]
    for application in applications:
        await message.answer(f'Артикул товара: {application.product_article}\nID пользователя: {application.user_id}'
                             f'\nДата и время создания: {application.created}')


@user_private_router.message(F.text == 'Остановить уведомления')
async def stop_mailing(message: types.Message):
    """Останавливаем рассылку сообщений определенному пользователю"""

    user_id = message.from_user.id
    if mailing_user_states.get(user_id, False):
        await message.answer('Рассылка сообщений остановлена!')
        mailing_user_states[user_id] = False
    else:
        await message.answer('Рассылка сообщений уже остановлена!')


@user_private_router.message(F.text == 'Получить информацию по товару')
async def get_product_info_button(message: types.Message):
    """Инициализируем получение информации о товаре"""

    await message.answer(
        'Введите артикул товара', reply_markup=types.ReplyKeyboardRemove()
    )


@user_private_router.message(F.text.isdigit())
async def get_product_info(message: types.Message, session: AsyncSession):
    """
    Пользователь вводит артикул товара и бот выводит ему информацию о товаре, предлагает подписаться
    и добавляет заявку в базу данных
    """

    product_article = int(message.text)
    try:
        all_stocks_quantity, product_name, product_price, product_rating = get_info_about_product(product_article)
        message_text = (f'Название товара: {product_name}\nАртикул товара: {product_article}\n'
                        f'Цена товара: {product_price} рублей\nРейтинг товара: {product_rating}'
                        f'\nКоличество товара на всех складах: {all_stocks_quantity}')
        await message.answer(
            message_text,
            reply_markup=get_inline_keyboard(
                btns={
                    'Подписаться': f'subscribe_{product_article}',
                }
            ))
        await orm_add_application(session, message.from_user.id, product_article, message_text)
    except IndexError:
        await message.answer('Такого товара нет, введите другой артикул!')
        return


@user_private_router.message(F.text != '/menu')
async def get_product_info_exception_error(message: types.Message):
    """Обрабатываем ситуацию в которой пользователю отправил не текст"""

    await message.answer('Вы ввели недопустимые данные, введите артикул товара')


@user_private_router.callback_query(F.data.startswith('subscribe'))
async def subscribe_on_mailing_callback(callback: types.CallbackQuery, bot, session: AsyncSession):
    """Обрабатываем callback с подпиской и начинаем отправку сообщений пользователю"""

    product_article = int(callback.data.split("_")[-1])
    user_id = callback.from_user.id
    if not mailing_user_states.get(user_id, False):
        mailing_user_states[user_id] = True
        message_text = (await orm_get_application(session, user_id, product_article))[-1].message_for_mailing
        await callback.answer('Вы успешно подписались на рассылку уведомлений!')
        await mailing(bot, user_id, message_text, 300)
    else:
        await callback.message.answer('Рассылка сообщений уже запущена!')
