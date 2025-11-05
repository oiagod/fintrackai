from typing import List, Optional
from app.models.transaction import Transaction
from datetime import date

class TransactionService:
    def __init__(self):
        self._transactions: List[Transaction] = []
        self._next_id = 1

    def create(self, amount: float, date_: date, description: Optional[str] = None) -> Transaction:
        txn = Transaction(id=self._next_id, amount=amount, date=date_, description=description)
        self._transactions.append(txn)
        self._next_id += 1
        return txn
    
    def list_all(self) -> List[Transaction]:
        return self._transactions

    def get_by_id(self, transaction_id: int) -> Optional[Transaction]:
        for t in self._transactions:
            if t.id == transaction_id:
                return t
        return None
