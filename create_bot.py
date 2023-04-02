"""Ініціалізація модулів Initialization of modules"""
import os
from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

# Імпорт токену бота для працювання з unit тестами; Bot token import for working with unit tests
try:
    from dotenv import load_dotenv
    load_dotenv(dotenv_path = '.env')
except Exception as e:
    print(e)

storage = MemoryStorage() # Сховище даних, використовується для роботи з FSMContext; Data store used to work with FSMContext
# Створення екземпляру бота; Creating a bot instance 
"""Ініціалізація бота Bot initialization"""
bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher(bot, storage=storage)