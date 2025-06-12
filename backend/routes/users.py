# backend/routes/users.py
from fastapi import APIRouter
from backend.database import users_col

router = APIRouter()

@router.get("/users")
def get_all_users():
    users = users_col.find()
    return {
        "users": [
            {
                "id": str(u["_id"]),
                "name": u.get("name", "Unnamed"),
                "email": u.get("email", "")
            }
            for u in users
        ]
    }
