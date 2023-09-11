from aiogram.fsm.state import StatesGroup, State


class Messaging(StatesGroup):
    message_inc = State()
    message_waiting = State()
