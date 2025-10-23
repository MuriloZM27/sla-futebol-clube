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

def test_get_loan_returns_saved_loan():
    svc = LoanService(UsersOK(), CatalogOK())
    loan = svc.loan_book(user_id=1, book_id=10)

    fetched = svc.get_loan(loan.id)

    assert fetched is not None
    assert fetched.id == loan.id
    assert fetched.user_id == 1
    assert fetched.book_id == 10
    assert fetched.status == "active"

def test_get_active_loans_by_user_only_active():
    svc = LoanService(UsersOK(), CatalogOK())
    # user 1 com dois empréstimos
    l1 = svc.loan_book(user_id=1, book_id=10)
    # devolve um deles para deixar "returned"
    svc.return_book(l1.id)
    # outro empréstimo ainda ativo
    l2 = svc.loan_book(user_id=1, book_id=11)
    # outro usuário (não deve aparecer)
    _ = svc.loan_book(user_id=2, book_id=12)

    active = svc.get_active_loans_by_user(user_id=1)

    assert len(active) == 1
    assert active[0].id == l2.id
    assert active[0].status == "active"
