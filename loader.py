# Подгружаем хранилища, диспетчера, бота и все-все в dp
from aiogram import Bot, types, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from utils.db_api.db_gino import db

from data import config

# Переменная бота с токеном.
bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)

# Хранилище в оперативной памяти.
storage = MemoryStorage()

# Диспетчер
dp = Dispatcher(bot, storage=storage)

__all__ = ['bot', 'storage', 'dp', 'db']