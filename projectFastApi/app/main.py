from fastapi import FastAPI
from database import Base, engine
from auth_router import router as auth_router
from crud_router import router as crud_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Auth Service")

app.include_router(auth_router)
app.include_router(crud_router)
