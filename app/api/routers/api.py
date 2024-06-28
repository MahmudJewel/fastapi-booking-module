from fastapi import APIRouter
from app.api.routers.user import user_router
from app.core.database import db_module
from app.api.routers.booking import booking_router
router = APIRouter()

router.include_router(db_module)
router.include_router(user_router)
router.include_router(booking_router)


