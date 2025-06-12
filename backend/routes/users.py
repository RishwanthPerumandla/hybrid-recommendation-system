from fastapi import APIRouter, Query
from backend.database import users_col

router = APIRouter()

@router.get("/users")
def get_all_users(skip: int = Query(0, ge=0), limit: int = Query(20, ge=1, le=100)):
    users_cursor = users_col.find().skip(skip).limit(limit)
    users = list(users_cursor)

    return {
        "users": [
            {
                "id": str(u["_id"]),
                "name": u.get("name", "Unnamed"),
                "email": u.get("email", "")
            }
            for u in users
        ],
        "pagination": {
            "skip": skip,
            "limit": limit,
            "returned": len(users)
        }
    }
