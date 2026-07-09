from datetime import date, timedelta

import pandas as pd
import yfinance as yf

from sqlalchemy.orm import Session

from app.models.stock_price import StockPrice


def sync_ticker(
    ticker: str,
    db: Session
):

    start = date.today() - timedelta(days=365)

    df = yf.download(
        ticker,
        start=start,
        auto_adjust=False,
        progress=False
    )

    if df.empty:
        return 0

    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    df = df.reset_index()

    inserted = 0

    for _, row in df.iterrows():

        exists = (
            db.query(StockPrice)
            .filter(
                StockPrice.ticker == ticker.upper(),
                StockPrice.date == row["Date"].date()
            )
            .first()
        )

        if exists:
            continue

        db.add(
            StockPrice(
                ticker=ticker.upper(),
                date=row["Date"].date(),
                open=float(row["Open"]),
                high=float(row["High"]),
                low=float(row["Low"]),
                close=float(row["Close"]),
                volume=float(row["Volume"])
            )
        )

        inserted += 1

    db.commit()

    return inserted