from fastapi import FastAPI

from app.api.router import api_router
from app.api.v1.endpoints.auth import router as auth_router

app = FastAPI(
    title="Risk AI",
    version="1.0.0"
)

app.include_router(api_router)
app.include_router(auth_router)