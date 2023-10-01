from aiogram import types
from loader import dp
from keyboards.default import kb_menu
from filters import IsPrivate
from utils.db_api import quick_commands as commands

@dp.message_handler(IsPrivate(), text='/start')
async def command_start(message: types.Message):
        user = await commands.select_user(message.from_user.id)
        await commands.add_user(user_id=message.from_user.id,
                                status='active',
                                username=message.from_user.username,
                                first_name=message.from_user.first_name,
                                last_name=message.from_user.last_name)
        await message.answer('Привет. С помощью этого бота ты сможешь арендовать дыньку.', reply_markup=kb_menu)
