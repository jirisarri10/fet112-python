"""Small, explicit Python client for FET112."""

from .client import FET112Client, pre_action_check
from .errors import FET112Error, FET112HTTPError, FET112ProtocolError
from .models import PreActionResult

__all__ = [
    "FET112Client",
    "FET112Error",
    "FET112HTTPError",
    "FET112ProtocolError",
    "PreActionResult",
    "pre_action_check",
]

__version__ = "0.1.0"
