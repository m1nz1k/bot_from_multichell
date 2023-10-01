from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from loader import dp
from utils.db_api import product_commands as commands


@dp.message_handler(lambda message: message.text.lower() == 'мои арендованные дыньки')
async def my_rented_products(message: types.Message, state: FSMContext):
    user_id = message.from_user.id

    # Получаем список арендованных дынь пользователя
    rented_products = await commands.get_rented_products(user_id)

    if not rented_products:
        await message.answer("У вас нет арендованных дынь.")
        return

    for product in rented_products:
        caption = f"Название: {product.name}\n" \
                  f"Размер: {product.size}\n" \
                  f"Цвет: {product.color}"

        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton(text="Отказаться от аренды",
                                          callback_data=f'cancel_rent_{product.id}'))

        await message.answer_photo(photo=product.photo_id, caption=caption, reply_markup=keyboard)


@dp.callback_query_handler(lambda c: c.data.startswith('cancel_rent_'))
async def cancel_rent(callback_query: types.CallbackQuery, state: FSMContext):
    product_id = int(callback_query.data.split('_')[-1])
    user_id = callback_query.from_user.id

    # Отменяем аренду дыни
    if await commands.update_product_rent_user_id(product_id, user_id):
        await callback_query.answer("Вы успешно отказались от аренды дыни.")
    else:
        await callback_query.answer("Произошла ошибка при отказе от аренды дыни.")

    await state.finish()
