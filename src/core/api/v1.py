from fastapi import FastAPI

from src.core.config import settings

__all__ = ("app",)

app = FastAPI(
    title=settings.project_title,
    description=settings.project_description,
    version="1.0.0",
)
