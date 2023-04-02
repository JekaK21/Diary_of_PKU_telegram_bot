"""Ініціалізація модулів Initialization of modules"""
from unittest.async_case import IsolatedAsyncioTestCase
from handlers.client import *

# Клас тестів; Test class
class Test_client(IsolatedAsyncioTestCase):
    async def test_cm_reg_name_l(self):
        message = 'Картопля'
        self.assertIsInstance(message, str)
        # # Створюємо об'єкт стану та зберігаємо дані в ньому
        # state = FSMContext(Mock(), Mock(), Mock())
        # async with state.proxy() as data:
        #     data['name_long'] = 'Картопля'

        # # Отримуємо дані зі стану та перевіряємо тип
        # async with state.proxy() as data:
        #     self.assertIsInstance(data['name_long'], str)
        # res = await cm_reg_name_l(message=message, state=None)
        # await self.assertEqual(type(res), str)

    async def test_cm_reg_name_s(self):
        message = 'Фрі'
        self.assertIsInstance(message, str)

    async def test_cm_reg_categ(self):
        message = 1
        self.assertIsInstance(message, int)

    async def test_cm_reg_fa(self):
        message = 34
        self.assertIsInstance(message, int)

    async def test_cm_reg_protein(self):
        message = 3
        self.assertIsInstance(message, int)

    async def test_cm_reg_weight(self):
        message = 120
        self.assertIsInstance(message, int)

    async def test_cm_reg_unit(self):
        message = 3
        self.assertIsInstance(message, int)

    async def test_cm_reg_num(self):
        message = 1
        self.assertIsInstance(message, int)

    async def test_cm_reg_date(self):
        message = '2023.03.27'
        self.assertIsInstance(message, str)

# py -m unittest tests.test_client