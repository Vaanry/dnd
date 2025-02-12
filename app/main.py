from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.routers import main_router

from .config import settings

templates = Jinja2Templates(directory="templates")

app = FastAPI(title=settings.app_title)

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def welcome(request: Request) -> dict:
    return templates.TemplateResponse("index.html", {"request": request})


app.include_router(main_router)
