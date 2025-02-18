import os
import sys
from typing import Annotated

from fastapi import APIRouter, Depends, Form, status
from fastapi.requests import Request
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from mongobase.create_char import (create_char, get_background_skills,
                                   get_backgrounds, get_class_skills,
                                   get_classes, get_races, get_subraces, get_class_equipment)
from mongobase.schemas import CharacterBackground, Stats, WeaponItem, ArmorItem, EquipmentItem

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import redisbase

from .auth import get_current_user

templates = Jinja2Templates(directory="templates")
router = APIRouter(prefix="/character", tags=["character"])

router.mount("/static", StaticFiles(directory="static"), name="characters")


@router.get("/", response_class=HTMLResponse)
async def create_race(
    request: Request, get_user: Annotated[dict, Depends(get_current_user)]
):
    """Choose race"""
    all_races = get_races()
    return templates.TemplateResponse(
        "character.html", {"request": request, "all_races": all_races, "choose": "race"}
    )


@router.post("/race/", response_class=HTMLResponse)
async def choose_subrace(
    request: Request,
    get_user: Annotated[dict, Depends(get_current_user)],
    name: str = Form(...),
    gender: str = Form(...),
    race_name: str = Form(...),
    kidness: str = Form(...),
    lawfullness: str = Form(...),
):
    """Choose subrace"""
    user_id = get_user.get("id")
    redisbase.set_char_init(user_id, name, gender, race_name, kidness, lawfullness)

    subraces = get_subraces(race_name)
    if subraces:
        return templates.TemplateResponse(
            "character.html",
            {"request": request, "subraces": subraces, "choose": "subrace"},
        )
    else:
        return templates.TemplateResponse(
            "redirect_to_class.html",
            {"request": request, "name": name, "race_name": race_name},
        )


@router.post("/class/", response_class=HTMLResponse)
async def create_class(
    request: Request,
    get_user: Annotated[dict, Depends(get_current_user)],
    subrace_name: str = Form(...),
):
    """Choose class"""
    user_id = get_user.get("id")
    redisbase.set_char_subrace(user_id, subrace_name)
    all_classes = get_classes()
    return templates.TemplateResponse(
        "character.html",
        {"request": request, "all_classes": all_classes, "choose": "class"},
    )


@router.post("/background/", response_class=HTMLResponse)
async def create_background(
    request: Request,
    get_user: Annotated[dict, Depends(get_current_user)],
    class_name: str = Form(...),
):
    """Choose background"""
    user_id = get_user.get("id")
    redisbase.set_char_class(user_id, class_name)
    all_backgrounds = get_backgrounds()
    return templates.TemplateResponse(
        "character.html",
        {
            "request": request,
            "all_backgrounds": all_backgrounds,
            "choose": "background",
        },
    )


@router.post("/next/", response_class=HTMLResponse)
async def choose_skills(
    request: Request,
    get_user: Annotated[dict, Depends(get_current_user)],
    background_name: str = Form(...),
):
    """Choose class skills"""
    user_id = get_user.get("id")
    redisbase.set_char_background(user_id, background_name)
    background_skills = get_background_skills(background_name)
    redisbase.delete_class_skills(user_id)
    redisbase.set_class_skills(user_id, background_skills)
    class_name = redisbase.get_char_class(user_id)
    skills = get_class_skills(class_name)
    return templates.TemplateResponse(
        "character_modification.html",
        {"request": request, "skills": skills},
    )


@router.post("/dices/", response_class=HTMLResponse)
async def rolling_dices(
    request: Request,
    get_user: Annotated[dict, Depends(get_current_user)],
    selected_skills: list[str] = Form(...),
):
    """Choose class skills"""
    user_id = get_user.get("id")
    redisbase.set_class_skills(user_id, selected_skills)
    return templates.TemplateResponse(
        "dices.html",
        {"request": request},
    )


@router.post("/add_dices/", response_class=JSONResponse)
async def add_dices(
    request: Request,
    get_user: Annotated[dict, Depends(get_current_user)],
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
    user_id = get_user.get("id")
    redisbase.set_char_ctats(user_id, stats.model_dump())
    class_name = redisbase.get_char_class(user_id)
    class_equipment = get_class_equipment(class_name)
    char_info = redisbase.get_char_info(user_id)

    return templates.TemplateResponse(
        "char.html",
        {"request": request, "char_info": char_info, "class_equipment": class_equipment},
    )


@router.post("/save/", response_class=RedirectResponse)
async def save_char(
    request: Request,
    get_user: Annotated[dict, Depends(get_current_user)],
    selected_equipment: str = Form(...),
    notes: str = Form(...),
):
    user_id = get_user.get("id")
    char_info = redisbase.get_char_info(user_id)
    class_equipment = get_class_equipment(char_info["char_class"])[int(selected_equipment)-1]
    
    if class_equipment['armor'] is not None:
        armor = [item['name'] for item in class_equipment['armor']]
    else:
        armor = None
        
    if class_equipment['weapon'] is not None:
        weapon = [item['name'] for item in class_equipment['weapon']]
    else:
        weapon = None
        
    if class_equipment['other'] is not None:
        equipment = [item['name'] for item in class_equipment['other']]
    else:
        equipment = []
    
    char = {
        "owner": user_id,
        "name": char_info["char_name"],
        "race": char_info["char_race"],
        "alignment": char_info["char_alignment"],
        "subrace": char_info["char_subrace"],
        "gender": char_info["char_gender"],
        "character_class": char_info["char_class"],
        "level": 1,
        "stats": {
            "Strength": char_info["char_stats"]["strength"],
            "Dexterity": char_info["char_stats"]["dexterity"],
            "Constitution": char_info["char_stats"]["constitution"],
            "Intelligence": char_info["char_stats"]["intelligence"],
            "Wisdom": char_info["char_stats"]["wisdom"],
            "Charisma": char_info["char_stats"]["charisma"],
        },
        "skills": char_info["char_skills"],
        "background": char_info["char_background"],
        "armor": armor,
        "weapon": weapon,
        "equipment":equipment,
        "notes": notes,
    }
    
    create_char(char)
    redisbase.delete_char_info(user_id)
    return RedirectResponse(
        url=f"/user/my_characters/{char_info["char_name"]}",
        status_code=status.HTTP_303_SEE_OTHER,
    )
