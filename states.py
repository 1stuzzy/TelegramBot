from aiogram.dispatcher.filters.state import State, StatesGroup


class Form(StatesGroup):
    message = State()
    photo = State()
