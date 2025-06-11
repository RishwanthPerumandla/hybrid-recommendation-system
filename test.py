from backend.database import posts_col
from pymongo.errors import ServerSelectionTimeoutError

try:
    # Try to count documents in the 'posts' collection
    count = posts_col.count_documents({})
    print(f"✅ MongoDB connected successfully! Total posts: {count}")
except ServerSelectionTimeoutError as e:
    print("❌ MongoDB connection failed:")
    print(e)
