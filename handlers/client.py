"""Ініціалізація модулів Initialization of modules"""
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from create_bot import dp, bot
from keyboards import kb_client, url
from database import pku_db

# Функція старту бота; Bot start function
async def command_start(message : types.Message): # Функція, виводить інструкцію про можливості бота;
    try: # Перевірка чи є вже чат розмови з ботом; Checking if there is already a chat conversation with the bot
        await bot.send_message(message.from_user.id, 
        'Бот дозволяє за допомогою навігаційних кнопок використовувати різні функції. \
        \nThe bot allows you to use various functions with the help of navigation buttons.' + 
        '\nЯк працює бот, дивись в інструкції \
        \nHow the bot works, see the instruction', reply_markup=url)
        await message.delete()
    except:
        await message.reply('Спілкування з ботом через особисті повідомлення, напишіть йому: \
                            \nCommunicating with the bot through private messages, write to him: \nhttps://t.me/PKUDiaryBot')

# Класи змінних, що представляють стовпці у базі даних; Variable classes representing columns in a database
class FSMAdd(StatesGroup):
    name_long = State()
    name_short = State()
    Categ = State()
    FA = State()
    Protein = State()
    Weight = State()
    Unit = State()
    Num = State()
    Date = State()

# Функція точки старту обробки додавання повідомлень; The function of the starting point of the processing of adding messages
async def add_product(message : types.Message):
    global User_ID
    User_ID = str(message.from_user.id)
    await FSMAdd.name_long.set()
    await message.reply('Повна назва продукту \nFull product name', reply_markup=kb_client)

# Вихід зі станів; Exiting states
async def cancel_handler(message : types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('OK')

async def cm_reg_name_l(message : types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name_long'] = message.text
    await FSMAdd.next()
    await message.reply('Коротка назва продукту \nShort product name')

async def cm_reg_name_s(message : types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name_short'] = message.text
    await FSMAdd.next()
    await message.reply('Категорія продукту \nProduct category')

async def cm_reg_categ(message : types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data['Categ'] = int(message.text)
        await FSMAdd.next()
        await message.reply('Фенілаланін продукту за 100г. \nPhenylalanine of the product per 100g.')
    except Exception as e:
        print(e)
        await message.reply('Виникла помилка, ви ввели не ціле число! \nAn error occurred, you did not enter an integer!')

async def cm_reg_fa(message : types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data['FA'] = float(message.text)
        await FSMAdd.next()
        await message.reply('Білок продукту за 100г. \nProduct protein per 100g.')
    except Exception as e:
        print(e)
        await message.reply('Виникла помилка, ви ввели не число! \nAn error occurred, you entered the wrong number!')

async def cm_reg_protein(message : types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data['Protein'] = float(message.text)
        await FSMAdd.next()
        await message.reply('Вага продукту \nProduct weight')
    except Exception as e:
        print(e)
        await message.reply('Виникла помилка, ви ввели не число! \nAn error occurred, you entered the wrong number!')

async def cm_reg_weight(message : types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data['Weight'] = int(message.text)
        await FSMAdd.next()
        await message.reply('Одиниця виміру \nUnit')
    except Exception as e:
        print(e)
        await message.reply('Виникла помилка, ви ввели не ціле число! \nAn error occurred, you did not enter an integer!')

async def cm_reg_unit(message : types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data['Unit'] = int(message.text)
        await FSMAdd.next()
        await message.reply('Кількість \nNumber')
    except Exception as e:
        print(e)
        await message.reply('Виникла помилка, ви ввели не ціле число! \nAn error occurred, you did not enter an integer!')
    
async def cm_reg_num(message : types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data['Num'] = int(message.text)
        await FSMAdd.next()
        await message.reply('Дата споживання \nDate of consumption')
    except Exception as e:
        print(e)
        await message.reply('Виникла помилка, ви ввели не ціле число! \nAn error occurred, you did not enter an integer!')

async def cm_reg_date(message : types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['Date'] = message.text
    print(state)
    await message.reply(f'Вітаю, {message.from_user.first_name} ваш продукт успішно додано! \
                        \nCongratulations, {message.from_user.first_name}, your product has been successfully added!')
    await pku_db.sql_register_products(state, User_ID)
    await state.finish()
        
# Функція перегляду записів; Record viewing function
async def view_month_cm(message : types.Message):
    await bot.send_message(message.from_user.id, 
        f'Перегляд історії спожитих продуктів {message.from_user.first_name}:\
        \nViewing the history of consumed products {message.from_user.first_name}:')
    await pku_db.sql_view_month(message)

# Загальний декоратор функцій; Generic function decorator
def register_handlers_client(dp : Dispatcher): # Декоратор, обробка подій; Deorator, event handler
    dp.register_message_handler(command_start, commands=['start', 'help'])
    dp.register_message_handler(cancel_handler, state="*", commands='cancel')
    dp.register_message_handler(cancel_handler, Text(equals='cancel', ignore_case=True), state="*")
    dp.register_message_handler(add_product, commands=['add_product'], state=None)
    dp.register_message_handler(cm_reg_name_l, state=FSMAdd.name_long)
    dp.register_message_handler(cm_reg_name_s, state=FSMAdd.name_short)
    dp.register_message_handler(cm_reg_categ, state=FSMAdd.Categ)
    dp.register_message_handler(cm_reg_fa, state=FSMAdd.FA)
    dp.register_message_handler(cm_reg_protein, state=FSMAdd.Protein)
    dp.register_message_handler(cm_reg_weight, state=FSMAdd.Weight)
    dp.register_message_handler(cm_reg_unit, state=FSMAdd.Unit)
    dp.register_message_handler(cm_reg_num, state=FSMAdd.Num)
    dp.register_message_handler(cm_reg_date, state=FSMAdd.Date)
    dp.register_message_handler(view_month_cm, commands=['view'])
    dp.register_callback_query_handler(pku_db.inline_bnts_logic)