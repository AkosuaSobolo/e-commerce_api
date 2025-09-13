# from fastapi import FastAPI
# from fastapi import HTTPException
# from pydantic import BaseModel
# from typing import List, Dict, Any
# from db import product_collection
# from db import user_db
# from db import cart_db

# app = FastAPI()


# # Models


# class CreateUserModel(BaseModel):
#     id: int
#     username: str
#     email: str 
#     password: str


# class CartItem(BaseModel):
#     product_id: int
#     quantity: int


# class ProductModel(BaseModel):
#     name: str
#     price: float
#     stock_quantity: int
#     description: str


# # Database Simulation

# # cart_db: Dict[int, List[Dict[str, Any]]] = {}

# # Routes


# @app.post("/products")
# def insert_product(product: ProductModel):
#     product_collection.insert_one(product.model_dump())
#     return {"message": "product added successfully"}


# @app.get("/")
# def get_home():
#     return {"message": "Oi, Hola Amigos! Welcome to our E-commerce API!"}


# # Products
# @app.get("/products")
# def get_all_products():
#     return {"products": product_collection}


# @app.get("/products/{product_id}")
# def get_products_by_id(product_id: int):
#     for product in product_collection:
#         if product["_id"] == product_id:
#             return {"product": product}
#     else:
#         raise HTTPException(status_code=404, detail="uh-oh! Product not found!")


# # Delete a product
# @app.delete("/products/{product_id}")
# def delete_product_by_id(product_id: int):
#     product = get_products_by_id(product_id)

#     if product:
#         del product_collection[product_id]

#     return {"message": f"{product_id}Product sucessfully deleted"}


# # Allow product update by management
# @app.patch("/product/{product_id}")
# def update_product(product_id: int, product: get_all_products):
#     get_all_products(product_id)
#     return {"message": f"{product_id}Product sucessfully updated"}


# # User registration
# @app.post("/register")
# def register_user(user: CreateUserModel):
#     # Check whether email already exists
#     for existing_user in user_db.find():
#         if existing_user["email"] == user.email:
#             raise HTTPException(status_code=409, detail="Sorry, email already exists!")
#     user.model_dump()
#     return {"message": "User registered successfully!"}


# @app.post("/login")
# def login_user(user: CreateUserModel):
#     existing_user = user_db.find_one({"email": user.email, "password": user.password})
#     if existing_user:
#         return {"message": "Login Succesful"}
#     raise HTTPException(status_code=401, detail="Invalid credentials, Please try again!")


# # Cart
# @app.post("/cart/{user_id}")
# def add_to_cart(user_id: int, item: CartItem):
#     # Check whether product exists
#     product = next((p for p in product_collection if p["_id"] == item.product_id), None)
#     if not product:
#         raise HTTPException(status_code=404, detail="uh-oh! Product not found!")

#     if user_id not in cart_db:
#         cart_db[user_id] = []

#     for cart_item in cart_db[user_id]:
#         if cart_item["product_id"] == item.product_id:
#             cart_item["quantity"] += item.quantity
#             return {"message": "Product quantity updated in cart"}

#     item.model_dump()
#     return {"message": "Product added to cart"}


# @app.get("/cart/{user_id}")
# def get_cart(user_id: int):
#     return {"user_id": user_id, "cart": cart_db.get(user_id, [])}


# # Checkout
# @app.post("/checkout/{user_id}")
# def checkout(user_id: int):
#     cart_items = cart_db.get(user_id, [])
#     if not cart_items:
#         raise HTTPException(
#             status_code=404, detail="Sorry, cart is empty, cannot checkout!"
#         )

#     total_amount = 0.0
#     order_summary = []

#     for item in cart_items:
#         product = next(
#             (p for p in product_collection if p["_id"] == item["product_id"]), None
#         )
#         if product:
#             subtotal = product["price"] * item["quantity"]
#             total_amount += subtotal
#             order_summary.append(
#                 {
#                     "product_name": product["name"],
#                     "quantity": item["quantity"],
#                     "price": product["price"],
#                     "subtotal": subtotal,
#                 }
#             )

#     return {
#         "order_summary": order_summary,
#         "total amount paid": total_amount,
#         "message": "Checkout successful, mate! Thank You For Coming, See You Next Time!!",
#     }



# from fastapi import FastAPI, HTTPException, Body
# from pydantic import BaseModel
# from typing import Dict, Any
# from db import product_collection, user_db, cart_db 

# app = FastAPI()


# # Models
# class CreateUserModel(BaseModel):
#     id: int
#     username: str
#     email: str
#     password: str


# class CartItem(BaseModel):
#     product_id: int
#     quantity: int


