from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_inline_keyboard(
        *,
        btns: dict[str, str],
        sizes: tuple[int] = (2,)
):
    """Генерируем клавиатуру из inline кнопок"""
    keyboard = InlineKeyboardBuilder()

    for text, data in btns.items():
        keyboard.add(InlineKeyboardButton(text=text, callback_data=data))

    return keyboard.adjust(*sizes).as_markup()
