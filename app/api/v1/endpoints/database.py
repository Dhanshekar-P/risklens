from fastapi import APIRouter
from sqlalchemy import text

from app.db.session import engine

router = APIRouter()


@router.get("/db-check")
def db_check():
    try:
        with engine.connect() as connection:

            result = connection.execute(
                text("SELECT 1")
            )

            return {
                "database": "connected",
                "result": result.scalar()
            }

    except Exception as e:
        return {
            "database": "failed",
            "error": str(e)
        }