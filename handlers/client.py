"""Ініціалізація модулів Initialization of modules"""
from aiogram import types, Dispatcher
from create_bot import dp, bot
from keyboards import kb_client
from database import pku_db
from aiogram.types import ReplyKeyboardRemove

# @dp.message_handler(commands=['start', 'help'])
async def command_start(message : types.Message): # Функція, виводить інформацію про можливості бота; The function displays information about the bot's capabilities
    try: # Перевірка чи є вже чат розмови з ботом; Checking if there is already a chat conversation with the bot
        await bot.send_message(message.from_user.id, 
        'Бот дозволяє за допомогою навігаційних кнопок використовувати різні функції.' + 
        '\nФункції бота:\n- Команда /register_product - регіструє назву і вагу (г.) у історію спожитих продуктів.' + 
        '\n- Команда /add_product_to_list - додає ваш продукт у постійний список, коротку назву, повну назву, вагу (г.), білок (г.), фенілаланін (мг ФА).' + 
        '\n- Команда /del_product - видаляє останній доданий продукт з історії спожитих продуктів.' + 
        '\n- Команда /view_day - показує всю інформацію про спожиті продукти за день та розраховує загальний рівень фенілаланіну.' + 
        '\n- Команда /view_week - показує всю інформацію про спожиті продукти за тиждень та розраховує загальний рівень фенілаланіну.' + 
        '\n- Команда /view_month - показує всю інформацію про спожиті продукти за місяць та розраховує загальний рівень фенілаланіну.', reply_markup=kb_client)
        await message.delete()
    except:
        await message.reply('Спілкування з ботом через особисті повідомлення, напишіть йому: \nhttps://t.me/PKUDiaryBot')

# @dp.message_handler(commands=['add_product'])
async def register_product_cm(message : types.Message):
    await bot.send_message(message.from_user.id, 
        f'Вітаю, {message.from_user.first_name}, ваш продукт успішно додано!', reply_markup=ReplyKeyboardRemove())
    
async def add_product_cm(message : types.Message):
    await bot.send_message(message.from_user.id, 
        f'Вітаю, {message.from_user.first_name} ваш продукт успішно додано у постійний список!')

# @dp.message_handler(commands=['del_product'])
async def del_product_cm(message : types.Message):
    await bot.send_message(message.from_user.id, 
        f'Вітаю, {message.from_user.first_name} ваш продукт успішно видалено!')

# @dp.message_handler(commands=['view_day'])
# async def view_day_cm(message : types.Message):
#     await bot.send_message(message.from_user.id, 
#         f'Перегляд історії спожитих продуктів {message.from_user.first_name} за день:')

# @dp.message_handler(commands=['view_week'])
# async def view_week_cm(message : types.Message):
#     await bot.send_message(message.from_user.id, 
#         f'Перегляд історії спожитих продуктів {message.from_user.first_name} за тиждень:')

# @dp.message_handler(commands=['view_month'])
async def view_month_cm(message : types.Message):
    await bot.send_message(message.from_user.id, 
        f'Перегляд історії спожитих продуктів {message.from_user.first_name} за місяць:')
    await pku_db.sql_view_month(message)

# @dp.message_handler(commands=['commands'])
# async def commands(message : types.message):
#     await bot.send_message(message.from_user.id, message)

def register_handlers_client(dp : Dispatcher): # Декоратор, обробка подій; Deorator, event handler
    dp.register_message_handler(command_start, commands=['start', 'help'])
    dp.register_message_handler(register_product_cm, commands=['add_product'])
    dp.register_message_handler(del_product_cm, commands=['del_product'])
    # dp.register_message_handler(view_day_cm, commands=['view_day'])
    # dp.register_message_handler(view_week_cm, commands=['view_week'])
    dp.register_message_handler(view_month_cm, commands=['view_month'])
    dp.register_message_handler(add_product_cm, commands=['add_product_to_list'])
    # dp.register_message_handler(commands, commands=['commands'])