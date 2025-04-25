import json
import os
from typing import Optional, List
from aio_pika import connect_robust, Message, ExchangeType
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app import models, schemas
from sqlalchemy.orm import selectinload
from fastapi import HTTPException


async def create_order(db: AsyncSession, order: schemas.OrderCreate) -> models.Order:
    # Vérifier si le client existe
    result = await db.execute(select(models.Customer).where(models.Customer.id == order.customer_id))
    customer = result.scalar_one_or_none()
    if customer is None:
        raise HTTPException(status_code=404, detail="Client non trouvé")
    
    # Créer la commande
    db_order = models.Order(
        customer_id=order.customer_id,
        total_amount=order.total_amount,
        status=order.status
    )
    # Créer les OrderItems associés
    db_order.items = [
        models.OrderItem(
            product_id=item.product_id,
            quantity=item.quantity,
            price=item.price
        )
        for item in order.items
    ]
    db.add(db_order)
    await db.commit()
    await db.refresh(db_order, attribute_names=["items"])
    return db_order

# Obtenir une commande par ID avec les items chargés
async def get_order(db: AsyncSession, order_id: int) -> Optional[models.Order]:
    result = await db.execute(
        select(models.Order)
        .options(selectinload(models.Order.items))
        .where(models.Order.id == order_id)
    )
    return result.scalar_one_or_none()

# Obtenir toutes les commandes avec les items chargés
async def get_orders(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[models.Order]:
    result = await db.execute(
        select(models.Order)
        .options(selectinload(models.Order.items))
        .offset(skip)
        .limit(limit)
    )
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
    RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "rabbitmq")
    RABBITMQ_PORT = int(os.getenv("RABBITMQ_PORT", "5672"))
    RABBITMQ_USER = os.getenv("RABBITMQ_USER", "guest")
    RABBITMQ_PASSWORD = os.getenv("RABBITMQ_PASSWORD", "guest")

    connection = await connect_robust(
        host=RABBITMQ_HOST,
        port=RABBITMQ_PORT,
        login=RABBITMQ_USER,
        password=RABBITMQ_PASSWORD
    )

    async with connection:
        channel = await connection.channel()
        exchange = await channel.declare_exchange("order_updates", ExchangeType.FANOUT)
        message_body = json.dumps({
            "action": "create",
            "data": {
                "id": order.id,
                "customer_id": order.customer_id,
                "total_amount": order.total_amount,
                "status": order.status
            }
        })
        message = Message(message_body.encode('utf-8'))
        await exchange.publish(message, routing_key="")