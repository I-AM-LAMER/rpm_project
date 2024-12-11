import asyncio
import logging
from typing import AsyncContextManager, Callable, AsyncIterator, Never, AsyncGenerator


import uvicorn

from aiogram import Dispatcher, Bot, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from contextlib import asynccontextmanager
from fastapi import FastAPI
from starlette_context import plugins
from starlette_context.middleware import RawContextMiddleware

from bg_tasks import background_tasks
from config.settings import settings
from instances import bot, dp
from api.router import router as webhook_router

from consumer.process_user.user import start_consumer

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:

    await bot.set_webhook(settings.BOT_WEBHOOK_URL)
    yield

    while background_tasks:
        asyncio.sleep(0)

    await bot.delete_webhook()

def create_app() -> FastAPI:
    app = FastAPI(docs_url='/swagger', lifespan=lifespan)
    app.include_router(webhook_router)

    return app


async def start_polling():

    await bot.delete_webhook()

    await dp.start_polling(bot)

    await start_consumer()

if __name__ == '__main__':
    if settings.BOT_WEBHOOK_URL != 'None':
        uvicorn.run('src.app:create_app', factory=True, host='0.0.0.0', port=8000, workers=1)
    else:
        asyncio.run(start_polling())