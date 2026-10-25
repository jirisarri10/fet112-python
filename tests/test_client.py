import pytest

from fet112.client import _required_text


def test_required_text_strips():
    assert _required_text("action", " transfer ") == "transfer"


def test_required_text_rejects_empty():
    with pytest.raises(ValueError):
        _required_text("action", " ")


def test_required_text_rejects_too_long():
    with pytest.raises(ValueError):
        _required_text("action", "x" * 257)
