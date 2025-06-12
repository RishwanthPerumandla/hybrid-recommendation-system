from pymongo import MongoClient
import pandas as pd
import os
from pathlib import Path
from dotenv import load_dotenv

# 🔐 Load env variables
load_dotenv()
client = MongoClient(os.getenv("MONGO_URI"))
db = client.get_database("Recommendations_Engine")

# Access the likes collection
likes_col = db.likes

# Query only user_id and post_id
likes = list(likes_col.find({}, {"user_id": 1, "post_id": 1, "_id": 0}))

# Convert to DataFrame
df = pd.DataFrame(likes)
df["interaction"] = 1  # Binary implicit feedback

# Save to processed path
output_path = Path("data/processed/interactions.csv")
output_path.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(output_path, index=False)

print(f"✅ Exported {len(df)} interactions to {output_path}")
