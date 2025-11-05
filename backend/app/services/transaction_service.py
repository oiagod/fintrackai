from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.models.transaction import TransactionORM
from datetime import date

class TransactionService:
    def __init__(self, db: AsyncSession):
        self.db= db

    async def create(self, amount: float, date_: date, description: str | None = None, category: str | None = None):
        txn = TransactionORM(amount=amount, date=date_, description=description, category=category)
        self.db.add(txn)
        await self.db.commit()
        await self.db.refresh(txn)
        return txn
    
    async def list_all(self):
        result = await self.db.execute(select(TransactionORM))
        return result.scalars().all()

    async def get_by_id(self, txn_id: int):
        result = await self.db.execute(select(TransactionORM).where(TransactionORM.id == txn_id))
        return result.scalar_one_or_none()