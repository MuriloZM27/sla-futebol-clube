from dataclasses import dataclass
from datetime import datetime

class LoanError(Exception):
    pass

@dataclass
class Loan:
    id: str
    user_id: int
    book_id: int
    loan_date: datetime
    return_date: datetime | None
    status: str  # "active" | "returned"
