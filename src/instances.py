from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from storage.redis_db import storage
from aiogram.fsm.storage.memory import MemoryStorage 

from config.settings import settings
# from bot.tg import router as start_router
from bot.auth.routes import router as auth_router
from bot.mainline.routes import router as main_router
from bot.mainline.add_event.routes import router as add_router

default = DefaultBotProperties(parse_mode=ParseMode.HTML)
bot = Bot(token=settings.BOT_TOKEN, default=default)
dp = Dispatcher(storage=storage)

dp.include_router(auth_router)
dp.include_router(main_router)
dp.include_router(add_router)