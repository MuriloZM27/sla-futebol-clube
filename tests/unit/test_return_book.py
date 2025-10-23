import pytest
from emprestimo.service import LoanService
from emprestimo.domain import LoanError

class UsersOK:
    def get_user(self, uid): return {"id": uid, "name": "Ana", "type": "student", "active": True}
    def is_active(self, uid): return True

class CatalogOK:
    def __init__(self):
        self.available = True
    def get_book(self, bid):
        return {"id": bid, "title": "Clean Code", "status": "available" if self.available else "loaned"}
    def is_available(self, bid): return self.available
    def mark_loaned(self, bid): self.available = False
    def mark_available(self, bid): self.available = True

def test_return_ok_changes_status_and_sets_return_date():
    svc = LoanService(UsersOK(), CatalogOK())
    loan = svc.loan_book(1, 10)

    returned = svc.return_book(loan.id)

    assert returned.status == "returned"
    assert returned.return_date is not None

def test_return_fails_if_already_returned():
    svc = LoanService(UsersOK(), CatalogOK())
    loan = svc.loan_book(1, 10)
    svc.return_book(loan.id)

    with pytest.raises(LoanError):
        svc.return_book(loan.id)
