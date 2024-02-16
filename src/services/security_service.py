from __future__ import annotations
from fastapi import Request
from datetime import datetime, timedelta
from typing import Union

from fastapi import Depends, HTTPException, status
from fastapi import Request
from jose import JWTError, jwt
from pydantic import BaseModel

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_token_from_cookies(request: Request):
    # Извлечение токена из cookies
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Access token is missing")
    return token


async def get_current_user(token: str = Depends(get_token_from_cookies)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # because token starts with Baerer
        payload = jwt.decode(token[7:], SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        # В вашем случае, вы можете возвращать полную информацию о пользователе,
        # если у вас есть соответствующая функция для ее получения.
        # Например, get_user(username) -> User
        return username  # Или объект пользователя
    except JWTError:
        raise credentials_exception
