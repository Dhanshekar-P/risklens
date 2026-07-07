from sqlalchemy import Column
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String

from sqlalchemy.orm import relationship

from app.db.session import Base


class Holding(Base):

    __tablename__ = "holdings"

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

    quantity = Column(
        Float,
        nullable=False
    )

    average_price = Column(
        Float,
        nullable=False
    )

    portfolio_id = Column(
        Integer,
        ForeignKey("portfolios.id"),
        nullable=False
    )

    portfolio = relationship(
        "Portfolio",
        back_populates="holdings"
    )