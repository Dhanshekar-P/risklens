from fastapi import APIRouter

from app.api.v1.endpoints import health
from app.api.v1.endpoints import database
from app.api.v1.endpoints.portfolio import router as portfolio_router

api_router = APIRouter()

api_router.include_router(
    health.router,
    tags=["Health"]
)

api_router.include_router(
    database.router,
    tags=["Database"]
)

api_router.include_router(portfolio_router)