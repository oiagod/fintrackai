from datetime import date
from pydantic import BaseModel, Field
from typing import Optional

class TransactionCreate(BaseModel):
    amount: float = Field(gt=0)
    date: date
    description: Optional[str] = None
    category: Optional[str] = None

class TransactionOut(BaseModel):
    id: int
    amount: float = Field(gt=0)
    date: date
    description: Optional[str] = None
    category: Optional[str] = None

    class Config:
        from_attributes = True