from fastapi import APIRouter

from app.api.v1.user import router as user_router
from app.api.v1.image import router as image_router

router = APIRouter(prefix="/v1")

router.include_router(user_router)
router.include_router(image_router)
