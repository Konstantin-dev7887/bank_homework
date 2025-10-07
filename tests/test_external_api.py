from __future__ import annotations

from typing import Any, Dict
from unittest.mock import Mock, patch

import pytest

from src.external_api import API_KEY, convert_to_rub


def _generate_transaction(amount: str, code: str) -> Dict[str, Any]:
    return {
        "operationAmount": {
            "amount": amount,
            "currency": {"name": code, "code": code},
        }
    }


def test_convert_rub_no_api_needed() -> None:
    data = _generate_transaction("123.45", "RUB")
    assert convert_to_rub(data) == 123.45


@patch("src.external_api.requests.get")
def test_convert_usd(mock: Mock, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv(API_KEY, "dummy")

    response = Mock()
    response.json.return_value = {"rates": {"RUB": 90.0}}
    response.raise_for_status.return_value = None
    mock.return_value = response

    transaction = _generate_transaction("10.00", "USD")
    assert convert_to_rub(transaction) == 900.00


@patch("src.external_api.requests.get")
def test_convert_eur(mock: Mock, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv(API_KEY, "dummy")
    response = Mock()
    response.json.return_value = {"rates": {"RUB": 100.0}}
    response.raise_for_status.return_value = None
    mock.return_value = response

    transaction = _generate_transaction("5", "EUR")
    assert convert_to_rub(transaction) == 500.00


def test_convert_raises_if_no_api_key(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv(API_KEY, raising=False)
    transaction = _generate_transaction("1.0", "USD")

    with pytest.raises(RuntimeError):
        convert_to_rub(transaction)


def test_convert_invalid_transaction_structure() -> None:
    with pytest.raises(ValueError):
        convert_to_rub({})
