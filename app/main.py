from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from jinja2 import Environment  # noqa
from starlette.middleware.base import BaseHTTPMiddleware

from app.routers import main_router
from app.routers.auth import get_current_user

from .config import settings

templates = Jinja2Templates(directory="templates")


app = FastAPI(title=settings.app_title)

app.mount("/static", StaticFiles(directory="static"), name="static")


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        token = request.cookies.get("users_access_token")
        try:
            user = await get_current_user(token)
            request.state.user = user
        except:
            request.state.user = None
        response = await call_next(request)
        return response


app.add_middleware(AuthMiddleware)


@app.get("/")
async def welcome(request: Request) -> dict:
    return templates.TemplateResponse("index.html", {"request": request})


app.include_router(main_router)
