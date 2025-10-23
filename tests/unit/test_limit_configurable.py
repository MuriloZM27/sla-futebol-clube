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

def test_limit_can_be_configured_per_instance():
    # queremos limitar para 1 via construtor
    svc = LoanService(UsersOK(), CatalogOK(), max_active_loans=1)  # <-- deve quebrar agora (RED)
    svc.loan_book(user_id=1, book_id=10)
    with pytest.raises(LoanError):
        svc.loan_book(user_id=1, book_id=11)
