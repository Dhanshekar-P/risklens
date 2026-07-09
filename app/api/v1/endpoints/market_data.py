from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.core.oauth2 import get_current_user

from app.db.dependencies import get_db

from app.models.user import User

from app.services.market_service import sync_ticker

router = APIRouter(
    prefix="/market",
    tags=["Market Data"]
)


@router.post("/sync/{ticker}")
def sync_market_data(
    ticker: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    inserted = sync_ticker(
        ticker,
        db
    )

    return {
        "ticker": ticker.upper(),
        "rows_inserted": inserted
    }