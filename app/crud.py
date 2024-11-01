import json
import os
from typing import Optional, List
from aio_pika import connect_robust, Message, ExchangeType
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app import models, schemas

# Créer une nouvelle commande
async def create_order(db: AsyncSession, order: schemas.OrderCreate) -> models.Order:
    db_order = models.Order(
        customer_id=order.customer_id,
        total_amount=order.total_amount,
        status=order.status
    )
    db.add(db_order)
    await db.commit()
    await db.refresh(db_order)

    # Publier un message dans RabbitMQ après la création de la commande
    await publish_order_created(db_order)

    return db_order

# Obtenir une commande par ID
async def get_order(db: AsyncSession, order_id: int) -> Optional[models.Order]:
    result = await db.execute(select(models.Order).where(models.Order.id == order_id))
    return result.scalar_one_or_none()

# Obtenir toutes les commandes
async def get_orders(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[models.Order]:
    result = await db.execute(select(models.Order).offset(skip).limit(limit))
    return result.scalars().all()

# Mettre à jour une commande
async def update_order(db: AsyncSession, order_id: int, order: schemas.OrderUpdate) -> Optional[models.Order]:
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
async def delete_order(db: AsyncSession, order_id: int) -> Optional[models.Order]:
    db_order = await get_order(db, order_id)
    if db_order:
        await db.delete(db_order)
        await db.commit()
        return db_order
    return None

# Publier un message dans RabbitMQ
async def publish_order_created(order: models.Order):
    RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
    RABBITMQ_PORT = os.getenv("RABBITMQ_PORT", "5672")

    connection = await connect_robust(
        f"amqp://guest:guest@{RABBITMQ_HOST}:{RABBITMQ_PORT}/"
    )

    async with connection:
        channel = await connection.channel()
        exchange = await channel.declare_exchange("orders", ExchangeType.FANOUT)
        message_body = json.dumps({
            "order_id": order.id,
            "customer_id": order.customer_id,
            "total_amount": order.total_amount,
            "status": order.status
        })
        message = Message(message_body.encode('utf-8'))
        await exchange.publish(message, routing_key="")
