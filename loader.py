from aiogram import Bot, Dispatcher
from aiogram.types import ParseMode
from aiogram.contrib.fsm_storage.memory import MemoryStorage


bot = Bot('', parse_mode=ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())
channel = -1002189593207

