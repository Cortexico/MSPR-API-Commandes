from sqlalchemy.future import select
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas import OrderCreate, OrderUpdate, Order
from app import crud
from app.database import get_db
from typing import List
from app import models
from sqlalchemy.orm import selectinload

router = APIRouter(
    prefix="/orders",
    tags=["orders"]
)

customer_router = APIRouter(
    prefix="/customers",
    tags=["customers"]
)

# GET /orders
@router.get("/", response_model=List[Order])
async def get_orders(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    orders = await crud.get_orders(db, skip=skip, limit=limit)
    return orders

# GET /orders/{order_id}
@router.get("/{order_id}", response_model=Order)
async def get_order(order_id: int, db: AsyncSession = Depends(get_db)):
    order = await crud.get_order(db, order_id=order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="Commande non trouvée")
    return order

# POST /orders
@router.post("/", response_model=Order, status_code=status.HTTP_201_CREATED)
async def create_order(
    order: OrderCreate,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
):
    db_order = await crud.create_order(db=db, order=order)
    background_tasks.add_task(crud.publish_order_created, db_order)
    # Valider l'objet ORM en modèle Pydantic avant de le retourner
    order_response = Order.model_validate(db_order)
    return order_response

# PUT /orders/{order_id}
@router.put("/{order_id}", response_model=Order)
async def update_order(order_id: int, order: OrderUpdate, db: AsyncSession = Depends(get_db)):
    db_order = await crud.update_order(db, order_id, order)
    if db_order is None:
        raise HTTPException(status_code=404, detail="Commande non trouvée")
    return db_order

# DELETE /orders/{order_id}
@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_order(order_id: int, db: AsyncSession = Depends(get_db)):
    db_order = await crud.delete_order(db, order_id)
    if db_order is None:
        raise HTTPException(status_code=404, detail="Commande non trouvée")
    return  # No content for 204 response

@customer_router.get("/{customer_id}/orders", response_model=List[Order])
async def get_orders_by_customer(customer_id: int, db: AsyncSession = Depends(get_db)):
    # Vérifier si le client existe dans la base locale
    result = await db.execute(select(models.Customer).where(models.Customer.id == customer_id))
    customer = result.scalar_one_or_none()
    if customer is None:
        raise HTTPException(status_code=404, detail="Client non trouvé")
    
    # Récupérer les commandes du client avec les items chargés
    result = await db.execute(
        select(models.Order)
        .options(selectinload(models.Order.items))
        .where(models.Order.customer_id == customer_id)
    )
    orders = result.scalars().all()
    return orders

# GET /customers/{customer_id}/orders/{order_id}/products
@customer_router.get("/{customer_id}/orders/{order_id}/products")
async def get_order_products(customer_id: int, order_id: int, db: AsyncSession = Depends(get_db)):
    # Vérifier si le client existe
    result = await db.execute(select(models.Customer).where(models.Customer.id == customer_id))
    customer = result.scalar_one_or_none()
    if customer is None:
        raise HTTPException(status_code=404, detail="Client non trouvé")

    # Vérifier si la commande existe et appartient au client, en chargeant les items et les produits associés
    result = await db.execute(
        select(models.Order)
        .options(
            selectinload(models.Order.items).selectinload(models.OrderItem.product)
        )
        .where(
            models.Order.id == order_id,
            models.Order.customer_id == customer_id
        )
    )
    order = result.scalar_one_or_none()
    if order is None:
        raise HTTPException(status_code=404, detail="Commande non trouvée")

    # Récupérer les produits de la commande
    products = []
    for item in order.items:
        product = item.product
        if product:
            products.append({
                "product_id": product.id,
                "name": product.name,
                "quantity": item.quantity,
                "price": item.price
            })
    return products