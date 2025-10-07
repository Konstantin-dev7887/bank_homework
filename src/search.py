from __future__ import annotations

import re
from collections import Counter
from typing import Any, Dict, Iterable, List, Mapping

Transaction = Dict[str, Any]


def process_bank_search(data: Iterable[Transaction],
                        search: str) -> List[Transaction]:
    """
    Вернуть транзакции,
    у которых в description встречается искомая строка (без учёта регистра).
    Пустые/отсутствующие description игнорируются.
    Поиск выполняется через re.search,
    искомая строка экранируется (буквальный поиск).
    """
    if not search:
        return []

    pattern = re.compile(re.escape(search), flags=re.IGNORECASE)
    result: List[Transaction] = []

    for transaction in data:
        description = transaction.get("description")

        if isinstance(description, str) and pattern.search(description):
            result.append(transaction)

    return result


def process_bank_operations(
        data: Iterable[Transaction],
        categories: Iterable[str],
) -> Mapping[str, int]:
    """
    Подсчитать количество операций
    по заданным категориям (по полю description),
    без учёта регистра. Используется collections.Counter.
    Возвращает dict: {категория: счётчик}.
    """
    full_categories = [category for category in categories if category]
    counter: Counter[str] = Counter({category: 0
                                     for category
                                     in full_categories})

    for transaction in data:
        description = transaction.get("description")

        if isinstance(description, str):
            low_description = description.lower()

            for category in full_categories:
                if category.lower() in low_description:
                    counter[category] += 1

    return dict(counter)
