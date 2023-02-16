from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram import types, Dispatcher
from create_bot import dp
from database import pku_db
from keyboards import kb_client

# Визначення змінних бази даних
class FSMAdmin(StatesGroup):
    name_long = State()
    name_short = State()
    FA = State()
    Dish_sign = State()
    Calc_sign = State()

# Функція точки старту обробки повідомлень
async def cm_start(message : types.Message):
    await FSMAdmin.name_long.set()
    await message.reply('Повна назва продукту', reply_markup=kb_client)

# Вихід зі стану
async def cancel_handler(message : types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('OK')

async def cm_reg_name_l(message : types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name_long'] = message.text
    await FSMAdmin.next()
    await message.reply('Коротка назва продукту')

async def cm_reg_name_s(message : types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name_short'] = message.text
    await FSMAdmin.next()
    await message.reply('Фенілаланін продукту')

async def cm_reg_fa(message : types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['FA'] = int(message.text)
    await FSMAdmin.next()
    await message.reply('Ознака блюда (True або False)')

async def cm_reg_dish_sign(message : types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['Dish_sign'] = message.text
    await FSMAdmin.next()
    await message.reply('Ознака розрахунку (True або False)')

async def cm_reg_calc_sign(message : types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['Calc_sign'] = message.text

    async with state.proxy() as data:
        await message.reply(str(data))
    await pku_db.sql_register_products(state)
    await state.finish()

def register_handlers_admin(dp : Dispatcher): # Декоратор, обробка подій; Deorator, event handler
    dp.register_message_handler(cm_start, commands=['admin'], state=None)
    dp.register_message_handler(cancel_handler, state="*", commands='cancel')
    dp.register_message_handler(cancel_handler, Text(equals='cancel', ignore_case=True), state="*")
    dp.register_message_handler(cm_reg_name_l, state=FSMAdmin.name_long)
    dp.register_message_handler(cm_reg_name_s, state=FSMAdmin.name_short)
    dp.register_message_handler(cm_reg_fa, state=FSMAdmin.FA)
    dp.register_message_handler(cm_reg_dish_sign, state=FSMAdmin.Dish_sign)
    dp.register_message_handler(cm_reg_calc_sign, state=FSMAdmin.Calc_sign)
