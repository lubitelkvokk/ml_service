from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from src.db.entities.AccountEntity import Account
from src.db.entities.ActionEntity import DBAction
from src.db.entities.ModelEntity import DBModel
from src.db.entities.UserEntity import DBUser
from src.db.session import get_db
from src.services.security_service import get_current_user

router = APIRouter(prefix="/main", tags=["main"])
templates = Jinja2Templates(directory="templates")


@router.get("/")
async def get_home_page(request: Request):
    return templates.TemplateResponse("main.html", {"request": request})

