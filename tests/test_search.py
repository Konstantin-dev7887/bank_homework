from __future__ import annotations

from typing import Any, Dict, List

import pytest

from src.search import process_bank_operations, process_bank_search


@pytest.fixture
def transactions() -> List[Dict[str, Any]]:
    return [
        {"id": 1, "description": "Перевод организации"},
        {"id": 2, "description": "Перевод со счета на счет"},
        {"id": 3, "description": "Оплата услуг"},
        {"id": 4, "description": None},
        {"id": 5},
    ]


@pytest.mark.parametrize(
    "needle, expected_ids",
    [
        ("перевод", [1, 2]),
        ("ОрГаНиЗаЦ", [1]),
        ("услуг", [3]),
        ("нет такого", []),
        ("", []),
    ],
)
def test_process_bank_search(transactions, needle, expected_ids) -> None:
    results = process_bank_search(transactions, needle)
    assert [transaction["id"] for transaction in results] == expected_ids


def test_process_bank_operations_counts(transactions) -> None:
    categories = ["перевод", "организации", "оплата", "вклад"]
    results = process_bank_operations(transactions, categories)

    assert results["перевод"] == 2
    assert results["организации"] == 1
    assert results["оплата"] == 1
    assert results["вклад"] == 0
