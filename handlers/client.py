"""Ініціалізація модулів Initialization of modules"""
from aiogram import types, Dispatcher
from create_bot import dp, bot

# @dp.message_handler(commands=['start', 'help'])
async def command_start(massage : types.message): # Функція, виводить інформацію про можливості бота; The function displays information about the bot's capabilities
    try: # Перевірка чи є вже чат розмови з ботом; Checking if there is already a chat conversation with the bot
        await bot.send_message(massage.from_user.id, 
        'Бот дозволяє за допомогою навігаційних кнопок використовувати різні функції.' + 
        '\nФункції бота:\n- Команда /add_product - додає кіль-ть (шт.), назву і вагу (г.) у істрію спожитих продуктів.' + 
        '\n- Команда /del_product - видаляє останній доданий продукт з історії спожитих продуктів.' + 
        '\n- Команда /view_day - показує всю інформацію про спожиті продукти за день та розраховує загальний рівень фенілаланіну.' + 
        '\n- Команда /view_week - показує всю інформацію про спожиті продукти за тиждень та розраховує загальний рівень фенілаланіну.' + 
        '\n- Команда /view_month - показує всю інформацію про спожиті продукти за місяць та розраховує загальний рівень фенілаланіну.')
        await massage.delete()
    except:
        await massage.reply('Спілкування з ботом через особисті повідомлення, напишіть йому: \nhttps://t.me/PKUDiaryBot')

# @dp.message_handler(commands=['add_product'])
async def add_product_cm(massage : types.message):
    await bot.send_message(massage.from_user.id, 
        'Продукт успішно додано!')

# @dp.message_handler(commands=['del_product'])
async def del_product_cm(massage : types.message):
    await bot.send_message(massage.from_user.id, 
        'Продукт успішно видалено!')

# @dp.message_handler(commands=['view_day'])
async def view_day_cm(massage : types.message):
    await bot.send_message(massage.from_user.id, 
        'Перегляд історії спожитих продуктів за день:')

# @dp.message_handler(commands=['view_week'])
async def view_week_cm(massage : types.message):
    await bot.send_message(massage.from_user.id, 
        'Перегляд історії спожитих продуктів за тиждень:')

# @dp.message_handler(commands=['view_month'])
async def view_month_cm(massage : types.message):
    await bot.send_message(massage.from_user.id, 
        'Перегляд історії спожитих продуктів за місяць:')

def register_handlers_client(dp : Dispatcher): # Декоратор, обробка подій; Deorator, event handler
    dp.register_message_handler(command_start, commands=['start', 'help'])
    dp.register_message_handler(add_product_cm, commands=['add_product'])
    dp.register_message_handler(del_product_cm, commands=['del_product'])
    dp.register_message_handler(view_day_cm, commands=['view_day'])
    dp.register_message_handler(view_week_cm, commands=['view_week'])
    dp.register_message_handler(view_month_cm, commands=['view_month'])