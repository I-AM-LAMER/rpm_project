from ...storage.pg import async_session
from ...schema import user_creds
from ...db.models import User
import msgpack
from aio_pika import Message

async def process_message(message: Message):
    data = msgpack.unpackb(message.body)
    user = user_creds.User(**data)

    async with async_session() as session:
        await session.add(User(**user.model_dump()))