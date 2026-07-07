from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.core.oauth2 import get_current_user
from app.db.dependencies import get_db

from app.models.holding import Holding
from app.models.portfolio import Portfolio
from app.models.user import User

from app.schemas.holding import (
    HoldingCreate,
    HoldingResponse
)

router = APIRouter(
    prefix="/holding",
    tags=["Holding"]
)


@router.post(
    "",
    response_model=HoldingResponse
)
def create_holding(
    holding: HoldingCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    portfolio = (
        db.query(Portfolio)
        .filter(
            Portfolio.id == holding.portfolio_id,
            Portfolio.user_id == current_user.id
        )
        .first()
    )

    if portfolio is None:
        raise HTTPException(
            status_code=404,
            detail="Portfolio not found"
        )

    new_holding = Holding(
        ticker=holding.ticker.upper(),
        quantity=holding.quantity,
        average_price=holding.average_price,
        portfolio_id=holding.portfolio_id
    )

    db.add(new_holding)

    db.commit()

    db.refresh(new_holding)

    return new_holding


@router.get(
    "/{portfolio_id}",
    response_model=list[HoldingResponse]
)
def get_holdings(
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
        raise HTTPException(
            status_code=404,
            detail="Portfolio not found"
        )

    return (
        db.query(Holding)
        .filter(
            Holding.portfolio_id == portfolio_id
        )
        .all()
    )


@router.delete("/{holding_id}")
def delete_holding(
    holding_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    holding = (
        db.query(Holding)
        .join(Portfolio)
        .filter(
            Holding.id == holding_id,
            Portfolio.user_id == current_user.id
        )
        .first()
    )

    if holding is None:
        raise HTTPException(
            status_code=404,
            detail="Holding not found"
        )

    db.delete(holding)

    db.commit()

    return {
        "message": "Holding deleted"
    }