from __future__ import annotations
from typing import Any, Dict, List

import pytest


@pytest.fixture
def operations() -> List[Dict[str, Any]]:
    """
    Набор тестовых операций для проверки функций filter_by_state и sort_by_date.
    """
    return [
        {"id": 1, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 2, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 3, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 4, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
        {"id": 5, "state": "EXECUTED", "date": "wrong-date"},
    ]