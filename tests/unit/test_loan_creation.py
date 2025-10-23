
import pytest
from datetime import datetime

# RED: ainda não existe implementação real em src/emprestimo/service.py
# Quando você rodar pytest, este teste deve FALHAR.
from emprestimo.service import LoanService
from emprestimo.domain import Loan, LoanError

class FakeUserService:
    def __init__(self, active=True): self.active = active
    def get_user(self, user_id):
        return {"id": user_id, "name": "Ana", "type": "student", "active": self.active}
    def is_active(self, user_id): return self.active

class FakeCatalogService:
    def __init__(self, available=True): self.available = available
    def get_book(self, book_id):
        status = "available" if self.available else "loaned"
        return {"id": book_id, "title": "Clean Code", "status": status}
    def is_available(self, book_id): return self.available
    def mark_loaned(self, book_id):
        if not self.available: raise RuntimeError("already loaned")
        self.available = False

def test_loan_ok_user_active_book_available():
    users = FakeUserService(active=True)
    catalog = FakeCatalogService(available=True)
    svc = LoanService(users, catalog)

    loan = svc.loan_book(user_id=1, book_id=10)

    assert isinstance(loan, Loan)
    assert loan.user_id == 1
    assert loan.book_id == 10
    assert loan.status == "active"
    assert loan.loan_date is not None
    assert catalog.available is False

def test_loan_fails_if_user_inactive():
    users = FakeUserService(active=False)
    catalog = FakeCatalogService(available=True)
    svc = LoanService(users, catalog)

    with pytest.raises(LoanError):
        svc.loan_book(user_id=1, book_id=10)

def test_loan_fails_if_book_not_available():
    users = FakeUserService(active=True)
    catalog = FakeCatalogService(available=False)
    svc = LoanService(users, catalog)

    with pytest.raises(LoanError):
        svc.loan_book(user_id=1, book_id=10)
