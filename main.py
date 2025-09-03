from fastapi import FastAPI
from pydantic import BaseModel
from fastapi import  HTTPException
from typing import List
from users import user_db

class User(BaseModel):
    id: int
    username: str
    email: str
    password: str

# class CartItem(BaseModel):
#      product_id: int
#      quantity: int


# class users_db:
#     def __init__(self, id, username, email, password):
#         self.id = id
#         self.username = username
#         self.email = email
#         self.password = password

app = FastAPI()

product_collection = [
                {"_id": 1, "name": "wireless mouse", "description": "black", "price": 300.00, "image": "product_image"}, 
                {"_id": 2, "name": "keyboard", "description": "black", "price": 150.00, "image": "product_image"},
                {"_id": 3, "name": "laptop", "description": "white", "price": 4000.00, "image": "product_image"},
                {"_id": 4, "name": "MiFi", "description": "black", "price": 200.00, "image": "product_image"}
                ]


# def cart_db():
# cart_db: Dict[int, List["CartItem"]] = {}    

Users_db: List[User] = []


@app.get("/")
def get_home():
    return{"message": "Welcome to our E-commerce API!"}

# List of sample products/ return all products
@app.get("/products")
def get_all_products():
    return{"products": product_collection}


# Get single product by id
@app.get("/products/{product_id}")
def get_products_by_id(product_id:int):
    # return {"product_id": product_id} 
    for product in product_collection:
            if product["_id"] == product_id:
              return {"product": product}
# If product is not found
    else:
            raise HTTPException(status_code=404, detail="Product not found")

# A list to store users' id, username, email and password
@app.post("/register")
def register_user(user: User):
    user_db = []
    # Check whether user info already exists
    for existing_user in user_db:
        if existing_user["email"] == user.email:
            raise HTTPException(status_code=409, detail="Email already exists")
    user_db.append(user)
    return{"message": "User registered successfully"}

# Check whether email/username and password match
@app.post("/login")
def login_user(user: User):
     for existing_user in user_db:
          if ((existing_user["username"] == user.username or existing_user["email"] == user.email) and existing_user["password"] == user.password):
               return{"message": "Login successful"}
          else:
               return{"message": "Invalid credentials"}
          
# @app.post("/cart")
# def add_to_cart(user_id, product_id, quantity):
#      for user_id in cart_db:
#           cart_db[user_id].append() 
#           return{"message": "Item added to cart", "cart": cart_db[user_id]}

# @app.get("/cart/{user_id}")
# def get_cart(user_id: int):
#      user_cart = cart_db.get(user_id, [])
#      return{"user_id": user_id, "cart": user_cart}