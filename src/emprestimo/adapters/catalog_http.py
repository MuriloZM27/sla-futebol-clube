from typing import Callable, Optional, Dict, Any


class CatalogHTTP:
    """
    Adapter do serviço de Catálogo.

    - Integra com o módulo externo de Catálogo (Equipe 2).
    - No futuro: fará chamadas HTTP reais (ex.: GET {BASE_URL}/books/{id}).
    - Atualmente: utiliza um 'provider' injetado que simula o retorno,
      permitindo a execução de testes unitários e de contrato sem dependência de rede.
    """

    def __init__(
        self,
        base_url: Optional[str] = None,
        provider: Optional[Callable[[int], Dict[str, Any]]] = None,
    ):
        """
        :param base_url: URL base do serviço de catálogo (opcional).
        :param provider: Função injetada usada em testes para simular o retorno do serviço.
        """
        self.base_url = base_url
        self._provider = provider

    # -------------------------------
    # Métodos públicos de interface
    # -------------------------------

    def get_book(self, book_id: int) -> Optional[Dict[str, Any]]:
        """
        Retorna um dicionário com as informações do livro.

        Exemplo de retorno esperado:
        {
            "id": 10,
            "title": "Clean Code",
            "status": "available"
        }
        """
        if self._provider is None:
            # Placeholder até integração real via HTTP
            return None
        return self._provider(book_id)

    def is_available(self, book_id: int) -> bool:
        """
        Retorna True se o livro estiver disponível, False caso contrário.
        """
        book = self.get_book(book_id)
        return bool(book and book.get("status") == "available")

    def mark_loaned(self, book_id: int) -> None:
        """
        Marca um livro como emprestado no catálogo.

        (No futuro, será implementado com requisições HTTP PUT/PATCH.)
        """
        pass

    def mark_available(self, book_id: int) -> None:
        """
        Marca um livro como disponível novamente no catálogo.

        (No futuro, será implementado com requisições HTTP PUT/PATCH.)
        """
        pass
