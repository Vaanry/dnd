import json

from fastapi import APIRouter, Form
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from mongobase.create_char import get_classes, get_races, get_subraces

templates = Jinja2Templates(directory="templates")
router = APIRouter(prefix="/character", tags=["character"])

router.mount("/static", StaticFiles(directory="static"), name="characters")


@router.get("/", response_class=HTMLResponse)
async def create_race(request: Request):
    """Choose race"""
    all_races = get_races()
    return templates.TemplateResponse(
        "character.html",
        {"request": request, "all_races": all_races, "choose": "race"}
    )


@router.post("/race/", response_class=HTMLResponse)
async def choose_subrace(
    request: Request,
    name: str = Form(...),
    race_name: str = Form(...),
):
    """Choose subrace"""
    subraces = get_subraces(race_name)
    return templates.TemplateResponse(
        "character.html",
        {"request": request, "subraces": subraces, "choose": "subrace"},
    )


@router.post("/class/", response_class=HTMLResponse)
async def create_class(
    request: Request,
    name: str = Form(...),
    race_name: str = Form(...),
):
    """Choose class"""
    all_classes = get_classes()
    return templates.TemplateResponse(
        "character.html",
        {"request": request, "all_classes": all_classes, "choose": "class"},
    )
