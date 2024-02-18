# schemas/users_repository.py
from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    login: str
    username: str
    email: EmailStr
    password: str
