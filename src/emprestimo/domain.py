from dataclasses import dataclass, asdict
from datetime import datetime

class LoanError(Exception):
    pass

@dataclass
class Loan:
    id: str
    user_id: int
    book_id: int
    loan_date: datetime          # ideal: timezone-aware (UTC)
    return_date: datetime | None # ideal: timezone-aware (UTC) ou None
    status: str                  # "active" | "returned"

# --- Helpers de serialização (contrato/integração) ---

def _dt_to_iso(dt: datetime | None) -> str | None:
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
