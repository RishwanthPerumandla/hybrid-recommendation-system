# backend/routes/likes.py

from fastapi import APIRouter, HTTPException
from backend.database import likes_col, posts_col

router = APIRouter()

@router.get("/likes/{user_id}")
def get_liked_posts(user_id: str):
    liked = likes_col.find({"user_id": user_id})
    post_ids = [entry["post_id"] for entry in liked]
    if not post_ids:
        raise HTTPException(status_code=404, detail="No likes found for user")

    posts = posts_col.find({"_id": {"$in": post_ids}})
    results = [{
        "_id": str(post.get("_id")),
        "title": post.get("title"),
        "category": post.get("category"),
        "post_type": post.get("post_type"),
        "image": post.get("image"),
    } for post in posts]

    return {"liked_posts": results}
