from fastapi import APIRouter

from .auth import router as auth_router
from .character import router as character_router
from .users import router as users_router

main_router = APIRouter()

main_router.include_router(character_router)
main_router.include_router(auth_router)
main_router.include_router(users_router)
