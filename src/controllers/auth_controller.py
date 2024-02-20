from datetime import timedelta

from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.services.user_service import user_service
from src.db.repository.users_repository import authenticate_user
from src.db.schemas.users import UserCreate
from src.db.session import get_db
from src.services.security_service import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter(prefix="/authentication", tags=["authentication"])
templates = Jinja2Templates(directory="templates")


@router.get("/register/")
def register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@router.post("/register/")
async def register(request: Request, username: str = Form(...), login: str = Form(...), email: str = Form(...),
                   password: str = Form(...), db: Session = Depends(get_db)):
    user_data = UserCreate(login=login, username=username, email=email, password=password)
    try:
        # Добавлено 'await' для ожидания выполнения асинхронной функции
        await user_service.create_new_user(user=user_data, db=db)
        return RedirectResponse("/authentication/login", status_code=302)
    except IntegrityError:
        # Возвращаем страницу регистрации с сообщением об ошибке
        return templates.TemplateResponse("register.html", {"request": request, "error": "Duplicate username or email"})


@router.get("/login")
async def render_login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.post("/login")
async def login_user(request: Request, login: str = Form(...), password: str = Form(...),
                     db: Session = Depends(get_db)):
    user = authenticate_user(login, password, db)
    if not user:
        return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid login or password"})
    # Создание токена доступа для пользователя
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.login}, expires_delta=access_token_expires
    )
    # Создание ответа с перенаправлением
    response = RedirectResponse("/home", status_code=302)
    # Добавление токена в заголовки куки (или вы можете выбрать другой способ передачи токена)
    response.set_cookie(key="access_token", value=f"Bearer {access_token}", httponly=True)
    return response
