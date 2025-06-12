import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from backend.database import posts_col, likes_col
from bson import ObjectId

def recommend_similar_posts(user_id: str, top_k: int = 10):
    """
    Fast content-based recommendation (text + image embeddings)
    """

    # 1. Get liked post ObjectIds
    liked_entries = list(likes_col.find({"user_id": user_id}, {"post_id": 1}))
    liked_ids = [entry["post_id"] for entry in liked_entries]

    if not liked_ids:
        return []

    # 2. Fetch liked posts in bulk (projection for efficiency)
    liked_posts = list(posts_col.find(
        {"_id": {"$in": liked_ids}},
        {"text_emb": 1, "image_emb": 1}
    ))

    liked_embeddings = [
        np.concatenate([np.array(p["text_emb"]), np.array(p["image_emb"])])
        for p in liked_posts if "text_emb" in p and "image_emb" in p
    ]

    if not liked_embeddings:
        return []

    user_profile = np.mean(np.stack(liked_embeddings), axis=0).reshape(1, -1)

    # 3. Fetch candidate posts (excluding liked) with required fields only
    candidate_cursor = posts_col.find(
        {"_id": {"$nin": liked_ids}},
        {"text_emb": 1, "image_emb": 1, "title": 1, "category": 1, "post_type": 1, "image": 1}
    )

    post_vectors = []
    post_docs = []

    for post in candidate_cursor:
        if "text_emb" in post and "image_emb" in post:
            vec = np.concatenate([np.array(post["text_emb"]), np.array(post["image_emb"])])
            post_vectors.append(vec)
            post_docs.append(post)

    if not post_vectors:
        return []

    vectors_np = np.stack(post_vectors)
    similarities = cosine_similarity(user_profile, vectors_np)[0]

    # 4. Use argsort for top-k
    top_indices = np.argpartition(-similarities, top_k)[:top_k]
    top_indices = top_indices[np.argsort(-similarities[top_indices])]

    recommendations = []
    for idx in top_indices:
        post = post_docs[idx]
        score = similarities[idx]
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
