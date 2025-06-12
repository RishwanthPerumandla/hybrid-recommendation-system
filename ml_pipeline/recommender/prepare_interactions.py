import json
import pandas as pd
from pathlib import Path

# Load likes.json
with open("data/raw/likes.json", "r") as f:
    data = json.load(f)

# Flatten into rows
rows = []
for item in data:
    user_id = item["user_id"]
    post_id = item["post_id"]
    rows.append({"user_id": user_id, "post_id": post_id, "interaction": 1})

# Save as CSV
df = pd.DataFrame(rows)
output_path = Path("data/processed/interactions.csv")
output_path.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(output_path, index=False)
print(f"✅ Saved to {output_path}")
