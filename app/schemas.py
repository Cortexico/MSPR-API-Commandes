from pydantic import BaseModel
from typing import Optional

class OrderBase(BaseModel):
    customer_id: int
    total_amount: float
    status: Optional[str] = "pending"

class OrderCreate(OrderBase):
    pass

class OrderUpdate(BaseModel):
    customer_id: Optional[int]
    total_amount: Optional[float]
    status: Optional[str]

class OrderResponse(OrderBase):
    id: int

    class Config:
        orm_mode = True
