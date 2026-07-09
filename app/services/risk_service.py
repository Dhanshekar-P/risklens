from sqlalchemy.orm import Session

from app.models.holding import Holding
from app.models.stock_price import StockPrice

import numpy as np


def portfolio_summary(
    portfolio_id: int,
    db: Session
):

    holdings = (
        db.query(Holding)
        .filter(
            Holding.portfolio_id == portfolio_id
        )
        .all()
    )

    summary = []

    total_value = 0
    total_invested = 0

    portfolio_returns = []

    for holding in holdings:

        prices = (
            db.query(StockPrice)
            .filter(
                StockPrice.ticker == holding.ticker
            )
            .order_by(
                StockPrice.date.asc()
            )
            .all()
        )

        if len(prices) < 2:
            continue

        latest = prices[-1]

        market_value = latest.close * holding.quantity

        invested = holding.average_price * holding.quantity

        pnl = market_value - invested

        total_value += market_value

        total_invested += invested

        closes = np.array([p.close for p in prices])

        daily_returns = np.diff(closes) / closes[:-1]

        portfolio_returns.extend(daily_returns)

        summary.append(
            {
                "ticker": holding.ticker,
                "quantity": holding.quantity,
                "average_price": holding.average_price,
                "current_price": latest.close,
                "market_value": round(market_value, 2),
                "invested": round(invested, 2),
                "profit_loss": round(pnl, 2),
                "return_percent": round((pnl / invested) * 100, 2)
            }
        )

    if len(portfolio_returns):

        portfolio_returns = np.array(portfolio_returns)

        annual_return = np.mean(portfolio_returns) * 252

        volatility = np.std(portfolio_returns) * np.sqrt(252)

        sharpe = (
            annual_return / volatility
            if volatility > 0
            else 0
        )

        var95 = np.percentile(
            portfolio_returns,
            5
        )

        cumulative = np.cumprod(
            1 + portfolio_returns
        )

        running_max = np.maximum.accumulate(
            cumulative
        )

        drawdown = (
            cumulative - running_max
        ) / running_max

        max_drawdown = drawdown.min()

    else:

        annual_return = 0
        volatility = 0
        sharpe = 0
        var95 = 0
        max_drawdown = 0

    weights = []

    for item in summary:

        if total_value == 0:
            break

        weights.append(
            item["market_value"] / total_value
        )

    concentration = (
        max(weights)
        if weights
        else 0
    )

    risk_score = (
        volatility * 40
        + concentration * 30
        + abs(max_drawdown) * 30
    )

    return {

        "portfolio_value": round(total_value, 2),

        "invested_amount": round(total_invested, 2),

        "profit_loss": round(
            total_value - total_invested,
            2
        ),

        "portfolio_return_percent": round(
            (
                (total_value - total_invested)
                / total_invested
                * 100
            )
            if total_invested
            else 0,
            2
        ),

        "annual_return": round(
            annual_return * 100,
            2
        ),

        "volatility": round(
            volatility * 100,
            2
        ),

        "sharpe_ratio": round(
            sharpe,
            2
        ),

        "max_drawdown": round(
            max_drawdown * 100,
            2
        ),

        "value_at_risk_95": round(
            var95 * 100,
            2
        ),

        "concentration_risk": round(
            concentration * 100,
            2
        ),

        "risk_score": round(
            risk_score,
            2
        ),

        "holdings": summary
    }