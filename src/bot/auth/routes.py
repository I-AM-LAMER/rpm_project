from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram import Router, F
from aiogram.types import Message
from ..states import AuthForm
from .validators import UsernameFilter, PasswordFilter
from ..middlewares.auth import AuthMiddleware
from typing import Awaitable, Optional, Callable
from ...storage.rabbit import channel_pool
from aio_pika import ExchangeType
import msgpack
import aio_pika
from ...schema.user_creds import User

router = Router()

@router.message(StateFilter(None), Command('start'))
async def set_name(message: Message, state: FSMContext):
    await state.set_state(AuthForm.name)
    await message.answer('Привет! Для работы со мной потребуется регистрация. Пожалуйста придумайте имя (the 26-letter Latin alphabet, the numerical digits from 0-9, and sometimes special characters including @, #, and * prefered)')
    

@router.message(
    UsernameFilter(),
    AuthForm.name
)
async def name_chosen(message: Message, state: FSMContext, clear: Optional[Callable[[FSMContext], Awaitable[None]]] = None):
    if clear:
        await clear(state)
        await message.answer('Успешно! Что бы начать пользоваться ботом, введите /start')
    else:
        await state.update_data(name=message.text.lower())

        await message.answer('Теперь введите пароль (не менее 6 символов и одной цифры!)')
        await state.set_state(AuthForm.password)

@router.message(
    AuthForm.name
)
async def name_chosen_incorrectly(message: Message, state: FSMContext):

    await message.answer('Вы ввели неккоректное имя. Придумайте другое!')
    await state.set_state(AuthForm.name)

@router.message(
    PasswordFilter(),
    AuthForm.password
)
async def set_password(message: Message, state: FSMContext, clear: Optional[Callable[[FSMContext], Awaitable[None]]] = None):
    if clear:
        await clear(state)
        await message.answer('Успешно! Что бы начать пользоваться ботом, введите /start')
    else:
        await state.update_data(password=message.text)

        curr_state = await state.get_data()

        channel: aio_pika.Channel

        async with channel_pool.acquire() as channel:
            exchange = await channel.declare_exchange("user_schedule", ExchangeType.DIRECT, durable=True)

            user_data = await channel.declare_queue(
                name='users_creds',
                durable=True,
            )

            await user_data.bind(
                exchange=exchange,
                routing_key=message.from_user.id,
            )

            await exchange.publish(
                aio_pika.Message(
                    msgpack.packb(
                        User(
                            user_id=message.from_user.id,
                            username=curr_state['name'],
                            password=curr_state['password'],
                        ).model_dump()
                    )
                ),
                'users_creds'
            )   
        await state.clear()
        await state.set_state(AuthForm.authentificated)
        await state.update_data(authentificated = message.chat.id)

@router.message(
    AuthForm.password
)
async def password_chosen_incorrectly(message: Message, state: FSMContext):

    await message.answer('Вы ввели неккоректный пароль. Придумайте другой!')
    await state.set_state(AuthForm.password)

