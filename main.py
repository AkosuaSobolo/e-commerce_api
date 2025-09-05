from fastapi import FastAPI
from fastapi import HTTPException
from pydantic import BaseModel
# from typing import List, Dict, Any
from db import product_collection
from db import user_db
from db import cart_db

app = FastAPI()


# Models


class CreateUserModel(BaseModel):
    id: int
    username: str
    email: str
    password: str


class CartItem(BaseModel):
    product_id: int
    quantity: int


# Database Simulation


# cart_db: Dict[int, List[Dict[str, Any]]] = {}

# Routes


@app.get("/")
def get_home():
    return {"message": "Oi, Hola Amigos! Welcome to our E-commerce API!"}


# Products
@app.get("/products")
def get_all_products():
    return {"products": product_collection}


@app.get("/products/{product_id}")
def get_products_by_id(product_id: int):
    for product in product_collection:
        if product["_id"] == product_id:
            return {"product": product}
    else:
        raise HTTPException(status_code=404, detail="uh-oh! Product not found!")

# Allow product update

# User registration
@app.post("/register")
def register_user(user: CreateUserModel):
    # Check whether email already exists
    for existing_user in user_db:
        if existing_user["email"] == user.email:
            raise HTTPException(status_code=409, detail="Sorry, email already exists!")
    user_db.append(user.model_dump())
    return {"message": "User registered successfully!"}


@app.post("/login")
def login_user(user: CreateUserModel):
    for existing_user in user_db:
        if (
            existing_user["username"] == user.username
            or existing_user["email"] == user.email
        ) and existing_user["password"] == user.password:
            return {"message": "Login successful"}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials, Please try again!")

# Cart
@app.post("/cart/{user_id}")
def add_to_cart(user_id: int, item: CartItem):
    # Check whether product exists
    product = next((p for p in product_collection if p["_id"] == item.product_id), None)
    if not product:
        raise HTTPException(status_code=404, detail="uh-oh! Product not found!")

    if user_id not in cart_db:
        cart_db[user_id] = []

    for cart_item in cart_db[user_id]:
        if cart_item["product_id"] == item.product_id:
            cart_item["quantity"] += item.quantity
            return {"message": "Product quantity updated in cart"}

    cart_db[user_id].append(item.model_dump())
    return {"message": "Product added to cart"}


@app.get("/cart/{user_id}")
def get_cart(user_id: int):
    return {"user_id": user_id, "cart": cart_db.get(user_id, [])}


# Checkout
@app.post("/checkout/{user_id}")
def checkout(user_id: int):
    cart_items = cart_db.get(user_id, [])
    if not cart_items:
        raise HTTPException(status_code=404, detail="Cart is empty, cannot checkout!")

    total_amount = 0.0
    order_summary = []

    for item in cart_items:
        product = next(
            (p for p in product_collection if p["_id"] == item["product_id"]), None
        )
        if product:
            subtotal = product["price"] * item["quantity"]
            total_amount += subtotal
            order_summary.append(
                {
                    "product_name": product["name"],
                    "quantity": item["quantity"],
                    "price": product["price"],
                    "subtotal": subtotal,
                }
            )

    return {
        "order_summary": order_summary,
        "total amount paid": total_amount,
        "message": "Checkout successful, mate! Thank You For Coming, See You Next Time!!"
        }
