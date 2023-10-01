# Точка входа. Запускаем именно этот файл. В on_startup закидываем все функции для их загрузки.
async def on_startup(dp):

    # Фильтры
    import filters
    filters.setup(dp)

    # База данных
    from loader import db
    from utils.db_api.db_gino import on_startup
    print('Подключение к PostgreSQL')
    await on_startup(dp)

    # print('Удаление базы данных')
    # await db.gino.drop_all()

    print('Создание таблиц')
    await db.gino.create_all()
    print('Готово')

    # Отправка админам о запуске бота.
    from utils.notify_admins import on_startup_notify
    await on_startup_notify(dp)

    # Установка дефолтных команд
    from utils.set_bot_commands import set_default_commands
    await set_default_commands(dp)

    print('Бот запущен')

if __name__ == '__main__':
    from aiogram import executor
    from handlers import dp

    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)