import asyncio

from aio_pika import ExchangeType, connect, Channel
from aio_pika.abc import AbstractIncomingMessage
from ...storage.rabbit import channel_pool

from .process import process_message

async def start_consumer() -> None:
    # Perform connection
    connection = await connect("amqp://guest:guest@localhost/")

    channel: Channel

    async with channel_pool.acquire() as channel:

        # Will take no more than 10 messages in advance
        await channel.set_qos(prefetch_count=10) # TODO почитать

        exchange = await channel.declare_exchange(
            "user_schedule", ExchangeType.DIRECT,
        )

        # Declaring queue
        queue = await channel.declare_queue('users_creds', durable=True)

        await queue.bind(exchange=exchange)

        await queue.consume(process_message)

        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(start_consumer())