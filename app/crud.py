import json
import asyncio
import os
from aio_pika import connect_robust, Message, ExchangeType
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app import models, schemas

# Récupérer une commande par ID
async def get_order(db: AsyncSession, order_id: int):
    result = await db.execute(select(models.Order).where(models.Order.id == order_id))
    return result.scalar_one_or_none()

# Récupérer toutes les commandes
async def get_orders(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(models.Order).offset(skip).limit(limit))
    return result.scalars().all()

# Créer une nouvelle commande
async def create_order(db: AsyncSession, order: schemas.OrderCreate):
    db_order = models.Order(**order.dict())
    db.add(db_order)
    await db.commit()
    await db.refresh(db_order)

    # Publier un message sur RabbitMQ
    asyncio.create_task(publish_order_created(db_order))

    return db_order

# Mettre à jour une commande
async def update_order(db: AsyncSession, order_id: int, order: schemas.OrderUpdate):
    db_order = await get_order(db, order_id)
    if db_order:
        update_data = order.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_order, key, value)
        await db.commit()
        await db.refresh(db_order)
        return db_order
    return None

# Supprimer une commande
async def delete_order(db: AsyncSession, order_id: int):
    db_order = await get_order(db, order_id)
    if db_order:
        await db.delete(db_order)
        await db.commit()
        return db_order
    return None

# Publier un message sur RabbitMQ
async def publish_order_created(order):
    RABBITMQ_HOST = os.getenv("RABBITMQ_HOST")
    RABBITMQ_PORT = os.getenv("RABBITMQ_PORT")

    connection = await connect_robust(
        f"amqp://guest:guest@{RABBITMQ_HOST}:{RABBITMQ_PORT}/"
    )

    async with connection:
        channel = await connection.channel()
        exchange = await channel.declare_exchange("orders", ExchangeType.FANOUT)
        message_body = json.dumps({
            "order_id": order.id,
            "customer_id": order.customer_id,
            "total_amount": order.total_amount
            # Incluez les détails des produits commandés ici
        })
        message = Message(message_body.encode('utf-8'))
        await exchange.publish(message, routing_key="")
