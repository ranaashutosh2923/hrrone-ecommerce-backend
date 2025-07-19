from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List
import re
from bson import ObjectId

from ..database.connection import get_database
from ..models.product import ProductCreate, ProductResponse, ProductCreateResponse

router = APIRouter()

@router.post("/products", response_model=ProductCreateResponse, status_code=201)
async def create_product(product: ProductCreate):
    try:
        db = get_database()
        collection = db.products
        
        product_dict = product.dict()
        result = collection.insert_one(product_dict)
        
        return ProductCreateResponse(
            message="Product created successfully",
            product_id=str(result.inserted_id)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/products", response_model=List[ProductResponse])
async def list_products(
    name: Optional[str] = Query(None),
    size: Optional[str] = Query(None),
    limit: Optional[int] = Query(None),
    offset: Optional[int] = Query(0)
):
    try:
        db = get_database()
        collection = db.products
        
        # Build query filter
        query_filter = {}
        
        if name:
            # Support regex/partial match for name
            query_filter["name"] = {"$regex": name, "$options": "i"}
        
        if size:
            query_filter["size"] = size
        
        # Create cursor with sorting by _id
        cursor = collection.find(query_filter).sort("_id", 1)
        
        # Apply offset
        if offset:
            cursor = cursor.skip(offset)
        
        # Apply limit
        if limit:
            cursor = cursor.limit(limit)
        
        # Convert results
        products = []
        for product in cursor:
            products.append(ProductResponse(
                id=str(product["_id"]),
                name=product["name"],
                size=product["size"],
                price=product["price"]
            ))
        
        return products
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))