"""Ініціалізація модулів Initialization of modules"""
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from create_bot import dp, bot
from keyboards import kb_client, url_client
from database import pku_db

# Зробити: Розділити функції по ролям на адміністратора і на клієнта (коли всі основні функції будуть зроблені).

# Функція старту бота
async def command_start(message : types.Message): # Функція, виводить інструкцію про можливості бота;
    try: # Перевірка чи є вже чат розмови з ботом; Checking if there is already a chat conversation with the bot
        await bot.send_message(message.from_user.id, 
        'Бот дозволяє за допомогою навігаційних кнопок використовувати різні функції.' + 
        '\nЯк працює бот, дивись в інструкції', reply_markup=url_client)
        await message.delete()
    except:
        await message.reply('Спілкування з ботом через особисті повідомлення, напишіть йому: \nhttps://t.me/PKUDiaryBot')

# Класи змінних, що представляють стовпці у базі даних;
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

class FSMDelete(StatesGroup):
    id_product = State()

# Функція точки старту обробки додавання повідомлень;
async def add_product(message : types.Message):
    global User_ID
    User_ID = str(message.from_user.id)
    await FSMAdd.name_long.set()
    await message.reply('Повна назва продукту', reply_markup=kb_client)

# Вихід зі станів
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
    await message.reply('Коротка назва продукту')

async def cm_reg_name_s(message : types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name_short'] = message.text
    await FSMAdd.next()
    await message.reply('Категорія продукту')

async def cm_reg_categ(message : types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['Categ'] = int(message.text)
    await FSMAdd.next()
    await message.reply('Фенілаланін продукту за 100г.')

async def cm_reg_fa(message : types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['FA'] = int(message.text)
    await FSMAdd.next()
    await message.reply('Білок продукту')

async def cm_reg_protein(message : types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['Protein'] = int(message.text)
    await FSMAdd.next()
    await message.reply('Вага продукту')

async def cm_reg_weight(message : types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['Weight'] = int(message.text)
    await FSMAdd.next()
    await message.reply('Одиниця виміру')

async def cm_reg_unit(message : types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['Unit'] = int(message.text)

    # async with state.proxy() as data:
    #     await message.reply(str(data))
    await FSMAdd.next()
    await message.reply('Кількість')
    
async def cm_reg_num(message : types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['Num'] = int(message.text)
    await FSMAdd.next()
    await message.reply('Дата споживання')

async def cm_reg_date(message : types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['Date'] = message.text
    print(state)
    await message.reply(f'Вітаю, {message.from_user.first_name} ваш продукт успішно додано!', reply_markup=kb_client)
    await pku_db.sql_register_products(state, User_ID)
    await state.finish()

# Функція точки старту обробки видалення повідомлень;
async def del_product(message : types.Message):
    await FSMDelete.id_product.set()
    await message.reply('Напиши id продукту, що треба видалити.', reply_markup=kb_client)

async def set_productId(message : types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data['id_product'] = int(message.text)
        # print(state)
        await message.reply(f'Вітаю, {message.from_user.first_name} ваш продукт успішно видалено!')
        await pku_db.sql_delete(state)
        await state.finish()
    except Exception as e:
        print(e)
        await message.reply(message.from_user.id, f'{message.from_user.first_name} у записі були букви!')
        await message.delete()
        
# Функція перегляду;
async def view_month_cm(message : types.Message):
    await bot.send_message(message.from_user.id, 
        f'Перегляд історії спожитих продуктів {message.from_user.first_name} за місяць:')
    await pku_db.sql_view_month(message)

# Загальний декоратор функцій;
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
    dp.register_message_handler(del_product, commands=['del_product'], state=None)
    dp.register_message_handler(set_productId, state=FSMDelete.id_product)
    dp.register_message_handler(view_month_cm, commands=['view'])