import sqlite3 as sq
from create_bot import dp, bot
from aiogram import Dispatcher
from prettytable import from_db_cursor, MSWORD_FRIENDLY

def sql_start():
    try:
        global base, cur
        base = sq.connect('db_pku.db')
        cur = base.cursor()
        if base:
            print('Data base successfuly connect!')
        base.execute('CREATE TABLE IF NOT EXISTS products(ID_products_prod INTEGER PRIMARY KEY UNIQUE, Name_long TEXT, \
                    Name_short TEXT, FA INTEGER, Dish_sign BOOLEAN, Calc_sign BOOLEAN, ID_categ INTEGER, \
                    ID_unit INTEGER, Coefficient_is_100g INTEGER, FOREIGN KEY (ID_categ) REFERENCES category(ID_category), \
                    FOREIGN KEY (ID_unit) REFERENCES units(ID_unit_units))')
        base.commit()
    except Exception as e:
        print(e)

async def sql_register_products(state):
    try:
        async with state.proxy() as data:
            cur.execute('INSERT INTO products (Name_long, Name_short, FA, Dish_sign, Calc_sign) VALUES (?, ?, ?, ?, ?)', tuple(data.values()))
            base.commit()
    except Exception as e:
        print(e)

async def sql_view_month(message):
    global note
    for note in cur.execute('SELECT * FROM products').fetchall():
        await bot.send_message(message.from_user.id, 
            f'Повна назва продукту - {note[1]}\nКоротка назва - {note[2]}\nФенілаланін - {note[3]}\nОзнака блюда - {note[4]}\
            \nОзнака розрахунку - {note[5]}\nКатегорія - {note[6]}\nОдиниця виміру - {note[7]}\nКофіцієнт на 100г - {note[8]}\n')
    for i in note:
        if i > 10:
            pass

    # cur.execute('SELECT * FROM products')
    # table = from_db_cursor(cur)
    # table.set_style(MSWORD_FRIENDLY)
    # await bot.send_message(message.from_user.id, table)