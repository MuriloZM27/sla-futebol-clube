from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Optional

# --- Mensagens padronizadas (usadas pelo service.py) ---
ERR_USER = "Usuário inválido ou inativo"
ERR_BOOK = "Livro inválido ou indisponível"
ERR_LOAN_NOT_FOUND = "Empréstimo inexistente"
ERR_ALREADY_RETURNED = "Empréstimo já devolvido"
ERR_LIMIT_REACHED = "Limite de empréstimos ativos atingido"

class LoanError(Exception):
    """Erro de regras de empréstimo/devolução."""
    pass

@dataclass
class Loan:
    id: str
    user_id: int
    book_id: int
    loan_date: datetime           # ideal: timezone-aware (UTC)
    return_date: Optional[datetime]  # None quando não devolvido
    status: str                   # "active" | "returned"

# --- Helpers de serialização (contrato/integração) ---

def _dt_to_iso(dt: Optional[datetime]) -> Optional[str]:
    """
    Converte datetime para string ISO-8601 (preserva timezone se existir).
    Retorna None se dt for None.
    """
    if dt is None:
        return None
    return dt.isoformat()

def loan_to_dict(loan: Loan) -> dict:
    """
    Serializa Loan em dict “pronto para JSON”, com datetimes em ISO-8601.
    Campos esperados: id, user_id, book_id, loan_date, return_date, status.
    """
    d = asdict(loan)
    d["loan_date"] = _dt_to_iso(d["loan_date"])
    d["return_date"] = _dt_to_iso(d["return_date"])
    return d

