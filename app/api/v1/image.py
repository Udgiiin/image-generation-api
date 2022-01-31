from fastapi import APIRouter, Header, Depends
from dependency_injector.wiring import inject, Provide
from app.services import image as services
from app.core.security import auth_required
from app.core.redis import create_redis_pool
from starlette.responses import StreamingResponse
from typing import Optional
import aioredis
import io
router = APIRouter(prefix="/image")


@router.get("/generate/{slug}")
@auth_required
@inject
async def generate_image(slug: str, authorization: Optional[str] = Header(None), user_id=None,
                         service = Depends(create_redis_pool)):
    image = await service.get(slug)
    if image:
        return StreamingResponse(io.BytesIO(image.encode('ISO-8859-1')), media_type="image/png")
    else:
        image = services.generate_image(slug).content
        await service.set(slug, image.decode('ISO-8859-1'))
        return StreamingResponse(io.BytesIO(image), media_type="image/png")