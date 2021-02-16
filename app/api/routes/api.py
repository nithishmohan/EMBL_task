from fastapi import APIRouter
from app.api.routes import index

router = APIRouter()
router.include_router(index.router, tags=["persons"], prefix="/person")
router.include_router(index.router, tags=["persons"])
