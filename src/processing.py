"""
Обработка операций: фильтрация по статусу и сортировка по дате.
"""
from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, Iterable, List

Transaction = Dict[str, Any]


def filter_by_state(
        operations: Iterable[Transaction],
        state: str = "EXECUTED") -> List[Transaction]:
    """
    Возвращает новый список словарей, у которых ключ 'state' == заданному.
    По умолчанию state == 'EXECUTED'.
    """
    return [operation
            for operation in operations
            if isinstance(operation, dict) and operation.get("state") == state]


def sort_by_date(
        operations: Iterable[Transaction],
        reverse: bool = True) -> List[Transaction]:
    """
    Сортирует по ключу 'date'. По умолчанию по убыванию (свежие первыми).
    Некорректные/пустые даты считаются минимальными.
    """
    operations = [operation
                  for operation in operations
                  if isinstance(operation, dict)]
    return sorted(operations,
                  key=lambda operation: _parse_iso8601(operation.get("date")),
                  reverse=reverse)


def _parse_iso8601(value: Any) -> datetime:
    if isinstance(value, str):
        try:
            return datetime.fromisoformat(value)
        except ValueError:
            pass

    return datetime.min
