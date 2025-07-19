from fastapi import FastAPI
from .routers import products, orders
from .database.connection import close_database
import atexit
import os

app = FastAPI(
    title="HROne Ecommerce Backend API",
    description="Backend API for ecommerce application",
    version="1.0.0"
)

# Include routers
app.include_router(products.router)
app.include_router(orders.router)

@app.get("/")
async def root():
    return {"message": "HROne Ecommerce Backend API is running!"}

# Close database connection on shutdown
atexit.register(close_database)