from fastapi import APIRouter

from app.api.v1.endpoints import health
from app.api.v1.endpoints import database
from app.api.v1.endpoints.portfolio import router as portfolio_router
from app.api.v1.endpoints.holding import router as holding_router
from app.api.v1.endpoints.market_data import router as market_router
from app.api.v1.endpoints.risk import router as risk_router

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

api_router.include_router(holding_router)

api_router.include_router(market_router)

api_router.include_router(risk_router)