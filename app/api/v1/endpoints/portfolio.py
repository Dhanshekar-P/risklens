from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.db.dependencies import get_db

from app.models.portfolio import Portfolio
from app.models.user import User

from app.schemas.portfolio import (
    PortfolioCreate,
    PortfolioResponse
)

from app.core.oauth2 import get_current_user

router = APIRouter(
    prefix="/portfolio",
    tags=["Portfolio"]
)


@router.post(
    "",
    response_model=PortfolioResponse
)
def create_portfolio(
    portfolio: PortfolioCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    new_portfolio = Portfolio(
        name=portfolio.name,
        user_id=current_user.id
    )

    db.add(new_portfolio)
    db.commit()
    db.refresh(new_portfolio)

    return new_portfolio


@router.get(
    "",
    response_model=list[PortfolioResponse]
)
def get_portfolios(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return (
        db.query(Portfolio)
        .filter(
            Portfolio.user_id == current_user.id
        )
        .all()
    )


@router.get(
    "/{portfolio_id}",
    response_model=PortfolioResponse
)
def get_portfolio(
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

    if not portfolio:
        raise HTTPException(
            status_code=404,
            detail="Portfolio not found"
        )

    return portfolio


@router.delete(
    "/{portfolio_id}"
)
def delete_portfolio(
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

    if not portfolio:
        raise HTTPException(
            status_code=404,
            detail="Portfolio not found"
        )

    db.delete(portfolio)
    db.commit()

    return {
        "message": "Portfolio deleted"
    }