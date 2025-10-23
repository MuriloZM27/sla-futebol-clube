from datetime import datetime, timezone  # <-- adicione timezone
from .domain import Loan, LoanError
import uuid

class LoanService:
    def __init__(self, user_service, catalog_service):
        self.users = user_service
        self.catalog = catalog_service
        self._loans: dict[str, Loan] = {}

    # --- refactors pequenos para clareza ---
    def _validate_user(self, user_id: int) -> None:
        user = self.users.get_user(user_id)
        if not user or not self.users.is_active(user_id):
            raise LoanError("Usuário inválido ou inativo")

    def _validate_book_available(self, book_id: int) -> None:
        book = self.catalog.get_book(book_id)
        if not book or not self.catalog.is_available(book_id):
            raise LoanError("Livro inválido ou indisponível")

    def loan_book(self, user_id: int, book_id: int) -> Loan:
        self._validate_user(user_id)
        self._validate_book_available(book_id)

        self.catalog.mark_loaned(book_id)

        loan = Loan(
            id=str(uuid.uuid4()),
            user_id=user_id,
            book_id=book_id,
            # timezone-aware para remover o warning
            loan_date=datetime.now(timezone.utc),
            return_date=None,
            status="active",
        )
        self._loans[loan.id] = loan
        return loan
    from datetime import datetime, timezone  # já está importado acima

    def return_book(self, loan_id: str):
        loan = self._loans.get(loan_id)
        if not loan:
            raise LoanError("Empréstimo inexistente")

        if loan.status == "returned":
            raise LoanError("Empréstimo já devolvido")

        self.catalog.mark_available(loan.book_id)
        loan.status = "returned"
        loan.return_date = datetime.now(timezone.utc)
        return loan

