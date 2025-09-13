from fastapi import FastAPI
from fastapi import HTTPException, status
from pydantic import BaseModel
from bson.objectid import ObjectId
# from typing import List, Dict, Any
from db import product_collection, user_db, cart_db
from utils import replace_mongo_id

app = FastAPI()


class CreateUserModel(BaseModel):
    id: int
    username: str
    email: str 
    password: str


class CartItem(BaseModel):
    user_id: str
    product_id: str
    quantity: int


class ProductModel(BaseModel):
    name: str
    price: float
    stock_quantity: int
    description: str

class UpdateProduct(BaseModel):
    name:str
    price: float
    description: str
    stock_quantity: int


# Database Simulation

# cart_db: Dict[int, List[Dict[str, Any]]] = {}

# Routes


@app.get("/")
def get_home():
    return {"message": "Oi, Hola Amigos! Welcome to our E-commerce API!"}


@app.post("/products")
def insert_product(product: ProductModel):
    product_collection.insert_one(product.model_dump())
    return {"message": "product added successfully"}


# Products
@app.get("/products")
def get_all_products(title="", description="", limit= 10, skip=0):
    # Get all events from database
    products = product_collection.find(
        filter={
            "$or": [
                {"title": {"$regex": title, "$options": "i"}},
                {"description": {"$regex": description, "$options": "i"}},
            ]
        },
        limit = int(limit),
        skip = int(skip),
    )

    # Return response
    return {"data": list(map(replace_mongo_id, products))}




@app.get("/products/{product_id}")
def get_products_by_id(product_id: str):
    # Check if event id is valid
    if not ObjectId.is_valid(product_id):
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, "Invalid mongo id received!")

    # Get event from database by id
    product = product_collection.find_one({"_id": ObjectId(product_id)})

    # Return response
    return {"data": replace_mongo_id(product)}



# Delete a product
@app.delete("/products/{product_id}")
def delete_product(product_id):
    # Check if event_id is valid mongo id
    if not ObjectId.is_valid(product_id):
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, "Invalid mongo id received!")
    # Delete event from database
    delete_result = product_collection.delete_one(filter={"_id": ObjectId(product_id)})
    if not delete_result.deleted_count:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Sorry, no product found to delete!")
    # Return reponse
    return{"message": "Product deleted successfully"}


# Allow product update by management
@app.patch("/products/{product_id}")
def update_product(product_id: str, product: UpdateProduct):
    if not ObjectId.is_valid(product_id):
        raise HTTPException(status_code=422, detail="Invalid MongoDB ID")

    result = product_collection.update_one(
        {"_id": ObjectId(product_id)},
        {"$set": product.dict()}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Product not found")

    return {"message": "Product successfully updated"}


# User registration
@app.post("/register")
def register_user(user: CreateUserModel):
    # Check whether email already exists
    for existing_user in user_db.find():
        if user_db.find_one({"email": user.email}):
            raise HTTPException(status_code=409, detail="Sorry, email already exists!")
    user.model_dump()
    user_db.insert_one({"email": user.email, "password": user.password})
    return {"message": "User registered successfully!"}


@app.post("/login")
def login_user(user: CreateUserModel):
    existing_user = user_db.find_one({"email": user.email, "password": user.password})
    if existing_user:
        return {"message": "Login Successful"}
    raise HTTPException(status_code=401, detail="Invalid credentials, Please try again!")


# Cart
@app.post("/cart")
def add_to_cart(item: CartItem):
    get_products_by_id(item.product_id)
    cart_db.insert_one(item.model_dump())
    # if not ObjectId.is_valid(item.product_id):
    #     raise HTTPException(status_code=422, detail="Invalid product id")
    # Check whether product exists
    # product = product_collection.find_one({"_id": ObjectId(item.product_id)})
    # if not product:
    #     raise HTTPException(status_code=404, detail="uh-oh! Product not found!")

    # if user_id not in cart_db:
    #     cart_db[user_id] = []

    # for cart_item in cart_db[user_id]:
    #     if cart_item["product_id"] == item.product_id:
    #         cart_item["quantity"] += item.quantity
    #         return {"message": "Product quantity updated in cart"}

    # cart_db[user_id],
    return {"message": "Product added to cart"}


@app.get("/cart/{user_id}")
def get_cart(user_id: str):
    user_cart = list(cart_db.find({"user_id": user_id}))
    items = [replace_mongo_id(item) for item in user_cart]
    return items


# Checkout
@app.post("/checkout/{user_id}")
def checkout(user_id: int):
    cart = cart_db.find_one({"user_id": user_id})
    if not cart or not cart["items"]:
        raise HTTPException(
            status_code=404, detail="Sorry, cart is empty, cannot checkout!"
        )

    total_amount = 0.0
    order_summary = []

    for item in cart["items"]:
        product = product_collection.find_one({"_id": item["product_id"]})
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

    # Clear the cart after checkout
    cart_db.update_one({"user_id": user_id}, {"$set": {"items": []}})

    return {
        "order_summary": order_summary,
        "total_amount_paid": total_amount,
        "message": "Checkout successful, mate! Thank You For Coming, See You Next Time!!",
    }