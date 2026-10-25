from __future__ import annotations

import json
from typing import Any, Mapping
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from .errors import FET112Error, FET112HTTPError, FET112ProtocolError
from .models import PreActionResult

DEFAULT_BASE_URL = "https://www.fet112.com"
DEFAULT_TIMEOUT = 10.0


class FET112Client:
    """Minimal synchronous client for the public FET112 REST API."""

    def __init__(self, *, base_url: str = DEFAULT_BASE_URL, timeout: float = DEFAULT_TIMEOUT) -> None:
        self.base_url = base_url.rstrip("/")
        if timeout <= 0:
            raise ValueError("timeout must be greater than zero")
        self.timeout = float(timeout)

    def pre_action_check(
        self,
        *,
        action: str,
        destination: str,
        amount: str,
        asset: str,
        metadata: Mapping[str, Any] | None = None,
    ) -> PreActionResult:
        payload = {
            "action": _required_text("action", action),
            "destination": _required_text("destination", destination),
            "amount": _required_text("amount", amount),
            "asset": _required_text("asset", asset),
            "metadata": dict(metadata or {}),
        }
        raw = self._post_json("/api/v1/pre_action_check", payload)
        return PreActionResult.from_payload(raw)

    def _post_json(self, path: str, payload: Mapping[str, Any]) -> Mapping[str, Any]:
        body = json.dumps(payload, ensure_ascii=False, separators=(",", ":"), allow_nan=False).encode("utf-8")
        request = Request(
            self.base_url + path,
            data=body,
            method="POST",
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
                "User-Agent": "fet112-python/0.1.0",
            },
        )
        try:
            with urlopen(request, timeout=self.timeout) as response:
                response_body = response.read()
        except HTTPError as exc:
            response_body = exc.read()
            parsed = _decode_json(response_body)
            message = _error_message(parsed) or exc.reason or "request failed"
            raise FET112HTTPError(exc.code, str(message), body=parsed) from exc
        except URLError as exc:
            raise FET112Error(f"could not reach FET112: {exc.reason}") from exc

        parsed = _decode_json(response_body)
        if not isinstance(parsed, Mapping):
            raise FET112ProtocolError("FET112 returned a non-object JSON response")
        return parsed


def pre_action_check(
    destination: str,
    *,
    action: str = "transfer",
    amount: str = "unspecified",
    asset: str = "FET",
    metadata: Mapping[str, Any] | None = None,
    base_url: str = DEFAULT_BASE_URL,
    timeout: float = DEFAULT_TIMEOUT,
) -> PreActionResult:
    """Convenience wrapper around :class:`FET112Client`.

    The destination/amount/asset fields are committed to the response through
    FET112's action hash, but FET112 v1 does not classify those action-specific
    risks. Inspect ``result.action_assessment`` when presenting the result.
    """
    return FET112Client(base_url=base_url, timeout=timeout).pre_action_check(
        action=action,
        destination=destination,
        amount=amount,
        asset=asset,
        metadata=metadata,
    )


def _required_text(name: str, value: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name} must be a non-empty string")
    value = value.strip()
    if len(value) > 256:
        raise ValueError(f"{name} exceeds maximum length of 256 characters")
    return value


def _decode_json(body: bytes) -> Any:
    try:
        return json.loads(body.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise FET112ProtocolError("FET112 returned invalid JSON") from exc


def _error_message(payload: Any) -> str | None:
    if not isinstance(payload, Mapping):
        return None
    for key in ("message", "detail", "error", "title"):
        value = payload.get(key)
        if isinstance(value, str) and value:
            return value
    return None
