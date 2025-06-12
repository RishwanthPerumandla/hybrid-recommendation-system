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
def get_content_recommendations(
    user_id: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=50)
):
    raw_recs = recommend_similar_posts(user_id, top_k=skip + limit)

    sliced = raw_recs[skip: skip + limit]
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
        for post in sliced
    ]
    return {
        "user_id": user_id,
        "skip": skip,
        "limit": limit,
        "returned": len(results),
        "recommendations": results
    }


@router.get("/recommend/collab")
def get_collab_recommendations(
    user_id: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=50)
):
    if user_id not in trainset._raw2inner_id_users:
        raise HTTPException(status_code=404, detail="User not found in training data")

    anti_testset = [entry for entry in trainset.build_anti_testset() if entry[0] == user_id]
    predictions = cf_model.test(anti_testset)
    predictions.sort(key=lambda x: x.est, reverse=True)

    sliced_preds = predictions[skip: skip + limit]
    top_post_ids = [pred.iid for pred in sliced_preds]

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

    return {
        "user_id": user_id,
        "skip": skip,
        "limit": limit,
        "returned": len(recommendations),
        "recommendations": recommendations
    }


@router.get("/recommend/hybrid")
def get_hybrid_recommendations(
    user_id: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=50)
):
    # Step 1: Collaborative
    anti_testset = [entry for entry in trainset.build_anti_testset() if entry[0] == user_id]
    predictions = cf_model.test(anti_testset)
    predictions.sort(key=lambda x: x.est, reverse=True)

    top_cf_ids = [pred.iid for pred in predictions]
    cf_posts = posts_col.find({"_id": {"$in": top_cf_ids}})
    cf_dict = {str(p["_id"]): p for p in cf_posts}

    hybrid_recs = []
    seen = set()

    for pid in top_cf_ids:
        if pid in seen:
            continue
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
            seen.add(pid)
        if len(hybrid_recs) >= skip + limit:
            break

    # Step 2: Content-based
    content_recs = recommend_similar_posts(user_id, top_k=100)
    for post in content_recs:
        pid = str(post["_id"])
        if pid in seen:
            continue
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
        seen.add(pid)
        if len(hybrid_recs) >= skip + limit:
            break

    paginated = hybrid_recs[skip: skip + limit]

    return {
        "user_id": user_id,
        "skip": skip,
        "limit": limit,
        "returned": len(paginated),
        "recommendations": paginated
    }
