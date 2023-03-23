"""Ініціалізація модулів Initialization of modules"""
import sqlite3 as sq
# import traceback
from create_bot import dp, bot
from keyboards import kb
from aiogram import types
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

# Зробити: Таймер очищення таблиць products, register (коли пройде 2 місяці від попередньої дати очищення, зрівнюючи з поточною).

# Додавання записів у базу;
async def sql_register_products(state, User_ID):
    try:
        global data
        insert = 'INSERT INTO products (Name_long, Name_short, ID_categ, FA, Protein, Weight, ID_unit, ID_user_tg) VALUES (?, ?, ?, ?, ?, ?, ?, ?)'
        insert2 = 'INSERT INTO registration (Date, ID_products_reg, Num) VALUES (?, ?, ?)'
        async with state.proxy() as data:
            res_fa = data['Weight'] * data['FA'] / 100
            data1 = (data['name_long'], data['name_short'], data['Categ'], res_fa, data['Protein'], data['Weight'], data['Unit'], User_ID)
            cur.execute(insert, data1)
            base.commit()
            ID_product_reg = cur.lastrowid
            data2 = (data['Date'], ID_product_reg, data['Num'])
            cur.execute(insert2, data2)
            base.commit()
    except Exception as e:
        print(e)
        # print(e, '\nПомилка:\n', traceback.format_exc())

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
    global note, msg_text, current_idx, prod_info
    select = "SELECT p.ID_products_prod, p.Name_long, p.Name_short, c.Name_category, p.FA, p.Protein, p.Weight, u.Name, r.Date, r.Num \
        FROM products AS p LEFT JOIN registration AS r ON p.ID_products_prod = r.ID_products_reg INNER JOIN category AS c ON p.ID_categ = c.ID_category \
        INNER JOIN units AS u ON p.ID_unit = u.ID_unit_units"
    note = cur.execute(select).fetchall()
    current_idx = 0
    msg_text = 'ID Продукту - {}\n' 'Повна назва продукту - {}\n' 'Коротка назва - {}\n'\
                'Категорія - {}\n' 'Фенілаланін - {}\n' 'Білок - {}\n' 'Вага - {}\n'\
                'Одиниця виміру - {}\n' 'Кількість - {}\n' 'Дата - {}\n'
    prod_info = note[current_idx]
    await message.answer(msg_text.format(prod_info[0], prod_info[1], prod_info[2], prod_info[3], prod_info[4],
                                        prod_info[5], prod_info[6], prod_info[7], prod_info[9], prod_info[8]), reply_markup=kb)

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
            msg_text.format(prod_info[0], prod_info[1], prod_info[2], prod_info[3], prod_info[4],
            prod_info[5], prod_info[6], prod_info[7], prod_info[9], prod_info[8]),
            query.from_user.id,
            query.message.message_id,
            reply_markup=kb)