from typing import Callable, Optional, Dict, Any

class UsersHTTP:
    """
    Adapter mínimo para o serviço de Usuários.
    - No futuro: fará chamadas HTTP (ex.: GET {BASE_URL}/users/{id}).
    - Agora: recebe um 'provider' injetado (callable) para facilitar testes/contratos.
    """

    def __init__(self, base_url: Optional[str] = None, provider: Optional[Callable[[int], Dict[str, Any]]] = None):
        self.base_url = base_url
        self._provider = provider

    def get_user(self, user_id: int) -> Optional[Dict[str, Any]]:
        if self._provider is None:
            # Placeholder até integrar HTTP de verdade
            return None
        return self._provider(user_id)

    def is_active(self, user_id: int) -> bool:
        user = self.get_user(user_id)
        return bool(user and user.get("active") is True)
