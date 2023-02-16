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
"""
{"message_id": 95, "from": {"id": 309565384, "is_bot": false, "first_name": "Женя 🇺🇦", "username": "JekaK21", "language_code": "uk"}, 
"chat": {"id": 309565384, "first_name": "Женя 🇺🇦", "username": "JekaK21", "type": "private"}, "date": 1674512522, "text": "/start", 
"entities": [{"type": "bot_command", "offset": 0, "length": 6}]}
"""

executor.start_polling(dp, skip_updates=True, on_startup=on_startup) # Команда старта бота; Bot start command