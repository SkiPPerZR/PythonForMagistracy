from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models import User
from schemas import UserRegister, UserLogin

router = APIRouter(prefix="/auth", tags=["Auth"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------- Регистрация ----------
@router.post("/register")
def register_user(data: UserRegister, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.login == data.login).first()
    if user:
        raise HTTPException(status_code=400, detail="Логин уже занят")

    new_user = User(login=data.login, password=data.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "Регистрация успешна", "user_id": new_user.id}


# ---------- Вход ----------
@router.post("/login")
def login_user(data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.login == data.login).first()
    if not user or user.password != data.password:
        raise HTTPException(status_code=401, detail="Неверный логин или пароль")
    return {"message": "Вход выполнен", "user_id": user.id}


# ---------- Выход ----------
@router.post("/logout")
def logout_user():
    return {"message": "Сессия завершена"}
