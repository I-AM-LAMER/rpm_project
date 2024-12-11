from aiogram.filters import BaseFilter
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from ..states import AuthForm


def check_if_cancel(text: str):
    return text == '/cancel'

async def clear_state(state: FSMContext):
    await state.clear()

class UsernameFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        username = message.text
        if check_if_cancel(username):
            return {'clear': clear_state}
        if len(username) < 3 or len(username) > 15:
            return False
        if not username.isalnum():
            return False
        return True
    
class PasswordFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        password = message.text
        if check_if_cancel(password):
            return {'clear': clear_state}
        if len(password) < 6:
            return False
        if not any(char.isdigit() for char in password):
            return False
        return True