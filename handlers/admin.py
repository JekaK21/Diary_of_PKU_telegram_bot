"""Ініціалізація модулів Initialization of modules"""
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from create_bot import dp, bot
from keyboards import kb_admin
from database import pku_db

# Класи змінних, що представляють стовпці у базі даних; Variable classes representing columns in a database
class FSMAdmin(StatesGroup):
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

ID = None

# Отримати ID адміністратора; Get admin ID
async def make_changes(message : types.Message):
    global ID
    ID = message.from_user.id
    await bot.send_message(message.from_user.id, f'Добрий день, адміністратор {message.from_user.first_name}!', reply_markup=kb_admin)
    await message.delete()

# Функція точки старту обробки додавання повідомлень; The function of the starting point of the processing of adding messages
async def add_product_ad(message : types.Message):
    if message.from_user.id == ID:
        await FSMAdmin.name_long.set()
        await message.reply('Повна назва продукту', reply_markup=kb_admin)

# Вихід зі станів; Exiting states
async def cancel_handler_ad(message : types.Message, state: FSMContext):
    if message.from_user.id == ID:
        current_state = await state.get_state()
        if current_state is None:
            return
        await state.finish()
        await message.reply('OK')

async def cm_reg_name_l(message : types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['name_long'] = message.text
        await FSMAdmin.next()
        await message.reply('Коротка назва продукту')

async def cm_reg_name_s(message : types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['name_short'] = message.text
        await FSMAdmin.next()
        await message.reply('Категорія продукту')

async def cm_reg_categ(message : types.Message, state: FSMContext):
    try:    
        if message.from_user.id == ID:
            async with state.proxy() as data:
                data['Categ'] = int(message.text)
            await FSMAdmin.next()
            await message.reply('Фенілаланін продукту за 100г.')
    except Exception as e:
        print(e)
        await message.reply('Виникла помилка, ви ввели не ціле число!')

async def cm_reg_fa(message : types.Message, state: FSMContext):
    try:    
        if message.from_user.id == ID:
            async with state.proxy() as data:
                data['FA'] = int(message.text)
            await FSMAdmin.next()
            await message.reply('Білок продукту')
    except Exception as e:
        print(e)
        await message.reply('Виникла помилка, ви ввели не ціле число!')

async def cm_reg_protein(message : types.Message, state: FSMContext):
    try:    
        if message.from_user.id == ID:
            async with state.proxy() as data:
                data['Protein'] = int(message.text)
            await FSMAdmin.next()
            await message.reply('Вага продукту')
    except Exception as e:
        print(e)
        await message.reply('Виникла помилка, ви ввели не ціле число!')

async def cm_reg_weight(message : types.Message, state: FSMContext):
    try:
        if message.from_user.id == ID:
            async with state.proxy() as data:
                data['Weight'] = int(message.text)
            await FSMAdmin.next()
            await message.reply('Одиниця виміру')
    except Exception as e:
        print(e)
        await message.reply('Виникла помилка, ви ввели не ціле число!')

async def cm_reg_unit(message : types.Message, state: FSMContext):
    try:
        if message.from_user.id == ID:
            async with state.proxy() as data:
                data['Unit'] = int(message.text)
            await FSMAdmin.next()
            await message.reply('Кількість')
    except Exception as e:
        print(e)
        await message.reply('Виникла помилка, ви ввели не ціле число!')
    
async def cm_reg_num(message : types.Message, state: FSMContext):
    try:    
        if message.from_user.id == ID:
            async with state.proxy() as data:
                data['Num'] = int(message.text)
            await FSMAdmin.next()
            await message.reply('Дата споживання')
    except Exception as e:
        print(e)
        await message.reply('Виникла помилка, ви ввели не ціле число!')

async def cm_reg_date(message : types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['Date'] = message.text
        print(state)
        await message.reply(f'Вітаю, {message.from_user.first_name} ваш продукт успішно додано!', reply_markup=kb_admin)
        await pku_db.sql_register_products(state, str(ID))
        await state.finish()

# Функція точки старту обробки видалення повідомлень; The function of the starting point of the processing of deleting messages
async def del_product_ad(message : types.Message):
    try:
        if message.from_user.id == ID:
            await FSMDelete.id_product.set()
            await message.reply('Напиши id продукту, що треба видалити.', reply_markup=kb_admin)
    except Exception as e:
        print(e)
        await message.reply('Виникла помилка, ви ввели не ціле число!')

async def set_productId(message : types.Message, state: FSMContext):
    try:
        if message.from_user.id == ID:
            async with state.proxy() as data:
                data['id_product'] = int(message.text)
            # print(state)
            await message.reply(f'Вітаю, {message.from_user.first_name} ваш продукт успішно видалено!')
            await pku_db.sql_delete(state)
            await state.finish()
    except Exception as e:
        print(e)
        if message.from_user.id == ID:
            await message.reply(message.from_user.id, f'{message.from_user.first_name} у записі були букви!')
            await message.delete()
        
# Функція перегляду записів; Record viewing function
async def view_ad(message : types.Message):
    if message.from_user.id == ID:
        await bot.send_message(message.from_user.id, 
            f'Перегляд історії спожитих продуктів {message.from_user.first_name} за місяць:')
        await pku_db.sql_view_month(message)

# Загальний декоратор функцій; Generic function decorator
def register_handlers_admin(dp : Dispatcher): # Декоратор, обробка подій; Deorator, event handler
    dp.register_message_handler(make_changes, commands=['admin'], is_chat_admin=True)
    dp.register_message_handler(cancel_handler_ad, state="*", commands='cancel_ad')
    dp.register_message_handler(cancel_handler_ad, Text(equals='cancel_ad', ignore_case=True), state="*")
    dp.register_message_handler(add_product_ad, commands=['add_product_ad'], state=None)
    dp.register_message_handler(cm_reg_name_l, state=FSMAdmin.name_long)
    dp.register_message_handler(cm_reg_name_s, state=FSMAdmin.name_short)
    dp.register_message_handler(cm_reg_categ, state=FSMAdmin.Categ)
    dp.register_message_handler(cm_reg_fa, state=FSMAdmin.FA)
    dp.register_message_handler(cm_reg_protein, state=FSMAdmin.Protein)
    dp.register_message_handler(cm_reg_weight, state=FSMAdmin.Weight)
    dp.register_message_handler(cm_reg_unit, state=FSMAdmin.Unit)
    dp.register_message_handler(cm_reg_num, state=FSMAdmin.Num)
    dp.register_message_handler(cm_reg_date, state=FSMAdmin.Date)
    dp.register_message_handler(del_product_ad, commands=['del_product_ad'], state=None)
    dp.register_message_handler(set_productId, state=FSMDelete.id_product)
    dp.register_message_handler(view_ad, commands=['view_ad'])
    dp.register_callback_query_handler(pku_db.inline_bnts_logic)