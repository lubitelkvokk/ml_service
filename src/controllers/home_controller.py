from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from src.services.security_service import get_current_user
router = APIRouter(prefix="/home", tags=["home"])
templates = Jinja2Templates(directory="templates")


@router.get("/")
async def get_home_page(request: Request, current_user: str = Depends(get_current_user)):
    return templates.TemplateResponse("home.html", {"request": request})
