import os
import json
import asyncio
import aio_pika
from app.database import async_session
from app.models import Customer

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "rabbitmq")
RABBITMQ_PORT = int(os.getenv("RABBITMQ_PORT", "5672"))
RABBITMQ_USER = os.getenv("RABBITMQ_USER", "guest")
RABBITMQ_PASSWORD = os.getenv("RABBITMQ_PASSWORD", "guest")

async def process_customer_message(message: aio_pika.IncomingMessage):
    async with message.process():
        data = json.loads(message.body)
        action = data.get('action')
        customer_data = data.get('data')

        async with async_session() as session:
            if action == 'create':
                customer = Customer(**customer_data)
                session.add(customer)
            elif action == 'update':
                customer = await session.get(Customer, customer_data['id'])
                if customer:
                    for key, value in customer_data.items():
                        setattr(customer, key, value)
            elif action == 'delete':
                customer = await session.get(Customer, customer_data['id'])
                if customer:
                    await session.delete(customer)
            await session.commit()

async def start_customer_consumer():
    connection = await aio_pika.connect_robust(
        host=RABBITMQ_HOST,
        port=RABBITMQ_PORT,
        login=RABBITMQ_USER,
        password=RABBITMQ_PASSWORD
    )
    channel = await connection.channel()
    exchange = await channel.declare_exchange('customer_exchange', aio_pika.ExchangeType.FANOUT)
    queue = await channel.declare_queue('', exclusive=True)
    await queue.bind(exchange)

    await queue.consume(process_customer_message)