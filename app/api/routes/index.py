from fastapi import APIRouter
from app.api.routes import api

router = APIRouter()
router.include_router(api.router, tags=["persons"], prefix="/person")
router.include_router(api.router, tags=["persons"])
