from sqlalchemy import Column, Integer, String, Numeric, Date, DateTime, func
from app.db.session import Base

class TransactionORM(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Numeric(10, 2), nullable=False)
    date = Column(Date, nullable=False)
    description = Column(String, nullable=True)
    category = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())