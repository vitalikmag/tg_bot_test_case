""" Для исключения ошибки импортов выносим их в отдельный файл"""

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from config import TG_TOKEN

bot = Bot(token=TG_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
