from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.requests import Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db_depends import get_db
from app.models import Users
from app.schemas import User
from mongobase.characters import get_user_character, get_user_characters
from mongobase.schemas import Character

from .auth import get_current_user

router = APIRouter(prefix="/user", tags=["user"])


templates = Jinja2Templates(directory="templates")


router.mount("/static", StaticFiles(directory="static"), name="static")


@router.get("/profile", response_model=User)
async def profile(
    request: Request,
    db: Annotated[AsyncSession, Depends(get_db)],
    get_user: Annotated[dict, Depends(get_current_user)],
):
    id = get_user.get("id")
    user = await db.scalar(select(Users).where(Users.id == id))

    return templates.TemplateResponse(
        "user/profile.html", {"request": request, "user": user, "profile": "my_profile"}
    )


@router.get("/users", response_model=list[User])
async def users(
    request: Request,
    db: Annotated[AsyncSession, Depends(get_db)],
    get_user: Annotated[dict, Depends(get_current_user)],
):
    id = get_user.get("id")
    result = await db.execute(select(Users))
    users = result.scalars().all()

    return templates.TemplateResponse(
        "user/users.html", {"request": request, "users": users}
    )


@router.get("/users/{username}", response_model=User)
async def users_info(
    request: Request,
    db: Annotated[AsyncSession, Depends(get_db)],
    get_user: Annotated[dict, Depends(get_current_user)],
    username: str,
):
    id = get_user.get("id")
    user = await db.scalar(select(Users).where(Users.username == username))

    return templates.TemplateResponse(
        "user/profile.html", {"request": request, "user": user, "profile": "user"}
    )


@router.get("/my_characters", response_model=list[Character])
async def my_characters(
    request: Request,
    get_user: Annotated[dict, Depends(get_current_user)],
):
    id = get_user.get("id")
    characters = get_user_characters(id)

    return templates.TemplateResponse(
        "user/characters.html",
        {"request": request, "characters": characters, "profile": "my_profile"},
    )


# тестовая страница +


@router.get("/test")
async def my_character(
    request: Request, get_user: Annotated[dict, Depends(get_current_user)]
):

    id = get_user.get("id")

    return templates.TemplateResponse("user/test.html", {"request": request})


# тестовая страница -

# тестовая страница +


@router.get("/test2")
async def my_character_test(
    request: Request, get_user: Annotated[dict, Depends(get_current_user)]
):

    id = get_user.get("id")
    character = get_user_character(id, "Onserey")
    return templates.TemplateResponse(
        "user/test2.html", {"request": request, "character": character}
    )


# тестовая страница -


@router.get("/my_characters/{name}")
async def my_character(
    request: Request, get_user: Annotated[dict, Depends(get_current_user)], name: str
):

    id = get_user.get("id")
    character = get_user_character(id, name)
    if character is None:
        raise HTTPException(status_code=404, detail="Персонаж не найден!")
    return templates.TemplateResponse(
        "user/character_card.html", {"request": request, "character": character}
    )


@router.get("/users/{username}/characters", response_model=list[Character])
async def users_characters(
    request: Request,
    db: Annotated[AsyncSession, Depends(get_db)],
    get_user: Annotated[dict, Depends(get_current_user)],
    username: str,
):
    id = get_user.get("id")
    user = await db.scalar(select(Users).where(Users.username == username))
    characters = get_user_characters(user.id)

    return templates.TemplateResponse(
        "user/characters.html",
        {
            "request": request,
            "characters": characters,
            "profile": "user",
            "username": username,
        },
    )


@router.get("/users/{username}/characters/{name}")
async def user_character(
    request: Request,
    db: Annotated[AsyncSession, Depends(get_db)],
    get_user: Annotated[dict, Depends(get_current_user)],
    username: str,
    name: str,
):

    id = get_user.get("id")
    user = await db.scalar(select(Users).where(Users.username == username))
    character = get_user_character(user.id, name)
    if character is None:
        raise HTTPException(status_code=404, detail="Персонаж не найден!")
    return templates.TemplateResponse(
        "user/character_card.html",
        {"request": request, "character": character, "profile": "user"},
    )
