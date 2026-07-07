from pydantic import BaseModel


class HoldingCreate(BaseModel):

    ticker: str

    quantity: float

    average_price: float

    portfolio_id: int


class HoldingResponse(BaseModel):

    id: int

    ticker: str

    quantity: float

    average_price: float

    portfolio_id: int

    class Config:
        from_attributes = True