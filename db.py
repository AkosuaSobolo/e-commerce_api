from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

# connect to mongo atlas cluster

mongo_client = MongoClient(os.getenv("MONGO_URI"))

# Access database 

eCommerce_db = mongo_client["eCommerce_db"]

# pick a collection to operate on
product_collection = eCommerce_db["products"]
user_db = eCommerce_db["users"]
cart_db = eCommerce_db["cart"]