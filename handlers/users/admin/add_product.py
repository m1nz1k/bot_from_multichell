from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from loader import dp, bot
from keyboards.default import kb_menu
from filters import IsPrivate
from utils.db_api import product_commands as commands
from data.config import admins
from states.product import bot_product
from states.product_dell import bot_dell_product
from aiogram.dispatcher import FSMContext



in_kb = InlineKeyboardMarkup(row_width=2)
in_kb.insert(InlineKeyboardButton(text='Добавляем дыньку', callback_data='add_product'))
in_kb.insert(InlineKeyboardButton(text='Удалить дыньку', callback_data='dell_product'))


@dp.message_handler(IsPrivate(), text='Дыньки', chat_id=admins)
async def edit_price(message: types.Message):
    await message.answer('Выбирай сынок:', reply_markup=in_kb)






@dp.callback_query_handler(lambda c: c.data == 'dell_product', state="*")
async def delete_product_callback(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.answer()
    await bot_dell_product.dell.set()
    await show_all_products(callback_query.message.chat.id)


async def show_all_products(chat_id):
    try:
        products = await commands.Product.query.gino.all()
        if not products:
            await bot.send_message(chat_id, "Список продуктов пуст.")
        else:
            message = "Список продуктов:\n"
            for product in products:
                message += f"{product.id}, {product.name}, {product.size}, {product.color}\n"
            await bot.send_message(chat_id, message)
    except Exception as e:
        print(f"Ошибка при получении списка продуктов: {e}")


@dp.message_handler(lambda message: message.text.isdigit(), state=bot_dell_product.dell)
async def delete_product_by_id(message: types.Message, state: FSMContext):
    product_id = int(message.text)
    product = await commands.Product.get(product_id)
    if product:
        await product.delete()
        await message.answer(f"Продукт с ID {product_id} успешно удален.")
    else:
        await message.answer(f"Продукт с ID {product_id} не найден.")

    await state.finish()






@dp.callback_query_handler(lambda c: c.data == 'add_product')
async def start_product_name(callback_query: types.CallbackQuery):
    await bot_product.name.set()
    await callback_query.message.answer("Укажите название дыньки")



@dp.message_handler(state=bot_product.name)
async def process_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text

    await message.answer("Введите размер продукта:")
    await bot_product.next()

@dp.message_handler(state=bot_product.size)
async def process_size(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['size'] = message.text

    await message.answer("Введите цвет продукта:")
    await bot_product.next()

@dp.message_handler(state=bot_product.color)
async def process_color(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['color'] = message.text

    await message.answer("Отправьте фото продукта (как фото, не как файл):")
    await bot_product.next()

@dp.message_handler(content_types=types.ContentTypes.PHOTO, state=bot_product.photo)
async def process_photo(message: types.Message, state: FSMContext):
    photo_id = message.photo[-1].file_id
    async with state.proxy() as data:
        data['photo'] = photo_id
        name = data['name']
        size = data['size']
        color = data['color']
        photo_id = data['photo']

    if await commands.create_product(name=name, size=size, color=color, status='created', rent_user_id=None, photo_id=photo_id):
        await message.answer(f"Продукт {name} успешно добавлен в базу данных.")
    else:
        await message.answer("Произошла ошибка при добавлении продукта в базу данных.")

    await state.finish()