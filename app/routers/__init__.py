from fastapi import APIRouter
from .character import router as character_router

main_router = APIRouter()

main_router.include_router(character_router)