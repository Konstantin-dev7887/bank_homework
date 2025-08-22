from __future__ import annotations

from typing import Any, Dict, List

import pytest

from src.generators import (
    CARD_MAX,
    card_number_generator,
    filter_by_currency,
    transaction_descriptions,
)


def test_filter_by_currency_usd(transactions: List[Dict[str, Any]]) -> None:
    usd_transactions = list(filter_by_currency(transactions, "USD"))
    assert len(usd_transactions) == 3
    assert ({transaction["id"]
            for transaction in usd_transactions} ==
            {939719570, 142264268, 895315941})


def test_filter_by_currency_absent(transactions: List[Dict[str, Any]]) -> None:
    eur_transactions = list(filter_by_currency(transactions, "EUR"))
    assert eur_transactions == []


def test_filter_by_currency_empty_list() -> None:
    assert list(filter_by_currency([], "USD")) == []


def test_transaction_descriptions_ok(transactions: List[Dict[str, Any]]) \
        -> None:
    result_descriptions = list(transaction_descriptions(transactions))
    assert result_descriptions[:3] == [
        "Перевод организации",
        "Перевод со счета на счет",
        "Перевод со счета на счет",
    ]


def test_transaction_descriptions_with_missing(
        transactions: List[Dict[str, Any]]) -> None:
    transactions.append({"operationAmount": {"currency": {"code": "USD"}}})
    result_descriptions = list(transaction_descriptions(transactions))
    assert "" in result_descriptions


@pytest.mark.parametrize(
    "start, stop, first, last",
    [
        (1, 3, "0000 0000 0000 0001", "0000 0000 0000 0003"),
        (10 ** 16 - 2, 10 ** 16 - 1,
         "9999 9999 9999 9998", "9999 9999 9999 9999"),
    ],
)
def test_card_number_generator_ok(start: int,
                                  stop: int,
                                  first: str,
                                  last: str) -> None:
    card_numbers = list(card_number_generator(start, stop))
    assert card_numbers[0] == first and card_numbers[-1] == last

    for card_number in card_numbers:
        assert len(card_number) == 19
        assert card_number[4] == card_number[9] == card_number[14] == " "


@pytest.mark.parametrize("start, stop",
                         [(-1, 5), (5, 1), (0, 1), (1, CARD_MAX + 1)])
def test_card_number_generator_invalid(start: int, stop: int) -> None:
    with pytest.raises(ValueError):
        list(card_number_generator(start, stop))
