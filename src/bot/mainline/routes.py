from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram import Router, F
from aiogram.types import Message
from ..states import AuthForm
from .keyboard import keyboard
from .states import AddEvent
from aiogram.types import ReplyKeyboardRemove
from ..middlewares.auth import AuthMiddleware


router = Router()

@router.message(
    AuthForm.authentificated,
    Command('start')
)
async def start(message: Message):
    await message.answer('Привет! Это бот для составления рассписаний. Ниже представлены доступные функции', reply_markup=keyboard)
    
@router.message(
    Command('cancel')
)
async def cancel(message: Message, state: FSMContext):
    await message.answer('Отмена произведена, что бы начать работу введите /start', reply_markup=ReplyKeyboardRemove())
    curr_state = await state.get_state()
    if curr_state not in AuthForm._get_all_states_names():
        await state.clear()
        await state.set_state(AuthForm.authentificated)
    
@router.message(
    AuthForm.authentificated,
    F.text == 'Добавить Событие'
)
async def add_event(message: Message, state: FSMContext):
    await message.answer('Введите название нового события', reply_markup=ReplyKeyboardRemove())
    await state.set_state(AddEvent.event_name)