# class ProductModel(BaseModel):
#     _id: int 
#     name: str
#     price: float
#     stock_quantity: int
#     description: str


# # Routes
# @app.get("/")
# def get_home():
#     return {"message": "Oi, Hola Amigos! Welcome to our E-commerce API!"}


# @app.post("/products")
# def add_product(product: ProductModel):
#     # Check if product ID already exists
#     existing = product_collection.find_one({"_id": product._id})
#     if existing:
#         raise HTTPException(status_code=409, detail="Product ID already exists!")

#     product_collection.find_one(product.model_dump())
#     return {"message": "Product added successfully"}


# @app.get("/products")
# def get_all_products():
#     products = list(product_collection.find({}, {"_id": 0}))
#     return {"products": products}


# @app.get("/products/{product_id}")
# def get_product_by_id(product_id: int):
#     product = product_collection.find_one({"_id": product_id}, {"_id": 0})
#     if not product:
#         raise HTTPException(status_code=404, detail="uh-oh! Product not found!")
#     return {"product": product}


# @app.delete("/products/{product_id}")
# def delete_product(product_id: int):
#     result = product_collection.delete_one({"_id": product_id})
#     if result.deleted_count == 0:
#         raise HTTPException(status_code=404, detail="Product not found")
#     return {"message": f"Product {product_id} deleted successfully"}


# @app.patch("/products/{product_id}")
# def update_product(product_id: int, product: Dict[str, Any] = Body(...)):
#     result = product_collection.update_one(
#         {"_id": product_id}, {"$set": product}
#     )
#     if result.matched_count == 0:
#         raise HTTPException(status_code=404, detail="Product not found")
#     return {"message": f"Product {product_id} updated successfully"}


# @app.post("/register")
# def register_user(user: CreateUserModel):
#     existing_user = user_db.find_one({"email": user.email})
#     if existing_user:
#         raise HTTPException(status_code=409, detail="Sorry, email already exists!")

#     user_db.insert_one(user.model_dump())
#     return {"message": "User registered successfully!"}


# @app.post("/login")
# def login_user(user: CreateUserModel):
#     existing_user = user_db.find_one({"email": user.email, "password": user.password})
#     if existing_user:
#         return {"message": "Login successful"}
#     raise HTTPException(status_code=401, detail="Invalid credentials, Please try again!")


# @app.post("/cart/{user_id}")
# def add_to_cart(user_id: int, item: CartItem):
#     # Check if product exists
#     product = product_collection.find_one({"_id": item.product_id})
#     if not product:
#         raise HTTPException(status_code=404, detail="uh-oh! Product not found!")

#     cart = cart_db.find_one({"user_id": user_id})
#     if not cart:
#         cart_db.insert_one({"user_id": user_id, "items": [item.model_dump()]})
#     else:
#         items = cart["items"]
#         for cart_item in items:
#             if cart_item["product_id"] == item.product_id:
#                 cart_item["quantity"] += item.quantity
#                 cart_db.update_one({"user_id": user_id}, {"$set": {"items": items}})
#                 return {"message": "Product quantity updated in cart"}

#         items.append(item.model_dump())
#         cart_db.update_one({"user_id": user_id}, {"$set": {"items": items}})

#     return {"message": "Product added to cart"}


# @app.get("/cart/{user_id}")
# def get_cart(user_id: int):
#     cart = cart_db.find_one({"user_id": user_id}, {"_id": 0})
#     if not cart:
#         return {"user_id": user_id, "cart": []}
#     return {"user_id": user_id, "cart": cart["items"]}


# @app.post("/checkout/{user_id}")
# def checkout(user_id: int):
#     cart = cart_db.find_one({"user_id": user_id})
#     if not cart or not cart["items"]:
#         raise HTTPException(
#             status_code=404, detail="Sorry, cart is empty, cannot checkout!"
#         )

#     total_amount = 0.0
#     order_summary = []

#     for item in cart["items"]:
#         product = product_collection.find_one({"_id": item["product_id"]})
#         if product:
#             subtotal = product["price"] * item["quantity"]
#             total_amount += subtotal
#             order_summary.append(
#                 {
#                     "product_name": product["name"],
#                     "quantity": item["quantity"],
#                     "price": product["price"],
#                     "subtotal": subtotal,
#                 }
#             )

#     # Clear the cart after checkout
#     cart_db.update_one({"user_id": user_id}, {"$set": {"items": []}})

#     return {
#         "order_summary": order_summary,
#         "total_amount_paid": total_amount,
#         "message": "Checkout successful, mate! Thank You For Coming, See You Next Time!!",
#     }
