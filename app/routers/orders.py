from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List
from bson import ObjectId
from pymongo.read_concern import ReadConcern
from pymongo.write_concern import WriteConcern
from pymongo.read_preferences import ReadPreference

from ..database.connection import get_database
from ..models.order import OrderCreate, OrderResponse, OrderCreateResponse, OrderItem

router = APIRouter()

@router.post("/orders", response_model=OrderCreateResponse, status_code=201)
async def create_order(order: OrderCreate):
    db = get_database()
    collection = db.orders
    products_collection = db.products
    client = collection.database.client
    with client.start_session() as session:
        with session.start_transaction(write_concern=WriteConcern("majority")):
            # Collect all product_ids from the order
            product_ids = []
            for item in order.items:
                try:
                    product_ids.append(ObjectId(item.product_id))
                except Exception:
                    raise HTTPException(
                        status_code=400,
                        detail=f"Invalid product_id format: {item.product_id}"
                    )
            # Fetch all products in one query
            found_products = set(doc["_id"] for doc in products_collection.find({"_id": {"$in": product_ids}}, session=session))
            for pid in product_ids:
                if pid not in found_products:
                    raise HTTPException(
                        status_code=400,
                        detail=f"Product with id {str(pid)} not found"
                    )
            order_dict = order.dict()
            result = collection.insert_one(order_dict, session=session)
            return OrderCreateResponse(
                message="Order created successfully",
                order_id=str(result.inserted_id)
            )

@router.get("/orders/{user_id}", response_model=List[OrderResponse])
async def get_user_orders(
    user_id: str,
    limit: Optional[int] = Query(None),
    offset: Optional[int] = Query(0)
):
    db = get_database()
    collection = db.orders
    client = collection.database.client
    with client.start_session() as session:
        with session.start_transaction(read_concern=ReadConcern("majority"), read_preference=ReadPreference.PRIMARY):
            query_filter = {"user_id": user_id}
            cursor = collection.find(query_filter, session=session).sort("_id", 1)
            if offset:
                cursor = cursor.skip(offset)
            if limit:
                cursor = cursor.limit(limit)
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