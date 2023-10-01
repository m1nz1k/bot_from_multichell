# Функции для работой с основной таблицей в БД: users.
from asyncpg import UniqueViolationError
from utils.db_api.db_gino import db
from utils.db_api.schemas.user import User
from datetime import datetime, date


# Добавление нового пользователя в БД
async def add_user(user_id: int, status: str, username: str, first_name: str, last_name: str):
    try:
        user = User(user_id=user_id, status=status, username=username, first_name=first_name, last_name=last_name)
        await user.create()
    except UniqueViolationError:
        print('Пользователь не добавлен.')


# Поиск всех юзеров.
async def select_all_users():
    users = await User.query.gino.all()
    return users


# Количество юзеров (общее)
async def count_users():
    count = await db.func.count(User.user_id).gino.scalar()
    return count

# Поиск первого юзера
async def select_user(user_id: int):
    user = await User.query.where(User.user_id == user_id).gino.first()
    return user

# Обновление статуса активности.
async def update_user_status(user_id, status):
    user = await select_user(user_id)
    await user.update(status=status).apply()

