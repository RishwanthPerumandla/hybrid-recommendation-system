import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from backend.database import posts_col, likes_col
from bson import ObjectId

def recommend_similar_posts(user_id: str, top_k: int = 10):
    """
    Recommends top-K posts based on hybrid similarity (text + image)
    """

    # 1. Get liked post IDs by user
    liked_post_ids = [entry["post_id"] for entry in likes_col.find({"user_id": user_id})]
    if not liked_post_ids:
        return []

    # 2. Get embeddings for liked posts
    liked_embeddings = []
    for post_id in liked_post_ids:
        post = posts_col.find_one({"_id": post_id})
        if post and "text_emb" in post and "image_emb" in post:
            combined = np.concatenate([np.array(post["text_emb"]), np.array(post["image_emb"])])
            liked_embeddings.append(combined)

    if not liked_embeddings:
        return []

    # 3. Average to get user profile vector
    user_profile = np.mean(np.stack(liked_embeddings), axis=0).reshape(1, -1)

    # 4. Fetch all posts excluding liked ones
    all_posts = list(posts_col.find({"_id": {"$nin": [ObjectId(pid) for pid in liked_post_ids]}}))

    post_vectors = []
    post_metadata = []

    for post in all_posts:
        if "text_emb" in post and "image_emb" in post:
            vec = np.concatenate([np.array(post["text_emb"]), np.array(post["image_emb"])])
            post_vectors.append(vec)
            post_metadata.append(post)

    if not post_vectors:
        return []

    # 5. Compute cosine similarity
    sims = cosine_similarity(user_profile, np.stack(post_vectors))[0]

    # 6. Get top-k post indices
    top_indices = sims.argsort()[::-1][:top_k]

    # 7. Prepare and return recommendations
    recommendations = []
    for idx in top_indices:
        post = post_metadata[idx]
        score = sims[idx]
        recommendations.append({
            "_id": str(post["_id"]),
            "title": post.get("title"),
            "category": post.get("category"),
            "post_type": post.get("post_type"),
            "image": post.get("image"),
            "similarity_score": round(float(score), 4),
            "matched_reason": "Similar to your liked content"
        })

    return recommendations
