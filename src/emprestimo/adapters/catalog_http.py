from typing import Callable, Optional, Dict, Any

class CatalogHTTP:
    """
    Adapter mínimo para o serviço de Catálogo.
    Futuro: chamadas HTTP reais (GET /books/{id} etc).
    Agora: usa 'provider' injetável para testes/contratos.
    """
    def __init__(self, base_url: Optional[str] = None,
                 provider: Optional[Callable[[int], Dict[str, Any]]] = None):
        self.base_url = base_url
        self._provider = provider

    def get_book(self, book_id: int) -> Optional[Dict[str, Any]]:
        if self._provider is None:
            return None
        return self._provider(book_id)

    def is_available(self, book_id: int) -> bool:
        book = self.get_book(book_id)
        return bool(book and book.get("status") == "available")

    def mark_loaned(self, book_id: int) -> None:
        # placeholder: na integração real vai chamar HTTP PUT/PATCH
        pass

    def mark_available(self, book_id: int) -> None:
        # placeholder: na integração real vai chamar HTTP PUT/PATCH
        pass
