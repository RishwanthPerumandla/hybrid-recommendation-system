import requests

BASE_URL = "http://localhost:8000"

def fetch_user_ids():
    try:
        resp = requests.get(f"{BASE_URL}/users")
        return resp.json().get("user_ids", [])
    except:
        return []

def fetch_liked_posts(user_id):
    try:
        resp = requests.get(f"{BASE_URL}/likes/{user_id}")
        return resp.json().get("liked_posts", [])
    except:
        return []

def get_recommendations(user_id, rec_type, top_k=5):
    if rec_type == "content":
        endpoint = f"/recommend/{user_id}?top_k={top_k}"
    else:
        endpoint = f"/recommendations/{rec_type}?user_id={user_id}&top_k={top_k}"
    try:
        resp = requests.get(BASE_URL + endpoint)
        return resp.json().get("recommendations", [])
    except:
        return []
