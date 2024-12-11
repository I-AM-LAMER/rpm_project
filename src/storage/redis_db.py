from redis.asyncio import Redis, ConnectionPool
from aiogram.fsm.storage.redis import RedisStorage

from config.settings import settings


pool = ConnectionPool(host=settings.REDIS_HOST, port=settings.REDIS_PORT)
redis_storage = Redis(connection_pool=pool)
storage = RedisStorage(redis_storage)