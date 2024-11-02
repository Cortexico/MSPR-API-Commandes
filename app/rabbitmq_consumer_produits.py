import os
import json
import asyncio
import aio_pika
from app.database import async_session
from app.models import Product

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "rabbitmq")
RABBITMQ_PORT = int(os.getenv("RABBITMQ_PORT", "5672"))
RABBITMQ_USER = os.getenv("RABBITMQ_USER", "guest")
RABBITMQ_PASSWORD = os.getenv("RABBITMQ_PASSWORD", "guest")

async def process_product_message(message: aio_pika.IncomingMessage):
    async with message.process():
        data = json.loads(message.body)
        action = data.get('action')
        product_data = data.get('data')

        async with async_session() as session:
            if action == 'create':
                product = Product(**product_data)
                session.add(product)
            elif action == 'update':
                product = await session.get(Product, product_data['_id'])
                if product:
                    for key, value in product_data.items():
                        setattr(product, key, value)
            elif action == 'delete':
                product = await session.get(Product, product_data['id'])
                if product:
                    await session.delete(product)
            await session.commit()

async def start_product_consumer():
    connection = await aio_pika.connect_robust(
        host=RABBITMQ_HOST,
        port=RABBITMQ_PORT,
        login=RABBITMQ_USER,
        password=RABBITMQ_PASSWORD
    )
    channel = await connection.channel()
    exchange = await channel.declare_exchange('product_exchange', aio_pika.ExchangeType.FANOUT)
    queue = await channel.declare_queue('', exclusive=True)
    await queue.bind(exchange)

    await queue.consume(process_product_message)