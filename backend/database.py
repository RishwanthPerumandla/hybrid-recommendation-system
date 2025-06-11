from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()  # 🔥 THIS IS ESSENTIAL

client = MongoClient(os.getenv("MONGO_URI"))
db = client.get_database("Recommendations_Engine")

users_col = db.users
posts_col = db.posts
likes_col = db.likes
