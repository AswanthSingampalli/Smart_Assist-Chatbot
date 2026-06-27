from pymongo import MongoClient
import time
from config import MONGO_URI, DB_NAME

client = MongoClient(MONGO_URI)
db = client[DB_NAME]

# Collections
users_col = db["users"]
products_col = db["products"]
orders_col = db["orders"]
chat_col = db["conversations"]

def save_chat(user_id, message, response, sentiment):
    try:
        chat_col.insert_one({
            "user_id": user_id,
            "message": message,
            "response": response,
            "sentiment": sentiment,
            "timestamp": time.time()
        })
    except Exception as e:
        print(f"Warning: Could not save chat to database. Is MongoDB running? Error: {e}")