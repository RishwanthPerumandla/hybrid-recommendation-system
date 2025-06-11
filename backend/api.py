from fastapi import FastAPI, Query
from typing import List
from ml_pipeline.recommender.content_recommender import recommend_similar_posts
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Enable CORS (if calling from frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/recommend")
def recommend(user_id: str = Query(...), top_k: int = Query(5)):
    try:
        posts = recommend_similar_posts(user_id, top_k)
        return {"recommendations": posts}
    except Exception as e:
        return {"error": str(e)}
