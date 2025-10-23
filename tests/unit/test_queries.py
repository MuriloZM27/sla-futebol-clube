class CatalogOK:
    def __init__(self):
        # status por livro: "available" (padrão) ou "loaned"
        self._status = {}  # dict[int, str]

    def _get_status(self, bid):
        return self._status.get(bid, "available")

    def get_book(self, bid):
        return {"id": bid, "title": "Clean Code", "status": self._get_status(bid)}

    def is_available(self, bid):
        return self._get_status(bid) == "available"

    def mark_loaned(self, bid):
        self._status[bid] = "loaned"

    def mark_available(self, bid):
        self._status[bid] = "available"
