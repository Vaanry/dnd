import json 
from fastapi import APIRouter
from fastapi.requests import Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from mongobase.create_char import get_classes, get_races

templates = Jinja2Templates(directory="templates")
router = APIRouter(prefix="/character", tags=["character"])

router.mount("/static", StaticFiles(directory="static"), name="characters")


@router.get("/")
async def create(request: Request):
    all_classes = [class_ for class_ in get_classes()]
    all_races = get_races()
    return templates.TemplateResponse(
        "character.html", {"request": request, "all_classes": all_classes, "all_races": all_races}
    )
