from fastapi import APIRouter, Depends, HTTPException
from datetime import date
from typing import Optional
from app.db.session import get_db
from app.services.transaction_service import TransactionService
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/transactions", tags=["transactions"])


@router.post("/")
async def create_transaction(amount: float, date_:date, description: Optional[str] = None, category: Optional[str] = None, db: AsyncSession = Depends(get_db)):
    service = TransactionService(db)
    return await service.create(amount, date_, description, category)

@router.get("/")
async def list_transactions(db: AsyncSession = Depends(get_db)):
    service = TransactionService(db)
    return await service.list_all()

@router.get("/{txn_id: int}")
async def get_transaction(txn_id: int, db: AsyncSession = Depends(get_db)):
    service = TransactionService(db)
    txn = await service.get_by_id(txn_id)
    if not txn:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return txn
