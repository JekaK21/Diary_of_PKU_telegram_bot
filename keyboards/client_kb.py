"""Ініціалізація модулів Initialization of modules"""
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton#, ReplyKeyboardRemove

"""Ініціалізація кнопок Button initialization"""
b1 = KeyboardButton('/register_product')
b2 = KeyboardButton('/del_product')
b3 = KeyboardButton('/add_product')
b4 = KeyboardButton('/view_day')
b5 = KeyboardButton('/view_week')
b6 = KeyboardButton('/view_month')
b7 = KeyboardButton('/admin')
b8 = KeyboardButton('/cancel')
# b7 = KeyboardButton('/commands')

kb_client = ReplyKeyboardMarkup(resize_keyboard=True) # Заміняє звичайну клав-ру на кнопки; Replaces the usual keyboard with buttons

kb_client.row(b1, b2).row(b3, b4).add(b5, b6).add(b7, b8) # .add(b7) Додавання кнопок, розположення; Adding buttons, location