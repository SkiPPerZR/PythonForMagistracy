from fastapi import APIRouter, Depends
from auth_utils import require_user_id

router = APIRouter(prefix="/crud")


@router.get("/items")
def get_items(user_id: int = Depends(require_user_id)):
    return {"message": "Вы авторизованы", "user_id": user_id}
