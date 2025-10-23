from typing import Callable, Optional, Dict, Any


class UsersHTTP:
    """
    Adapter do serviço de Usuários.

    - Integra com a camada externa de Usuários (Equipe 1).
    - No futuro: realizará chamadas HTTP reais (ex.: GET {BASE_URL}/users/{id}).
    - Atualmente: utiliza um 'provider' injetado para simular o retorno,
      permitindo a execução de testes unitários e de contrato sem dependência de rede.
    """

    def __init__(
        self,
        base_url: Optional[str] = None,
        provider: Optional[Callable[[int], Dict[str, Any]]] = None,
    ):
        """
        :param base_url: URL base do serviço de usuários (opcional).
        :param provider: Função injetada usada em testes para simular o retorno do serviço.
        """
        self.base_url = base_url
        self._provider = provider

    # -------------------------------
    # Métodos públicos de interface
    # -------------------------------

    def get_user(self, user_id: int) -> Optional[Dict[str, Any]]:
        """
        Obtém um dicionário representando o usuário.

        Exemplo de retorno esperado:
        {
            "id": 1,
            "name": "Ana",
            "type": "student",
            "active": True
        }
        """
        if self._provider is None:
            # Placeholder até integrar HTTP real
            return None
        return self._provider(user_id)

    def is_active(self, user_id: int) -> bool:
        """
        Retorna True se o usuário estiver ativo, False caso contrário.
        """
        user = self.get_user(user_id)
        return bool(user and user.get("active") is True)

