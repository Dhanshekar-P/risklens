from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.core.oauth2 import get_current_user

from app.db.dependencies import get_db

from app.models.portfolio import Portfolio
from app.models.user import User

from app.services.risk_service import portfolio_summary
from app.services.ai_service import analyze_portfolio

router = APIRouter(
    prefix="/ai",
    tags=["AI"]
)


@router.get("/{portfolio_id}")
def ai_analysis(
    portfolio_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    portfolio = (
        db.query(Portfolio)
        .filter(
            Portfolio.id == portfolio_id,
            Portfolio.user_id == current_user.id
        )
        .first()
    )

    if portfolio is None:
        return {
            "detail": "Portfolio not found"
        }

    summary = portfolio_summary(
        portfolio_id,
        db
    )

    analysis = analyze_portfolio(
        summary
    )

    return {

        "risk_summary": summary,

        "ai_analysis": analysis

    }