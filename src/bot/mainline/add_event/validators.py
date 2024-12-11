from aiogram.filters import BaseFilter
from aiogram.types import Message
import re
from datetime import datetime
from aiogram.fsm.context import FSMContext
from ...states import AuthForm

def check_if_cancel(text: str):
    return text == '/cancel'

async def clear_state(state: FSMContext):
    curr_state = await state.get_state()
    if curr_state not in AuthForm._get_all_states_names():
        await state.clear()
        await state.set_state(AuthForm.authentificated)


class EventNameFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        event_name = message.text
        if check_if_cancel(event_name):
            return {'clear': clear_state}
        if len(event_name) < 3 or len(event_name) > 15:
            return False
        if not event_name.isalnum():    
            return False
        return True
    
class EventDescriptionFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        description = message.text
        if check_if_cancel(description):
            return {'clear': clear_state}
        if len(description) < 6 or len(description) > 255:
            return False
        return True
    
class EventDatetimeFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        datetime_str = message.text
        try:
            datetime.strptime(datetime_str, '%m-%d-%y %H:%M:%S')
        except ValueError:
            return False
        return True