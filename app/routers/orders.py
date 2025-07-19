from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List
from bson import ObjectId

from ..database.connection import get_database
from ..models.order import OrderCreate, OrderResponse, OrderCreateResponse, OrderItem

router = APIRouter()

@router.post("/orders", response_model=OrderCreateResponse, status_code=201)
async def create_order(order: OrderCreate):
    try:
        db = get_database()
        collection = db.orders
        
        # Verify that all products exist
        products_collection = db.products
        for item in order.items:
            try:
                product_id = ObjectId(item.product_id)
                product = products_collection.find_one({"_id": product_id})
                if not product:
                    raise HTTPException(
                        status_code=400, 
                        detail=f"Product with id {item.product_id} not found"
                    )
            except Exception:
                raise HTTPException(
                    status_code=400, 
                    detail=f"Invalid product_id format: {item.product_id}"
                )
        
        order_dict = order.dict()
        result = collection.insert_one(order_dict)
        
        return OrderCreateResponse(
            message="Order created successfully",
            order_id=str(result.inserted_id)
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/orders/{user_id}", response_model=List[OrderResponse])
async def get_user_orders(
    user_id: str,
    limit: Optional[int] = Query(None),
    offset: Optional[int] = Query(0)
):
    try:
        db = get_database()
        collection = db.orders
        
        # Query orders for specific user
        query_filter = {"user_id": user_id}
        
        # Create cursor with sorting by _id
        cursor = collection.find(query_filter).sort("_id", 1)
        
        # Apply offset
        if offset:
            cursor = cursor.skip(offset)
        
        # Apply limit
        if limit:
            cursor = cursor.limit(limit)
        
        # Convert results
        orders = []
        for order in cursor:
            order_items = []
            for item in order["items"]:
                order_items.append(OrderItem(
                    product_id=item["product_id"],
                    quantity=item["quantity"]
                ))
            
            orders.append(OrderResponse(
                order_id=str(order["_id"]),
                user_id=order["user_id"],
                items=order_items
            ))
        
        return orders
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))