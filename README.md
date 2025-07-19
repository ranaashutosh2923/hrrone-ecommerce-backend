# HROne Ecommerce Backend API

A FastAPI-based backend application for an ecommerce platform with product and order management capabilities.

## Features

- **Product Management**: Create and list products with filtering and pagination
- **Order Management**: Create orders and retrieve user-specific orders
- **MongoDB Integration**: Efficient data storage and retrieval
- **RESTful API Design**: Clean and well-structured endpoints

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

- **Products Collection**: Stores product information (name, size, price)
- **Orders Collection**: Stores order data with user references and item details

## Deployment

This application is designed to be deployed on platforms like Render or Railway with MongoDB Atlas as the database.