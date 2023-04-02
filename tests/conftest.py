from aiogram import Bot, Dispatcher
import pytest
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from tests.mocked_bot import MockedBot

@pytest.fixture(scope='session')
async def storage():
    temp_storage = MemoryStorage()
    try:
        yield temp_storage
    finally:
        await temp_storage.close()

@pytest.fixture()
def bot():
    bot = MockedBot()
    token = Bot.set_current(bot)
    try:
        yield bot
    finally:
        Bot.reset_current(token)


@pytest.fixture()
async def dispatcher():
    dp = Dispatcher()
    await dp.emit_startup()
    try:
        yield dp
    finally:
        await dp.emit_shutdown()