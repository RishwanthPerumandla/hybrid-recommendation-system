from ml_pipeline.recommender.content_recommender import recommend_similar_posts
from bson import ObjectId

user_id = "5d7c994d5720533e15c3b1e9"  # replace with any user ID from your 'likes' collection

recommendations = recommend_similar_posts(user_id, top_k=5)
for idx, post in enumerate(recommendations):
    print(f"{idx+1}. {post['title']} | {post['category']} | {post['post_type']}")
