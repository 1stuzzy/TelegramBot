from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def menu_keyboard():
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("1️⃣", callback_data="select_one"))
    keyboard.insert(InlineKeyboardButton("2️⃣", callback_data="select_two"))
    keyboard.insert(InlineKeyboardButton("3️⃣", callback_data="select_three"))
    return keyboard


def back_btn():
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("В главное меню ↩️", callback_data="back_menu"))
    return keyboard