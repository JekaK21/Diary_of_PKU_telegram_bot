"""Ініціалізація модулів Initialization of modules"""
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton#, ReplyKeyboardRemove

"""Ініціалізація кнопок Button initialization"""
b1 = KeyboardButton('/add_product')
b2 = KeyboardButton('/del_product')
b3 = KeyboardButton('/view_day')
b4 = KeyboardButton('/view_week')
b5 = KeyboardButton('/view_month')

kb_client = ReplyKeyboardMarkup(resize_keyboard=True) # Заміняє звичайну клав-ру на кнопки; Replaces the usual keyboard with buttons

kb_client.row(b1, b2).row(b3, b4).add(b5) # Додавання кнопок, розположення; Adding buttons, location