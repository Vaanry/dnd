from fastapi import FastAPI, HTTPException, status
from fastapi.requests import Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi_csrf_protect.exceptions import CsrfProtectError
from starlette.middleware.base import BaseHTTPMiddleware

from app.routers import main_router
from app.routers.auth import get_current_user

from .config import settings

# from starlette.middleware.sessions import SessionMiddleware


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
# app.add_middleware(SessionMiddleware, secret_key="your_secret_key")


@app.get("/")
async def welcome(request: Request) -> dict:
    return templates.TemplateResponse(
        "index.html", {"request": request, "message": "Добро пожаловать!"}
    )


app.include_router(main_router)


@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    if exc.status_code in (401, 404):
        return templates.TemplateResponse(
            "errors/400.html",
            {"request": request, "detail": exc.detail, "status": exc.status_code},
            status_code=exc.status_code,
        )

    return HTMLResponse(
        content=f"<h1>{exc.status_code} - {exc.detail}</h1>",
        status_code=exc.status_code,
    )


@app.exception_handler(CsrfProtectError)
def csrf_protect_exception_handler(request: Request, exc: CsrfProtectError):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})
