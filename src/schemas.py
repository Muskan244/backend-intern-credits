from datetime import datetime
from pydantic import BaseModel, Field

class CreditBalance(BaseModel):
    user_id: int
    credits: int = Field(ge=0)
    last_updated: datetime

    class Config:
        from_attributes = True

class AmountIn(BaseModel):
    amount: int = Field(gt=0)

class ApplySchemaSQL(BaseModel):
    sql: str
    token: str | None = None
