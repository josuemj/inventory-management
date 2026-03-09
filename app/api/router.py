from fastapi import APIRouter

from app.modules.companies.router import router as companies_router
from app.modules.users.router import router as users_router


api_router = APIRouter()
api_router.include_router(companies_router)
api_router.include_router(users_router)
