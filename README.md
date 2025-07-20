# HROne Ecommerce Backend API

A FastAPI-based backend application for an ecommerce platform with product and order management capabilities.

## Features

- **Product Management**: 
  - Create and list products with filtering and pagination
  - Automatic duplicate product detection
  - Text-based search optimization for product names
  - Efficient data indexing
- **Order Management**: 
  - Create orders and retrieve user-specific orders
  - Optimized product verification
  - Transaction-safe operations
- **MongoDB Integration**: 
  - Efficient data storage and retrieval
  - Automatic indexing for performance
  - Transaction support for data consistency
- **RESTful API Design**: 
  - Clean and well-structured endpoints
  - Proper error handling
  - Pagination support

## Tech Stack

- **Language**: Python 3.13
- **Framework**: FastAPI
- **Database**: MongoDB (with pymongo)
- **Cloud Database**: MongoDB Atlas M0 (Free Tier)

## Project Structure

```
hrrone-ecommerce-backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry point
│   ├── database/
│   │   ├── __init__.py
│   │   └── connection.py    # MongoDB connection logic
│   ├── models/
│   │   ├── __init__.py
│   │   ├── product.py       # Product data models
│   │   └── order.py         # Order data models
│   └── routers/
│       ├── __init__.py
│       ├── products.py      # Product API endpoints
│       └── orders.py        # Order API endpoints
├── .env                     # Environment variables
├── requirements.txt         # Python dependencies
└── README.md               # Project documentation
```

## Installation & Setup

1. **Clone or download the project**
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Configure environment variables** in `.env`:
   ```
   MONGODB_URL=your_mongodb_atlas_connection_string
   DATABASE_NAME=ecommerce
   ```

## Running the Application

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## API Endpoints

### Products API

#### Create Product
- **POST** `/products`
- **Request Body**:
  ```json
  {
    "name": "Product Name",
    "size": "large",
    "price": 499
  }
  ```

#### List Products
- **GET** `/products`
- **Query Parameters**: `name`, `size`, `limit`, `offset`

### Orders API

#### Create Order
- **POST** `/orders`
- **Request Body**:
  ```json
  {
    "user_id": "user123",
    "items": [
      {"product_id": "product_id_here", "quantity": 2}
    ]
  }
  ```

#### Get User Orders
- **GET** `/orders/{user_id}`
- **Query Parameters**: `limit`, `offset`

## Database Design

### Products Collection
- Stores product information (name, size, price)
- Indexes:
  - Text index on `name` field for efficient text search
  - Compound unique index on `{name, size, price}` for duplicate prevention

### Orders Collection
- Stores order data with user references and item details
- Optimized queries for product verification
- Transaction-safe operations

## Performance Optimizations
- Text indexing for efficient product searches
- Optimized database queries to prevent N+1 query issues
- Transaction management for data consistency
- Proper read/write concerns for MongoDB operations

## Deployment

This application is designed to be deployed on platforms like Render or Railway with MongoDB Atlas as the database.

### Deployment Prerequisites
- MongoDB Atlas cluster (M0 or higher)
- Proper environment variables configuration
- Node.js runtime environment