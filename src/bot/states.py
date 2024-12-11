from aiogram.fsm.state import State, StatesGroup

class AuthForm(StatesGroup):
    name = State()
    password = State()
    authentificated = State()