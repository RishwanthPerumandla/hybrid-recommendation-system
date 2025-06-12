from fastapi import APIRouter, HTTPException, Query
from backend.database import likes_col, posts_col

router = APIRouter()

@router.get("/likes/{user_id}")
def get_liked_posts(user_id: str, skip: int = Query(0, ge=0), limit: int = Query(10, ge=1, le=50)):
    liked_cursor = likes_col.find({"user_id": user_id}).skip(skip).limit(limit)
    liked = list(liked_cursor)
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

    return {
        "liked_posts": results,
        "pagination": {
            "skip": skip,
            "limit": limit,
            "returned": len(results)
        }
    }
