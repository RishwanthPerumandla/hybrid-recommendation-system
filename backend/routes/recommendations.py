from fastapi import APIRouter, HTTPException, Query
from typing import List
import pandas as pd
import joblib
from pathlib import Path

from backend.database import posts_col
from ml_pipeline.recommender.content_recommender import recommend_similar_posts
from surprise import Dataset, Reader
from collections import defaultdict

router = APIRouter()

# --- Load model & data once ---
cf_model = joblib.load("ml_pipeline/recommender/cf_model.pkl")
df = pd.read_csv("data/processed/interactions.csv")
reader = Reader(rating_scale=(0, 1))
data = Dataset.load_from_df(df[["user_id", "post_id", "interaction"]], reader)
trainset = data.build_full_trainset()

# ---------- ROUTES ---------- #

@router.get("/recommend/content")
def get_content_recommendations(user_id: str, top_k: int = 10):
    raw_recs = recommend_similar_posts(user_id, top_k)

    results = [
        {
            "_id": str(post.get("_id")),
            "title": post.get("title"),
            "category": post.get("category"),
            "post_type": post.get("post_type"),
            "image": post.get("image"),
            "similarity_score": round(post.get("similarity_score", 0), 4),
            "matched_reason": post.get("matched_reason", "Content match"),
            "source": "content"
        }
        for post in raw_recs
    ]
    return {"user_id": user_id, "top_k": top_k, "recommendations": results}


@router.get("/recommend/collab")
def get_collab_recommendations(user_id: str, top_k: int = Query(5, ge=1, le=20)):
    if user_id not in trainset._raw2inner_id_users:
        raise HTTPException(status_code=404, detail="User not found in training data")

    anti_testset = [entry for entry in trainset.build_anti_testset() if entry[0] == user_id]
    predictions = cf_model.test(anti_testset)
    predictions.sort(key=lambda x: x.est, reverse=True)
    top_post_ids = [pred.iid for pred in predictions[:top_k]]

    posts = posts_col.find({"_id": {"$in": top_post_ids}})
    post_dict = {str(post["_id"]): post for post in posts}

    recommendations = []
    for pid in top_post_ids:
        post = post_dict.get(pid)
        if post:
            recommendations.append({
                "_id": str(post["_id"]),
                "title": post.get("title"),
                "category": post.get("category"),
                "post_type": post.get("post_type"),
                "image": post.get("image"),
                "source": "collaborative"
            })

    return {"user_id": user_id, "top_k": top_k, "recommendations": recommendations}


@router.get("/recommend/hybrid")
def get_hybrid_recommendations(user_id: str, top_k: int = 10):
    # Collaborative
    anti_testset = [entry for entry in trainset.build_anti_testset() if entry[0] == user_id]
    predictions = cf_model.test(anti_testset)
    predictions.sort(key=lambda x: x.est, reverse=True)
    top_cf_ids = [pred.iid for pred in predictions[:top_k]]

    # Fetch posts
    cf_posts = posts_col.find({"_id": {"$in": top_cf_ids}})
    cf_dict = {str(p["_id"]): p for p in cf_posts}

    hybrid_recs = []
    for pid in top_cf_ids:
        post = cf_dict.get(pid)
        if post:
            hybrid_recs.append({
                "_id": str(post["_id"]),
                "title": post.get("title"),
                "category": post.get("category"),
                "post_type": post.get("post_type"),
                "image": post.get("image"),
                "source": "collaborative"
            })

    # Content-based
    content_based = recommend_similar_posts(user_id, top_k * 2)
    seen = set(top_cf_ids)
    for post in content_based:
        pid = str(post["_id"])
        if pid not in seen:
            hybrid_recs.append({
                "_id": pid,
                "title": post.get("title"),
                "category": post.get("category"),
                "post_type": post.get("post_type"),
                "image": post.get("image"),
                "similarity_score": round(post.get("similarity_score", 0), 4),
                "matched_reason": post.get("matched_reason", "Content match"),
                "source": "content"
            })
        if len(hybrid_recs) >= top_k:
            break

    return {"user_id": user_id, "top_k": top_k, "recommendations": hybrid_recs}
