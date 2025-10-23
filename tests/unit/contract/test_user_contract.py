from typing import Callable
from emprestimo.adapters.users_http import UsersHTTP  # <-- ainda não existe (RED)

def test_user_service_contract_fields_and_types():
    # vamos injetar um "provider" fake para não chamar rede
    def provider(user_id: int) -> dict:
        return {"id": user_id, "name": "Ana", "type": "student", "active": True}

    svc = UsersHTTP(provider=provider)

    user = svc.get_user(42)
    assert set(user.keys()) == {"id", "name", "type", "active"}
    assert isinstance(user["id"], int)
    assert isinstance(user["name"], str)
    assert isinstance(user["type"], str)
    assert isinstance(user["active"], bool)

    assert svc.is_active(42) is True
