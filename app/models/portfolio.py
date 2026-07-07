from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from app.db.session import Base


class Portfolio(Base):
    __tablename__ = "portfolios"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String(100),
        nullable=False
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    user = relationship(
        "User",
        back_populates="portfolios"
    )

    # holdings = relationship(
    #     "Holding",
    #     back_populates="portfolio",
    #     cascade="all, delete-orphan"
    # )