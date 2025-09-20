
# E-commerce API

A simple E-commerce API built with **FastAPI + MongoDB** that supports product management, user authentication, shopping cart, and checkout functionality.

## Features

1. User Registration and Login
2. Product Management (Add, Update, Delete, View Products)
3. Search and Filter Products with Pagination
4. Add Products to Cart
5. View Cart by User
6. Checkout with Order Summary
7. Built with **FastAPI** for speed and scalability

## Tech Stack

1. Backend Framework: FastAPI
2. Database: MongoDB
3. Validation: Pydantic
4. Authentication: Basic (email + password)
5. Error Handling: FastAPI’s HTTPException


## How to Run

1. Clone this repo

2. Install dependencies: pip install -r requirements.txt

3. Set up .env file in the project root with your MongoDB URI (example):
   env (MONGO_URI=mongodb://localhost:27017)

4. Start the server: fastapi dev

5. Open in browser or Postman at: http://127.0.0.1:8000/docs
   

## API Endpoints

### Home

GET /
  Response:

  json
  {"message": "Oi, Hola Amigos! Welcome to our E-commerce API!"}

### User Authentication

#### Register User

POST /register
  Request:

json
{
  "id": 1,
  "username": "Akosua",
  "email": "akos@example.com",
  "password": "secret123"
}

Response:

json
{"message": "User registered successfully!"}

#### Login User

POST /login
  Request:

json
{
  "id": 1,
  "username": "Akosua",
  "email": "akos@example.com",
  "password": "secret123"
}

Response:

json
{"message": "Login Successful"}

### Product Management

#### Add Product

POST /products
  Request:

json
{
  "name": "Laptop",
  "price": 1200.50,
  "stock_quantity": 5,
  "description": "High-performance black laptop"
}

Response:

json
{"message": "product added successfully"}

#### Get All Products

GET /products?title=\&description=\&limit=10\&skip=0
  Response Example:

json
{
  "data": [
    {
      "name": "Laptop",
      "price": 1200.50,
      "stock_quantity": 5,
      "description": "High-performance black laptop"
    },
    {
      "name": "Headphones",
      "price": 200.00,
      "stock_quantity": 20,
      "description": "Noise cancelling"
    }
  ]
}

#### Get Product by ID

GET /products/{product\_id}
  Response:

json
{
  "data": {
    "name": "Laptop",
    "price": 1200.50,
    "stock_quantity": 5,
    "description": "High-performance black laptop"
  }
}

#### Update Product

PATCH /products/{product\_id}
  Request:

json
{
  "name": "Gaming Laptop",
  "price": 1500.00,
  "description": "Updated version",
  "stock_quantity": 10
}

Response:

json
{"message": "Product successfully updated"}

#### Delete Product

DELETE /products/{product\_id}
  Response:

json
{"message": "Product deleted successfully"}

### Cart Management

#### Add to Cart

POST /cart
  Request:

json
{
  "user_id": "123",
  "product_id": "64f1c9b3e7a4f84b0c1c2d99",
  "quantity": 2
}

Response:

json
{"message": "Product added to cart"}

#### View Cart

GET /cart/{user\_id}
  Response:

json
[
  {
    "user_id": "123",
    "product_id": "64f1c9b3e7a4f84b0c1c2d99",
    "quantity": 2
  }
]

### Checkout

#### Checkout User Cart

POST /checkout/{user\_id}
  Response Example:

json
{
  "order_summary": [
    {
      "product_name": "Laptop",
      "quantity": 2,
      "price": 1200.50,
      "subtotal": 2401.00
    }
  ],
  "total_amount_paid": 2401.00,
  "message": "Checkout successful, mate! Thank You for Coming, See You Next Time!!"
}

## Error Handling

1. Invalid MongoDB ID: Returns 422 Unprocessable Entity
2. Product not found: Returns 404 Not Found
3. Email already exists: Returns 409 Conflict
4. Invalid login credentials: Returns 401 Unauthorized
5. Empty cart at checkout: Returns 404 Not Found
  

## Future Improvements

1. JWT Authentication for secure endpoints
2. User Profiles with order history
3. Payment Gateway Integration (Stripe/PayPal)
4. Role-based Access Control (Admin vs Customer)
5. Product Categories & Advanced Search
6. Docker Deployment
7. JWT authentication
