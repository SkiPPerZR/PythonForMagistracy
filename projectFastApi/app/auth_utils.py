from fastapi import Header, HTTPException


def require_user_id(user_id: int | None = Header(default=None, alias="X-User-ID")):
    if not user_id:
        raise HTTPException(status_code=403, detail="Требуется авторизация")

    return user_id
