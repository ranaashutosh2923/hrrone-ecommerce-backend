from pydantic import BaseModel
from typing import List

class OrderItem(BaseModel):
    product_id: str
    quantity: int

class OrderCreate(BaseModel):
    user_id: str
    items: List[OrderItem]

class OrderResponse(BaseModel):
    order_id: str
    user_id: str
    items: List[OrderItem]

class OrderCreateResponse(BaseModel):
    message: str
    order_id: str