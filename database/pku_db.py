"""Ініціалізація модулів Initialization of modules"""
import sqlite3 as sq
from create_bot import dp, bot
from keyboards import kb
from aiogram import Dispatcher
from aiogram.types import CallbackQuery

# Ініціалізація бази даних;
def sql_start():
    try:
        global base, cur
        base = sq.connect('db_pku.db')
        cur = base.cursor()
        if base:
            print('Data base successfuly connect!')
        base.execute('PRAGMA foreign_keys = 1; CREATE TABLE IF NOT EXISTS products(ID_products_prod INTEGER PRIMARY KEY UNIQUE, Name_long TEXT, \
                    Name_short TEXT, FA INTEGER, Dish_sign BOOLEAN, Calc_sign BOOLEAN, ID_categ INTEGER, \
                    ID_unit INTEGER, Coefficient_is_100g INTEGER, FOREIGN KEY (ID_categ) REFERENCES category(ID_category), \
                    FOREIGN KEY (ID_unit) REFERENCES units(ID_unit_units))')
        base.commit()
    except Exception as e:
        print(e)

# Зробити: Додати у функцію можливість вcтавляти дані у декілька таблиць.
# Додати у функцію додавання записів можливість додавати дані у деклька таблиць (додавання назви (str), наприклад категорії, а не сам id (int)).

# Додавання записів у базу;
async def sql_register_products(state):
    try:
        insert = 'INSERT INTO products (Name_long, Name_short, ID_categ, FA, Protein, Weight, ID_unit) VALUES (?, ?, ?, ?, ?, ?, ?)'
        async with state.proxy() as data:
            cur.execute(insert, tuple(data.values()))
            base.commit()
    except Exception as e:
        print(e)

# Видалення записів з бази;
async def sql_delete(state):
    try:
        delete = 'DELETE FROM products WHERE ID_products_prod = (?)'
        async with state.proxy() as data:
            cur.execute(delete, tuple(data.values()))
            base.commit()
    except Exception as e:
        print(e)

# Вивід даних з бази;
async def sql_view_month(message):
    global note, msg_text, current_idx
    note = cur.execute('SELECT * FROM products').fetchall() # , registration
    current_idx = 0
    msg_text = 'ID Продукту - {}\n' 'Повна назва продукту - {}\n' 'Коротка назва - {}\n'\
                'Категорія - {}\n' 'Фенілаланін - {}\n' 'Білок - {}\n' 'Вага - {}\n' 'Одиниця виміру - {}'
    prod_info = note[current_idx]
    await message.answer(msg_text.format(prod_info[0], prod_info[1], prod_info[2], prod_info[8], prod_info[3],
                                        prod_info[4], prod_info[5], prod_info[9]), reply_markup=kb)

# Функція редагування повідомлення для перегляду наступного запису;
@dp.callback_query_handler()
async def inline_bnts_logic(query: CallbackQuery):
    data = query.data
    global current_idx

    if data == 'next':
        current_idx = current_idx + 1
        prod_info = note[current_idx]
    elif data == 'prev':
        current_idx = current_idx - 1
        prod_info = note[current_idx]

    await bot.edit_message_text(
            msg_text.format(prod_info[0], prod_info[1], prod_info[2], prod_info[8], prod_info[3],
            prod_info[4], prod_info[5], prod_info[9]),
            query.from_user.id,
            query.message.message_id,
            reply_markup=kb)