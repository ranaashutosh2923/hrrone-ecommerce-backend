from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List
import re
from bson import ObjectId
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from pymongo.read_concern import ReadConcern
from pymongo.write_concern import WriteConcern
from pymongo.read_preferences import ReadPreference

from ..database.connection import get_database
from ..models.product import ProductCreate, ProductResponse, ProductCreateResponse

router = APIRouter()

@router.post("/products", response_model=ProductCreateResponse, status_code=201)
async def create_product(product: ProductCreate):
    db = get_database()
    collection = db.products
    # Use a session for transaction
    client = collection.database.client
    with client.start_session() as session:
        with session.start_transaction(write_concern=WriteConcern("majority")):
            try:
                product_dict = product.dict()
                result = collection.insert_one(product_dict, session=session)
                return ProductCreateResponse(
                    message="Product created successfully",
                    product_id=str(result.inserted_id)
                )
            except DuplicateKeyError:
                raise HTTPException(
                    status_code=409,
                    detail="Product already exists with same name, size, and price."
                )

@router.get("/products", response_model=List[ProductResponse])
async def list_products(
    name: Optional[str] = Query(None),
    size: Optional[str] = Query(None),
    limit: Optional[int] = Query(None),
    offset: Optional[int] = Query(0)
):
    db = get_database()
    collection = db.products
    client = collection.database.client
    with client.start_session() as session:
        with session.start_transaction(
            read_concern=ReadConcern("majority"),
            read_preference=ReadPreference.PRIMARY,
            write_concern=WriteConcern("majority")
        ):
            query_filter = {}
            if name:
                # Use text index for efficient name search
                query_filter["$text"] = {"$search": name}
            if size:
                query_filter["size"] = size
                
            # Optimize query with projection and index usage
            projection = {
                "_id": 1,
                "name": 1,
                "size": 1,
                "price": 1
            }
            
            cursor = collection.find(
                query_filter,
                projection=projection,
                session=session
            ).sort("_id", 1)
            
            if offset:
                cursor = cursor.skip(offset)
            if limit:
                cursor = cursor.limit(limit)
                
            products = []
            for product in cursor:
                products.append(ProductResponse(
                    id=str(product["_id"]),
                    name=product["name"],
                    size=product["size"],
                    price=product["price"]
                ))
            return products