from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from datetime import datetime
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.core.dependencies import get_current_user
from app.services.transaction_service import TransactionService
from app.services.classifier import Classifier

import csv 
from io import TextIOWrapper
from decimal import Decimal

router = APIRouter(prefix="/transactions", tags=["transactions"])


@router.post("/")
async def create_transaction(
    amount: float,
    date_:datetime,
    description: Optional[str] = None,
    category: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    svc = TransactionService(db, user_id=current_user.id)
    return await svc.create(
        amount=amount,
        date_=date_.date(),
        description=description,
        category=category
    )

@router.get("/")
async def list_transactions(
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    svc = TransactionService(db, user_id=current_user.id)
    return await svc.list_all()

@router.get("/{txn_id: int}")
async def get_transaction(txn_id: int, db: AsyncSession = Depends(get_db)):
    svc = TransactionService(db)
    txn = await svc.get_by_id(txn_id)
    if not txn:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return txn

@router.post("/import-csv")
async def import_csv(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user),
):
    if not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="Envie um arquivo .csv")

    wrapper = TextIOWrapper(file.file, encoding="utf-8")
    reader = csv.DictReader(wrapper)

    clf = Classifier()
    svc = TransactionService(db, user_id=current_user.id)

    inserted = 0
    errors: List[str] = []

    async def _parse_date(s: str):
        try:
            return datetime.strptime(s.strip(), "%Y-%m%d").date()
        except Exception:
            return None
        
    async def _parse_amount(s: str):
        try:
            raw = s.strip().replace(".", "").replace(",", ".")
            return Decimal(raw)
        except Exception:
            return None

    for row in reader:
        d = (row.get("date") or "").strip()
        desc = (row.get("description") or "").strip()
        amt = (row.get("amount") or "").strip()
        cat0 = (row.get("category") or "").strip() or None

        date_parsed = await _parse_date(d)
        amount_parsed = await _parse_amount(amt)

        if not date_parsed or amount_parsed is None:
            errors.append(f"Linha inválida: {row}")
            continue
        
        pred_cat, conf = clf.predict_one(desc)

        await svc.create(
            amount=float(amount_parsed),
            date_=date_parsed,
            description=desc or None,
            category=cat0,
            predicted_category=pred_cat,
            confidence=conf,
        )
        inserted += 1

    return {"inserted": inserted, "errors": errors}
