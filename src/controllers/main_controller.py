from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix="/main", tags=["main"])
templates = Jinja2Templates(directory="templates")


@router.get("/")
async def get_home_page(request: Request):
    return templates.TemplateResponse("main.html", {"request": request})

