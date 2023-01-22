"""Ініціалізація модулів Initialization of modules"""
from aiogram.utils import executor
from create_bot import dp
from handlers import client, admin

async def on_startup(_):
    print('Бот вийшов у онлайн.')

client.register_handlers_client(dp)
"""Клієнтська частина"""

"""Адмінська частина"""
"""Загальна частина"""
# @dp.message_handler()
# async def echo_send(massage : types.message):
#     if massage.text == 'Додати продукт':
#         await massage.answer('Продукт успішно додано!')
#     # await massage.answer(massage.text)
#     elif massage.text == 'Видалити продукт':
#         await bot.send_message(massage.from_user.id, 'Продукт успішно видалено!')
#     # Код команд на перегляд інформації у базі даних.
#     elif massage.text == 'Переглянути історію спожитих продуктів за день':
#         await massage.answer('Перегляд історії спожитих продуктів за день:')
#     elif massage.text == 'Переглянути історію спожитих продуктів за тиждень':
#         await massage.answer('Перегляд історії спожитих продуктів за тиждень:')
#     elif massage.text == 'Переглянути історію спожитих продуктів за місяць':
#         await massage.answer('Перегляд історії спожитих продуктів за місяць:')

executor.start_polling(dp, skip_updates=True, on_startup=on_startup) # Команда старта бота; Bot start command