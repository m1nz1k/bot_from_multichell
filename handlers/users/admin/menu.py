# Комманда /menu для вывод менюшки только для администрации.
from aiogram import types
from aiogram.dispatcher.filters import Command

from data.config import admins
from keyboards.default import kb_menu
from keyboards.default.keyboard_menu import kb_menu_admin
from loader import dp

@dp.message_handler(Command("menu"), chat_id=admins)
async def menu(message: types.Message):
    await message.answer("Меню для админа", reply_markup=kb_menu_admin)