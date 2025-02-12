import os
import sys

from fastapi import APIRouter, Form
from fastapi.requests import Request
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from mongobase.create_char import (get_class_skills, get_classes, get_races,
                                   get_subraces)
from mongobase.schemas import Stats

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import redisbase

templates = Jinja2Templates(directory="templates")
router = APIRouter(prefix="/character", tags=["character"])

router.mount("/static", StaticFiles(directory="static"), name="characters")

USER_ID = 111  # дефолтный юзер для тестирования


@router.get("/", response_class=HTMLResponse)
async def create_race(request: Request):
    """Choose race"""
    all_races = get_races()
    return templates.TemplateResponse(
        "character.html", {"request": request, "all_races": all_races, "choose": "race"}
    )


@router.post("/race/", response_class=HTMLResponse)
async def choose_subrace(
    request: Request,
    name: str = Form(...),
    race_name: str = Form(...),
):
    """Choose subrace"""
    redisbase.set_char_init(USER_ID, name, race_name)

    subraces = get_subraces(race_name)
    if subraces:
        return templates.TemplateResponse(
            "character.html",
            {"request": request, "subraces": subraces, "choose": "subrace"},
        )
    else:
        redisbase.set_char_subrace(USER_ID, None)
        return templates.TemplateResponse(
            "redirect_to_class.html",
            {"request": request, "name": name, "race_name": race_name},
        )


@router.post("/class/", response_class=HTMLResponse)
async def create_class(
    request: Request,
    subrace_name: str = Form(...),
):
    """Choose class"""
    redisbase.set_char_subrace(USER_ID, subrace_name)
    all_classes = get_classes()
    return templates.TemplateResponse(
        "character.html",
        {"request": request, "all_classes": all_classes, "choose": "class"},
    )


@router.post("/next/", response_class=HTMLResponse)
async def choose_skills(
    request: Request,
    class_name: str = Form(...),
):
    """Choose class skills"""
    redisbase.set_char_class(USER_ID, class_name)
    skills = get_class_skills(class_name)
    return templates.TemplateResponse(
        "character_modification.html",
        {"request": request, "skills": skills},
    )


@router.post("/dices/", response_class=HTMLResponse)
async def rolling_dices(
    request: Request,
    selected_skills: list[str] = Form(...),
):
    """Choose class skills"""
    redisbase.set_class_skills(USER_ID, selected_skills)
    return templates.TemplateResponse(
        "dices.html",
        {"request": request},
    )


@router.post("/add_dices/", response_class=JSONResponse)
async def add_dices(
    request: Request,
    strength: str = Form(...),
    dexterity: str = Form(...),
    intelligence: str = Form(...),
    wisdom: str = Form(...),
    charisma: str = Form(...),
    constitution: str = Form(...),
    ):
    stats = Stats(
        strength=strength,
        dexterity=dexterity,
        constitution=constitution,
        intelligence=intelligence,
        wisdom=wisdom,
        charisma=charisma,
    )
    redisbase.set_char_ctats(USER_ID, stats.model_dump())
    char_info = redisbase.get_char_info(USER_ID)
    return templates.TemplateResponse(
        "char.html",
        {"request": request, "char_info": char_info},
    )


