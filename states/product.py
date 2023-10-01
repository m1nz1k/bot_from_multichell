

from aiogram.dispatcher.filters.state import StatesGroup, State


class bot_product(StatesGroup):
    name = State()
    size = State()
    color = State()
    photo = State()