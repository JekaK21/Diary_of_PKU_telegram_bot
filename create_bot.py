"""Ініціалізація модулів Initialization of modules"""
from aiogram import Bot
from aiogram.dispatcher import Dispatcher
import os

"""Ініціалізація бота Bot initialization"""
bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher(bot)