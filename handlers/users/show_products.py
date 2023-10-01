from aiogram import types
from loader import dp
from keyboards.default import kb_menu
from filters import IsPrivate
from utils.db_api import product_commands as commands
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Обработчик текстового сообщения "Список дынек"
@dp.message_handler(lambda message: message.text.lower() == 'список дынек', state="*")
async def list_dines(message: types.Message):
    try:
        # Получаем список всех дынь с rent_user_id=None
        products = await commands.Product.query.where(commands.Product.rent_user_id.is_(None)).gino.all()

        if not products:
            await message.answer("Список дынек пуст.")
        else:
            for product in products:
                # Создаем сообщение с информацией о каждой дыне
                text = f"Название - {product.name}\n" \
                       f"Размер - {product.size}\n" \
                       f"Цвет - {product.color}"

                # Создаем инлайн-кнопку "Взять в аренду"
                keyboard = InlineKeyboardMarkup()
                keyboard.add(InlineKeyboardButton(text="Взять в аренду", callback_data=f'rent_product_{product.id}'))

                # Отправляем сообщение с информацией о дыне и кнопкой "Взять в аренду"
                await message.answer_photo(product.photo_id, caption=text, reply_markup=keyboard)

    except Exception as e:
        print(f"Ошибка при получении списка дынек: {e}")


@dp.callback_query_handler(lambda c: c.data.startswith('rent_product_'))
async def rent_product(callback_query: types.CallbackQuery):
    try:
        product_id = int(callback_query.data.split('_')[-1])
        user_id = callback_query.from_user.id

        # Обновляем `rent_user_id` для продукта
        if await commands.update_product_rent_user_id_one(product_id, user_id):
            await callback_query.answer("Вы успешно арендовали дыню.")
        else:
            await callback_query.answer("Продукт с указанным ID не существует или произошла ошибка при аренде.")

    except ValueError:
        await callback_query.answer("Произошла ошибка при аренде дыни.")

