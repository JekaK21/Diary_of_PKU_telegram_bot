"""Ініціалізація модулів Initialization of modules"""
import os
from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

try:
    from dotenv import load_dotenv
    load_dotenv(dotenv_path = '.env')
except Exception as e:
    print(e)

storage = MemoryStorage()
# Створення екземпляру бота; Creating a bot instance 
"""Ініціалізація бота Bot initialization"""
bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher(bot, storage=storage)