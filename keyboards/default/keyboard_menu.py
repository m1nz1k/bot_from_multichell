# Здесь создаем обычные кнопки для меню.
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Менюшка для всех
kb_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Список дынек'),
        ],
        [
            KeyboardButton(text='Мои арендованные дыньки'),
        ],
    ],
    resize_keyboard=True
)

# Админская менюшка

kb_menu_admin = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Дыньки'),
        ],

    ],
    resize_keyboard=True
)
