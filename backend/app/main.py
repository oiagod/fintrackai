from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

app = FastAPI(title="Fintrack AI API")

@app.get("/health")
def health():
    return {"status": "ok"}

class EchoPayload(BaseModel):
    amount: float = Field(gt=0, description="Value > 0")
    date: date
    description: Optional[str] = None

@app.post("/echo")
def echo(payload: EchoPayload) -> EchoPayload:
    return payload