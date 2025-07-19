from pydantic import BaseModel
from typing import Optional

class ProductCreate(BaseModel):
    name: str
    size: str
    price: int

class ProductResponse(BaseModel):
    id: str
    name: str
    size: str
    price: int

class ProductCreateResponse(BaseModel):
    message: str
    product_id: str