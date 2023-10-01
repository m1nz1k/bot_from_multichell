import os

# Загружаем токен из .env
from dotenv import load_dotenv
load_dotenv()
BOT_TOKEN = str(os.getenv("BOT_TOKEN"))

# В списке указываем id админов.
admins = [
    379563196,
]


# Данные БД подгружаются с .env (Опять же безопастность)
ip = os.getenv('ip')
PGUSER = str(os.getenv('PGUSER'))
PGPASSWORD = str(os.getenv('PGPASSWORD'))
DATABASE = str(os.getenv('DATABASE'))

POSTGRES_URI = f'postgresql://{PGUSER}:{PGPASSWORD}@{ip}/{DATABASE}'