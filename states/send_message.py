from aiogram.dispatcher.filters.state import State, StatesGroup

class SendMessage(StatesGroup):
    nickname = State()
    message = State()