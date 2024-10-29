from pydantic import BaseModel
from typing import Optional

class OrderBase(BaseModel):
    customer_id: int
    total_amount: float
    status: Optional[str] = "pending"

class OrderCreate(OrderBase):
    pass

class OrderUpdate(BaseModel):
    customer_id: Optional[int] = None
    total_amount: Optional[float] = None
    status: Optional[str] = None

class OrderResponse(OrderBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
    
    #depreciated
    #class Config:
     #   orm_mode = True
