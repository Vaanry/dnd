from datetime import datetime, timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, Form, HTTPException, Response, status
from fastapi.requests import Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security import HTTPBasic, OAuth2PasswordBearer
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from jose import ExpiredSignatureError, JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db_depends import get_db
from app.models import Users
from app.schemas import CreateUser

from ..config import settings

router = APIRouter(prefix="/auth", tags=["auth"])
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

security = HTTPBasic()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm

templates = Jinja2Templates(directory="templates")
templates.env.globals["is_authenticated"] = (
    lambda request: hasattr(request.state, "user") and request.state.user is not None
)
router.mount("/static", StaticFiles(directory="static"), name="static")


async def authanticate_user(
    db: Annotated[AsyncSession, Depends(get_db)], user_data: CreateUser
):
    user = await db.scalar(select(Users).where(Users.username == user_data.username))
    if (
        not user
        or not bcrypt_context.verify(user_data.password, user.hashed_password)
        or user.hashed_password is None
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def create_access_token(
    username: str, id: int, is_admin: bool, expires_delta: timedelta
):

    encode = {"sub": username, "id": id, "is_admin": is_admin}
    expires = datetime.now() + expires_delta
    encode.update({"exp": datetime.timestamp(expires)})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


@router.get("/login/", response_class=HTMLResponse)
async def login_form(request: Request):
    """
    Отображает HTML-форму для входа.
    """
    return templates.TemplateResponse(
        "login.html", {"request": request, "is_registration": False}
    )


@router.post("/login/")
async def auth_user(
    request: Request,
    db: Annotated[AsyncSession, Depends(get_db)],
    response: Response,
    username: str = Form(...),
    password: str = Form(...),
):
    try:
        user_data = CreateUser(username=username, password=password)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Validation error: {e}")

    check = await authanticate_user(db, user_data)
    if check is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверное имя пользователя или пароль",
        )
    access_token = await create_access_token(
        check.username,
        check.id,
        check.is_admin,
        timedelta(weeks=2),
    )
    response.set_cookie(
        key="users_access_token",
        value=access_token,
        httponly=True,
        secure=False,
        path="/",
    )

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "message": "Успешный вход в систему!",
        },
    )


def get_token(request: Request):
    token = request.cookies.get("users_access_token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token not found"
        )
    return token


async def get_current_user(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
            options={"verify_exp": False},
        )
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Токен истёк. Пожалуйста, войдите снова.",
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Токен не валидный!",
        )

    username: str = payload.get("sub")
    id: int = payload.get("id")
    is_admin: bool = payload.get("is_admin")
    if username is None or id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Невозможно проверить пользователя.",
        )

    return {"username": username, "id": id, "is_admin": is_admin}


@router.get("/registration", response_class=HTMLResponse)
async def registration_form(request: Request):
    """
    Отображает HTML-форму для регистрации.
    """
    return templates.TemplateResponse(
        "login.html", {"request": request, "is_registration": True}
    )


@router.post("/registration")
async def registration_confirm(
    request: Request,
    db: Annotated[
        AsyncSession,
        Depends(get_db),
    ],
    username: str = Form(...),
    password: str = Form(...),
):

    try:
        user = CreateUser(username=username, password=password)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Validation error: {e}")

    hash_password = bcrypt_context.hash(user.password)
    await db.execute(
        insert(Users), [{"username": username, "hashed_password": hash_password}]
    )

    await db.commit()
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "message": "Успешная регистрация! Вы можете зайти со своим логином и паролем.",
        },
    )


@router.get("/logout/")
async def logout_user(response: Response):
    response.delete_cookie(key="users_access_token")
    return RedirectResponse(
        url="/",
        status_code=status.HTTP_302_FOUND,
        headers=response.headers,
    )
