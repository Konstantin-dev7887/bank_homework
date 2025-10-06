from __future__ import annotations

from typing import Any, Dict, Iterable, Iterator

CARD_NUM_LEN: int = 16
CARD_MIN: int = 1
CARD_MAX: int = 10 ** 16 - 1
GROUP: int = 4


def filter_by_currency(transactions: Iterable[Dict[str, Any]],
                       code: str) -> Iterator[Dict[str, Any]]:
    """
    Итератор по транзакциям, где currency.code == code.
    Нечёткие/битые записи тихо пропускаем.
    """
    target = str(code).strip()

    for transaction in transactions:
        try:
            if transaction["operationAmount"]["currency"]["code"] == target:
                yield transaction
        except Exception:
            continue


def transaction_descriptions(transactions: Iterable[Dict[str, Any]]) \
        -> Iterator[str]:
    """
    Генератор описаний транзакций. Если описания нет — отдаёт пустую строку.
    """
    for transaction in transactions:
        desciption = ""

        try:
            desciption = transaction.get("description", "") or ""
        except Exception:
            pass

        yield desciption


def card_number_generator(start: int, stop: int) -> Iterator[str]:
    """
    Генератор номеров карт в виде 'XXXX XXXX XXXX XXXX'
    для диапазона [start, stop].
    Ограничения: 1 <= start <= stop <= 9999_9999_9999_9999.
    """
    if not (CARD_MIN <= start <= stop <= CARD_MAX):
        raise ValueError("Invalid range for card_number_generator")

    for number in range(start, stop + 1):
        raw = f"{number:0{CARD_NUM_LEN}d}"
        yield " ".join(raw[i: i + GROUP]
                       for i in range(0, CARD_NUM_LEN, GROUP))
