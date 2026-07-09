from sqlalchemy import Column
from sqlalchemy import Date
from sqlalchemy import Float
from sqlalchemy import Integer
from sqlalchemy import String

from app.db.session import Base


class StockPrice(Base):

    __tablename__ = "stock_prices"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    ticker = Column(
        String(20),
        nullable=False,
        index=True
    )

    date = Column(
        Date,
        nullable=False,
        index=True
    )

    open = Column(
        Float,
        nullable=False
    )

    high = Column(
        Float,
        nullable=False
    )

    low = Column(
        Float,
        nullable=False
    )

    close = Column(
        Float,
        nullable=False
    )

    volume = Column(
        Float,
        nullable=False
    )