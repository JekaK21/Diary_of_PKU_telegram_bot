"""Ініціалізація модулів Initialization of modules"""
from aiogram.utils import executor
from create_bot import dp
from handlers import client, admin
from database import pku_db
# Файл входу, старт бота Login file, start the bot
async def on_startup(_):
    print('Бот вийшов у онлайн.')
    pku_db.sql_start()

client.register_handlers_client(dp)
admin.register_handlers_admin(dp)

executor.start_polling(dp, skip_updates=True, on_startup=on_startup) # Команда старта бота; Bot start command