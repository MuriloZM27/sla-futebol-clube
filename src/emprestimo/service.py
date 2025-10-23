import uuid
from datetime import datetime
from .domain import Loan, LoanError

class LoanService:
    def __init__(self, user_service, catalog_service):
        self.users = user_service
        self.catalog = catalog_service
        self._loans: dict[str, Loan] = {}

    def loan_book(self, user_id: int, book_id: int) -> Loan:
        user = self.users.get_user(user_id)
        if not user or not self.users.is_active(user_id):
            raise LoanError("Usuário inválido ou inativo")

        book = self.catalog.get_book(book_id)
        if not book or not self.catalog.is_available(book_id):
            raise LoanError("Livro inválido ou indisponível")

        self.catalog.mark_loaned(book_id)

        loan = Loan(
            id=str(uuid.uuid4()),
            user_id=user_id,
            book_id=book_id,
            loan_date=datetime.utcnow(),
            return_date=None,
            status="active",
        )
        self._loans[loan.id] = loan
        return loan
