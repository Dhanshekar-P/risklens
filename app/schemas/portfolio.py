from pydantic import BaseModel


class PortfolioCreate(BaseModel):
    name: str


class PortfolioResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True