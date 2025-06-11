from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from typing import List
import os

# Local imports
from ml_pipeline.recommender.content_recommender import recommend_similar_posts

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI()

# CORS setup for frontend calls
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update with frontend URL if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Post Recommender API is running 🚀"}

@app.get("/recommend/{user_id}")
def get_recommendations(user_id: str, top_k: int = 10):
    raw_recs = recommend_similar_posts(user_id, top_k)

    clean_recs = [
        {
            "_id": str(post.get("_id")),
            "title": post.get("title"),
            "category": post.get("category"),
            "post_type": post.get("post_type"),
            "image": post.get("image"),
            "similarity_score": round(post.get("similarity_score", 0), 4),
            "matched_reason": post.get("matched_reason", "Recommended based on your interests")
        }
        for post in raw_recs
    ]

    return {"recommendations": clean_recs}

