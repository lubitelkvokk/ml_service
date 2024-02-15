from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from src.db.session import get_db
from src.db.schemas.users import UserCreate
from src.db.repository.users import create_new_user
from sqlalchemy.exc import IntegrityError

router = APIRouter(prefix="/authentication", tags=["authentication"])
templates = Jinja2Templates(directory="templates")


@router.get("/register/")
def register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@router.post("/register/")
async def register(request: Request, username: str = Form(...), login: str = Form(...), email: str = Form(...),
                   password: str = Form(...), db: Session = Depends(get_db)):
    user = UserCreate(login=login, username=username, email=email,
                      password=password)  # Используйте значение email из формы
    try:
        user = create_new_user(user=user, db=db)
        return RedirectResponse("/main",
                                status_code=302)  # Перенаправление на главную страницу после успешной регистрации
    except IntegrityError:
        return templates.TemplateResponse("register.html", {"request": request, "error": "Duplicate username or email"})


@router.get("/login")
async def render_login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.post("/login")
def login_user(request: Request, login: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    # Здесь должна быть логика проверки пользователя
    # Если проверка прошла успешно:
    return RedirectResponse("/main", status_code=302)  # Перенаправление на главную страницу
    # В противном случае вернуть страницу входа с сообщением об ошибке
