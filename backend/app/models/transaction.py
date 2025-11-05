from datetime import date
from pydantic import BaseModel, Field
from typing import Optional

class Transaction(BaseModel):
    id: int
    amount: float = Field(gt=0)
    date: date
    description: Optional[str] = None