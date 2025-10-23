from dataclasses import is_dataclass
from datetime import datetime, timezone
from emprestimo.domain import Loan, loan_to_dict  # <-- loan_to_dict ainda não existe (RED)

def test_loan_dto_serializes_with_expected_fields_and_types():
    loan = Loan(
        id="abc",
        user_id=1,
        book_id=10,
        loan_date=datetime.now(timezone.utc),
        return_date=None,
        status="active",
    )
    assert is_dataclass(loan) is True

    data = loan_to_dict(loan)
    assert set(data.keys()) == {"id","user_id","book_id","loan_date","return_date","status"}
    assert isinstance(data["id"], str)
    assert isinstance(data["user_id"], int)
    assert isinstance(data["book_id"], int)
    assert isinstance(data["status"], str)
    assert isinstance(data["loan_date"], str)                # ISO-8601
    assert data["return_date"] is None or isinstance(data["return_date"], str)
