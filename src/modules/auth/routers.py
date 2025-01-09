from fastapi import APIRouter

from .google.routers import router as google_router

router = APIRouter(prefix="/auth")
router.include_router(google_router)
