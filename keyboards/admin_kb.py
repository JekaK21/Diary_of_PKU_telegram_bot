"""Ініціалізація модулів Initialization of modules"""
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

# Зробити: Видалити непотрібні кнопки (коли все буде зроблено і все буде працювати, як терба).
"""Ініціалізація кнопок Button initialization"""
b1 = KeyboardButton('/add_product_ad')
b2 = KeyboardButton('/cancel_ad')
b3 = KeyboardButton('/del_product_ad')
b4 = KeyboardButton('/view_ad')

# Заміняє звичайну клав-ру на кнопки; Replaces the usual keyboard with buttons
kb_admin = ReplyKeyboardMarkup(resize_keyboard=True)
kb = InlineKeyboardMarkup().row(
    InlineKeyboardButton('<-', callback_data='prev'),
    InlineKeyboardButton('->', callback_data='next')
)

# Додавання кнопок, розположення; Adding buttons, location
kb_admin.row(b1, b2).row(b3, b4)