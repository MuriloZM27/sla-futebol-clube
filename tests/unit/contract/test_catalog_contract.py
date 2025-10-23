from emprestimo.adapters.catalog_http import CatalogHTTP  # <-- RED: ainda não existe

def test_catalog_get_book_contract_fields_and_status():
    def provider(book_id: int) -> dict:
        return {"id": book_id, "title": "Clean Code", "status": "available"}

    svc = CatalogHTTP(provider=provider)

    book = svc.get_book(10)
    assert set(book.keys()) == {"id", "title", "status"}
    assert isinstance(book["id"], int)
    assert isinstance(book["title"], str)
    assert book["status"] in {"available", "loaned"}

def test_catalog_is_available_consistent_with_get_book_status():
    # provider controlando dinamicamente o status
    state = {"status": "available"}
    def provider(book_id: int) -> dict:
        return {"id": book_id, "title": "Clean Code", "status": state["status"]}

    from emprestimo.adapters.catalog_http import CatalogHTTP
    svc = CatalogHTTP(provider=provider)

    state["status"] = "available"
    assert svc.is_available(1) is True

    state["status"] = "loaned"
    assert svc.is_available(1) is False

