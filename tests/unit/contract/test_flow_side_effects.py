from emprestimo.service import LoanService

class UsersOK:
    def get_user(self, uid): return {"id": uid, "name": "Ana", "type": "student", "active": True}
    def is_active(self, uid): return True

class CatalogSpy:
    def __init__(self):
        self._status = {}
        self.called_mark_loaned = []
        self.called_mark_available = []

    def _get_status(self, bid): return self._status.get(bid, "available")
    def get_book(self, bid): return {"id": bid, "title": "Clean Code", "status": self._get_status(bid)}
    def is_available(self, bid): return self._get_status(bid) == "available"

    def mark_loaned(self, bid):
        self.called_mark_loaned.append(bid)
        self._status[bid] = "loaned"

    def mark_available(self, bid):
        self.called_mark_available.append(bid)
        self._status[bid] = "available"

def test_flow_marks_catalog_on_loan_and_return():
    users = UsersOK()
    catalog = CatalogSpy()
    svc = LoanService(users, catalog)

    loan = svc.loan_book(1, 10)
    assert 10 in catalog.called_mark_loaned

    svc.return_book(loan.id)
    assert 10 in catalog.called_mark_available
