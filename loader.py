from aiogram import Bot, Dispatcher
from aiogram.types import ParseMode
from aiogram.contrib.fsm_storage.memory import MemoryStorage


bot = Bot('', parse_mode=ParseMode.HTML) # Здесь нужно вставить токен бота из @BotFather
dp = Dispatcher(bot, storage=MemoryStorage())
moderation = -1002180447685

