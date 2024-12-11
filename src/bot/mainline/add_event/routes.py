from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram import Router, F
from aiogram.types import Message
from ..states import AddEvent
from .validators import EventNameFilter, EventDescriptionFilter, EventDatetimeFilter
from ...states import AuthForm
from ...middlewares.auth import AuthMiddleware 
from typing import Optional, Awaitable, Callable

router = Router()

@router.message(
    EventNameFilter(),
    AddEvent.event_name,
)
async def event_name_chosen(message: Message, state: FSMContext, clear: Optional[Callable[[FSMContext], Awaitable[None]]] = None):
    if clear:
        await clear(state)
        await message.answer('Успешно! Что бы начать пользоваться ботом, введите /start')
    else:
        await state.update_data(event_name=message.text)
        await message.answer('Теперь укажи описание события')
        await state.set_state(AddEvent.event_description)

@router.message(
    AddEvent.event_name,
)
async def event_name_chosen_incorrectly(message: Message, state: FSMContext):
    await message.answer('Try again')
    await state.set_state(AddEvent.event_name)

@router.message(
    EventDescriptionFilter(),
    AddEvent.event_description,
)
async def event_description_chosen(message: Message, state: FSMContext, clear: Optional[Callable[[FSMContext], Awaitable[None]]] = None):
    if clear:
        await clear(state)
        await message.answer('Успешно! Что бы начать пользоваться ботом, введите /start')
    else:
        await state.update_data(event_description=message.text)
        await message.answer('Теперь укажи дату и время окончания события')
        await state.set_state(AddEvent.event_close_time)

@router.message(
    AddEvent.event_description,
)
async def event_descpiption_chosen_incorrectly(message: Message, state: FSMContext):
    await message.answer('Try again')
    await state.set_state(AddEvent.event_description)

@router.message(
    EventDatetimeFilter(),
    AddEvent.event_close_time,
)
async def event_time_chosen(message: Message, state: FSMContext, clear: Optional[Callable[[FSMContext], Awaitable[None]]] = None):
    if clear:
        await clear(state)
        await message.answer('Успешно! Что бы начать пользоваться ботом, введите /start')
    else:
        await state.update_data(event_close_time=message.text)
        await message.answer('Отлично! что бы посмотреть события напишите "Список Событий"')
        await state.clear()
        await state.set_state(AuthForm.authentificated)


@router.message(
    AddEvent.event_close_time,
)
async def event_time_chosen_incorrectly(message: Message, state: FSMContext):
    await message.answer('Try again')
    await state.set_state(AddEvent.event_close_time)
