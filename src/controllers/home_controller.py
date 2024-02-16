from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from src.db.session import get_db
from src.db.schemas.users import UserCreate
from src.db.repository.users import create_new_user, authenticate_user
from sqlalchemy.exc import IntegrityError

router = APIRouter(prefix="/home", tags=["home"])
templates = Jinja2Templates(directory="templates")


@router.get("/")
async def get_home_page(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})
