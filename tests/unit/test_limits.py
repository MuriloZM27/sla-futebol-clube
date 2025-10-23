import pytest
from emprestimo.service import LoanService
from emprestimo.domain import LoanError

class UsersOK:
    def get_user(self, uid): return {"id": uid, "name": "Ana", "type": "student", "active": True}
    def is_active(self, uid): return True

class CatalogOK:
    def __init__(self):
        self._status = {}
    def _get_status(self, bid): return self._status.get(bid, "available")
    def get_book(self, bid): return {"id": bid, "title": "Clean Code", "status": self._get_status(bid)}
    def is_available(self, bid): return self._get_status(bid) == "available"
    def mark_loaned(self, bid): self._status[bid] = "loaned"
    def mark_available(self, bid): self._status[bid] = "available"

def test_user_cannot_exceed_active_loan_limit():
    svc = LoanService(UsersOK(), CatalogOK())
    # supondo limite = 2
    svc.loan_book(user_id=1, book_id=10)
    svc.loan_book(user_id=1, book_id=11)
    with pytest.raises(LoanError):
        svc.loan_book(user_id=1, book_id=12)

def test_get_active_loans_by_user_returns_most_recent_first():
    svc = LoanService(UsersOK(), CatalogOK())
    l1 = svc.loan_book(user_id=2, book_id=20)  # mais antigo
    l2 = svc.loan_book(user_id=2, book_id=21)  # mais recente

    active = svc.get_active_loans_by_user(user_id=2)

    assert [loan.id for loan in active] == [l2.id, l1.id]
