from __future__ import annotations


class FET112Error(Exception):
    """Base error for the FET112 client."""


class FET112HTTPError(FET112Error):
    """FET112 returned a non-success HTTP response."""

    def __init__(self, status: int, message: str, *, body: object | None = None) -> None:
        super().__init__(f"FET112 HTTP {status}: {message}")
        self.status = status
        self.body = body


class FET112ProtocolError(FET112Error):
    """FET112 returned a response that does not match the expected contract."""
