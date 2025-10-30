from src.interface.app import app

def test_index_route_returns_html():
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200
    assert b"Sistema de Empr\xc3\xa9stimo" in response.data

def test_loans_api_returns_json(monkeypatch):
    client = app.test_client()

    dummy_loans = [
        {"id": 1, "user": "Alice", "book": "1984", "status": "ativo"},
        {"id": 2, "user": "Bob", "book": "Dom Casmurro", "status": "devolvido"},
    ]

    monkeypatch.setattr("src.interface.app.service.list_loans", lambda: dummy_loans)

    response = client.get("/api/loans")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) == 2
    assert "user" in data[0]
