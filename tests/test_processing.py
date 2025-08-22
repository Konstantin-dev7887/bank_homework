from typing import Any, Dict, List

import pytest

from src.processing import filter_by_state, sort_by_date


@pytest.mark.parametrize("status, expected_ids", [
    ("EXECUTED", [1, 2, 5]),
    ("CANCELED", [3, 4]),
    ("PENDING", []),
])
def test_filter_by_state_param(operations: List[Dict[str, Any]], status: str, expected_ids: Any) -> None:
    filtered_operations = filter_by_state(operations, state=status)
    assert [operation["id"] for operation in filtered_operations] == expected_ids


def test_sort_by_date_desc(operations: List[Dict[str, Any]]) -> None:
    sorted_operations = sort_by_date(operations, reverse=True)
    assert [operation["id"] for operation in sorted_operations][:2] == [1, 4]
    assert sorted_operations[-1]["date"] == "wrong-date"


def test_sort_by_date_asc(operations: List[Dict[str, Any]]) -> None:
    sorted_operations = sort_by_date(operations, reverse=False)
    assert sorted_operations[0]["date"] == "wrong-date"
