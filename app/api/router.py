from fastapi import APIRouter

from app.modules.auth.router import router as auth_router
from app.modules.categories.router import router as categories_router
from app.modules.change_logs.router import router as change_logs_router
from app.modules.inventory_movements.router import router as movements_router
from app.modules.items.router import router as items_router
from app.modules.organizations.router import router as organizations_router
from app.modules.providers.router import router as providers_router
from app.modules.users.router import router as users_router

api_router = APIRouter()
api_router.include_router(auth_router)
api_router.include_router(organizations_router)
api_router.include_router(users_router)
api_router.include_router(categories_router)
api_router.include_router(providers_router)
api_router.include_router(items_router)
api_router.include_router(movements_router)
api_router.include_router(change_logs_router)
