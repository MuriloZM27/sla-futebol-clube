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
