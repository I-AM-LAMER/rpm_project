from aiogram.fsm.state import State, StatesGroup

class AddEvent(StatesGroup):
    event_name = State()
    event_description = State()
    event_close_time = State()
