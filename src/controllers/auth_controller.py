import json

from fastapi import APIRouter, Depends, Request, Body, Form
from fastapi.responses import FileResponse
from models.User import User
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix="/authentication", tags=["authentication"])

# @router.get("/users")
# def get_users(user: User):
#     return {"message": "Get Users from User Controller"}

templates = Jinja2Templates(directory="templates")


@router.get("/login")
async def render_login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.get("/register")
async def render_register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@router.post("/login")
def create_user(data=Body()):
    # TODO IF USER IS VALIDATE RETURN HOME PAGE ELSE REPEAT TURN
    # return username
    # print(data['login'])
    # if data["login"] == "abobaaab":
    return FileResponse("templates/home.html")
    # return {"data": data["login"]}
    # return templates.TemplateResponse("home.html", {"request": request})

@router.post("/register")
def create_user(data=Body()):
    return FileResponse("templates/home.html")