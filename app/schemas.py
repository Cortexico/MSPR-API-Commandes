# from pydantic import BaseModel, ConfigDict
# from typing import Optional

# class OrderBase(BaseModel):
#     customer_id: int
#     total_amount: float
#     status: Optional[str] = "pending"

# class OrderCreate(OrderBase):
#     pass

# class OrderUpdate(BaseModel):
#     customer_id: Optional[int] = None
#     total_amount: Optional[float] = None
#     status: Optional[str] = None

# class OrderResponse(OrderBase):
#     id: int

#     model_config = ConfigDict(from_attributes=True)
    
#     #depreciated
#     #class Config:
#      #   orm_mode = True
     
from pydantic import BaseModel, ConfigDict
from typing import List, Optional

class OrderItemBase(BaseModel):
    product_id: str
    quantity: int
    price: float

    model_config = ConfigDict(from_attributes=True)

class OrderItemCreate(OrderItemBase):
    pass

class OrderItem(OrderItemBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

class OrderBase(BaseModel):
    customer_id: int
    total_amount: float
    status: str

    model_config = ConfigDict(from_attributes=True)

class OrderCreate(OrderBase):
    items: List[OrderItemCreate]

class OrderUpdate(BaseModel):
    total_amount: Optional[float] = None
    status: Optional[str] = None

class Order(OrderBase):
    id: int
    items: List[OrderItem]

    model_config = ConfigDict(from_attributes=True)
