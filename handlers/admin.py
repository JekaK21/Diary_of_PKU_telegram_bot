"""Ініціалізація модулів Initialization of modules"""
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from create_bot import dp, bot
from keyboards import kb_client, url_client
from database import pku_db

