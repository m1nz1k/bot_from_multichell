
import logging

from asyncpg import UniqueViolationError
from utils.db_api.schemas.product import Product

# Создаем таблицу.
async def create_product(name: str, size: str, color: str, status: str, rent_user_id: int, photo_id: str):
    try:
        product = Product(name=name, size=size, color=color, status=status, rent_user_id=rent_user_id, photo_id=photo_id)
        await product.create()
        return product.id
    except UniqueViolationError:
        print('Продукт дынька не создан.')
        return False


# Указываем статус создано.
async def select_product(status: str = 'created'):
    product = await Product.query.where(Product.status == status).gino.first()
    return product

# Поиск по id таблицы.
async def select_product_by_id(id: int):
    product = await Product.query.where(Product.id == id).gino.first()
    return product
# Поиск таблицы по id юзера.

async def select_product_by_user_id(user_id: int):
    product = await Product.query.where(Product.rent_user_id == user_id).gino.first()
    return product

# Удаление дынек по id
async def delete_product_by_id(product_id: int):
    try:
        product = await Product.get(product_id)
        if product:
            await product.delete()
            return True
        else:
            print(f"Продукт с ID {product_id} не найден.")
            return False
    except Exception as e:
        print(f"Ошибка при удалении продукта с ID {product_id}: {e}")
        return False

async def update_product_rent_user_id_one(product_id: int, user_id: int):
    try:
        # Получаем продукт по его ID
        product = await select_product_by_id(product_id)



        if product:
            await Product.update.values(rent_user_id=user_id).where(Product.id == product_id).gino.status()
            await Product.update.values(rent_user_id=user_id, status='rent').where(Product.id == product_id).gino.status()

            return True
        else:
            logging.warning(f"Продукт с ID {product_id} не найден.")
            return False
    except Exception as e:
        logging.error(f"Произошла ошибка при обновлении `rent_user_id` продукта: {e}")
        return False
# Функция для получения списка арендованных дынь пользователя
async def get_rented_products(user_id: int):
    try:
        products = await Product.query.where(Product.rent_user_id == user_id).gino.all()
        return products
    except Exception as e:
        logging.error(f"Произошла ошибка при получении арендованных дынь: {e}")
        return []

async def update_product_rent_user_id(product_id: int, user_id: int, rent_user_id=None, status='created'):
    try:
        # Получаем продукт по его ID
        product = await select_product_by_id(product_id)

        if product:
            # Устанавливаем новые значения для полей `rent_user_id` и `status`
            await Product.update.values(rent_user_id=rent_user_id, status=status).where(Product.id == product_id).gino.status()
            return True
        else:
            logging.warning(f"Продукт с ID {product_id} не найден.")
            return False
    except Exception as e:
        logging.error(f"Произошла ошибка при обновлении `rent_user_id` продукта: {e}")
        return False



