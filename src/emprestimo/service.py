import uuid
from datetime import datetime, timezone
from .domain import Loan, LoanError

class LoanService:
    """
    Serviço de Empréstimos/Devoluções.
    - Valida usuário e livro via serviços externos (ports).
    - Controla limite de empréstimos ativos por usuário.
    - Mantém um storage em memória (_loans).
    """

    def __init__(self, user_service, catalog_service, max_active_loans: int = 2):
        self.users = user_service
        self.catalog = catalog_service
        self.max_active_loans = max_active_loans
        self._loans: dict[str, Loan] = {}

    # ---------- helpers ----------
    def _validate_user(self, user_id: int) -> None:
        user = self.users.get_user(user_id)
        if not user or not self.users.is_active(user_id):
            raise LoanError("Usuário inválido ou inativo")

    def _validate_book_available(self, book_id: int) -> None:
        book = self.catalog.get_book(book_id)
        if not book or not self.catalog.is_available(book_id):
            raise LoanError("Livro inválido ou indisponível")

    def _validate_limit(self, user_id: int) -> None:
        if len(self.get_active_loans_by_user(user_id)) >= self.max_active_loans:
            raise LoanError("Limite de empréstimos ativos atingido")

    # ---------- operações ----------
    def loan_book(self, user_id: int, book_id: int) -> Loan:
        """Cria empréstimo (status=active) se usuário/livro ok e limite não estourado."""
        self._validate_user(user_id)
        self._validate_book_available(book_id)
        self._validate_limit(user_id)

        self.catalog.mark_loaned(book_id)

        loan = Loan(
            id=str(uuid.uuid4()),
            user_id=user_id,
            book_id=book_id,
            loan_date=datetime.now(timezone.utc),  # timezone-aware
            return_date=None,
            status="active",
        )
        self._loans[loan.id] = loan
        return loan

    def return_book(self, loan_id: str) -> Loan:
        """Finaliza empréstimo: status=returned e define return_date."""
        loan = self._loans.get(loan_id)
        if not loan:
            raise LoanError("Empréstimo inexistente")
        if loan.status == "returned":
            raise LoanError("Empréstimo já devolvido")

        self.catalog.mark_available(loan.book_id)
        loan.status = "returned"
        loan.return_date = datetime.now(timezone.utc)
        return loan

    # ---------- consultas ----------
    def get_loan(self, loan_id: str) -> Loan | None:
        return self._loans.get(loan_id)

    def get_active_loans_by_user(self, user_id: int) -> list[Loan]:
        """Retorna ativos do usuário ordenados do mais recente para o mais antigo."""
        active = [
            loan for loan in self._loans.values()
            if loan.user_id == user_id and loan.status == "active"
        ]
        return sorted(active, key=lambda l: l.loan_date, reverse=True)
