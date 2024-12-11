import asyncio
from asyncio import Task
from typing import Any

from aiogram.methods.base import TelegramType, TelegramMethod
from aiogram.types import Update
from starlette.requests import Request
import logging

from src.api import router
from src.instances import dp, bot
from src.bg_tasks import background_tasks


@router.post("/webhook")
async def webhook(
    request: Request,
) -> None:
    data = await request.json()
    update = Update(**data)
    
    task: Task[TelegramMethod[Any] | None] = asyncio.create_task(dp.feed_webhook_update(bot, update))
    background_tasks.add(task)
    task.add_done_callback(background_tasks.discard)
