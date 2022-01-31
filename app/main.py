from fastapi import FastAPI

from app.api import router
from app.core.config import settings


def get_application() -> FastAPI:
    _app = FastAPI(title=settings.PROJECT_NAME, debug=True)
    _app.include_router(router)
    return _app


app = get_application()
