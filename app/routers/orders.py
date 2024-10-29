from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas import OrderCreate, OrderUpdate, OrderResponse
from app import crud
from app.database import get_db
from typing import List

router = APIRouter(
    prefix="/orders",
    tags=["orders"]
)

# GET /orders
@router.get("/", response_model=List[OrderResponse])
async def get_orders(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    orders = await crud.get_orders(db, skip=skip, limit=limit)
    return orders

# GET /orders/{order_id}
@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(order_id: int, db: AsyncSession = Depends(get_db)):
    order = await crud.get_order(db, order_id=order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="Commande non trouvée")
    return order

# POST /orders
@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def create_order(
    order: OrderCreate,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
):
    db_order = await crud.create_order(db=db, order=order)
    background_tasks.add_task(crud.publish_order_created, db_order)
    return db_order

# PUT /orders/{order_id}
@router.put("/{order_id}", response_model=OrderResponse)
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
