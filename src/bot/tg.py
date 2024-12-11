from aiogram.client.default import DefaultBotProperties
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.enums import ParseMode

from aio_pika import connect_robust, ExchangeType, DeliveryMode
import aio_pika
import logging
from aiogram import Router

router = Router()

@router.message()
async def start(message: Message) -> None:
    await message.answer(message.text)