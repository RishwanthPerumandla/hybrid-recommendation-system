# streamlit_app/api/fetch_data.py
import requests

API_BASE = "http://localhost:8000"

def get_liked_posts(user_id):
    res = requests.get(f"{API_BASE}/likes/{user_id}")
    if res.status_code == 200:
        return res.json().get("liked_posts", [])
    return []

def get_content_recommendations(user_id, top_k=5):
    res = requests.get(f"{API_BASE}/recommend/{user_id}?top_k={top_k}")
    if res.status_code == 200:
        return res.json().get("recommendations", [])
    return []

def get_collab_recommendations(user_id, top_k=5):
    res = requests.get(f"{API_BASE}/recommendations/collab?user_id={user_id}&top_k={top_k}")
    if res.status_code == 200:
        return res.json().get("recommendations", [])
    return []

def get_hybrid_recommendations(user_id, top_k=5):
    res = requests.get(f"{API_BASE}/recommendations/hybrid?user_id={user_id}&top_k={top_k}")
    if res.status_code == 200:
        return res.json().get("recommendations", [])
    return []
