from fastapi import APIRouter, HTTPException
from datetime import date
from typing import Optional
from app.services.transaction_service import TransactionService

router = APIRouter(prefix="/transactions", tags=["transactions"])

service = TransactionService()

@router.post("/")
def create_transaction(amount: float, date_:date, description: Optional[str] = None):
    return service.create(amount, date_, description)

@router.get("/")
def list_transactions():
    return service.list_all()

@router.get("/{txn_id: int}")
def get_transaction(txn_id: int):
    txn = service.get_by_id(txn_id)
    if not txn:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return txn
