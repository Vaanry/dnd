import json

from fastapi import APIRouter, Form
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse, JSONResponse

from mongobase.create_char import get_classes, get_races, get_subraces, get_class_skills
from mongobase.schemas import Stats

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
    if subraces:
        return templates.TemplateResponse(
            "character.html",
            {"request": request, "subraces": subraces, "choose": "subrace"},
        )
    else:
        return templates.TemplateResponse(
    "redirect_to_class.html",
    {"request": request, "name": name, "race_name": race_name}
)


@router.post("/class/", response_class=HTMLResponse)
async def create_class(
    request: Request,
    subrace_name: str = Form(...),
):
    """Choose class"""
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
    return templates.TemplateResponse(
        "dices.html",
        {"request": request},
    )


@router.post("/add_dices/", response_class=JSONResponse)
async def add_dices(stats: Stats):
    # Логика обработки атрибутов
    print(f"Полученные атрибуты: {stats}")

    # Пример обработки данных (вы можете добавить свою логику)
    # Можно вернуть подтверждение или результат
    return {"message": "Данные успешно получены", "data": stats.model_dump()}
 

@router.get("/add_dices/", response_class=HTMLResponse)
async def add_dices1(
    request: Request):

    # Пример обработки данных (вы можете добавить свою логику)
    # Можно вернуть подтверждение или результат
    #return {"message": "Данные успешно получены", "data": stats.model_dump()}
    return templates.TemplateResponse(
        "dices.html",
        {"request": request},
    )
