from ml_pipeline.embeddings.text_embedder import TextEmbedder
from ml_pipeline.embeddings.image_embedder import ImageEmbedder
from backend.database import posts_col
from tqdm import tqdm
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("BatchEmbedder")

# Initialize embedders
text_model = TextEmbedder()
image_model = ImageEmbedder()

logger.info("🚀 Starting batch embedding of posts...")

# Find posts that haven't been embedded yet
posts = posts_col.find({
    "text_emb": {"$exists": False},
    "image_emb": {"$exists": False}
})

count = 0
for post in tqdm(posts, desc="Embedding posts"):
    title = post.get("title", "")
    image_b64 = post.get("image", "")

    # Generate embeddings
    text_vec = text_model.encode(title).tolist()
    image_vec = image_model.encode(image_b64).tolist()

    # Update the post document with embeddings
    result = posts_col.update_one(
        {"_id": post["_id"]},
        {"$set": {
            "text_emb": text_vec,
            "image_emb": image_vec
        }}
    )

    if result.modified_count == 1:
        count += 1

logger.info(f"✅ Embedded and updated {count} posts in MongoDB.")
