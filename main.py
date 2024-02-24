from fastapi import FastAPI, Request, HTTPException, status
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from starlette.responses import RedirectResponse

from src.controllers.auth_controller import router as auth_router
from src.controllers.home_controller import router as home_router
from src.controllers.main_controller import router as main_router

app = FastAPI()
app.include_router(main_router)
app.include_router(auth_router)
app.include_router(home_router)

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.exception_handler(HTTPException)
async def unicorn_exception_handler(request: Request, exc: HTTPException):
    if (exc.status_code == status.HTTP_401_UNAUTHORIZED):
        return RedirectResponse("/authentication/login", status_code=302)