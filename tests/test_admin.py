"""Ініціалізація модулів Initialization of modules"""
from unittest.async_case import IsolatedAsyncioTestCase
from handlers.admin import *

# Клас тестів; Test class
class Test_admin(IsolatedAsyncioTestCase):
    async def test_cm_reg_name_l(self):
        message = 'Банан'
        self.assertEqual(type(message), str)

    async def test_cm_reg_name_s(self):
        message = 'Банан'
        self.assertIsInstance(message, str)

    async def test_cm_reg_categ(self):
        message = 2
        self.assertIsInstance(message, int)

    async def test_cm_reg_fa(self):
        message = 44
        self.assertIsInstance(message, int)

    async def test_cm_reg_protein(self):
        message = 2
        self.assertIsInstance(message, int)

    async def test_cm_reg_weight(self):
        message = 150
        self.assertIsInstance(message, int)

    async def test_cm_reg_unit(self):
        message = 3
        self.assertIsInstance(message, int)

    async def test_cm_reg_num(self):
        message = 2
        self.assertIsInstance(message, int)

    async def test_cm_reg_date(self):
        message = '2023.03.27'
        self.assertIsInstance(message, str)

    async def test_set_productId(self):
        message = 3
        self.assertIsInstance(message, int)

# py -m unittest tests.test_admin