from pydantic import BaseModel


class UserRegister(BaseModel):
    login: str
    password: str


class UserLogin(BaseModel):
    login: str
    password: str
