from typing import Annotated

from fastapi import APIRouter, Depends
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


@router.get("/my_characters", response_model=list[Character])
async def my_characters(
    request: Request,
    get_user: Annotated[dict, Depends(get_current_user)],
):
    id = get_user.get("id")
    characters = get_user_characters(id)

    return templates.TemplateResponse(
        "user/characters.html", {"request": request, "characters": characters}
    )


@router.get("/my_characters/{name}")
async def my_character(
    request: Request, get_user: Annotated[dict, Depends(get_current_user)], name: str
):

    id = get_user.get("id")
    character = get_user_character(id, name)

    return templates.TemplateResponse(
        "user/character_card.html", {"request": request, "character": character}
    )
