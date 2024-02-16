# schemas/users.py
from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    login: str
    username: str
    email: EmailStr
    password: str
