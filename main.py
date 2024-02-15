from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from src.controllers.auth_controller import router as auth_router

app = FastAPI()

app.include_router(auth_router)

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def read_root():
    html_content = "<h2>Hello METANIT.COM!</h2>"
    return HTMLResponse(content=html_content)
